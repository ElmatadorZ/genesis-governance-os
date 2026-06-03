# Changelog

## v2.0 — 2026-06
Full-system release as an open standard (language-agnostic).

### Added — execution standards (the floor)
- GTS-1 Task State — short-term task tracking; five invariants; JSON schema.
- GPS-2 Permission — deny-by-default preventive gate; risk tiers; five invariants.
- GOP-3 Orchestration — decompose/route/monitor loop; hard loop guard.

### Added — governance (the scale layer)
- GOS-0 Constitution — 7 branches, 6 modes, Capability Request loop, 19 laws.

### Added — adoption
- Two-layer README (solo quickstart + dev deep).
- QUICKSTART with a worked, conformant 3-agent example.
- Reference example (content org) clearly separated from the standard.
- Claude Skill reference implementation.

### Design stance
- Positioned as a standard (implement in any language/model), not a framework.
- Examples are reference implementations, not the core.

### Added — reference implementation
- Python reference (dependency-free): GTS-1, GPS-2, GOP-3 implemented.
- Conformance suite — 18 invariant checks, all passing.
- Runnable demo of the QUICKSTART 3-agent workflow.
- CONTRIBUTING + GitHub issue templates.

### Fixed
- GPS-2 decision order: deny-by-default now evaluated before the irreversible
  rule, so an unauthorized irreversible action is denied outright (not escalated).
  Caught by the conformance suite during implementation. Spec updated to match.

### Roadmap
- JSON schemas for GPS-2 and GOP-3.
- TypeScript reference implementation.
- Conformance suite as an importable package for third-party implementations.
