# Experiments — copier-template-copier-template

The method: isolate one **variable under test** from **relative constants**
(mise, prek, hooks, the agentic layer itself). What you learn about the
variable is attributable to the variable because the constants only move
deliberately. Log constant changes as `[harness]` entries so they never
quietly contaminate a conclusion.

## Log

Append newest first. One entry per deliberate change or finding.

### 2026-10-26 — [harness] opencode pin ownership: unowned http block → scheduled tool-bump workflow

- Question: can pinned CLI tools stay current without a human remembering
  to refresh URLs and checksums?
- Setup: found the `http:opencode` pin stale (2.0.32 while upstream was on
  2.x). Registry short name (aqua) and npm both resolve only the 1.x
  stream — upstream publishes 2.x as tags with no release objects — so the
  pin keeps the http backend but gains a scheduled owner:
  `scripts/update-opencode.sh` + a weekly workflow that bumps version,
  URLs, and checksums atomically. Aqua-backed pins (prek, tombi,
  worktrunk) ride Renovate's native mise manager. Policy in
  docs/tool-updates.md.
- Result: first scripted bump took the pin 2.0.32 → 2.2.0 with fresh
  checksums; every concrete pin in mise.toml now has a scheduled update
  path; python = "3.12" is the only deliberate exception, reason recorded.
- Verdict: promote-to-tooling

### YYYY-MM-DD — [variable] <what is being tried>

- Question:
- Setup:
- Result:
- Verdict: keep | revert | promote-to-tooling

<!-- managed by agentic-project-template -->
