# CLAUDE.md

## What This Project Is

A Copier **meta-template**: a template (`meta_template/`) that generates other Copier templates. Running `copier copy` against this repo scaffolds a new, fully-configured Copier template project. The repo is self-hosted — changes to generic content (README, CI config, etc.) should go in `meta_template/` so downstream users receive them on `copier update`.

## Commands

Examples

```sh
mise run install # Install prek hooks and uv dependencies
mise run test    # Run the full test suite
mise run cog     # Regenerate cogapp-managed files (e.g. .gitignore)
mise tasks       # See all project commands
```

Pass additional args to pytest via `--`:

```sh
mise run test -- -k test_name_here
mise run test -- tests/test_copy.py -v
```

## Architecture

### Dual test suites

- `tests/` — validates that this meta-template works (runs `copier copy`/`copier update`)
- `meta_template/tests/` — shipped inside every generated template; runs within a generated project, not this repo

### Template delimiters

Custom delimiters (defined in `copier.yml`) replace Copier's defaults to avoid conflicts with template file content:

| Role | Delimiter |
|---|---|
| Variable | `<< variable >>` |
| Block | `<% if ... %>` / `<% endif %>` |
| Comment | `<# ... #>` |

The `template_style` question lets generated projects use `[[ ]]` instead. Template source files use the `.tmpl` extension.
