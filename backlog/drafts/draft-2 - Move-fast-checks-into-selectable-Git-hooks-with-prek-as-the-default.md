---
id: draft-2
title: Move fast checks into selectable Git hooks with prek as the default
status: Draft
created_date: 2026-10-26 15:41
labels:
- hooks
- prek
- pre-commit
- quality
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Goal
Let users choose prek or pre-commit for Git hooks, with prek as the default. Move suitable fast checks out of manual-only mise commands and into the commit workflow.

Scope
- Add a hook_runner question with prek and pre-commit values; default to prek.
- Generate the native configuration and installation commands for the selected runner.
- Keep prek.toml for prek and use .pre-commit-config.yaml for pre-commit. Do not generate both active configurations.
- Put fast, deterministic checks such as lint, formatting, YAML/TOML validation, and selected alint rules in pre-commit hooks.
- Keep slow tests, deep review, release, and other expensive work out of the default commit path.
- Preserve conventional commit checks and existing optional integrations.
- Document migration behavior when an existing project changes runner.

Acceptance criteria
- The default render selects prek and installs its hooks through the normal mise setup task.
- The pre-commit render provides equivalent hook behavior through pre-commit.
- Only one hook runner owns a given check.
- Local hook behavior and CI use the same underlying commands where practical.
- Tests render and validate both runner choices, including optional alint integration.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
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
