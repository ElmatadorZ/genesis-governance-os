"""
Conformance test suite for Genesis Governance OS reference implementation.
Each test maps to a named invariant in the spec. Run: python -m pytest -v
(or just `python conformance_test.py` for a dependency-free run).
"""
import sys
from genesis_gos import (
    TaskState, Status, GTSViolation,
    Grant, evaluate, Verdict,
    Orchestrator, Agent, LoopGuard,
)

results = []
def check(name, cond):
    results.append((name, bool(cond)))
    print(f"  {'✅' if cond else '❌'} {name}")


def test_gts1():
    print("\nGTS-1 · Task State")
    # invariant 3: done_when required
    try:
        TaskState(id="TASK-X", goal="g", done_when=[], owner="a"); ok = False
    except GTSViolation: ok = True
    check("inv3: empty done_when rejected", ok)

    t = TaskState(id="TASK-1", goal="g", done_when=["a", "b"], owner="agent1")

    # invariant 2: append-only attempts
    t.add_attempt("agent1", "try", "rejected"); t.add_attempt("agent1", "try2", "accepted")
    check("inv2: attempts append-only grows", len(t.attempts) == 2)

    # invariant 3: cannot mark done early
    try:
        t.set_status(Status.IN_PROGRESS); t.set_status(Status.DONE); ok = False
    except GTSViolation: ok = True
    check("inv3: done blocked until done_when satisfied", ok)

    # satisfy then done
    t.mark_done_check("a"); t.mark_done_check("b")
    t.set_status(Status.DONE)
    check("inv3: done allowed when all checks met", t.status == Status.DONE)

    # invariant 1+4: handoff carries note, single owner
    t2 = TaskState(id="TASK-2", goal="g", done_when=["x"], owner="a")
    try:
        t2.handoff_to("b", ""); ok = False
    except GTSViolation: ok = True
    check("inv4: empty handoff note rejected", ok)
    t2.handoff_to("b", "context note")
    check("inv1: single owner changes atomically", t2.owner == "b")

    # illegal transition
    t3 = TaskState(id="TASK-3", goal="g", done_when=["x"], owner="a")
    try:
        t3.set_status(Status.DONE); ok = False
    except GTSViolation: ok = True
    check("transition: pending->done illegal", ok)


def test_gps2():
    print("\nGPS-2 · Permission")
    g = Grant(agent="w", allow=["read:docs", "write:drafts"],
              deny=["send:email"], escalate=["publish:post"])

    # inv1: deny-by-default
    check("inv1: unlisted action denied", evaluate(g, "exec:shell").verdict == Verdict.DENY)
    # explicit deny wins
    check("explicit deny -> DENY", evaluate(g, "send:email").verdict == Verdict.DENY)
    # allow scope
    check("in allow -> ALLOW", evaluate(g, "read:docs").verdict == Verdict.ALLOW)
    # inv3: irreversible -> escalate without human
    check("inv3: publish escalates without human", evaluate(g, "publish:post").verdict == Verdict.ESCALATE)
    # with human gate -> allow
    check("inv3: publish allowed with human gate",
          evaluate(g, "publish:post", human_gate_passed=True).verdict == Verdict.ALLOW)
    # unknown tool treated dangerous
    check("unknown action treated as irreversible", evaluate(g, "weird:thing").verdict in (Verdict.ESCALATE, Verdict.DENY))


def test_gop3():
    print("\nGOP-3 · Orchestration")

    # a tiny 2-step workflow: research -> (handoff) -> writer -> done
    def research_act(task):
        return ("read:docs", True, None, "writer", "facts ready")
    def writer_act(task):
        task.mark_done_check("drafted")
        return ("write:drafts", True, None, None, None)

    agents = {
        "researcher": Agent("researcher", {"research"},
                            Grant("researcher", allow=["read:docs"]), research_act),
        "writer": Agent("writer", {"write"},
                        Grant("writer", allow=["write:drafts"]), writer_act),
    }
    orch = Orchestrator(agents=agents)
    t = TaskState(id="TASK-W", goal="post", done_when=["drafted"], owner="researcher")
    orch.run(t)
    check("workflow reaches done", t.status == Status.DONE)
    check("handoff recorded with note", t.handoff and t.handoff.note == "facts ready")

    # inv3: loop guard trips, escalates instead of infinite retry
    def stuck_act(task):
        return ("read:docs", False, None, None, None)  # never satisfies done_when
    ag = {"x": Agent("x", {"research"}, Grant("x", allow=["read:docs"]), stuck_act)}
    orch2 = Orchestrator(agents=ag, guard=LoopGuard(max_total_steps=5))
    t2 = TaskState(id="TASK-LOOP", goal="g", done_when=["never"], owner="x")
    orch2.run(t2)
    check("inv3: loop guard escalates (human_gate set)", t2.human_gate is True)
    tripped = any(e.get("event") == "loop_guard_tripped" for e in orch2.audit)
    check("inv3: loop guard event logged", tripped)

    # honest failure path
    def block_act(task):
        return ("read:docs", False, "missing OCR capability", None, None)
    ag3 = {"y": Agent("y", {"research"}, Grant("y", allow=["read:docs"]), block_act)}
    orch3 = Orchestrator(agents=ag3)
    t3 = TaskState(id="TASK-BLOCK", goal="g", done_when=["z"], owner="y")
    orch3.run(t3)
    check("honest failure: status blocked, not fake-done", t3.status == Status.BLOCKED)


def main():
    test_gts1(); test_gps2(); test_gop3()
    passed = sum(1 for _, ok in results if ok)
    total = len(results)
    print(f"\n{'='*48}\nCONFORMANCE: {passed}/{total} passed")
    if passed != total:
        print("FAILED:", [n for n, ok in results if not ok]); sys.exit(1)
    print("✅ ALL INVARIANTS HOLD — GOS-2.0 conformant")


if __name__ == "__main__":
    main()
