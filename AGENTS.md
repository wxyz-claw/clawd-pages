# Historical public archive

Every tracked file and commit to this origin is public. Do not add personalized
briefings, private records, private-site identifiers or credentials. Preserve
existing editions.

The daily briefing publishing responsibility has retired from this repository.
Do not dispatch Pages/Worker deployment, revive scheduled jobs, run digest
generators or use the reading importer to write/push new content. Existing HTML
and configuration are retained for provenance, not deployment instructions.

Maintenance covers source reliability, tests and sanitized archive documentation.
Use synthetic local fixtures and temporary output paths. Do not invoke bird,
summary providers or live sources. Run `python3 -m unittest discover -s tests -v`
and `node tests/test_cache_ownership.cjs`. Tests do not establish hosted behavior.
See [review ledger](docs/reviews/2026-10-15.md) for coverage and rollback boundaries.
