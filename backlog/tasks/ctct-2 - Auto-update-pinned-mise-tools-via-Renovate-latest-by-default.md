---
id: CTCT-2
title: Auto-update pinned mise tools via Renovate (latest by default)
status: Done
created_date: 2026-10-27 06:21
updated_date: 2026-10-27 17:58
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The http:opencode pin in mise.toml went stale (2.0.32 while upstream is 2.1.4) because nothing scheduled updates it and its checksums are hand-maintained. Make tool versions track latest by default using the repo's existing scheduler (Renovate), and document the deliberate exceptions.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 mise.toml installs opencode via the registry short name (aqua backend) at the current latest version, with the hand-maintained checksum block removed
- [ ] #2 Renovate updates the opencode pin via a custom manager (github-tags on anomalyco/opencode)
- [ ] #3 Renovate automerges mise tool updates; python stays pinned at 3.12 with the reason recorded
- [ ] #4 docs/tool-updates.md records the versioning policy, the scheduled flow, and the deliberate exceptions
- [ ] #5 mise run check passes and mise-installed opencode --version reports the pinned version
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->
Merged to main as c2bb61f (feat: scheduled tool updates: renovate mise manager for aqua-backed pins + tool-bump workflow/scripts for opencode 2.0.32->2.2.0), e2bf798 (macOS portability), 43d5b13 (doc/rule accuracy). Fast loop: 182 fail (2 low) -> fixed; 187/188 pass with zero findings; review 182 closed with resolution comment. Gate: mise run check green (3 pre-existing repo infos). opencode --version verifies 2.2.0 via mise. Remaining (user): install Mend Renovate App; push main.
<!-- SECTION:IMPLEMENTATION_NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->

<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
<!-- DOD:END -->
