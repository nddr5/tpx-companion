"""Validate TPx reporting-card YAML files against ``reporting_card.schema.json``.

Usage, from this directory::

    python3 validate_cards.py examples/*.yaml

Requires PyYAML and jsonschema (``python3 -m pip install -r requirements.txt``
from the repository root). Two checks that JSON Schema cannot express are
applied on top of the schema: deprecated TPx label spellings are rejected
anywhere in the file, and ``same as L_*`` language references must resolve to
an explicit language list without cycles.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SCHEMA_PATH = Path(__file__).resolve().parent / "reporting_card.schema.json"
DEPRECATED_LABELS = {"T-then-R", "R-then-T", "Lang-agnostic"}
LANGUAGE_ROLES = ("L_q", "L_e", "L_a", "L_r")
REFERENCE_RE = re.compile(r"^same as (L_[qear])$")


def import_dependencies():
    try:
        import yaml
        from jsonschema import validators
    except ImportError as exc:
        print(
            f"validate_cards.py needs PyYAML and jsonschema ({exc}). "
            "Install them with: python3 -m pip install -r requirements.txt",
            file=sys.stderr,
        )
        raise SystemExit(2)
    return yaml, validators


def make_loader(yaml):
    """SafeLoader that keeps ISO 639 codes such as ``no`` (Norwegian) as strings.

    PyYAML implements YAML 1.1, which would otherwise read ``no``, ``yes``,
    ``on`` and ``off`` as booleans.
    """

    class CardLoader(yaml.SafeLoader):
        pass

    CardLoader.yaml_implicit_resolvers = {
        first: [(tag, regexp) for tag, regexp in resolvers if tag != "tag:yaml.org,2002:bool"]
        for first, resolvers in yaml.SafeLoader.yaml_implicit_resolvers.items()
    }
    return CardLoader


def resolve_language(role: str, languages: dict, seen: set[str]):
    """Follow ``same as L_*`` references; return None on a cycle or dangling reference."""
    value = languages.get(role)
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        match = REFERENCE_RE.match(value.strip())
        if match:
            target = match.group(1)
            if target == role or target in seen:
                return None
            return resolve_language(target, languages, seen | {role})
    return None


def validate_card(path: Path, validator, loader, yaml) -> list[str]:
    errors: list[str] = []
    raw_text = path.read_text(encoding="utf-8")

    for deprecated in sorted(DEPRECATED_LABELS):
        if deprecated in raw_text:
            errors.append(
                f"deprecated TPx label `{deprecated}` found; use official labels only"
            )

    try:
        card = yaml.load(raw_text, Loader=loader)
    except yaml.YAMLError as exc:
        return errors + [f"YAML parse error: {exc}"]
    if not isinstance(card, dict):
        return errors + ["card must be a YAML mapping"]

    for error in sorted(
        validator.iter_errors(card), key=lambda e: [str(p) for p in e.absolute_path]
    ):
        location = "/".join(str(part) for part in error.absolute_path) or "<root>"
        errors.append(f"{location}: {error.message}")

    languages = card.get("language_config")
    if isinstance(languages, dict):
        for role in LANGUAGE_ROLES:
            value = languages.get(role)
            if (
                isinstance(value, str)
                and REFERENCE_RE.match(value.strip())
                and resolve_language(role, languages, set()) is None
            ):
                errors.append(
                    f"`language_config.{role}`: `{value.strip()}` is circular or "
                    "does not resolve to a language list"
                )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate TPx reporting-card YAML files against the JSON Schema."
    )
    parser.add_argument("cards", nargs="+", type=Path, help="YAML reporting cards to validate")
    parser.add_argument(
        "--schema", type=Path, default=SCHEMA_PATH, help="JSON Schema file (default: %(default)s)"
    )
    args = parser.parse_args()

    yaml, validators = import_dependencies()
    schema = json.loads(args.schema.read_text(encoding="utf-8"))
    validator_class = validators.validator_for(schema)
    validator_class.check_schema(schema)
    validator = validator_class(schema)
    loader = make_loader(yaml)

    had_errors = False
    for card_path in args.cards:
        errors = validate_card(card_path, validator, loader, yaml)
        if errors:
            had_errors = True
            print(f"{card_path}: FAIL")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"{card_path}: OK")

    if had_errors:
        print("Validation failed.", file=sys.stderr)
        return 1
    print(f"Validation passed for {len(args.cards)} card(s) against {args.schema.name}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
