---
id: draft-5
title: Multi-tool profile subsystem (prefer Copier-native)
status: Draft
created_date: 2026-10-27 10:57
labels:
- profiles
- copier
- configuration
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Goal
Let a named **profile** select settings across several tools at once (alint
rulesets, openspec, backlog, prek, license defaults), and possibly an
editor-facing CLI to save and update values among profiles.

Draft direction
- A profile is a named, versioned, template-side map of answers spanning
  multiple tools; the renderer expands it.
- Use Copier's native mechanisms (defaults/data file, choices, reusable
  `.copier-answers.yml`) first; build a custom CLI or file format only for what
  Copier cannot already express.
- Multi-select profiles compose (e.g. an agentic profile with one or more
  language profiles), replacing the current single-profile design.

Open questions
- What exactly does Copier's defaults/data + answers-reuse cover, and what
  remains that needs a new format?
- Storage location and merge rules for profiles when several are selected.
- Whether a CLI is justified, and if so its audience and write model.
- Relationship to layer templates (draft-4): profiles may be the selection
  mechanism by which layers are chosen.

Acceptance criteria
- A written comparison of Copier-native mechanisms vs. what a new profile
  format/CLI would add.
- A proposed profile file format and merge rule, or a decision to defer both.
- A decision on whether the CLI ships now or later.
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
