---
name: olivia-discover
description: Find candidate opportunities (clients, partners, jobs, investors, tenders) for an OLIVIA opportunity profile by searching LinkedIn posts, people and companies, then write them as leads with status "discovered". Use when the user asks to look for prospects, leads or opportunities for a profile in profiles/.
---

# OLIVIA · Discover

Turn an opportunity profile into a list of candidate leads, each backed by one recent public post.

## Inputs

- A profile from `profiles/*.yaml`. Read `segments` (in priority order), `geography`, `language` and `qualification.max_days_since_last_post`.
- Read-only access to LinkedIn search (the user's own logged-in browser) and to the web.

## Steps

1. **Posts first.** For each segment, in order, run a LinkedIn **content** search per `search_terms` entry, filtered to the profile's recency window (default: past month). Posts give evidence and recency at the same time; people searches only give headlines.
2. **People and companies second.** Run people and company searches with the same terms to catch active people the post search missed.
3. **For every candidate, record:**
   - name, headline, organization, country;
   - the post URL, its date and a one-sentence factual summary of what it says (`evidence_url`, `evidence_date`, `evidence_summary`);
   - whether the post or profile offers services ("Ver mis servicios", a site, an email).
4. **Write leads** as rows matching `schemas/lead.schema.json` with `status: discovered`. Leave `opener` and `complement` empty for now; `olivia-personalize` fills them.

## Rules

- **Read only.** Never connect, follow, react, comment or message during discovery.
- **Evidence or nothing.** A candidate without a dated public post in the window is not a lead.
- **Summaries are factual.** Describe what the post says. Do not infer opinions, mood or relationships.
- **Respect geography.** Drop candidates outside `geography.countries` unless the user says otherwise.
- Stop after 2–3 failed attempts on a page and report what blocked you; do not retry the same action in a loop.

## Output

A CSV (or rows in the configured registry) plus a short summary: how many candidates per segment and which segments came back thin.
