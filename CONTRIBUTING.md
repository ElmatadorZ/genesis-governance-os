# Contributing to Genesis Governance OS

This is an open **standard**, not a product. Contributions that matter most:

## High-value contributions
1. **Conformant implementations** in other languages (TypeScript, Go, Rust). Port
   the invariants, pass an equivalent conformance suite, link it here.
2. **Conformance test cases** that expose ambiguity in a spec.
3. **Spec clarifications** — if an invariant is unclear, open an issue with the
   concrete case that confused you.

## Ground rules
- The **spec** (`/spec`) is the source of truth. Code serves the spec, not the reverse.
- Do not weaken the safety invariants: separation of powers, honest-failure,
  human-in-the-loop on irreversible actions, capability-as-constitutional-act.
  A fork that removes these must be renamed (see LICENSE §3).
- Keep the floor layer (GTS-1/GPS-2/GOP-3) small. The value is that a solo builder
  can adopt it in an afternoon. Resist scope creep into the floor.
- Examples are examples. Don't merge domain-specific agents into the core.

## Proposing a spec change
Open an issue using the **Spec Clarification** template. Include: the invariant,
the ambiguous case, and what you expected vs what's written. Spec changes that
alter an invariant require a version bump and a CHANGELOG entry.

Attribution for all derivative work: *Built on Genesis Governance OS by Bunyawat Dechanon (ElmatadorZ)*.
