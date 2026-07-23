<div align="center">

# Genesis Governance OS

**An open standard for multi-agent systems that stay legible, safe, and accountable —
in any language, on any model.**

`GTS-1` Task State · `GPS-2` Permission · `GOP-3` Orchestration · `GOS-0` Constitution

Open Cognitive License v1.0 · by Bunyawat Dechanon (ElmatadorZ)

</div>

---

## The bottleneck this targets

Multi-agent systems rarely fail because the agents are weak. They fail because:

- nobody can tell **where a task is** or **who owns it** → work loops and duplicates
- permissions are checked **after** the damage, or never → an agent emails a client, runs a destructive command
- there's no coordinator → capable agents thrash in an endless meeting
- it grows past what one person can watch → it slowly becomes something you didn't intend

Genesis Governance OS is **not a framework** and **not tied to a model**. It is a
small set of standards you implement in whatever language and stack you already
use — the way OpenAPI or MCP are standards, not libraries.

---

## Two ways in

### → If you're a solo builder: start here (10 minutes)

You need exactly three things to stop the worst failures. Read these, implement
the five invariants of each in your stack:

1. **[GTS-1 · Task State](spec/GTS-1-task-state.md)** — track where each task is. Six fields minimum.
2. **[GPS-2 · Permission](spec/GPS-2-permission.md)** — deny-by-default, check before acting.
3. **[GOP-3 · Orchestration](spec/GOP-3-orchestration.md)** — route by fit, hard loop guard.

That's a conformant system. A 3-agent line (Research → Write → Review) with
done_when on each task and a loop guard is enough to start.

See **[QUICKSTART.md](QUICKSTART.md)** for a worked 3-agent example — or run the
**[Python reference implementation](reference/python/)** right now:

```bash
cd reference/python
python demo.py              # the 3-agent workflow, executing live
python conformance_test.py  # 18 invariant checks — proves the spec holds
```

### → If you're scaling / building infra: go deep

Add the governance layer when the number of agents grows past what one person can
watch:

4. **[GOS-0 · Constitution](spec/GOS-0-constitution.md)** — 7 branches, 6 modes, separation of powers, the self-improvement loop, and 19 constitutional laws.

Machine-validatable schema: **[schemas/task-state-v1.json](schemas/task-state-v1.json)**.

---

## Claiming conformance

**[spec/CONFORMANCE.md](spec/CONFORMANCE.md)** is the normative authority: RFC-2119 requirement
language, stable requirement IDs (`GTS-1.3`, `GPS-2.5`, …), three conformance levels
(**L1 Core** → **L2 Full** → **L3 Governed**), and an honest coverage matrix stating which
requirements are machine-verified and which require attestation.

The reference suite runs on Linux, macOS, and Windows across Python 3.9/3.11/3.12 in CI —
every check asserts, so a violated invariant fails the build.

---

## The whole thing on one page

```
GOS-0  Constitution   — what is allowed, who checks whom        ← scale layer
  │
GOP-3  Orchestration  — who does the work next (loop-bounded)
  │
GPS-2  Permission     — what each agent may do (prevented early)
  │                                                              ← floor layer
GTS-1  Task State     — where each piece of work is, right now      (start here)
  │
  your runtime — any language, any model (Claude / GPT / Ollama / …)
```

`GTS-1` = where work is · `GPS-2` = what's allowed · `GOP-3` = who's next · `GOS-0` = how it stays aligned.

---

## Design principles

1. **Separation of powers** — no part legislates, executes, and judges at once.
2. **Honest failure** — a blocked agent says so; it never fakes completion.
3. **Prevent first, audit always** — irreversible actions are gated before they happen.
4. **Capability = constitutional act** — the system can grow new abilities, but can't rewrite its own rules.
5. **Human decides** — irreversible calls stay with a person.
6. **Loop guard, always** — no unbounded retry, ever.

---

## What's a standard vs what's an example

The **standards** (`spec/`, `schemas/`) are model- and language-agnostic — yours to implement.

The **[examples/](examples/)** (a finance content org, a coffee-science org) are
*reference implementations* by the author. They show one way to map the standards
onto real domains. **You do not copy them** — you map the standards onto *your* domain.

A reference Claude Skill lives in **[skills/genesis-governance-os/](skills/genesis-governance-os/)**
for those running on Claude.

---

## Contributing

This is an early open standard. Issues and conformant implementations in any
language are welcome. Implementations that strip the safety invariants
(separation of powers, honest-failure, human-in-the-loop) must be renamed and
must not imply endorsement (see LICENSE §3).

---

## License

**[Open Cognitive License v1.0](LICENSE.md)** — free to use, attribution required,
2% gross-revenue royalty only above $10M USD/year.

> Built on Genesis Governance OS by Bunyawat Dechanon (ElmatadorZ)

---

<div align="center">
<em>"รัฐธรรมนูญที่ดี ไม่ได้ทำให้ประชาชนฉลาดขึ้น — แต่ทำให้แม้ประชาชนฉลาดขึ้น ระบบก็ยังไม่พัง"</em><br>
<em>A good constitution doesn't make the citizens smarter — it ensures that even as they do, the system doesn't break.</em>
</div>
