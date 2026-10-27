---
id: draft-1
title: Simplify the mise project-management interface
status: Draft
created_date: 2026-10-26 15:41
labels:
- mise
- interface
- project-management
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Goal
Provide a small, task-oriented mise interface for daily project work. Keep advanced commands available, but hide their composition behind a few memorable entry points.

Current problem
The template exposes many low-level commands, including format-check, type-check, quality, backlog-list, roborev-status, and update-template-auto. Users must know which commands exist and how to combine them.

Draft direction
- Define a compact command taxonomy before implementation. Candidates are install, check, fix, test, tasks, board, review, and ci.
- Compose existing tasks rather than duplicating their shell logic.
- Keep low-level tasks as an advanced interface where they remain useful.
- Render optional-tool tasks only when their integration is selected.
- Check native mise alias, dependency, and argument-passing capabilities before adding any wrapper script.

Acceptance criteria
- A new user can discover and run the common workflow from mise tasks.
- One entry point runs the complete local verification suite.
- Common task and board operations do not require remembering the selected backlog CLI.
- Optional integrations do not leave broken commands in projects that did not select them.
- Tests cover the public command set and the existing advanced commands that remain supported.
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
