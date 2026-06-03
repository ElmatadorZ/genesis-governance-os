# GTS-1 · Task State Standard

> **Genesis Task State (GTS) v1.0** — a language-agnostic standard for tracking
> *what a single piece of work is doing right now* across a multi-agent system.
> Part of Genesis Governance OS. Implement in any language.

---

## Why this exists (the bottleneck)

Most multi-agent systems fail not because the agents are weak, but because
**no one can answer three questions at runtime:**

1. Where is this task right now?
2. Who is holding it?
3. What was already tried — so we don't loop?

Long-term memory (a knowledge base, a "genome") answers *what the system learned
over time*. It does **not** answer *where this specific task is right now*. That
short-term layer is what goes missing — and it is the #1 cause of agents looping,
duplicating work, and losing accountability.

GTS is that missing layer. It is deliberately small.

---

## The object

Every unit of work is one `TaskState` object. One task = one object = one owner
at a time. That is the whole idea.

```yaml
task:
  id: TASK-2026-0042              # stable, unique, never reused
  title: "Draft launch post from product sheet"
  status: pending                 # see lifecycle below
  owner: writer-agent             # exactly ONE owner at any moment
  created_by: orchestrator
  created_at: 2026-06-03T09:00:00Z
  updated_at: 2026-06-03T09:14:00Z

  goal: "A publish-ready post, reviewed, under 280 words"
  done_when:                      # explicit, checkable — not vibes
    - "post drafted"
    - "reviewer marked APPROVED"

  inputs:
    product_sheet: "ref://docs/sheet-12"
  outputs:
    draft: "ref://drafts/post-42-v2"   # filled as work progresses

  attempts:                       # append-only — never overwrite
    - by: writer-agent
      at: 2026-06-03T09:05:00Z
      action: "drafted v1"
      result: rejected
      reason: "too long, 340 words"
    - by: writer-agent
      at: 2026-06-03T09:14:00Z
      action: "drafted v2, trimmed"
      result: pending_review

  decisions:                      # why, not just what
    - by: writer-agent
      choice: "cut the founder quote"
      because: "redundant with headline"

  handoff:                        # the note that travels WITH the task
    from: writer-agent
    to: reviewer-agent
    note: "v2 is 270 words. Check the CTA line — unsure it lands."

  error: null                     # populated only on failure
  human_gate: false               # true = blocked, needs human approval
  parent: TASK-2026-0040          # if this is a sub-task
  audit_ref: "audit://chain/0042" # link to tamper-evident log (GOS)
```

---

## Lifecycle (status values)

```
pending ──► in_progress ──► blocked ──► in_progress ──► review ──► done
                │                                          │
                └──────────────► failed ◄──────────────────┘
                                   │
                                   └──► (retry → in_progress, attempts++)

archived  ← terminal, read-only, after done/failed is closed out
```

| status | meaning | who can set |
|---|---|---|
| `pending` | created, not started | orchestrator |
| `in_progress` | an owner is working | owner agent |
| `blocked` | needs a capability or input it lacks | owner agent (honest-failure) |
| `review` | work submitted, awaiting check | owner → reviewer |
| `done` | `done_when` all satisfied + verified | reviewer / orchestrator |
| `failed` | could not complete | owner / orchestrator |
| `archived` | closed, immutable | orchestrator |

**Hard rule:** an agent that cannot proceed sets `blocked` and writes why.
It must **never** silently set `done` (see GOS Constitutional Law: Honest Failure).

---

## The five invariants (conformance)

An implementation is GTS-1 conformant if and only if:

1. **Single owner** — at most one `owner` at any instant. Handoff changes owner atomically.
2. **Append-only attempts** — `attempts` and `decisions` are never edited or deleted, only appended. This is what kills loops: the next owner sees what failed.
3. **Explicit done_when** — `done` is reachable only when every `done_when` item is checkable and checked. No implicit completion.
4. **Handoff carries context** — changing owner requires a `handoff.note`. A task never moves silently.
5. **Audit link** — every state change is referenced in an external tamper-evident log (`audit_ref`).

---

## Minimal vs full

**Solo / quick start** — you only need: `id, status, owner, goal, done_when, attempts`.
That alone stops looping and lost work. Six fields.

**Production / dev** — add `decisions, handoff, human_gate, parent, audit_ref` for
full accountability and orchestration.

---

## What GTS is NOT

- Not long-term memory. Learned patterns live in the Genome (separate).
- Not a message bus. It is the *state*, not the transport.
- Not tied to any framework, DB, or language. Store it in JSON, a row, a file — your call.

---

*GTS-1 · Genesis Governance OS · Open Cognitive License v1.0 · ElmatadorZ*
