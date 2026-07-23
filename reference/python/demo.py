"""
Runnable demo: the QUICKSTART 3-agent workflow, actually executing.
Run:  python demo.py
"""
import sys

from genesis_gos import TaskState, Status, Grant, Orchestrator, Agent

# Windows consoles default to cp1252 and cannot encode the status glyphs below.
try:
    sys.stdout.reconfigure(encoding="utf-8")
    OK_MARK = "✅"
except Exception:  # pragma: no cover - depends on host console
    OK_MARK = "[OK]"


def research_act(task):
    task.mark_done_check("facts gathered")
    return ("read:docs", True, None, "writer-agent", "3 verified facts attached")


def writer_act(task):
    task.mark_done_check("draft written")
    return ("write:drafts", True, None, "reviewer-agent", "draft 270 words, check CTA")


def reviewer_act(task):
    task.mark_done_check("reviewer APPROVED")
    return ("write:reviews", True, None, None, None)


def main():
    agents = {
        "research-agent": Agent("research-agent", {"research"},
            Grant("research-agent", allow=["read:docs", "read:web"], deny=["write:*", "send:*"]),
            research_act),
        "writer-agent": Agent("writer-agent", {"write"},
            Grant("writer-agent", allow=["read:docs", "write:drafts"],
                  deny=["send:*", "pay:*"], escalate=["publish:post"]),
            writer_act),
        "reviewer-agent": Agent("reviewer-agent", {"review"},
            Grant("reviewer-agent", allow=["read:drafts", "write:reviews"], deny=["publish:post"]),
            reviewer_act),
    }

    task = TaskState(
        id="TASK-0001",
        goal="publish-ready launch post, < 280 words, reviewed",
        done_when=["facts gathered", "draft written", "reviewer APPROVED"],
        owner="research-agent",
    )

    orch = Orchestrator(agents=agents)
    print("Running 3-agent workflow…\n")
    orch.run(task)

    print(f"Final status : {task.status.value}")
    print(f"Done satisfied: {task.is_done_satisfied()}")
    print(f"Attempts     : {len(task.attempts)}")
    print("\nAudit trail:")
    for e in orch.audit:
        print("  ", e)

    assert task.status == Status.DONE, "workflow should complete"
    print(f"\n{OK_MARK} workflow completed cleanly")


if __name__ == "__main__":
    main()
