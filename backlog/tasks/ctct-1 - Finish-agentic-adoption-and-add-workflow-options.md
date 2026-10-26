---
id: CTCT-1
title: Finish agentic adoption and add workflow options
status: In Progress
created_date: 2026-10-25 20:22
updated_date: 2026-10-25 20:59
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Port applicable Python quality practices and add independently selectable OpenSpec and Backlog.md/backlog-md-py support without regressing the fork.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Existing fork answers, licensing, generated-template behavior, and tasks remain intact
- [x] #2 Python lint, format, and type-check practices are available through mise
- [x] #3 OpenSpec and either backlog implementation can be selected independently and generate initialized, runnable project files and agent guidance
- [x] #4 Default generation stays free of optional planning tools and the full test suite passes
- [x] #5 Generated templates can independently opt into alint with pinned tooling, configuration, hooks, and verification tasks
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->
Agentic layer stamped through its merge CLI; Python practices and planning options remain to implement.
Also add an optional alint integration for generated templates; the agentic layer already adopts alint in this repository.
Implemented independent OpenSpec, Backlog.md/backlog-md-py, and alint options with initialized files and agent guidance. Ported Ruff/format/mypy quality gates without the Typer scaffold. Verified 37 passed / 2 skipped, quality and check gates, generated-project prek, both backlog CLIs, OpenSpec init, alint, and mise install.
<!-- SECTION:IMPLEMENTATION_NOTES:END -->
## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Added independent opt-in OpenSpec, Backlog.md/backlog-md-py, and alint workflows; added Python quality gates; preserved existing fork behavior. Full suite: 37 passed, 2 skipped.
<!-- SECTION:FINAL_SUMMARY:END -->
## Definition of Done
<!-- DOD:BEGIN -->
<!-- DOD:END -->
