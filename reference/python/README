# Genesis Governance OS — Python Reference Implementation

A dependency-free reference implementation of the four standards. Use it to
verify your understanding, or as a starting point. The **spec** is the source of
truth (`../../spec/`); this is one conformant implementation.

## Run

```bash
python demo.py              # the 3-agent QUICKSTART workflow, executing
python conformance_test.py  # the conformance suite (18 invariant checks)
```

No dependencies — pure stdlib, Python 3.10+.

## Modules

| Module | Standard | What it enforces |
|---|---|---|
| `task_state.py` | GTS-1 | single owner, append-only attempts, explicit done_when, handoff notes, legal transitions |
| `permission.py` | GPS-2 | deny-by-default gate, risk tiers, irreversible⇒human |
| `orchestrator.py` | GOP-3 | capability-match routing, hard loop guard, obeys the gates |

## Conformance

`conformance_test.py` checks all five invariants of each standard. A passing run
prints `✅ ALL INVARIANTS HOLD — GOS-2.0 conformant`. Your own implementation in
any language is conformant if it passes equivalent checks.

> Note: the GPS-2 decision order was corrected during implementation —
> deny-by-default is evaluated *before* the irreversible rule, so an
> unauthorized irreversible action is denied outright rather than escalated.
> The spec reflects this. (This is exactly why a reference implementation
> matters: it caught a real ordering flaw.)
