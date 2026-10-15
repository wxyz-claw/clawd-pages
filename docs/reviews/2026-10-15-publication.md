# Public archive publication investigation — 2026-10-15

Follow-up to the [six-area review](2026-10-15.md). Evidence observed around
04:40–04:43 UTC through read-only GitHub and Cloudflare APIs. No hosting setting,
workflow, scope, domain, archived edition or public content was changed.

## Verified production behavior

- Remote `main` remains `7fa4c4fe5c11454189a202e97cc65e3a6d26af18`.
- GitHub Pages is **built**, uses legacy branch publishing, and selects
  `main` at `/`. Its latest recorded deployment is `7081111235`, environment
  `github-pages`, created `2026-10-15T01:03:47Z` for that exact commit.
  Associated build/status/deploy checks completed successfully. Therefore a
  push to main can auto-deploy even without a checked-in Actions workflow.
- GitHub lists an active dynamic Pages workflow and a historical Eye Rest
  Android workflow. The current main tree has no `.github` directory; fetching
  the historical Android workflow file on main returns 404. Recent runs are
  dynamic Pages builds on main. No new workflow is added by the review branch.
- Repository webhooks list is empty. That does not itself rule out GitHub Apps.
- In the connected Cloudflare account, all three Pages projects were examined
  for repository linkage: none matches `clawd-pages`. No Worker is named
  `clawd-pages` or matches the historical domain label. Both existing Workers
  have tags; each build-trigger list returns HTTP 200 with zero triggers.
  Thus no matching Cloudflare automatic branch build was found in this account.

## Safe preservation route

The user explicitly authorized a non-deploying review branch if supported by
read-only evidence. Publish only `review/six-area-20261015`; do not push main,
create a PR, dispatch a workflow, change Pages configuration or run Wrangler.
GitHub Pages selects main only; the current branch tree has no workflow files,
no repository webhooks were found, and the connected Cloudflare account has no
matching build integration. Changed files are maintenance source, synthetic
tests and sanitized documentation; no archive HTML edition or digest payload.

The branch contains fixes `23927a3a2ef93422654a9e2f9722a389954ed218` and review
record `5859e08ed9590f52b61a511faea8a3bbb8e2f9b9`, plus this follow-up. It does
not apply the service-worker or CLI changes to the existing public deployment.

Verification after push must compare the exact remote branch commit, fetch its
objects and compare file hashes/tree, confirm remote main is unchanged, and
re-read Pages/deployment/Actions metadata for this branch. Preserve the published
review branch with normal history; do not merge it into main while main remains
a deployment source. No access/sharing or scheduler change is part of this work.

## Reproducible read-only checks

```sh
gh api repos/wxyz-claw/clawd-pages/pages
gh api 'repos/wxyz-claw/clawd-pages/deployments?per_page=5'
gh api repos/wxyz-claw/clawd-pages/actions/workflows
gh api 'repos/wxyz-claw/clawd-pages/actions/runs?branch=review%2Fsix-area-20261015&per_page=5'
git ls-remote origin refs/heads/main refs/heads/review/six-area-20261015
python3 -m unittest discover -s tests -v
node tests/test_cache_ownership.cjs
```

Cloudflare reads used GET `/accounts/{account}/pages/projects` (all pages),
GET `/accounts/{account}/workers/scripts`, and GET
`/accounts/{account}/builds/workers/{tag}/triggers` for both returned Workers.
No token, account identity, environment variable or deployment-hook URL is
recorded here. A first Pages request with unsupported pagination was rejected;
retry with page 1/per_page 10 returned all three projects successfully.

## Unknowns and remaining consequential finding

**CP-3, high confidence / high operational priority:** the requested historical
archive boundary does not match the still-enabled main-branch Pages publisher.
It must not be treated as a dormant deployment. Parent/source-automation owners
should reconcile future writes and retirement separately. Disabling Pages or
changing schedules would alter production and is deliberately not performed.

Other Cloudflare accounts, unrelated hosting providers, out-of-band pollers and
future configuration changes are not proven absent. The safety conclusion is
limited to the inspected repository, current provider configuration and connected
Cloudflare account. This read does not establish that old digest-generation jobs
are stopped. No claim of a universal or permanent no-deployment guarantee.

## Remote preservation verified

Published review source commit:
`f1cad3c5c20eb23a43bc21146296445e22c6c51e` on
[`review/six-area-20261015`](https://github.com/wxyz-claw/clawd-pages/tree/review/six-area-20261015).
A fresh fetch matched its complete tree and SHA-256 for all ten changed files.
No HTML edition or JSON digest payload changed. Python and Node regressions pass.
Post-push GitHub reads showed zero Actions runs for the review branch; Pages
still selected main and its latest deployment remained `7081111235` for
`7fa4c4fe5c11454189a202e97cc65e3a6d26af18`. No PR was created.

The original local main contains the earlier maintenance commits; **do not push
local main**. Remote main and production remain at the baseline archive commit.
This follow-up preserves maintenance on the review branch without disabling or
reviving production publishing.

## Explicitly approved maintenance publication

The user explicitly confirmed merging, pushing and publishing the reviewed
maintenance candidate `acadee9e4be232d59e9b447e1effb86a7730b098` to this
repository's existing public website on 2026-10-15. This resolves the earlier
missing-publication-approval hold for this exact action. It does not broaden
content, sharing, hosting, schedules or provider access. The daily briefing
responsibility remains retired here. Only the reviewed safeguards, synthetic
tests and sanitized maintenance/release documentation are in scope.

Fresh read-only preflight confirms remote main and the latest successful Pages
build remain `7fa4c4fe5c11454189a202e97cc65e3a6d26af18`, deployment
`7081111235`, with source main at `/` and public destination
`https://wxyz-claw.github.io/clawd-pages/`. The endpoint responds HTTP 200; both
served service-worker files match that baseline. The candidate's ten-file diff
contains no HTML editions or digest/reading JSON changes. Added-line checks
found no high-confidence credential, signed URL, private-site identifier or
personal-path pattern; this scoped check is not a universal secret guarantee.

The connected Cloudflare account was rechecked: all three Pages projects and
both Workers have no matching repository/domain linkage; both Worker build
trigger lists return HTTP 200 with zero triggers, and the historical custom
domain has no matching Worker mapping. Other accounts and out-of-band triggers
remain unverified. Repository hooks are empty; main's active dynamic Pages
workflow is the intended publisher. No Wrangler command, workflow dispatch,
hosting/configuration change or provider-permission request is needed.

Integrate with a normal merge whose first parent is the baseline above, then
push normally to main and let the existing Pages publisher run. The intended
live changes are `/sw.js` and `/eye-rest/sw.js` cache-deletion ownership; the
Python importer remains static source on Pages and rejects unsupported CLI
publication modes locally. All other historical page/asset bytes are preserved.
Verify deployment SHA/status, both served worker identities, root, reading,
eye-rest, digest and historical archive routes. Do not run any generator or
personal-source/provider call to test this release.

Rollback is a normal `git revert -m 1 <maintenance-merge>` followed by the same
authorized main/Pages path, restoring baseline tracked source without rewriting
history or editions. A later documentation-only release record can be reverted
separately. Retain baseline `7fa4c4fe5c11454189a202e97cc65e3a6d26af18` and
deployment `7081111235`. Rollback is not executed as a test. Existing browser
registrations may update only when checked by their browser; deleted caches
cannot be reconstructed by a source revert. Restoring the old workers would
also restore their broader cache-deletion behavior. No cache purge, unregister,
client-storage reset, recovery or irreversible cleanup is part of this release.

Release preflight reran both Python retirement regressions (two tests, 0.006s)
and the Node test of the real worker activation handlers: all pass. Syntax/diff
checks and the ten-file added-line scope/privacy check pass. Historical HTML,
JSON, manifests, styles, XML, `.nojekyll` and hosting configuration are unchanged.
These fixtures do not prove browser update timing, installation/offline behavior
or live provider access. HTTP deployment/route/worker verification follows the
approved push; no generator, provider or source-ingestion call is involved.
