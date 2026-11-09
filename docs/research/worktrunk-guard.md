# Does Worktrunk already provide the worktree guard?

Question asked from the wayfinder template-stack effort: we hand-rolled a
"worktree guard" (a `prek` pre-commit hook that refuses an agent commit made
from the main checkout). Worktrunk documents its own `pre-commit` hook type and
ships an OpenCode plugin with a **worktree isolation** capability. Are we
duplicating it, conflicting with it, or correctly placed?

**Answer: correctly placed, and one half of mechanism B is already built by
Worktrunk.** No conflict. But two facts change the design: (1) a Worktrunk
`pre-commit` hook does **not** fire on a plain `git commit`, so it cannot
replace our guard; (2) a Worktrunk *project* hook **fails open** when the human
declines the approval prompt, so it must never be the enforcement point. The
plugin's worktree strategy, however, does cover the session-start half of
mechanism B.

## The decisive table: which hook fires on which commit path

| Commit path | Our `prek` guard fires | Worktrunk `pre-commit` fires |
|---|---|---|
| `git commit` | **yes** | **no** |
| `git commit --no-verify` | no (by design) | no |
| `wt step commit` | yes (git hooks run) | yes |
| `wt step squash` | yes | yes |
| `wt merge` | yes | yes |

Evidence for the right-hand column: `wt hook --help`, hook-purpose table —
"`pre-commit` — Formatters, linters, type checking — runs before any Worktrunk
commit (`wt step commit`, `wt step squash`, and the commit `wt merge` makes)".
The trigger is a **Worktrunk commit**, not a git commit. Repeated verbatim at
<https://worktrunk.dev/hook/> § Hook Types.

So the two mechanisms overlap only on the three `wt`-driven paths, and diverge
exactly where the original failure happened: an agent running `git commit` in
the main checkout. **Our guard is the only one of the two that fires there.**

This is why the placement is right rather than merely tolerable. We need a git
hook; Worktrunk offers a lifecycle hook.

## The approval gate: a Worktrunk project hook fails open

From `wt hook --help` § SECURITY, and the same text at
<https://worktrunk.dev/hook/#security>:

> "Declining skips every project command for that operation — including any
> already approved — and continues without them; saved approvals are
> unaffected"

A guard implemented as `.config/wt.toml` `pre-commit` would therefore stop
guarding the moment a human answered `n` at a first-run prompt — and the
operation would proceed. That is a guard that can be satisfied by habit, which
is the shape our guard exists to eliminate. It is disqualified as an
enforcement point for that reason alone, independent of the trigger gap.

The same section notes `--no-hooks` is accepted by `wt switch`, `wt merge`,
`wt remove`, `wt step commit`, `wt step squash`. A user-hook failure is
stronger: "For `pre-*` hooks, a user-hook failure skips project hooks" (hook.md
§ Project vs user hooks) — but user hooks are not where a *project's* policy
belongs, cannot be stamped into a project, and would still not fire on a plain
`git commit`.

## Worktree isolation: OpenCode 2 has a native strategy, and the plugin wires it

The agent-integration table (<https://worktrunk.dev/claude-code/>) lists
capabilities per agent CLI. Relevant rows:

| Capability | Claude Code | Codex | OpenCode |
|---|---|---|---|
| Activity tracking | ✓ | ✓ | ✓ |
| Worktree isolation | ✓ | — | ✓ |

> "Worktree isolation needs worktree-lifecycle hooks, which only Claude Code and
> OpenCode 2 expose, so Codex, Pi, oh-my-pi, and Gemini users invoke
> `wt switch --create` and `wt remove` directly."

> "Under OpenCode 2, the plugin registers a `worktrunk` worktree strategy, so
> worktrees OpenCode creates and removes go through the same commands. Each gets
> a branch named after the worktree name OpenCode chooses, at the path from
> `worktree-path`; OpenCode's `worktree.directory` setting is ignored. New
> branches start from the default branch (or the starting ref OpenCode passes),
> not the current checkout's HEAD. A dirty worktree fails removal with
> worktrunk's message rather than an offer to force."

**This is mechanism B's session-start half, already shipped.** It routes
OpenCode-initiated worktree creation through `wt switch --create`, which means
worktrees created by an agent get the configured `worktree-path`
(`{{ repo_path }}/.worktrees/{{ branch | sanitize }}` on this machine, verified
via `wt config show`) and the project's lifecycle hooks.

Verified locally: `wt config show` reports `OPENCODE — Plugin not installed;
run wt config plugins opencode install`, and `ls ~/.config/opencode/plugins/`
shows only `git-ai.ts`. **The capability exists and is not installed.**

## Shell integration

Verified via `wt config show`: "Shell integration not configured" for both bash
and zsh, detected shell zsh, binary at
`~/.local/share/mise/installs/worktrunk/0.81.0/wt`.

Shell integration is what lets `wt switch` change the *calling shell's* working
directory. It cannot help an agent's tool-call subprocess (each call is a fresh
shell), which is why the original failure — a session using worktrees as
command targets while its own cwd stayed in the main checkout — is not fixed by
it. Install it for human convenience (`wt config shell install`), not as an
agent guard.

## Recommended placement

**Keep the guard as a git hook.** It is the only mechanism that fires on a
plain `git commit`, which is the failure's actual path.

Two additions, both supported by evidence above:

1. **Also declare a Worktrunk `pre-commit` hook** for the `wt`-driven paths.
   Not for enforcement — the git hook already covers those — but because those
   paths are where a *fast* check pays. Low value; optional.
2. **Install the OpenCode plugin** (`wt config plugins opencode install`) and
   evaluate it for mechanism B's session-start half. It already routes
   OpenCode-created worktrees through `wt switch --create` with the project's
   path template and hooks. That is closer to what mechanism B wanted than a
   bespoke remediation script would be.

### Rejected: replace the guard with a Worktrunk hook

Disqualified twice over — it does not fire on `git commit`, and a declined
approval silently skips it. Either alone is fatal.

### Rejected: rely on shell integration

Does not affect an agent's tool-call subprocess. The failure was precisely that
the session's cwd never changed while worktrees were created.

## What mechanism B should now be

Original shape: take the raised error, create the worktree, mark it owned by a
session. Two of those three are now covered elsewhere:

| Piece | Covered by |
|---|---|
| Create the worktree from the error | OpenCode 2 worktree strategy via the Worktrunk plugin |
| Name and place it per project policy | `worktree-path` template + `wt switch --create` |
| **Mark it owned by a session; one writer per branch** | **still ours to build** |

So mechanism B narrows to the ownership record. That is a smaller change than
the original design, and it is the only part Worktrunk has no opinion about.

## UNVERIFIED

- Whether OpenCode 2's worktree strategy fires on a *new session started in the
  main checkout*, or only when a session explicitly asks for a worktree. The
  docs describe creation and removal, not automatic per-session creation. This
  determines whether the plugin alone eliminates the original failure or only
  handles worktrees the agent asks for. **Not tested — the plugin is not
  installed.**
- Whether `wt config plugins opencode install` is safe to run under chezmoi
  management (it writes `~/.config/opencode/plugins/worktrunk.ts`, which chezmoi
  may try to remove on the next apply if it is not declared).
- Worktrunk's own repository for any isolation-enforcement feature beyond the
  plugin; I read the documentation site and the installed binary's help, not the
  full source.
