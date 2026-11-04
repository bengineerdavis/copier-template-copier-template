---
id: CTCT-11
title: Make TOML formatting deterministic across tool versions
status: Done
created_date: 2026-11-04 17:07
updated_date: 2026-11-04 18:02
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Retrying pre-commit run 40605717289 on current main failed because tombi-format modified one TOML file, although local mise run check passed. Reproduce the version difference and make CI and local hook results deterministic.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 The exact CI tombi version/invocation and the differing TOML edit are identified
- [ ] #2 Committed TOML is stable under both the local and CI formatter invocations
- [ ] #3 The affected checks pass locally and on a fresh CI run
- [ ] #4 Tool-bump failure 41474087600 is separately diagnosed and either addressed by this task or linked to its existing task
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->
Reproduced on retry 40605717289 and scheduled tool-bump 41474087600: uv-lock and tombi-format alternated uv.lock indentation. Generated prek.toml was invalid TOML and .tmpl templates escaped file-type detection. Branch ctct-11-stabilize-ci-format has per-hook uv.lock excludes, a top-level generated-config exclude, and a parsing regression test. Local: mise run check green; 45 passed, 2 skipped; formatter -> uv-lock -> formatter stable. Awaiting CI on 1adc59c.
CI passed on pushed 1adc59c (run 41876313818) and 52cb94b (run 41876741889). Follow-up fixes generated jsonschema/alint TOML: parsing and prek validation now assert all 20 hook IDs survive. Tool-bump 41474087600 had the identical tombi-format failure; no separate opencode updater defect. Final local gate: 45 passed, 2 skipped; mise run check green. Awaiting fast-loop reviews.
Fast loop: job 274 found Python 3.10 tomllib incompatibility; fixed in 4e624ce and verified on Python 3.10.17. Job 278 passed and recommended full hook attributes; strengthened in 86720d8. Jobs 274/278 closed. Job 281 passed 4e624ce with no findings. Latest review 282 pending. GitHub received pushed 4e624ce/86720d8 but has not started Actions runs for them; earlier 1adc59c and 52cb94b pre-commit runs passed. Preparing clean wt merge; preserve external Lore-owned changes.
Merged to local main ending 8c08e89. Root TOML-formatter and generated-prek-config fixes reviewed in jobs 274, 278, 281, 282; all findings resolved and affected code reviews pass. Full Python 3.10 suite independently passed 45 tests with 2 skips; Python 3.14 run also 45 passed, 2 skipped. Pre-merge mise run check green; formatter -> uv-lock -> formatter stable. Branch CI 41876313818 and 41876741889 green. Later pushes were not assigned Actions runs; main push will retrigger CI. Lore housekeeping included in the merged series to prevent data loss from concurrent generated files. Remote main push still pending.
<!-- SECTION:IMPLEMENTATION_NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->

<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
<!-- DOD:END -->
