# Clawd Pages — historical public archive

This repository preserves public digests, reports, reading pages and small web
utilities. Existing editions remain historical evidence. The daily briefing
publishing responsibility has moved away from this repository; this checkout
must not receive new personalized content or private records.

Start with [archive maintenance instructions](AGENTS.md) and the
[review ledger](docs/reviews/2026-10-15.md). The retained `wrangler.jsonc` describes
a former static Worker deployment. It is historical configuration, not an
instruction to deploy. Do not dispatch a public deployment or restart old jobs.
There is no checked-in GitHub Actions workflow.

The reading importer permits only an offline preview using an explicit local
thread fixture and no live summary provider:

```sh
python3 reading/ingest.py --dry-run --thread-file /tmp/synthetic-thread.txt --no-summary
python3 -m unittest discover -s tests -v
node tests/test_cache_ownership.cjs
```

These source checks do not modify editions or publish anything. Historical
generators and templates remain for provenance; do not run them against the
archive. External schedules, hosting and authentication are not proven by source
review.

Read-only follow-up confirmed that **GitHub Pages still publishes from `main`**.
Maintenance preservation uses a separate review branch; do not push these changes
to main or infer that retirement disabled hosting. See the
[provider evidence and limits](docs/reviews/2026-10-15-publication.md).
