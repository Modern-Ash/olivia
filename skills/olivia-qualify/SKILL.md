---
name: olivia-qualify
description: Score and filter OLIVIA leads with status "discovered" against an opportunity profile, verify each person's identity, and find a public contact channel. Use after olivia-discover, before writing any message.
---

# OLIVIA · Qualify and verify

Decide who is worth contacting, confirm they are who we think they are, and find how to reach them.

## 1. Qualify

Drop or downgrade a lead when any of these is true:

- Their employer is in `qualification.exclude_employers` (large consultancies, by default).
- They sell what the profile's sender sells (`qualification.exclude_if_offers`): that is a competitor, not an opportunity.
- Their last post is older than `qualification.max_days_since_last_post`.
- `qualification.require_offers_services` is true and nothing shows they sell services.

Set `priority: high` for the top segment's strongest matches (recent post, offers services, mutual connections), `normal` otherwise. Status → `qualified`.

## 2. Verify identity (mandatory)

Open the profile you plan to contact and confirm that **name, headline and organization** all match the person from the evidence post. Only then set `identity_verified: true`.

> In the seed campaign a search by name returned a different person with the same surname in another country. A shared surname is not a match.

## 3. Find the channel

In order of preference:

1. An address **published** by the person or their organization (contact page, site footer, LinkedIn contact info). Record it in `email`, its page in `email_source_url`, and set `email_is_generic: true` for info@/contacto@-style inboxes.
2. Otherwise `channel: linkedin_dm`.

Never guess addresses from name patterns and never use address-finding services. If a site hides the address behind a form, record the form URL in `notes` and use LinkedIn.

## Output

Leads with `status: qualified`, `identity_verified` set, and `channel` chosen. Report how many were dropped and why.
