# Changelog

## v2.1 — 2026-07

### Changed — licensing (no requirement changes)
- **Relicensed from Open Cognitive License v1.0 to Apache-2.0.** The prior licence was a custom
  one carrying a 2% gross-revenue royalty above $10M USD/year, which most corporate open-source
  review processes treat as a commercial agreement requiring individual legal review. Apache-2.0
  removes that adoption barrier. The previous licence text remains in the git history.
- The naming/endorsement requirement formerly in LICENSE §3 is preserved in [NOTICE](NOTICE),
  backed by Apache-2.0 §6 (Trademarks): a derivative that strips the safety invariants
  (separation of powers, honest-failure, human-in-the-loop) must be renamed and must not imply
  endorsement. Conformance claims are governed by `spec/CONFORMANCE.md`.

### Added — conformance machinery
- `spec/CONFORMANCE.md` — the normative authority for conformance claims: RFC 2119/8174
  requirement language, stable requirement IDs (`GTS-1.1` … `GOS-0.17`), three conformance levels
  (L1 Core / L2 Full / L3 Governed), an honest verified-vs-attested coverage matrix, and
  versioning rules (a new or promoted MUST requires a MAJOR bump; retired IDs are never reused).
- CI: conformance suite, pytest, and demo across Linux/macOS/Windows × Python 3.9/3.11/3.12;
  JSON Schema validation; filename-hygiene gate.
- `SECURITY.md` (treating specification flaws as a distinct, higher-severity class),
  `CODE_OF_CONDUCT.md`, a PR template gating spec changes, and `CITATION.cff`.

### Fixed
- The conformance suite contained no assertions, so under `pytest` — the invocation its own
  docstring recommends — a violated invariant still reported green. `check()` now asserts.
- `conformance_test.py` and `demo.py` crashed with `UnicodeEncodeError` on Windows consoles
  (cp1252 cannot encode U+2705/U+274C). Both now use UTF-8 with an ASCII fallback.
- Removed `reference/python/tests`, a 2-byte placeholder file where a package was intended.
- Added `.md` extensions to `.github/ISSUE_TEMPLATE/implementation`, `reference/python/README`,
  and `examples/content-org`.

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
