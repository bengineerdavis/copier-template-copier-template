---
id: CTCT-12
title: Use the official alint pre-commit integration by default
status: In Progress
created_date: 2026-11-10 00:33
labels:
- alint
updated_date: 2026-11-10 00:41
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Structure linting belongs in every stamped template. Use the documented asamarts/alint-pre-commit mirror at a tagged release for the hook; keep mise owning the alint CLI for direct task and LSP usage. Propagate to the agentic template and ai-prompt-library through their normal update paths.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 include_alint defaults to true and new stamps get the documented tagged mirror hook
- [ ] #2 mise declares the alint CLI and the quality task uses it
- [ ] #3 tests prove fresh stamp and real hook behavior
<!-- AC:END -->

## Implementation Notes

Draft PR: https://github.com/bengineerdavis/copier-template-copier-template/pull/2 (CTCT-12). Official integration: https://alint.org/docs/integrations/pre-commit/.

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->
2026-11-09: 46 passed, 1 skipped; official mirror hook passed. PR is opened on the author fork, never upstream.
<!-- SECTION:IMPLEMENTATION_NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->

<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
<!-- DOD:END -->
