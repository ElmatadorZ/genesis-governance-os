"""
GOP-3 Orchestration — reference implementation.
One coordinator loop with a HARD loop guard. Routes by capability fit.
Obeys GPS-2 and GTS-1 — it schedules, it does not rule.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable

from .task_state import TaskState, Status
from .permission import Grant, evaluate, Verdict


class LoopGuardTripped(Exception):
    """Raised when attempts/handoffs/steps exceed the ceiling. Escalate to human."""


@dataclass
class LoopGuard:
    max_attempts_per_task: int = 3
    max_handoffs: int = 5
    max_total_steps: int = 25
    _steps: int = 0
    _handoffs: int = 0

    def step(self) -> None:
        self._steps += 1
        if self._steps > self.max_total_steps:
            raise LoopGuardTripped(f"max_total_steps {self.max_total_steps} exceeded")

    def handoff(self) -> None:
        self._handoffs += 1
        if self._handoffs > self.max_handoffs:
            raise LoopGuardTripped(f"max_handoffs {self.max_handoffs} exceeded")

    def check_attempts(self, task: TaskState) -> None:
        if len(task.attempts) > self.max_attempts_per_task:
            raise LoopGuardTripped(f"max_attempts_per_task {self.max_attempts_per_task} exceeded")


@dataclass
class Agent:
    name: str
    capabilities: set[str]          # for capability-match routing
    grant: Grant
    # act(task) -> (action_str, ok, blocked_reason|None, handoff_to|None, note|None)
    act: Callable[[TaskState], tuple]


@dataclass
class Orchestrator:
    agents: dict[str, Agent]
    guard: LoopGuard = field(default_factory=LoopGuard)
    audit: list[dict] = field(default_factory=list)

    def _log(self, **kw) -> None:
        self.audit.append(kw)

    def route(self, task: TaskState, need: str) -> str:
        """Capability-match routing — by fit, never by availability."""
        for name, ag in self.agents.items():
            if need in ag.capabilities:
                return name
        raise LoopGuardTripped(f"no agent matches capability '{need}' -> capability request")

    def run(self, task: TaskState) -> TaskState:
        try:
            while task.status not in (Status.DONE, Status.FAILED, Status.ARCHIVED):
                self.guard.step()
                self.guard.check_attempts(task)

                if task.status == Status.PENDING:
                    task.set_status(Status.IN_PROGRESS)

                agent = self.agents[task.owner]
                action, ok, blocked_reason, handoff_to, note = agent.act(task)

                # GPS-2 gate BEFORE doing anything
                decision = evaluate(agent.grant, action)
                self._log(event="permission", agent=agent.name, action=action,
                          verdict=decision.verdict.value, reason=decision.reason)
                if decision.verdict == Verdict.DENY:
                    task.add_attempt(agent.name, action, "failed", decision.reason)
                    continue
                if decision.verdict == Verdict.ESCALATE:
                    task.human_gate = True
                    self._log(event="escalate_to_human", task=task.id, action=action)
                    return task  # pause for human

                # honest failure
                if blocked_reason:
                    task.declare_blocked(agent.name, blocked_reason)
                    self._log(event="blocked", task=task.id, reason=blocked_reason)
                    return task  # raise capability request upstream

                task.add_attempt(agent.name, action, "accepted" if ok else "rejected")

                if handoff_to:
                    self.guard.handoff()
                    task.handoff_to(handoff_to, note or "(no note)")
                    self._log(event="handoff", to=handoff_to, note=note)
                elif ok and task.is_done_satisfied():
                    task.set_status(Status.DONE)
                    self._log(event="done", task=task.id)

            return task
        except LoopGuardTripped as e:
            task.human_gate = True
            self._log(event="loop_guard_tripped", task=task.id, detail=str(e))
            return task  # never retry forever — escalate
