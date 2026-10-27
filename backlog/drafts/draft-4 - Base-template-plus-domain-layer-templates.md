---
id: draft-4
title: Base template plus domain layer templates
status: Draft
created_date: 2026-10-27 10:57
labels:
- architecture
- layering
- copier
- composition
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Goal
Restructure this repo from one flat meta-template into a **base template** plus
composable **layer templates** (python, agentic) that add or modify tooling and
configuration per domain.

Draft direction
- **base template** — the foundation every generated project gets, independent
  of language or agent workflow.
- **layer template** — a domain-isolated unit (python tooling, agentic loops,
  CI platform, per-language LSPs) applied over the base; owns its own tools and
  config and stays out of other domains.
- Layers trade flat options (include_openspec, include_alint, task_management)
  for composition units, so each domain's complexity is edited in one place.
- **litmus test** — a tool belongs in the agentic layer only if it could not be
  used without agents; otherwise it belongs in the base or a non-agentic
  (language, workflow, quality) layer.
- **copier-cat owns composition** — inter-template ordering and dependency
  resolution are reserved for copier-cat; native Copier composes only within a
  single template, so today the domains stay flat, each owning whole blocks so
  later extraction into layer templates is mechanical.
- **keep the layer count small** — a generated project needing ~10 layers is
  too many; layers are broad domains (python, agentic), not one-tool-per-layer.

Open questions
- Layer templates are separate Copier templates applied over a shrinking base;
  their sequencing/ordering is reserved for copier-cat. Native Copier is
  single-template (managed blocks only), confirmed.
- Where do today's flat options (openspec, backlog, alint) land once python and
  agentic become layers? Quality/workflow stay flat until a domain reaches
  ~2-3 tools, then graduate.
- Terminology: "layer" already means an inner agentic *concern* in the managed
  glossary. Use "layer template" for the composition unit; rename the inner
  sense separately.

Acceptance criteria
- A crisp definition of "base template" and "layer template" that does not clash
  with the managed glossary.
- A concrete composition mechanism (sequenced templates vs. sections, and the
  tool that applies them) stated and agreed.
- A migration note explaining where each current flat option moves.
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
