---
id: CTCT-13
title: Preserve customized files during the meta-template self-update
status: To Do
created_date: 2026-11-10 01:36
labels:
- update
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Observed 2026-11-09 on an isolated committed copy of this repository: copier update from the template left conflict markers in AGENTS.md, README.md, mise.toml, prek.toml, .alint.yml and other customized files. The self-update must stop and report conflicts for review, never auto-resolve or silently discard project customizations (branch-sync adoption decision T3). This is a separate update-preservation issue, not a passing test.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 self-update on a customized meta-template child stops with an actionable conflict report and no conflict markers
- [ ] #2 a regression test proves a clean self-update preserves recorded answers and customizations
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->

<!-- SECTION:IMPLEMENTATION_NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->

<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
<!-- DOD:END -->
