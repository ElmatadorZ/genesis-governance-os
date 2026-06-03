# GPS-2 · Permission & Capability Standard

> **Genesis Permission Standard (GPS) v1.0** — a language-agnostic standard for
> deciding *what an agent is allowed to do, before it does it*. Part of Genesis
> Governance OS. Implement in any language.

---

## Why this exists (the bottleneck)

A review that happens *after* an agent sends the email, deletes the file, or
spends the money is not a safeguard — it is a post-mortem. The bottleneck most
multi-agent systems hit: **permission is checked too late, or not at all.**

GPS turns permission into a **preventive gate**: an action is simulated against a
matrix and either `ALLOW`, `DENY`, or `ESCALATE` *before* it executes. Nothing
irreversible happens without passing the gate.

---

## The matrix

Each agent declares a capability scope. Each tool declares a risk tier. The gate
is the intersection.

```yaml
# per-agent grant
agent: writer-agent
allow:
  - read:docs
  - write:drafts
deny:
  - send:email
  - exec:shell
  - pay:*
escalate:                 # allowed only with human approval
  - publish:post

# per-tool risk tier (global)
tools:
  read:docs:      { tier: 0, reversible: true }
  write:drafts:   { tier: 1, reversible: true }
  publish:post:   { tier: 2, reversible: false }   # external, public
  send:email:     { tier: 3, reversible: false }
  pay:*:          { tier: 3, reversible: false }
  exec:shell:     { tier: 3, reversible: false }
```

### Risk tiers
| tier | meaning | default rule |
|---|---|---|
| 0 | read-only, internal | ALLOW |
| 1 | write, reversible, internal | ALLOW if in scope |
| 2 | external but recoverable | ESCALATE |
| 3 | irreversible / money / external send / shell | DENY unless explicitly granted + human gate |

---

## The gate (decision order)

Evaluate in this exact order. First match wins.

```
1. Is the action in the agent's  deny  list?           → DENY (final)
2. Is it in NEITHER allow nor escalate?                 → DENY (deny-by-default)
3. Is it irreversible and no human gate passed?         → ESCALATE
4. Is it in the agent's  escalate  list?                → ESCALATE
5. Otherwise (in allow, reversible or gated)            → ALLOW
```

**Deny-by-default is mandatory and is checked *before* the irreversible rule.**
An irreversible action that the grant never authorized is denied outright — it
does not get an escalation path. Irreversibility raises the bar for in-scope
actions; it never creates scope that wasn't granted. This is the single most
important ordering in the standard.

---

## Decision object (what the gate emits)

```yaml
permission_decision:
  agent: writer-agent
  action: publish:post
  verdict: ESCALATE              # ALLOW | DENY | ESCALATE
  tier: 2
  reversible: false
  reason: "tier-2 external action requires human approval"
  matched_rule: "escalate:publish:post"
  human_gate_id: HG-2026-0007    # if ESCALATE, the approval request id
  audit_ref: "audit://chain/perm-0007"
  at: 2026-06-03T09:20:00Z
```

Every decision — including every DENY — is logged. A DENY that leaves no trace is
a silent failure.

---

## The five invariants (conformance)

1. **Deny-by-default** — anything not explicitly allowed is denied.
2. **Pre-execution** — the gate runs *before* the tool call, never after.
3. **Irreversible ⇒ human** — any `reversible: false` action requires either an
   explicit grant *and* a passed human gate, or it is denied.
4. **Every decision logged** — ALLOW, DENY, and ESCALATE all write to audit.
5. **Agent cannot widen its own scope** — only the governance layer (a human or
   the Legislative branch) edits grants. An agent editing its own permissions is
   a constitutional violation.

---

## Relationship to governance (GOS)

GPS is the *preventive* arm of the Judicial branch. The Judicial VETO reviews
decisions; GPS stops them from happening. Together: **prevent first, audit always.**

---

## Solo vs dev

**Solo** — three lists per agent (`allow / deny / escalate`) + deny-by-default.
That alone prevents the scary failures (agent emails a client, agent runs a
destructive command).

**Dev** — full tier model, decision objects, human-gate ids, audit links,
and integration with the orchestrator (GOP-3) so ESCALATE pauses the task.

---

*GPS-2 · Genesis Governance OS · Open Cognitive License v1.0 · ElmatadorZ*
