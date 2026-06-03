# Example — Content Organization (reference implementation)

> ⚠️ **This is an example, not the standard.** It shows *one* way the author maps
> Genesis Governance OS onto a real domain (a finance-content brand). Do not copy
> it — map the standards onto *your own* domain. The value is in the mapping
> pattern, not these specific agents.

## Domain: a content brand that ships analysis posts

### Branches → real roles (GOS-0)

| Branch | Here it is… |
|---|---|
| Legislative | the editor-in-chief: what topics, what voice, what's off-limits |
| Executive | the writing/research/design agents that produce posts |
| Judicial | a fact-check + compliance pass with veto over publishing |
| Intelligence | a market-data agent that supplies evidence |
| Development | finds a new capability when blocked (e.g. a charting tool) |
| External | the publishing/community agent (escalates to human) |
| Security | guards brand voice + checks any new tool before adoption |

### A task in flight (GTS-1)

```yaml
task:
  id: TASK-CONTENT-0210
  status: review
  owner: factcheck-agent
  goal: "post on rate-cut scenario, sourced, on-voice, < 600 words"
  done_when:
    - "every claim has a source"
    - "voice check passed"
    - "factcheck APPROVED"
  attempts:
    - { by: writer-agent, action: "draft v1", result: pending_review }
  handoff:
    from: writer-agent
    to: factcheck-agent
    note: "2 claims need a second source — flagged inline"
```

### Permissions (GPS-2)

```yaml
writer-agent:    { allow: [read:data, write:drafts], escalate: [publish:post] }
factcheck-agent: { allow: [read:drafts, read:data, write:reviews], deny: [publish:post] }
publish-agent:   { escalate: [publish:post], deny: [pay:*, send:bulk] }
# publishing is ALWAYS a human-gated escalate — irreversible, public
```

### What the loop guard caught (GOP-3)

In testing, writer ↔ factcheck bounced a claim 3 times. The loop guard tripped at
attempt 3 and escalated to a human instead of burning tokens forever. The human
resolved the source dispute in one message. **That is the system working.**

---

*Reference example only. The standards are in `/spec`. Open Cognitive License v1.0.*
