# Generic repository types — a taxonomy the meta template can capture once

Research for the wayfinder template-stack effort. Question: what generic,
recurring categories of software project should the **meta** template record
once, so overlay templates act on what was already stamped?

**Answer up front:** project type is not one choice, it is **four orthogonal
axes**. Three are load-bearing for scaffolding (they change which files exist);
one is metadata. A meta template should record the axes — not a single enum —
because ecosystems routinely combine them (verified below: a Cargo package can
carry both a library and a binary target).

Each claim below cites the source that owns it. Where I could not verify
something I say UNVERIFIED rather than asserting it.

## The four axes

### Axis 1 — Distribution form: is it installable as a named artifact?

Does the project publish a named, versioned artifact that others depend on
(PyPI distribution, crates.io crate, npm package), or is it consumed only by
running it?

**Load-bearing:** decides whether `pyproject.toml`'s `[project]` carries a
distribution `name`, whether a version must be single-sourced, whether
`description`/`readme`/`license` metadata is required, and whether publishing
configuration exists at all.

**Evidence it recurs:** Python separates "distribution package" (what
`pip install pkg` names) from "import package" (what `import pkg` loads), and
states the indices *do not enforce any relationship* between them — the Pillow
distribution provides the `PIL` import package.
Source: <https://packaging.python.org/en/latest/discussions/distribution-package-vs-import-package/>

### Axis 2 — Entry point: does it install a command?

Is there an executable the user invokes, or is it imported/called by other
code?

**Load-bearing:** decides whether an entry-point table exists, whether a CLI
module is stamped, and whether argument parsing is a dependency.

**Evidence it recurs:** Python defines two special entry-point groups,
`console_scripts` and `gui_scripts`; "the difference … only affects Windows
systems" — console scripts attach to a console and can use the standard
streams, GUI scripts cannot unless the app redirects them. Installers wrap both
into the scripts directory but do not put that directory on `PATH`.
Source: <https://packaging.python.org/en/latest/specifications/entry-points/#use-for-scripts>

Rust makes the same split a first-class flag: `cargo new --bin` creates a
package with a binary target (`src/main.rs`); `cargo new --lib` creates a
library target (`src/lib.rs`).
Source: <https://doc.rust-lang.org/cargo/commands/cargo-new.html>

**Verified locally (2026-11-06, cargo on this machine):** `cargo new --lib p`
yields `src/lib.rs` containing a `pub fn` plus a `#[cfg(test)] mod tests`;
`cargo new --bin p` yields `src/main.rs` containing `fn main()`. Adding
`main.rs` to a `--lib` package then running `cargo metadata` reports targets
`[['lib'], ['bin']]` — **the two coexist in one package**, so this axis is
multi-valued, not exclusive.

### Axis 3 — Interface: terminal or graphical?

**Load-bearing, but narrow.** Python's own spec says the `console_scripts` /
`gui_scripts` distinction "only affects Windows systems; other platforms do
not have the same distinction." So the scaffolding consequence is real but
platform-conditional.

**Recommendation:** record it, but do not let it multiply the template matrix.
A `gui: true` flag that swaps the entry-point group is enough until a stamped
project genuinely needs GUI scaffolding (bundling, icons, app manifests).

### Axis 4 — Deployment posture: is it run as a service, or invoked by hand?

Not a packaging concept at all — a runtime one. A project that installs a
long-running service needs a unit/plist, log paths, restart policy, and a
health check; one invoked by hand needs none.

**Load-bearing:** the strongest file-level consequence of any axis in this
repo — the loreai topic carries `lore-gateway.service.j2` and
`lore-gateway.plist.j2` precisely because it is a service.

**Evidence it recurs:** Ansible's own docs draw the same line between
`ansible.builtin.systemd_service` (long-running daemons) and
`ansible.builtin.command` (one-shot invocation); the distinction drives which
module you reach for.
Source: <https://docs.ansible.com/ansible/latest/collections/ansible/builtin/systemd_service_module.html>
UNVERIFIED detail — I read the module's existence and purpose, not a passage
asserting the taxonomy.

**Note:** this axis is not language-agnostic in the T3 sense — it is
*runtime*-agnostic. It belongs to whatever layer owns service wiring.

## What is NOT a type axis

- **Language** — already an axis of the stack (base template per language).
- **Repo layout** (`src/` vs flat) — a *consequence* of the distribution form
  and language, not an independent choice. Python documents it as a discussion
  with tradeoffs, not a project category:
  <https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/>
- **Monorepo vs single package** — a workspace concern. Real, but it belongs to
  the base template's workspace question, not to project type.
- **License, VCS platform, CI provider** — orthogonal configuration the meta
  already asks.

## Minimum question set for the meta template

Four questions, one per axis. Three are booleans, one is a two-value choice:

| Question | Type | Default | What it changes |
|---|---|---|---|
| `is_distributed` | bool | `false` | `[project]` name/version/metadata, publish config |
| `has_entry_point` | bool | `false` | entry-point table, CLI module, arg-parsing dep |
| `gui` | bool | `false` | entry-point group; Windows-specific |
| `is_service` | bool | `false` | unit/plist, log paths, restart policy, health check |

Derived, not asked:
- `cli = has_entry_point and not gui`
- `library = is_distributed and not has_entry_point`

Why booleans rather than a single `project_type: library | cli | gui-app |
service` enum: the verified Cargo behaviour shows real projects hold a library
*and* a binary simultaneously. An enum forces a lossy choice; four flags
compose. This also matches the maintainer's stated preference for
mechanically-computed behaviour over per-classification tables.

## Gap: the meta captures no project-type axis today

Verified 2026-11-06 against `copier-template-copier-template/copier.yml`.
Current top-level questions:

```
template_name, vcs_platform, output_template_name, template_style,
var_start, var_end, include_pydantic_validation, include_template_extensions,
include_openspec, task_management, include_alint (plus alint_bundle_aliases,
alint_profile, alint_extra_bundles), tool_update_platform_is_github,
tool_update_strategy, all_python_versions, min_python_version, python_versions,
license_type, license, copyright_year, copyright_name, needs_extensions,
needs_trust
```

**None of these is a project-type axis.** They configure the *template* (name,
delimiters, which optional blocks to include) and *repo governance* (VCS, alint,
tool updates, licenses). A stamped project today cannot tell a downstream
overlay whether it is a library, a CLI, or a service.

Related: `python-project-template` asks `package_name`, `project_slug`,
`cli_name`, `installer`, `type_checker` — but `cli_name` is **unconditional**.
`template/pyproject.toml.jinja:31` always emits
`{{ cli_name }} = "{{ project_slug }}.cli:app"`, and
`template/src/{{ project_slug }}/cli.py.jinja` is always stamped. So the python
base cannot currently produce a non-CLI project — the exact generalisation the
maintainer asked for.

## Recommended shape, given the ADR-0002 contract

Per ADR-0002 §2 a base publishes `provides:` and an overlay consumes it. So:

1. **Meta asks the four axes** and stamps them into the project's answers file
   as ordinary variables — no new mechanism needed.
2. **Each base** (python, chezmoi, …) consumes the subset it understands and
   maps it to its own files. Python: `is_distributed` → `[project]` metadata;
   `has_entry_point` → entry-point table; `gui` → `gui_scripts` group.
3. **Overlays** consume what their domain needs. The agentic overlay already
   has a natural `is_service` consumer (service wiring); the chezmoi base will
   too.
4. **An axis a base does not understand is simply not read** — that is what
   `extends:` declares, and ADR-0002 records it as review-enforced for now.

## Prior art, verified vs not

| Ecosystem | Names the distinction | Source |
|---|---|---|
| Rust / Cargo | `--lib` vs `--bin`; both coexist | cargo-new(1), verified locally |
| Python packaging | `console_scripts` vs `gui_scripts` | entry-points spec |
| Python packaging | distribution package vs import package | packaging.python.org discussion |
| npm | `bin` field installs commands; absence means library-only | verified: `npm view typescript bin` → `{ tsc: 'bin/tsc' }` |
| Ansible | service module vs command module | systemd_service docs (existence only) |

**UNVERIFIED — I did not fetch these, so do not cite them as evidence:**
Cookiecutter Data Science project structure, Nx generators, Yeoman, and
`cargo-generate` option sets. If the ticket needs cross-tool comparison beyond
the four rows above, fetch those primary sources before relying on them.

## Open questions

1. **Does `is_service` belong to the meta at all?** By the wayfinder criterion
   (language-agnostic AND every stamped project wants it) it fails the second
   half — most repos are not services. It may belong to the layer that owns
   service wiring rather than the meta.
2. **Should `gui` be a meta question or a base question?** The python spec says
   the difference is Windows-only, so a chezmoi or agentic base has nothing to
   do with it.
3. **Does the py310-style floor analogy apply?** That is: should the meta record
   *derived* facts (`cli`, `library`) or only the four raw axes, letting bases
   derive? Recording raw only keeps one source of truth; deriving duplicates
   logic per base.
