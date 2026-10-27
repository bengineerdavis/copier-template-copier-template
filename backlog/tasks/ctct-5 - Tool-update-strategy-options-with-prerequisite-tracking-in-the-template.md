---
id: CTCT-5
title: Tool-update strategy options with prerequisite tracking in the template
status: To Do
created_date: 2026-10-27 20:10
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Downstream repos get renovate.json stamped unconditionally with no scheduler and no signal about what is missing (the hosted app requires a browser-consent install; Actions variants need a workflow and, for PAT, a secret). Add a tool_update_strategy question (github-app default / actions-github-token / actions-pat / none), stamp the matching artifacts, and ship a check-tool-updates script + mise task that reads the strategy from the answers file and reports each prerequisite as OK or MISSING with fix instructions. This repo's own instance mirrors the check (github-app + opencode tool-bump prereqs).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 copier.yml asks tool_update_strategy with the four choices, trade-off help text, and default github-app
- [ ] #2 renovate.json is stamped for all strategies except none
- [ ] #3 an Actions-based renovate.yml is stamped only for the two actions strategies, pinned to renovatebot/github-action v46.3.10 digest, wiring GITHUB_TOKEN vs secrets.RENOVATE_TOKEN per variant
- [ ] #4 stamped scripts/check-tool-updates.sh verifies each strategy's prerequisites with OK/MISSING output and fix hints, degrading gracefully without gh or auth, always exiting 0
- [ ] #5 the stamped install task runs the check so users are informed at apply time
- [ ] #6 render tests cover all four strategies (artifact presence/absence and token wiring)
- [ ] #7 this repo gains the same check wired to its own state (github-app + tool-bump workflow prereqs) and docs/tool-updates.md documents the strategies and prerequisite matrix
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
