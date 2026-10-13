"""Loading and validating profiles and leads against the JSON Schemas in /schemas."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_DIR = REPO_ROOT / "schemas"

# Lead fields that arrive as strings from CSV but are booleans in the schema.
_BOOL_FIELDS = {"identity_verified", "email_is_generic"}


class ValidationError(Exception):
    """Raised when a profile or lead does not match its schema."""

    def __init__(self, source: str, errors: list[str]):
        self.source = source
        self.errors = errors
        super().__init__(f"{source}: " + "; ".join(errors))


def _validator(name: str) -> Draft202012Validator:
    schema = json.loads((SCHEMA_DIR / name).read_text(encoding="utf-8"))
    return Draft202012Validator(schema)


def _errors(validator: Draft202012Validator, data: Any) -> list[str]:
    out = []
    for err in sorted(validator.iter_errors(data), key=lambda e: list(e.path)):
        where = "/".join(str(p) for p in err.path) or "(root)"
        out.append(f"{where}: {err.message}")
    return out


def load_profile(path: str | Path) -> dict[str, Any]:
    """Load an opportunity profile YAML and validate it.

    Template paths in the profile are resolved relative to the repo root.
    """
    path = Path(path)
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    errors = _errors(_validator("opportunity-profile.schema.json"), data)
    if errors:
        raise ValidationError(str(path), errors)
    return data


def _coerce(row: dict[str, str]) -> dict[str, Any]:
    """Drop empty CSV cells and turn boolean-like strings into booleans."""
    lead: dict[str, Any] = {}
    for key, value in row.items():
        if key is None:
            continue
        value = (value or "").strip()
        if value == "":
            continue
        if key in _BOOL_FIELDS:
            lead[key] = value.lower() in {"true", "1", "yes", "sí", "si", "x"}
        else:
            lead[key] = value
    return lead


def load_leads(path: str | Path) -> tuple[list[dict[str, Any]], dict[str, list[str]]]:
    """Read a leads CSV.

    Returns the leads that parsed, plus a map of lead_id (or row number) to
    schema errors for rows that did not.
    """
    validator = _validator("lead.schema.json")
    leads: list[dict[str, Any]] = []
    invalid: dict[str, list[str]] = {}
    with Path(path).open(encoding="utf-8", newline="") as fh:
        for index, row in enumerate(csv.DictReader(fh), start=2):
            lead = _coerce(row)
            errors = _errors(validator, lead)
            if errors:
                invalid[lead.get("lead_id", f"row {index}")] = errors
            else:
                leads.append(lead)
    return leads, invalid
