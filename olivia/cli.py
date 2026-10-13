"""Command line entry point: `olivia validate` and `olivia render`."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

from .render import render
from .schema import ValidationError, load_leads, load_profile


def _load(args: argparse.Namespace):
    try:
        profile = load_profile(args.profile)
    except ValidationError as exc:
        print(f"Profile is invalid:\n  " + "\n  ".join(exc.errors), file=sys.stderr)
        raise SystemExit(2)
    leads, invalid = load_leads(args.leads)
    for lead_id, errors in invalid.items():
        print(f"[schema] {lead_id}: " + "; ".join(errors), file=sys.stderr)
    return profile, leads, invalid


def cmd_validate(args: argparse.Namespace) -> int:
    profile, leads, invalid = _load(args)
    blocked = 0
    for lead in leads:
        draft = render(lead, profile)
        for issue in draft.issues:
            print(f"[{issue.severity}] {draft.lead_id} {issue.code}: {issue.message}")
        blocked += draft.blocked
    ready = len(leads) - blocked
    print(f"\n{ready} ready, {blocked} blocked, {len(invalid)} invalid rows.")
    return 1 if blocked or invalid else 0


def cmd_render(args: argparse.Namespace) -> int:
    profile, leads, invalid = _load(args)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    report_rows = []
    for lead in leads:
        draft = render(lead, profile)
        status = "blocked" if draft.blocked else "drafted"
        if not draft.blocked:
            (out / f"{draft.lead_id}.md").write_text(
                f"---\nlead_id: {draft.lead_id}\nchannel: {draft.channel}\n"
                f"register: {draft.register}\nto: {lead.get('email') or lead.get('linkedin_url', '')}\n"
                f"subject: {draft.subject}\n---\n\n{draft.body}",
                encoding="utf-8",
            )
        report_rows.append({
            "lead_id": draft.lead_id,
            "name": lead["name"],
            "channel": draft.channel,
            "register": draft.register,
            "status": status,
            "issues": " | ".join(f"{i.severity}:{i.code}" for i in draft.issues),
        })
    for lead_id, errors in invalid.items():
        report_rows.append({"lead_id": lead_id, "name": "", "channel": "", "register": "",
                            "status": "invalid", "issues": " | ".join(errors)})
    with (out / "report.csv").open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(report_rows[0]) if report_rows else ["lead_id"])
        writer.writeheader()
        writer.writerows(report_rows)
    drafted = sum(r["status"] == "drafted" for r in report_rows)
    print(f"{drafted} drafts written to {out}/, report in {out}/report.csv. Nothing was sent.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="olivia", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for name, func, help_text in [
        ("validate", cmd_validate, "Run schema and guardrail checks on a leads CSV."),
        ("render", cmd_render, "Write a draft per ready lead plus report.csv. Sends nothing."),
    ]:
        p = sub.add_parser(name, help=help_text)
        p.add_argument("leads", help="Path to a leads CSV (see schemas/lead.schema.json).")
        p.add_argument("--profile", required=True, help="Opportunity profile YAML.")
        if name == "render":
            p.add_argument("--out", default="outbox", help="Output folder for drafts.")
        p.set_defaults(func=func)
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
