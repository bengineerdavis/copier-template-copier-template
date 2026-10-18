# HANDOFF — fork state (2026-10-18)

Scope: this repository only — the customized fork of
cbrown1234/copier-template-copier-template. Project-family context lives in
each sibling's own HANDOFF (see Related repos below).

## What this fork changed vs upstream

1. **mise replaced go-task everywhere** (commit 8aed071): repo-root
   `mise.toml` and generated-template `mise.toml.tmpl` replace Taskfile.yaml
   and both taskfile/ trees; GitHub Actions use `jdx/mise-action` with
   `install: false`, GitLab CI installs via mise.run, renovate custom
   managers track `jdx/mise`. Task names are flat and hyphenated (mise
   forbids colons).
2. **Licensing expanded** (commits 0b97d2c, ef89843, e74778c): 16 options
   as SPDX identifiers — MIT, Apache-2.0, BSD-2/3-Clause, ISC, MPL-2.0,
   0BSD, CC0-1.0, Unlicense, GPL-3.0/LGPL-3.0/AGPL-3.0-only,
   **BlueOak-1.0.0** (https://blueoakcouncil.org — maintainer's preferred
   plain-language philosophy), and the Fair Source pair **FSL-1.1-MIT /
   FSL-1.1-ALv2** (https://fsl.software, https://fair.io). LICENSE texts
   are verbatim from spdx/license-list-data and the official FSL templates.
   FSL is not SPDX-listed: the generated pyproject omits the PEP 639
   `license` key for FSL choices (license-files still lands).
3. **Hermetic tests** (in 8aed071): `test_tasks.py` runs mise with
   `--skip-tools` and an isolated `MISE_GLOBAL_CONFIG_ROOT` so the suite
   does not depend on the developer's global mise config; the
   docker-mount test skips without a daemon. Suite: 31 passed / 2 skipped.
4. **prek-native hooks folded in** (2026-10-18): the template now
   generates `prek.toml` (prek's native TOML config), `.yamllint.yaml`,
   and a `pre-commit` GitHub Actions workflow. This removes the
   composition dependency on the private
   `git@gitlab.com:browniantech/pre-commit-copier-template` — its
   `.copier-answers.pre-commit.yml` was deleted, so every scaffolded
   project's update path is now fully under our control. While porting,
   the go-task-era `check-taskfile` hook and the stale
   `scripts/install-task.sh` shellcheck exclude were dropped, the
   broken `prek auto-update` mise task was fixed to `prek update`
   (renamed in prek 0.5.x), and `prek>=0.5.5` became the floor (prek.toml
   needs 0.5+). Renovate keeps hook revs fresh via a custom regex
   manager on `prek.toml` (depType `prek-hook`, grouped + automerged) —
   native support is pending in renovatebot/renovate#42254; swap the
   custom manager out when it lands.

## Upstream sync strategy (open decision)

The fork diverges from upstream in the task runner and licensing. Options,
in order of preference: (a) keep `upstream` remote and merge selectively,
accepting conflict churn in Taskfile-shaped areas; (b) detach if this
template joins the copier-cat monorepo (cc Phase 3), at which point
upstream sync stops being a goal. Do not contribute the mise swap upstream
without the maintainer's buy-in — it is opinionated.

## Gotchas learned here

- The generated template's copier.yml uses custom jinja delimiters
  (`<< >>`, `<% %>`, `<# #>`) and `.tmpl` suffix — never write `{{ }}` in
  template content.
- yamllint caps lines at 120 — long help strings go in YAML comments.
- Inline TOML tables must stay single-line; long hook entries become
  `[[repos.hooks]]` sub-tables (tombi-format expands inline tables into
  invalid TOML otherwise).
- prek hook config is `prek.toml` (native TOML, checked by the
  `check-toml` hook); `.tmpl` files are skipped by hooks because the
  suffix defeats file-type detection.
- After moving this repo, re-run `mise trust` and delete/recreate `.venv`
  (uv sync) — stale absolute paths fail to spawn.

## Next steps for this repo

- Serve as the make-a-template base: scaffold cc's future templates with
  it (and note that generated templates inherit mise + the expanded
  licensing).
- When copier-cat's monorepo phase lands (cc ROADMAP Phase 3), migrate
  this template into it and resolve the upstream-sync question.
- Consider upstreaming the licensing expansion alone (runner-agnostic) as
  a candidate PR to cbrown1234.

## Related repos (each has its own scoped handoff)

- `../agentic-project-template` — the agentic layer that composes on top of
  templates like this one; its HANDOFF covers the family context.
- `../copier-cat` — the template manager; this fork is a candidate member
  of its monorepo.
