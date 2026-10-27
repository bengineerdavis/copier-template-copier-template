---
id: CTCT-6
title: Stop upstream tags from polluting local copier resolution
status: To Do
created_date: 2026-10-27 20:12
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Upstream release tags (v0.18.2, v0.18.3) fetched via the upstream remote leak into local copier tag resolution: run_copy/run_update with vcs_ref=None pick the highest tag among all local refs, so tests and local renders resolve non-fork code (v0.18.3 requires copier >=9.19.1 vs the fork's 9.18.2). Fix the tag-hygiene root cause so a clean local tree resolves only fork tags.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 test_update_default no longer resolves the upstream v0.18.3 tag on a clean local tree
- [ ] #2 Local copier copy/update without an explicit vcs_ref resolves a fork tag, not an upstream release
- [ ] #3 The chosen fix (test pinning, upstream tag pruning, or both) is documented in HANDOFF or docs/
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
