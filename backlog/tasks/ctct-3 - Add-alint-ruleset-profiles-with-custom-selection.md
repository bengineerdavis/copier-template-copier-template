---
id: CTCT-3
title: Add alint ruleset profiles with custom selection
status: Done
created_date: 2026-10-27 17:55
updated_date: 2026-10-27 20:11
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Replace the hardcoded generated .alint.yml with answer-driven profile selection: minimal/python/python-agentic/custom profiles, an additive alias list, ci/github-actions auto-append on GitHub, alias validation, and an answer-driven render instead of alint init.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 copier.yml gains alint_profile (choices) and alint_extra_bundles (yaml list) gated on include_alint, plus a hidden alint_bundle_aliases whitelist
- [x] #2 Generated .alint.yml renders from answers: oss-baseline always, then profile bundles, additive extras, and ci/github-actions auto-added on github
- [x] #3 Unknown aliases are rejected at render via a validator
- [x] #4 Default generation (include_alint false) is byte-unchanged and still omits .alint.yml
- [x] #5 Repo root .alint.yml stays its five bundles; tests cover each profile, custom, extras, and CI auto-append; mise run check and the full suite pass
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->
Merged as 5cc838c, 22f5914, 985873a. Evidence: profile/custom/extras/CI/dedup/rejection tests all pass; mise run check green; roborev 197 fixed, 198-199 pass. Full suite 44 passed / 1 skipped / 1 pre-existing failure (test_update_default resolves upstream tag v0.18.3).
<!-- SECTION:IMPLEMENTATION_NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->

<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
<!-- DOD:END -->
