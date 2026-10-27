---
id: CTCT-4
title: 'Correct renovate app install docs: CLI reality + manual fallback'
status: Done
created_date: 2026-10-27 19:14
updated_date: 2026-10-27 19:21
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
Merged as 8127f04 (docs: correct renovate app install guidance). Review 192 fail (gh browse rejects bare URLs) -> amended; re-review 195 pass, zero findings; 192 closed. Install verified impossible via CLI/API for third-party apps (browser consent by design; enterprise-only API route).
<!-- SECTION:IMPLEMENTATION_NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->

<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
<!-- DOD:END -->
