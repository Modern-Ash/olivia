"""Checks that block a message before a human ever sees it as "ready".

Every rule here comes from a mistake found in the October 2026 seed campaign:
openers that claimed things nobody had verified, a profile link that pointed to
a different person with the same surname, the sender's own address left in the
recipient column, and voseo/tú mixed up by country.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

BLOCK = "block"
WARN = "warn"


@dataclass(frozen=True)
class Issue:
    code: str
    severity: str
    message: str


# Openers that assert a relationship or attention we cannot prove.
UNVERIFIABLE_PATTERNS = [
    r"\bsigo de cerca\b",
    r"\bsigo con (mucho |gran )?interés\b",
    r"\bsigo (tu|su) (trabajo|trayectoria|carrera)\b",
    r"\bsigo las ediciones\b",
    r"\bsiempre (leo|veo|sigo)\b",
    r"\bcon mucha admiración\b",
]

# Second-person markers. Kept as explicit word lists: a generic "-ás/-és"
# suffix rule would also match "además", "también", "interés", "país"...
VOSEO_MARKERS = [
    "vos", "sos", "podés", "querés", "tenés", "sabés", "hacés", "liderás",
    "gestionás", "aportás", "promovés", "trabajás", "llegás", "contás",
    "fijate", "mirá", "escribime", "decime",
]
TU_MARKERS = [
    "tú", "eres", "puedes", "quieres", "tienes", "sabes", "haces", "lideras",
    "gestionas", "aportas", "impulsas", "cubres", "aseguras", "trabajas",
    "llegas", "cuentas", "fíjate", "mira", "escríbeme", "dime",
]


def register_for(country: str, profile: dict[str, Any]) -> str:
    """Return "voseo" or "tu" for a lead's country."""
    voseo = profile.get("language", {}).get("voseo_countries", ["Argentina", "Uruguay"])
    normalized = {c.strip().lower() for c in voseo}
    # Accept "Argentina (Rosario)" style values from registries.
    base = country.split("(")[0].strip().lower()
    return "voseo" if base in normalized else "tu"


def _find_markers(text: str, markers: list[str]) -> list[str]:
    found = []
    lowered = text.lower()
    for word in markers:
        if re.search(rf"(?<!\w){re.escape(word)}(?!\w)", lowered):
            found.append(word)
    return found


def check_lead(lead: dict[str, Any], profile: dict[str, Any]) -> list[Issue]:
    """Checks that only need the lead record (run before rendering)."""
    issues: list[Issue] = []

    if not lead.get("identity_verified"):
        issues.append(Issue(
            "identity_unverified", BLOCK,
            "Name, headline and organization have not been cross-checked against the profile.",
        ))

    if not lead.get("evidence_url") or not lead.get("evidence_summary"):
        issues.append(Issue(
            "missing_evidence", BLOCK,
            "The opener needs a public source (evidence_url + evidence_summary).",
        ))

    opener = lead.get("opener", "")
    for pattern in UNVERIFIABLE_PATTERNS:
        if re.search(pattern, opener, flags=re.IGNORECASE):
            issues.append(Issue(
                "unverifiable_claim", BLOCK,
                f"Opener claims ongoing attention we cannot prove ({pattern!r}). "
                "Reference the specific post instead.",
            ))
            break

    sender_email = profile["sender"]["email"].strip().lower()
    if lead.get("channel") == "email":
        email = lead.get("email", "").strip().lower()
        if not email:
            issues.append(Issue("missing_email", BLOCK, "Channel is email but no address is set."))
        elif email == sender_email:
            issues.append(Issue(
                "recipient_is_sender", BLOCK,
                "Recipient address is the sender's own address.",
            ))
        elif not lead.get("email_source_url"):
            issues.append(Issue(
                "email_unsourced", BLOCK,
                "Address has no public source. Guessed addresses are not allowed.",
            ))

    qualification = profile.get("qualification", {})
    org = lead.get("organization", "").lower()
    for employer in qualification.get("exclude_employers", []):
        if employer.lower() in org:
            issues.append(Issue(
                "excluded_employer", BLOCK,
                f"Works at {employer}, which the profile excludes.",
            ))

    countries = {c.lower() for c in profile["geography"]["countries"]}
    base_country = lead.get("country", "").split("(")[0].strip().lower()
    if base_country and base_country not in countries:
        issues.append(Issue(
            "country_out_of_scope", WARN,
            f"{lead.get('country')} is not in the profile's geography.",
        ))

    if not lead.get("subject") and lead.get("channel") == "email":
        issues.append(Issue("missing_subject", WARN, "No subject; a generic one will be used."))

    return issues


def check_message(text: str, register: str) -> list[Issue]:
    """Checks on the rendered message text."""
    other = TU_MARKERS if register == "voseo" else VOSEO_MARKERS
    found = _find_markers(text, other)
    if found:
        expected = "voseo" if register == "voseo" else "tú"
        return [Issue(
            "register_mismatch", BLOCK,
            f"Message should use {expected} but contains: {', '.join(found)}.",
        )]
    return []


def is_blocked(issues: list[Issue]) -> bool:
    return any(i.severity == BLOCK for i in issues)
