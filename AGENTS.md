# Historical public archive

Every tracked file and commit to this origin is public. Do not add personalized
briefings, private records, private-site identifiers or credentials. Preserve
existing editions.

The daily briefing publishing responsibility has retired from this repository.
Do not dispatch Pages/Worker deployment without explicit maintenance-publication
approval, revive scheduled jobs, run digest
generators or use the reading importer to write/push new content. Existing HTML
and configuration are retained for provenance, not deployment instructions.

Maintenance covers source reliability, tests and sanitized archive documentation.
Use synthetic local fixtures and temporary output paths. Do not invoke bird,
summary providers or live sources. Run `python3 -m unittest discover -s tests -v`
and `node tests/test_cache_ownership.cjs`. Tests do not establish hosted behavior.
See [review ledger](docs/reviews/2026-10-15.md) for coverage and rollback boundaries.

Read-only provider checks on 2026-10-15 confirmed active GitHub Pages legacy
publishing from main. The user authorized preservation on the separate
`review/six-area-20261015` branch after checking branch triggers. The user then
explicitly approved merging/pushing its reviewed maintenance candidate
`acadee9e4be232d59e9b447e1effb86a7730b098` to the existing public website on
2026-10-15. This permits that bounded maintenance publication through the normal
main/Pages path, including sanitized release evidence. It does not permit new
briefing editions, private content, configuration/access changes, a separate
Worker deployment or restarted schedules. Future publication requires its own
applicable authorization.
See [publication evidence](docs/reviews/2026-10-15-publication.md).
