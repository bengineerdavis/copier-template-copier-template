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

- `python = "3.12"` — the template targets Python 3.12 (`requires-python`),
  and crossing minors (or picking patches) is a template decision, so
  Renovate is disabled for it outright (`matchDepNames: ["python"]`).
  Without that rule the pin's protection would be accidental: Renovate
  reads the two-component `3.12` as an invalid semver and simply proposes
  nothing — normalizing it to `3.12.4` would let the automerged group move
  Python across minors unreviewed.
- `opencode` via `http:` backend — kept for two reasons: the `-baseline`
  x64 assets (compatible with pre-AVX2 CPUs, which the registry recipes do
  not guarantee) and explicit, committed checksums (a mismatch fails
  `mise install` closed). npm's stream demonstrably lags 2.x; the aqua
  recipe currently proxies opencode.ai assets anyway, but switching would
  surrender checksum control and the baseline choice.

## Operational notes

- Renovate runs as the Mend Renovate GitHub App
  (https://github.com/apps/renovate — the slug is `renovate`, not
  `mend-renovate`), installed once with your GitHub login and no separate
  account. There is no CLI or API install path for third-party apps: GitHub
  requires the interactive consent page by design (the only API install
  route is enterprise-admin scoped), so the fallback is one click: open
  https://github.com/apps/renovate/installations/new in a browser
  (`xdg-open` on Linux, `open` on macOS — note `gh browse` rejects bare
  URLs) and choose "All repositories" (zero-touch for every future repo on
  the account) or "Only select repositories" + this repo for a smaller
  blast radius. Verify afterwards with `gh pr list --author "app/renovate"`:
  the onboarding PR is the first thing Renovate opens.
- GitHub disables scheduled workflows after 60 days without repo activity;
  ordinary commits re-arm them, or trigger `tool-bump` manually.
- The `http:opencode` disable rule in `renovate.json` is future-proofing:
  Renovate's mise manager already skips `http:`-backend tools entirely, so
  no dep is extracted to race with the workflow today. The rule keeps that
  guarantee explicit if Renovate ever grows http support.

## Local verification

```
mise install            # installs everything at pinned versions; verifies checksums
opencode --version      # must match the mise.toml pin
mise run check          # alint + tombi
mise run tool-bump      # manual dry-run of the scheduled bump
```
