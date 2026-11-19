---
id: CTCT-15
title: Adopt shared workflow plugin refresh in the meta-template
status: Done
created_date: 2026-11-12 04:54
assignee:
- opencode-dotagents-projection
updated_date: 2026-11-19 21:21
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
The agentic layer is adopted and must consume APT-47 through the ordinary update path, not duplicate its plugin declarations. Recover from any conflicts honestly and do not silently overwrite customized child state.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 The manifest and bootstrap match the shared composition path; project-specific tool choices and unrelated customizations survive.
- [x] #2 A real disposable-HOME install projects tdd, grilling, and writing-for-agents from the reviewed Matt Pocock plugin.
- [x] #3 The update and test results, including any conflicts and deliberate non-goals, are recorded before publication.
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:IMPLEMENTATION_NOTES:BEGIN -->
2026-11-17: Scoped child propagation uses the composed APT-47 fragment, not an independent plugin list. Broad update produced conflicts in agents.toml, .lore.md, and docs/experiments.md; isolated worktree was reset and no broad update is claimed. Preserving current backlog/lore/worktree choices avoids unrelated migration. Exact refresh body ran twice with a fresh test-user HOME and projected tdd, grilling, and writing-for-agents. Upstream software-factory frontmatter remains an explicit warning. Full suite 47 passed, 1 skipped; all prek hooks pass.
2026-11-19: Parent APT-47 / agentic-project-template PR #17 merged as d8d3bf1. Child branch is current with its origin/main (no new merge required). Rebuilt stale moved venv: 47 passed, 1 skipped, 46 Copier dirty-worktree warnings caused by untracked generated artifacts; uv run prek run --all-files passed all applicable hooks. Local untracked generated files remain outside commits: .agents/skills/backlog-workflow/, .opencode/skills/, .pr-body.md, CODING_STANDARDS.md, docs/agents/, scripts/check-worktree.sh, scripts/wt-owners.sh. No broad layer update claimed.
Generated untracked runtime artifacts were preserved before worktree retirement under /Users/ben.davis/code/personal/templates/copier-template-copier-template/.worktree-preserved/ctct-dotagents-projection/. No broad Copier update or unrelated backlog/lore/worktree migration is claimed. APT-48 is separately merged; any child ADHD adoption is future composition work, not silently applied here.
<!-- SECTION:IMPLEMENTATION_NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Merged scoped child PR #3 as cdf3fb6f2c45ee3c500cb947e9604a8e2d128ac0 after parent APT-47 merged. The child preserves its customized bootstrap and existing backlog/lore/worktree choices. Local verification after rebuilding the moved venv: 47 passed, 1 skipped; all applicable prek hooks passed. CI passed pre-commit and Python 3.10-3.14.
<!-- SECTION:FINAL_SUMMARY:END -->

## Definition of Done
<!-- DOD:BEGIN -->
<!-- DOD:END -->
