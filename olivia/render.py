"""Turn a lead + profile into a draft message."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from string import Template
from typing import Any

from . import guardrails
from .schema import REPO_ROOT

DEFAULT_SUBJECT = "Propuesta de colaboración"

_NUMBER_WORDS = {1: "una", 2: "dos", 3: "tres", 4: "cuatro", 5: "cinco"}


@dataclass
class Draft:
    lead_id: str
    channel: str
    register: str
    subject: str
    body: str
    issues: list[guardrails.Issue] = field(default_factory=list)

    @property
    def blocked(self) -> bool:
        return guardrails.is_blocked(self.issues)


def _template_path(profile: dict[str, Any], channel: str, register: str) -> Path:
    templates = profile["templates"]
    base = templates.get(channel) or templates["email"]
    return REPO_ROOT / f"{base}.{register}.txt"


def _intro(sender: dict[str, Any]) -> str:
    parts = [f"Soy {sender['name']}"]
    title, org = sender.get("title"), sender.get("organization")
    if title and org:
        parts.append(f"{title.lower()} de {org}")
    elif title:
        parts.append(title)
    elif org:
        parts.append(f"de {org}")
    sentence = ", ".join(parts)
    if sender.get("location"):
        sentence += f", en {sender['location']}"
    return sentence + "."


def _offer_lines(offer: dict[str, Any]) -> tuple[str, str]:
    lines = offer["lines"]
    heading = offer.get("lines_heading") or (
        f"Trabajamos en {_NUMBER_WORDS.get(len(lines), str(len(lines)))} "
        f"línea{'s' if len(lines) != 1 else ''}:"
    )
    body = "\n".join(f"- {line['name']}: {line['pitch'].strip()}" for line in lines)
    return heading, body


def _calendar_line(sender: dict[str, Any], register: str) -> str:
    url = sender.get("calendar_url")
    if not url:
        return ""
    verb = "podés" if register == "voseo" else "puedes"
    comfy = "te queda más cómodo" if register == "voseo" else "te resulta más cómodo"
    return f"\nP.D.: Si {comfy}, {verb} agendar directamente en mi calendario: {url}"


def _attention_line(lead: dict[str, Any]) -> str:
    # Shared inboxes (info@, contacto@) need the person's name up front.
    if lead.get("channel") == "email" and lead.get("email_is_generic"):
        return f"(A la atención de {lead['name']})\n"
    return ""


def render(lead: dict[str, Any], profile: dict[str, Any]) -> Draft:
    """Render one lead. The returned Draft carries every guardrail issue found."""
    register = guardrails.register_for(lead.get("country", ""), profile)
    channel = lead["channel"]
    issues = guardrails.check_lead(lead, profile)

    sender = profile["sender"]
    heading, offer_lines = _offer_lines(profile["offer"])
    complement = lead["complement"].strip()
    prefix = profile.get("complement_prefix")
    if prefix:
        complement = f"{prefix} {complement}"

    template = Template(_template_path(profile, channel, register).read_text(encoding="utf-8"))
    body = template.substitute(
        first_name=lead.get("first_name") or lead["name"].split()[0],
        attention_line=_attention_line(lead),
        opener=lead["opener"].strip(),
        intro=_intro(sender),
        offer_summary=profile["offer"]["summary"].strip(),
        offer_lines_heading=heading,
        offer_lines=offer_lines,
        complement=complement,
        call_to_action=profile["call_to_action"][register],
        sender_name=sender["name"],
        calendar_line=_calendar_line(sender, register),
    )
    body = re.sub(r"\n{3,}", "\n\n", body).strip() + "\n"

    issues += guardrails.check_message(body, register)
    return Draft(
        lead_id=lead["lead_id"],
        channel=channel,
        register=register,
        subject=lead.get("subject") or DEFAULT_SUBJECT,
        body=body,
        issues=issues,
    )
