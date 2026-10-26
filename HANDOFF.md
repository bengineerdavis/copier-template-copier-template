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
5. **Agentic layer adopted** (2026-10-25): the agentic-project-template CLI
   merged its review, isolation, tasking, orchestration, and enforcement
   layers without replacing the fork's answers, licensing, or template
   behavior. Backlog.md tasks use `ctct-` IDs. Python practices from
   python-project-template add Ruff format checks and Ruff/mypy quality
   tasks; the unrelated Typer application scaffold was rejected because
   this repository is a template rather than a CLI package.
6. **Optional agent workflows** (2026-10-25): generated templates can
   independently select OpenSpec, Backlog.md or backlog-md-py, and alint.
   Selected tools include initialized files, agent guidance, mise/uv tool
   installation, and convenience tasks. A single mutually-exclusive
   workflow choice was rejected: Backlog tracks repository-wide work while
   OpenSpec tracks change-specific specifications and checklists, so they
   can coexist. Setup-command-only integration was rejected because a
   selected tool must be usable immediately after the documented install.

## Upstream sync strategy (RESOLVED 2026-10-18 — detached)

The fork diverges from upstream in the task runner, licensing, and the
prek hook layer. Decision: **detach** — `.copier-answers.copier-template.yml`
now points at this fork (`origin`, `_commit` = the SHA that introduced the
prek fold-in), so `copier update` / `mise run update-template` renders
from our own template: true self-hosting. Upstream improvements are
cherry-picked by hand from the `upstream` remote (kept configured for
that purpose). Upstream contributions are declined (2026-10-18): the
licensing expansion was validated to port cleanly (candidate branch
discarded) but the author judges both it and the mise swap too far off
the beaten path for the original maintainer — the fork keeps them, and
`upstream` stays read-only. When the fork cuts its own first
semantic-release tag, move `_commit` off the raw SHA onto it.

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
- Keep `backlog-md-py` at 2.1.0 until its config migration is evaluated.
  A 2026-10-25 smoke test of 2.2.0 rewrote the Backlog.md-compatible
  camelCase config as snake_case and cleared `projectName`.

## Next steps for this repo

- Serve as the make-a-template base: scaffold cc's future templates with
  it (and note that generated templates inherit mise + the expanded
  licensing).
- When copier-cat's monorepo phase lands (cc ROADMAP Phase 3), migrate
  this template into it. (Upstream sync already resolved: detached
  2026-10-18 — see above.)
- ~~Consider upstreaming the licensing expansion alone (runner-agnostic)
  as a candidate PR to cbrown1234.~~ Declined (2026-10-18): these are
  the author's own fork preferences, judged too far off the beaten path
  for the original maintainer. A candidate branch was prepared and
  validated (3 cherry-picks onto upstream/main, one conflict resolved,
  renders + upstream's test_license.py green) then discarded — the
  knowledge that it ports cleanly is retained here.

## Related repos (each has its own scoped handoff)

- `../agentic-project-template` — the agentic layer that composes on top of
  templates like this one; its HANDOFF covers the family context.
- `../copier-cat` — the template manager; this fork is a candidate member
  of its monorepo.
