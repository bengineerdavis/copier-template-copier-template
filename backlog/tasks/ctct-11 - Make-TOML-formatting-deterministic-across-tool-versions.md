---
id: CTCT-11
title: Make TOML formatting deterministic across tool versions
status: Done
created_date: 2026-11-04 17:07
updated_date: 2026-11-04 22:29
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Retrying pre-commit run 40605717289 on current main failed because tombi-format modified one TOML file, although local mise run check passed. Reproduce the version difference and make CI and local hook results deterministic.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 The exact CI tombi version/invocation and the differing TOML edit are identified
- [x] #2 Committed TOML is stable under both the local and CI formatter invocations
- [x] #3 The affected checks pass locally and on a fresh CI run
- [x] #4 Tool-bump failure 41474087600 is separately diagnosed and either addressed by this task or linked to its existing task
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->
Reproduced on retry 40605717289 and scheduled tool-bump 41474087600: uv-lock and tombi-format alternated uv.lock indentation. Generated prek.toml was invalid TOML and .tmpl templates escaped file-type detection. Branch ctct-11-stabilize-ci-format has per-hook uv.lock excludes, a top-level generated-config exclude, and a parsing regression test. Local: mise run check green; 45 passed, 2 skipped; formatter -> uv-lock -> formatter stable. Awaiting CI on 1adc59c.
CI passed on pushed 1adc59c (run 41876313818) and 52cb94b (run 41876741889). Follow-up fixes generated jsonschema/alint TOML: parsing and prek validation now assert all 20 hook IDs survive. Tool-bump 41474087600 had the identical tombi-format failure; no separate opencode updater defect. Final local gate: 45 passed, 2 skipped; mise run check green. Awaiting fast-loop reviews.
Fast loop: job 274 found Python 3.10 tomllib incompatibility; fixed in 4e624ce and verified on Python 3.10.17. Job 278 passed and recommended full hook attributes; strengthened in 86720d8. Jobs 274/278 closed. Job 281 passed 4e624ce with no findings. Job 282 passed the strengthened test. Merged to local main ending 8c08e89 with full local gates green.
Published fcc376d CI passed: Tests 41911569712 across all five supported Python versions, pre-commit 41911569801, Release 41911569982. Review 300 passed the follow-up scoped exclusion: only check-toml excludes uv.lock; uv-lock and gitleaks remain eligible. Local Python 3.10 evidence: 45 passed, 2 skipped, using uv run --python 3.10 --frozen pytest -q on a tree free of upstream release tags. If upstream tags have been fetched, CTCT-6 records the independent tag-pollution failure affecting test_update_default; this does not affect the published CI evidence.
Final scoped-exclusion merge and publication pending.
Combined CTCT-5/CTCT-11 rebased tree: 52 passed, 2 skipped on Python 3.10; mise run check green. Formatter -> uv-lock -> formatter repeated stable. Review 301 evidence caveat addressed with the CTCT-6 precondition in the task record.
<!-- SECTION:IMPLEMENTATION_NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Formatter ownership and generated prek configuration are deterministic: uv-lock remains responsible for uv.lock; only the generic TOML check excludes it. Main CI passed on fcc376d across Python 3.10-3.14, pre-commit, and Release. Final scoped-exclusion follow-up has 45 passing tests and 2 skips on Python 3.10 under the documented tag-clean precondition; merge/publication pending.
Combined-tree verification adds 52 passing tests and 2 skips on Python 3.10.
<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
<!-- DOD:END -->
