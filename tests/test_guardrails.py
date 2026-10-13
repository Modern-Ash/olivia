"""Guardrail tests. Each case reproduces a mistake from the seed campaign."""

from pathlib import Path

import pytest

from olivia.render import render
from olivia.schema import load_leads, load_profile

ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="module")
def profile():
    return load_profile(ROOT / "profiles" / "modernash-partners.yaml")


@pytest.fixture(scope="module")
def leads():
    rows, invalid = load_leads(ROOT / "examples" / "leads.example.csv")
    assert not invalid, invalid
    return {lead["lead_id"]: lead for lead in rows}


def codes(draft):
    return {issue.code for issue in draft.issues}


def test_profiles_validate():
    for path in (ROOT / "profiles").glob("*.yaml"):
        load_profile(path)


def test_ready_voseo_email(profile, leads):
    draft = render(leads["L001"], profile)
    assert not draft.blocked, draft.issues
    assert draft.register == "voseo"
    assert "¿cómo estás?" in draft.body
    assert "podés agendar" in draft.body
    # Shared inbox gets the person's name up front.
    assert "(A la atención de Laura Ejemplo)" in draft.body


def test_ready_tu_dm(profile, leads):
    draft = render(leads["L002"], profile)
    assert not draft.blocked, draft.issues
    assert draft.register == "tu"
    assert "puedes agendar" in draft.body


def test_unverifiable_opener_is_blocked(profile, leads):
    draft = render(leads["L003"], profile)
    assert draft.blocked
    assert {"unverifiable_claim", "missing_evidence"} <= codes(draft)


def test_sender_as_recipient_and_wrong_register(profile, leads):
    draft = render(leads["L004"], profile)
    assert draft.blocked
    assert {"recipient_is_sender", "identity_unverified", "register_mismatch"} <= codes(draft)


def test_excluded_employer(profile, leads):
    lead = dict(leads["L002"], organization="Deloitte Argentina")
    assert "excluded_employer" in codes(render(lead, profile))


def test_guessed_email_is_blocked(profile, leads):
    lead = dict(leads["L001"])
    lead.pop("email_source_url")
    assert "email_unsourced" in codes(render(lead, profile))
