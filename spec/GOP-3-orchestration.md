# GOP-3 · Orchestration Protocol

> **Genesis Orchestration Protocol (GOP) v1.0** — a language-agnostic standard for
> *how work is decomposed, routed between agents, and prevented from looping*.
> Part of Genesis Governance OS. Implement in any language.

---

## Why this exists (the bottleneck)

A team of capable agents with no one assigning and tracking work is not a system —
it is a meeting that never ends. The bottleneck: **no clear answer to "who does
this next, and is it actually progressing?"**

GOP defines the loop a single coordinator runs. It does not make agents smarter.
It makes the *flow* legible and bounded.

---

## The coordinator is not a superuser

Critical design point: the orchestrator **routes**, it does not **rule**. It cannot
override a permission DENY (GPS-2), cannot mark a task `done` that fails its
`done_when` (GTS-1), and cannot bypass a human gate. It schedules; the constitution
governs.

---

## The loop

```
        ┌─────────────────────────────────────────────┐
        │              ORCHESTRATION LOOP             │
        └─────────────────────────────────────────────┘

  INTAKE      receive goal from human/branch
     │        → create root TaskState (GTS-1)
     ▼
  DECOMPOSE   split into sub-tasks with explicit done_when
     │        → each sub-task is its own TaskState, parent set
     ▼
  ROUTE       pick owner by capability match (not by availability)
     │        → check GPS-2 scope BEFORE assigning
     ▼
  MONITOR     watch status; enforce progress + loop guard
     │        ┌── blocked?  → CRP (capability request) or human gate
     │        ├── review?   → route to reviewer
     │        ├── failed?   → retry within budget, else escalate
     │        └── looping?  → loop guard trips (see below)
     ▼
  INTEGRATE   when sub-tasks done → assemble → verify root done_when
     │
     ▼
  CLOSE       mark done, archive, write final summary for human
```

---

## Routing rule

Route by **capability match**, never by "whoever is free." An agent receives a
task only if its declared capability covers the task's need *and* its GPS-2 scope
permits the actions the task will require. If no agent matches → the task is
`blocked` and a Capability Request is raised (GOS / CRP), not forced onto a
mismatched agent.

---

## Loop guard (the anti-thrash rule)

The most common multi-agent failure is silent looping. GOP requires a hard guard:

```yaml
loop_guard:
  max_attempts_per_task: 3        # from GTS-1 attempts[] length
  max_handoffs_per_task: 5
  max_total_steps: 25             # whole workflow ceiling
  on_trip: escalate_to_human      # never "try again forever"
```

When any limit trips, the task goes to `blocked` with `human_gate: true`. The
system stops and asks. **No unbounded retry. Ever.** This single rule prevents the
runaway-token, infinite-debate failure mode.

---

## Handoff contract

Every routing step is a handoff and must satisfy GTS-1 invariant #4: owner changes
atomically and carries a `handoff.note`. The orchestrator records:

```yaml
handoff_event:
  task: TASK-2026-0042
  from: writer-agent
  to: reviewer-agent
  note: "v2, 270 words, check CTA"
  at: 2026-06-03T09:14:00Z
  audit_ref: "audit://chain/ho-0042-2"
```

---

## The five invariants (conformance)

1. **Decompose with done_when** — no sub-task without checkable completion criteria.
2. **Capability-match routing** — assignment by fit, never by availability.
3. **Loop guard enforced** — hard ceilings on attempts/handoffs/steps; trip → human.
4. **Orchestrator obeys the gates** — cannot override GPS-2 DENY, GTS-1 done_when, or a human gate.
5. **Human-visible close** — every workflow ends with a summary a human can audit.

---

## Solo vs dev

**Solo** — a 3-agent line (e.g. Research → Write → Review) with done_when on each
and a loop guard. That is a conformant GOP system. Start here.

**Dev** — full decompose/integrate tree, capability registry for routing,
CRP integration on `blocked`, parallel sub-tasks, and budget-aware retry.

---

## How the three standards click together

```
GOP-3 routes work        →  creates & moves  →  GTS-1 task states
GOP-3 assigns an owner    →  checks against    →  GPS-2 permission gate
Any blocked/escalate      →  surfaces to       →  human / Capability Request
Every move                →  written to        →  audit chain (GOS)
```

`GTS-1` = where work is. `GPS-2` = what's allowed. `GOP-3` = who does it next.
Three small standards. Together they are the execution floor the governance layer
stands on.

---

*GOP-3 · Genesis Governance OS · Open Cognitive License v1.0 · ElmatadorZ*
