# 0001. Layer-template architecture: single template now, copier-cat later

- Status: Accepted
- Date: 2026-10-27

## Context

This repository is a Copier meta-template: it generates other Copier templates,
each of which bundles Python tooling and many optional domains (alint, OpenSpec,
Backlog, agentic loops) as flat `copier.yml` options. As those options multiply,
every shared file (`mise.toml`, `pyproject.toml`, `AGENTS.md`, `prek.toml`,
`README.md`) accumulates cross-cut conditionals, and each domain edits the same
objects from several directions.

We considered decomposing into separate "layer templates" applied in sequence
over a shrinking base. Native Copier is single-template: it composes only
within one template (managed blocks, conditional files, subdirectory) and has no
multi-template sequencing or dependency resolution. `copier-cat` is the intended
home of inter-template ordering and dependencies (HANDOFF Phase 3), but it does
not exist yet.

## Decision

Keep one base template now, but structure it so later extraction is mechanical
rather than a rewrite. Specifically:

- Adopt the vocabulary **base template** and **layer template** (the latter kept
  distinct from the managed glossary's inner "layer" sense).
- Each domain owns **whole blocks** in shared files — a `mise` task block, an
  `AGENTS.md` managed section, a `prek` `[[repos]]` block, a README section —
  and never edits another domain's objects. This is the composition contract.
- Use the **litmus test** to sort tooling: agentic-only tools belong to the
  agentic layer; everything else stays in the base or a non-agentic layer.
- Apply the **earn-a-layer rule**: a domain becomes a separate layer template
  once it reaches roughly 2–3 tools and its own cadence. Python and agentic are
  the layer targets; quality/workflow stay flat options until they grow.
- Reserve inter-template ordering and dependency resolution for copier-cat.

## Consequences

- Positive: shared files stay editable one-domain-at-a-time; domains can later
  be cut into layer templates without re-editing shared logic; the litmus test
  stops agent-only tooling from creeping into the base.
- Negative: the flat options still exist today and still carry conditionals;
  the "quality" and "workflow" domains are too thin to justify layers yet, so
  they remain flat a while longer.
- Deferred: the python and agentic layers cannot ship as separate sequenced
  templates until copier-cat provides ordering. Until then they live as block
  owners inside the single template.
