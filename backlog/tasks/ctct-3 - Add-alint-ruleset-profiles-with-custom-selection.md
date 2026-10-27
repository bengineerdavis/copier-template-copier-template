---
id: CTCT-3
title: Add alint ruleset profiles with custom selection
status: In Progress
created_date: 2026-10-27 17:55
updated_date: 2026-10-27 19:17
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Replace the hardcoded generated .alint.yml with answer-driven profile selection: minimal/python/python-agentic/custom profiles, an additive alias list, ci/github-actions auto-append on GitHub, alias validation, and an answer-driven render instead of alint init.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 copier.yml gains alint_profile (choices) and alint_extra_bundles (yaml list) gated on include_alint, plus a hidden alint_bundle_aliases whitelist
- [ ] #2 Generated .alint.yml renders from answers: oss-baseline always, then profile bundles, additive extras, and ci/github-actions auto-added on github
- [ ] #3 Unknown aliases are rejected at render via a validator
- [ ] #4 Default generation (include_alint false) is byte-unchanged and still omits .alint.yml
- [ ] #5 Repo root .alint.yml stays its five bundles; tests cover each profile, custom, extras, and CI auto-append; mise run check and the full suite pass
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
