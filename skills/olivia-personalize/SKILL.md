---
name: olivia-personalize
description: Write the personalized opener, complement paragraph and subject for qualified OLIVIA leads, then run `olivia render` to produce guardrail-checked drafts for human approval. Use after olivia-qualify, when the user wants outreach messages drafted.
---

# OLIVIA · Personalize

Each message has four parts. Only the first two are written per lead; the rest come from the profile.

| Part | Source |
|---|---|
| Opener (1–2 sentences) | Written per lead from `evidence_summary` |
| Complement (1 sentence) | Written per lead, guided by the segment's `complement_hint` |
| Offer block | `profile.offer` |
| Call to action and signature | `profile.call_to_action`, `profile.sender` |

## Writing the opener

- Cite **one specific thing the person published**: the post's idea, a figure they quoted, an event they announced. Paraphrase; do not paste long quotes.
- Then one sentence on why it matters for the sender's offer.
- Never claim a relationship you cannot prove: "Sigo de cerca tu trabajo", "Sigo con interés", "Siempre leo…" are blocked by the guardrails.
- If the only evidence is a headline, say so honestly: "Vi tu perfil y tu trabajo en…".

## Writing the complement

One sentence: what they do + what the sender does, as two halves of one job. Start from the segment's `complement_hint`.

## Register

Use voseo for countries in `language.voseo_countries` (default Argentina and Uruguay) and tú everywhere else. The renderer picks the template; your opener and complement must match it (for example "vos definís" vs "tú defines"). Mismatches are blocked.

## Subject

Short, specific to their topic, no clickbait, no emoji. Example: "ISO 42001 en los equipos de desarrollo".

## Then render

```bash
olivia render leads.csv --profile profiles/<profile>.yaml --out outbox/
```

Show the user the drafts in `outbox/` and every blocked row in `outbox/report.csv` with its reason. **Never send.** Sending happens only after the user approves each message (see the future `olivia-send` skill).
