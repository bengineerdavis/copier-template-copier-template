# Tool versions — policy and scheduled updates

Policy: **latest by default**. Concrete pins in `mise.toml` exist for
reproducible installs, not to freeze versions; every pin has a scheduled
update path and lands in CI-checked, automerge-eligible PRs.

## Scheduled flow

Two mechanisms, cleanly partitioned:

**Renovate** (the Mend GitHub App; same scheduler that bumps workflow
digests, prek hooks, and lockfiles) owns every registry-resolvable tool
through its native mise manager:

- `prek` → `aqua:j178/prek`
- `tombi` → `aqua:tombi-toml/tombi`
- `worktrunk` → `aqua:max-sixty/worktrunk`

These updates are grouped as "mise tools" and automerged once CI passes.

**The `tool-bump` workflow** (`.github/workflows/tool-bump.yml`) owns the
one pin Renovate cannot: `opencode`. Upstream (opencode.ai, mirrored at
`anomalyco/opencode`) publishes the 2.x line as git tags with no matching
GitHub release objects — stock datasources stop at v1.19.4 — and the pin
carries per-platform sha256 checksums that Renovate cannot recompute. The
workflow runs Mondays 06:14 UTC (`workflow_dispatch` works anytime) and
calls `mise run tool-bump` (`scripts/update-opencode.sh`), which:

1. finds the newest stable `v2.*` tag via `git ls-remote` (no auth, no
   rate limit),
2. streams each release asset to `sha256sum`,
3. rewrites the version, URLs, and checksums atomically,
4. exits 0 without changes when already current.

When the pin moves, the workflow runs `mise run check` on the result and
opens a PR (`chore/opencode-<version>`); merge it like any other PR.

Tools declared `= "latest"` (uv, dotagents, alint, roborev) resolve at
install time, so fresh installs already track newest; run `mise up` to
refresh an existing machine.

## Deliberate exceptions

- `python = "3.12"` — the template targets Python 3.12 (`requires-python`).
  Renovate advances it within 3.12.x only; crossing to a new minor is a
  deliberate template decision, because consumer projects pin the same
  floor.
- `opencode` via `http:` backend — kept deliberately because the aqua/npm
  streams lag the opencode.ai 2.x line; the scheduled workflow and
  committed checksums make that safe (a mismatched checksum fails
  `mise install` closed).

## Operational notes

- Renovate needs the Mend Renovate App installed on the repository (once,
  with your GitHub login — no separate account).
- GitHub disables scheduled workflows after 60 days without repo activity;
  ordinary commits re-arm them, or trigger `tool-bump` manually.
- The `http:opencode` pin is explicitly disabled in Renovate
  (`matchDepNames: ["http:opencode"]`) so the two schedulers never race.

## Local verification

```
mise install            # installs everything at pinned versions; verifies checksums
opencode --version      # must match the mise.toml pin
mise run check          # alint + tombi
mise run tool-bump      # manual dry-run of the scheduled bump
```
