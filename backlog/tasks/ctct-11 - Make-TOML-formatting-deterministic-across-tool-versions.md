---
id: CTCT-11
title: Make TOML formatting deterministic across tool versions
status: In Progress
created_date: 2026-11-04 17:07
updated_date: 2026-11-04 17:18
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
<!-- SECTION:IMPLEMENTATION_NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->

<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
<!-- DOD:END -->
