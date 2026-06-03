# GOS-0 · Governance Constitution

> **Genesis Governance OS (GOS) v2.0 — Constitution** — the language-agnostic
> governance layer that sits *above* the three execution standards
> (GTS-1, GPS-2, GOP-3). This is the deep layer. Most solo users can ship on the
> three standards alone and adopt this as they scale.

---

## What this layer is for

The execution standards make a multi-agent system *work and stay legible*. This
layer makes it *stay aligned as it grows* — when you go from 3 agents to 50, the
hard problem is no longer "make an agent," it is "keep the whole thing from
slowly becoming something you did not intend."

```
A good constitution does not make the agents smarter.
It ensures that even as the agents get smarter, the system does not break.
```

---

## Seven branches (separation of powers)

No single branch may legislate, execute, and judge at once. Map your agents/skills
onto these roles.

| Branch | Role | Owns |
|---|---|---|
| Legislative | vision, policy, budget | what the system should do |
| Executive | operations | domain agents that do the work (uses GOP-3) |
| Judicial | audit, compliance, **VETO** | reviews + the GPS-2 preventive gate |
| Intelligence | data, forecast | evidence for every major decision |
| Development | capability, talent | finds/builds new capability (the self-improvement engine) |
| External | stakeholders | outward communication |
| Security | protection, resilience | threats, continuity, supply-chain of new tools |

---

## Six modes

One system, different posture by context: **Design** (build structure),
**Govern** (daily ops), **Audit** (check actual vs intended), **Reform** (change
structure at the root), **Succession** (hand over without losing memory),
**Crisis** (compress cycle — but never suspend the constitution).

---

## The self-improvement loop (Capability Request)

When any agent is `blocked` (GTS-1) because it lacks a capability, it does not
guess and it does not fake completion. It raises a Capability Request:

```
BLOCKED → REQUEST → [Judicial Gate 1: legitimate?] → DISCOVER (find/compose tool)
        → EVALUATE → [Judicial Gate 2: constitutional? safe?] → INSTALL
        → VERIFY (external check) → RECORD to Genome (via audit only)
```

The system grows its own capability — but **installing a new capability is a
constitutional act that the Judicial branch can veto.** The system can extend
itself; it cannot rewrite its own constitution.

---

## Constitutional laws (the invariants that never bend)

```
01  Separation of powers   — no branch holds legislate + execute + judge
02  Universal accountability — every action traces to a responsible owner
03  Transparency by default  — closed needs a reason
04  Judicial independence    — judicial is never under executive
05  Evidence-based decisions — major decisions cite intelligence
06  Proportionality          — response fits the issue
07  Sunset clauses           — major policy expires/reviews
08  Institutional memory     — knowledge survives personnel change
09  Stakeholder representation
10  Conflict-of-interest disclosure
11  Constitutional supremacy — base epistemics > constitution > policy > action
12  Right to appeal
13  Continuity of governance — crisis is never a permanent power grab
14  Capacity before authority
15  Human decides            — irreversible actions stay with a human
16  Honest failure           — a blocked agent declares it; never fakes done
17  Capability = constitutional act — new tools pass Judicial review
18  Genome integrity         — learning is written via audit only; failure log never deleted; entries expire at 6 months
19  Self-improvement bounded — the system extends itself but cannot edit its own constitution
```

---

## How the layers stack

```
GOS-0  Constitution        — what is allowed, who checks whom        (this file)
  │
GOP-3  Orchestration       — who does the work next, loop-bounded
  │
GPS-2  Permission          — what each agent may do, prevented early
  │
GTS-1  Task State          — where each piece of work is, right now
  │
(your runtime, any language)
```

A solo builder can ship on GTS-1 + GPS-2 + GOP-3 alone. The constitution is what
you adopt when the population of agents grows past what one person can watch.

---

## Conformance

A system is **GOS-2.0 conformant** if it implements the three execution standards
(GTS-1, GPS-2, GOP-3) and enforces, at minimum, constitutional laws 01, 02, 15,
16, 17 — i.e. separation of powers, accountability, human-decides, honest-failure,
and capability-as-constitutional-act. The remaining laws are strongly recommended
and required for the "governmental-scale" profile.

---

*GOS-0 · Genesis Governance OS v2.0 · Open Cognitive License v1.0 · Bunyawat Dechanon (ElmatadorZ)*
