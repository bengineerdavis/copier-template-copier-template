---
id: CTCT-4
title: 'Correct renovate app install docs: CLI reality + manual fallback'
status: In Progress
created_date: 2026-10-27 19:14
updated_date: 2026-10-27 19:14
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
docs/tool-updates.md links a nonexistent app slug (mend-renovate; the real app is github.com/apps/renovate) and implies the app install is automatable. GitHub requires browser consent for third-party app installs (no API path outside enterprise admins), so record the CLI-assisted manual flow and post-install verification.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Operational notes name the correct app slug and install URL
- [ ] #2 Notes state that CLI/API installation is not possible for third-party apps and give the one-command manual fallback
- [ ] #3 Notes give a CLI verification step for post-install (onboarding PR by app/renovate)
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
