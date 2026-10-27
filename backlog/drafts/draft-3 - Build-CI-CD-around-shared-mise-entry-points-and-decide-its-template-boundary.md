---
id: draft-3
title: Build CI/CD around shared mise entry points and decide its template boundary
status: Draft
created_date: 2026-10-26 15:41
labels:
- ci
- cd
- mise
- architecture
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Goal
Move suitable verification and release orchestration into CI/CD while keeping local and hosted behavior aligned. Decide whether CI/CD remains part of this template or becomes a composable template later.

Draft direction
- Define a small set of CI entry points, such as test, check, and release, that call the same mise tasks used locally.
- Build GitHub Actions and GitLab CI from those entry points rather than duplicating shell commands.
- Include selected optional integrations in CI only when present.
- Separate fast pull-request checks from full tests, release, deep review, and scheduled work.
- Record the tradeoffs between retaining CI/CD here and extracting a dedicated template: independent updates, composition complexity, shared-file ownership, platform choices, and migration of existing projects.
- Do not extract a separate template until that comparison produces an explicit decision.

Acceptance criteria
- CI failures provide the same command a maintainer can run locally to reproduce them.
- Workflow YAML contains orchestration rather than duplicate quality logic.
- Both supported VCS platforms have tested generation paths.
- The design records which files and questions would move if CI/CD becomes independent.
- Existing projects have a documented update path for the chosen boundary.
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
