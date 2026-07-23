# Quickstart — a conformant 3-agent system in one page

This is the smallest thing that counts as a Genesis Governance OS system. No
framework, no model lock-in. Pseudocode — port it to anything.

## The workflow

```
product sheet → Research → Writer → Reviewer → publish-ready post
```

## 1. Define agents + permissions (GPS-2)

```yaml
agents:
  research-agent:
    allow: [read:docs, read:web]
    deny:  [write:*, send:*, pay:*]
  writer-agent:
    allow: [read:docs, write:drafts]
    deny:  [send:*, pay:*, exec:*]
    escalate: [publish:post]        # needs a human
  reviewer-agent:
    allow: [read:drafts, write:reviews]
    deny:  [publish:post, send:*]
# everything not listed = DENIED (deny-by-default)
```

## 2. Create the task (GTS-1)

```yaml
task:
  id: TASK-0001
  status: pending
  owner: research-agent
  goal: "publish-ready launch post, < 280 words, reviewed"
  done_when:
    - "facts gathered"
    - "draft written"
    - "reviewer APPROVED"
  attempts: []
```

## 3. Run the orchestration loop (GOP-3)

```python
def run(task):
    guard = {"steps": 0, "max": 25}            # loop guard — hard ceiling

    while task.status not in ("done", "failed"):
        guard["steps"] += 1
        if guard["steps"] > guard["max"]:
            return escalate_to_human(task, "loop guard tripped")

        if task.status == "pending":
            assign(task, owner="research-agent")     # route by fit

        owner = task.owner
        action = owner.next_action(task)

        # GPS-2: gate BEFORE doing anything
        decision = permission_gate(owner, action)
        if decision.verdict == "DENY":
            log(decision); continue
        if decision.verdict == "ESCALATE":
            return wait_for_human(task, decision)

        result = owner.do(action)
        task.attempts.append(result)             # append-only

        # honest failure, not fake-done
        if result.blocked:
            task.status = "blocked"
            return raise_capability_request(task)

        # handoff carries a note
        if owner == research-agent and result.ok:
            handoff(task, to="writer-agent", note="3 verified facts attached")
        elif owner == writer-agent and result.ok:
            handoff(task, to="reviewer-agent", note=f"draft {result.words}w")
        elif owner == reviewer-agent and result.approved:
            task.status = "done"                 # done_when satisfied + verified

    summarize_for_human(task)                    # human-visible close
```

## What makes this conformant

- **GTS-1**: single owner, append-only `attempts`, explicit `done_when`, handoff notes.
- **GPS-2**: deny-by-default, gate runs before the action, `publish` escalates to a human.
- **GOP-3**: capability-match routing, hard loop guard, human-visible close.

That's it. Scale up by adding more done_when'd sub-tasks, more agents (each with a
tight permission scope), and — when it gets big — the constitution layer (GOS-0).

---

*Quickstart · Genesis Governance OS · Apache-2.0*
