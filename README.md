# Clawd Pages — historical public archive

This repository preserves public digests, reports, reading pages and small web
utilities. Existing editions remain historical evidence. The daily briefing
publishing responsibility has moved away from this repository; this checkout
must not receive new personalized content or private records.

Start with [archive maintenance instructions](AGENTS.md) and the
[review ledger](docs/reviews/2026-10-15.md). The retained `wrangler.jsonc` describes
a former static Worker deployment. It is historical configuration, not an
instruction to deploy. Public maintenance publication requires explicit approval;
do not restart old jobs.
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
The user explicitly approved the reviewed October 15 maintenance publication
through that existing main/Pages path. This applies only to the cache-ownership
and retired-importer safeguards, synthetic tests and sanitized documentation;
archive editions and digest payloads stay unchanged. It does not revive briefing
publication or authorize private content, hosting changes or schedules. See the
[provider evidence and limits](docs/reviews/2026-10-15-publication.md).
