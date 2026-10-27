---
id: draft-6
title: Design which language servers are installed
status: Draft
created_date: 2026-10-27 10:57
labels:
- lsp
- tooling
- editors
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Goal
Decide which language servers (LSPs) each generated project — and each layer
template — installs and configures, as part of the base/layer model.

Draft direction
- Each layer template that owns a language or domain also owns the editor
  language servers its tooling wants (e.g. python layer -> ruff/pyright LSP).
- Keep LSP installation reviewable and versioned like any other tool pin, not
  ad hoc.

Open questions
- Scope: per-language LSPs installed by the python (and future) layers, or a
  broader review including alint's editor/LSP integration?
- Which LSPs are in scope for the first pass, and where their config lives
  (editors, mise tools, dev-dependencies)?

Acceptance criteria
- A list of language servers per layer, each with a reason to include.
- A stated home for LSP config and installation.
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
