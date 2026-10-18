# copier-template-copier-template

[![Tests](https://github.com/cbrown1234/copier-template-copier-template/actions/workflows/test.yml/badge.svg)](https://github.com/cbrown1234/copier-template-copier-template/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

A [Copier](https://copier.readthedocs.io/) meta-template — a template that scaffolds new Copier templates with modern Python project tooling preconfigured.

## Features

- **Best Practices:** template in subdirectory, [multiple (composable) template compatibility](https://copier.readthedocs.io/en/stable/configuring/#applying-multiple-templates-to-the-same-subproject)
- **Plain-language licensing** [SPDX](https://spdx.org/licenses/) options including the [Blue Oak Model License](https://blueoakcouncil.org/license/1.0.0) — the [Blue Oak Council's](https://blueoakcouncil.org) plain-English alternative to MIT/Apache, plus the [Functional Source License](https://fsl.software) from [Fair Source](https://fair.io)
- **Test harness included** pytest setup with examples and helpers, ready to test your template, and it's usage
- **Modern Batteries included** uv, semantic release, Renovate, and [mise](https://mise.jdx.dev/) automation all preconfigured
- **CI/CD out of the box** Supports GitLab CI or GitHub Actions, with matrix testing across Python versions
- **Optional Copier extensions**
    - [Pydantic validation](https://pypi.org/project/copier-pydantic/) for answers
    - [local Jinja extensions](https://pypi.org/project/copier-template-extensions/)

## Install Copier

```bash
uv tool install copier
# or
pipx install copier
# or
brew install copier
```

## Usage

### Create a new project

```bash
# SSH
copier copy git@github.com:cbrown1234/copier-template-copier-template.git /path/to/new-template
# HTTPS
copier copy https://github.com/cbrown1234/copier-template-copier-template.git /path/to/new-template
```

For non-interactive usage (scripts, CI, AI agents), see `copier copy --help` for the `--defaults` and `--data` flags.

### Update an existing project

```bash
cd /path/to/your/project
copier update --answers-file .copier-answers.copier-template.yml
```

For non-interactive updates, use `--skip-answered` to reuse all existing answers without prompting.

## Demo

[![demo](https://asciinema.org/a/bFcXBgVNxzAaNAjO.svg)](https://asciinema.org/a/bFcXBgVNxzAaNAjO)

## Development

Prerequisites: [uv](https://docs.astral.sh/uv/) and [mise](https://mise.jdx.dev/).

Run `mise tasks` to see available commands (mise is the task runner). See [CONTRIBUTING.md](CONTRIBUTING.md) for the full development guide.

### Self-hosted

This repo uses itself. See `.copier-answers.copier-template.yml` for the answers used.

### Git hooks

Generated projects get a prek-native `prek.toml` (https://prek.j178.dev) with a curated hook set, a `pre-commit` GitHub Actions workflow, and a `.yamllint.yaml`. Hooks run with [prek](https://github.com/j178/prek) (`mise run lint`); pinned hook revisions are kept current by Renovate (custom regex manager for `prek.toml`) and by `mise run maintenance` (`prek update`).
