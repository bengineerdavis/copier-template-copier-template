---
id: decision-1
title: Test the contract we own, not the dependency
date: 2026-11-10 01:35
status: accepted
---

## Context

Upstream tests establish a dependency's behavior at a particular release under its supported interfaces. They do not establish that this template selects the dependency, renders its configuration, combines it with other layers, or runs it in a fresh project. Repeating upstream tests adds maintenance without proving our integration.

## Decision

Test the contract we own, not the dependency.

Our test seams are:

- Copier stamp and update: defaults, opt-outs, recorded answers, and preservation of project customizations.
- Fresh project through prek: the official hook installs and runs successfully.
- Layer composition: the agentic overlay adds its concern without removing base-template hooks or project-owned configuration.
- Version selection: the mirror's tagged hook and the mise-managed CLI are updated through an explicit policy. Upstream does not certify compatibility between independently selected `rev` and `latest` versions.

Do not duplicate upstream rule-engine, parsing, wheel-packaging, or pre-commit-protocol tests. Do not snapshot incidental configuration order or repeat one integration contract in several tests.

A real integration failure is a failure, never a passing test. An existing project's self-update that leaves conflict markers is an update-preservation issue and must stop for review rather than silently discard customizations.

## Consequences

The meta-template's fresh stamp runs `prek run alint --all-files`; its opt-out test removes the integration cleanly. The agentic overlay's fresh stamp runs the same hook and retains base-template hooks. The full matrix remains in CI for local shift-left feedback.

`mise run lint` owns the commit check through prek's official alint hook. A separate alint task would run the same check twice. mise retains the CLI declaration for `alint lsp` and direct use.

The propagation and testkit work consumes this boundary rather than introducing tests of upstream semantics.
