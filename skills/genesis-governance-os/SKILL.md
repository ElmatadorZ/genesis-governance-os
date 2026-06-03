---
name: genesis-governance-os
description: "GENESIS GOVERNANCE OS v2.0 — an open standard for multi-agent systems that stay legible, safe, and accountable on any model or language. ALWAYS trigger for: multi-agent system design, agent orchestration, agent task state, agent permissions, tool permission, agent looping, agents duplicating work, who owns this task, orchestrator design, multi-agent company, AI org structure, separation of powers for agents, self-improving agent system, capability gap, agent stuck, governance framework, ออกแบบระบบ multi-agent, agent วนซ้ำ, ใครรับผิดชอบงาน, ระบบ AI หลายตัว, สภา AI, บริษัท AI. Provides four standards: GTS-1 Task State (where work is), GPS-2 Permission (what's allowed, prevented early), GOP-3 Orchestration (who's next, loop-bounded), GOS-0 Constitution (7 branches, separation of powers, self-improvement loop). Solo builders start with the three execution standards; scale with the constitution."
license: "Open Cognitive License v1.0"
---

# Genesis Governance OS — Skill

You are operating a multi-agent system under the Genesis Governance OS standard.
Apply these four standards. The first three are the execution floor; the fourth is
the scale layer. Full specs live alongside this skill in `spec/`.

## When this triggers

Any task about designing, running, or debugging a system of multiple agents:
routing work, tracking task state, setting permissions, stopping loops, deciding
who's accountable, or scaling an AI organization.

## GTS-1 — Task State (where work is)

Track every unit of work as one object with one owner. Minimum fields:
`id, status, owner, goal, done_when, attempts`. `attempts` is append-only.
Status: pending → in_progress → blocked → review → done (or failed → retry/archive).
A blocked agent declares `blocked` and writes why — it never silently marks done.

## GPS-2 — Permission (what's allowed, before acting)

Deny-by-default. Each agent has `allow / deny / escalate` lists. Decision order:
deny? → DENY · irreversible-no-gate? → ESCALATE · in escalate? → ESCALATE ·
in allow? → ALLOW · else → DENY. The gate runs *before* the tool call. Any
irreversible action (send, pay, publish, shell) requires a human gate. An agent
never widens its own scope.

## GOP-3 — Orchestration (who's next)

Run one loop: intake → decompose (with done_when) → route by capability-fit (not
availability) → monitor → integrate → close with a human-visible summary. Enforce
a hard loop guard (max attempts/handoffs/steps); when it trips, escalate to a
human — never retry forever. Every handoff carries a note. The orchestrator routes
but cannot override a permission DENY, a failed done_when, or a human gate.

## GOS-0 — Constitution (how it stays aligned at scale)

Seven branches (Legislative, Executive, Judicial, Intelligence, Development,
External, Security) with separation of powers — no branch legislates, executes,
and judges at once. When an agent is blocked for lack of capability, run the
Capability Request loop: request → Judicial gate → discover → Judicial gate →
install → verify → record. Installing a new capability is a constitutional act the
Judicial branch can veto. Core laws that never bend: separation of powers,
accountability, human-decides, honest-failure, capability-as-constitutional-act.

## Output

When designing a system, state which standard each recommendation implements, and
end with a confidence note and the open unknowns. Keep examples mapped to the
user's domain — never assume they want the author's finance/coffee reference orgs.
