# Glossary

Base-project terms for copier-template-copier-template. The agentic layer keeps
its own managed glossary at `.context/glossary.md`; do not duplicate those terms
here.

> Naming note: the managed glossary's **layer** means an inner agentic *concern*
> (environment, isolation, orchestration, …). Here, **layer template** means
> something else — a composition unit. The two senses coexist and are kept
> apart by wording: always write "layer template" for the composition unit.

- **base template** — the foundation every generated project gets, independent
  of language or agent workflow (license, CI scaffolding, README/CONTRIBUTING,
  task-runner entry points, the Copier structure itself).
- **layer template** — a domain-isolated unit of tooling and configuration
  (python, agentic) applied over the base. A layer owns its own tools, config,
  and release cadence and stays out of other domains.
- **litmus test** — a tool belongs in the agentic layer only if it could not be
  used without agents; otherwise it belongs in the base or a non-agentic
  (language, workflow, quality) layer.
- **composition contract** — each domain owns *whole blocks* in shared files (a
  `mise` task block, an `AGENTS.md` managed section, a `prek` `[[repos]]` block,
  a README section) and never edits another domain's objects. Generalizes the
  agentic layer's `<!-- BEGIN managed -->` convention.
- **earn-a-layer rule** — a domain graduates from flat base options to a layer
  template once it has enough self-contained surface and evolves on its own
  cadence; keep the total layer count small (a project needing ~10 layers is
  too many).
