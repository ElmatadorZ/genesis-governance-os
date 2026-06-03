"""
GTS-1 Task State — reference implementation.
Enforces the five invariants of the Genesis Task State standard.
Pure stdlib, no dependencies. Port the logic, not the language.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class Status(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    REVIEW = "review"
    DONE = "done"
    FAILED = "failed"
    ARCHIVED = "archived"


# allowed transitions — anything not listed raises
_TRANSITIONS: dict[Status, set[Status]] = {
    Status.PENDING: {Status.IN_PROGRESS, Status.FAILED},
    Status.IN_PROGRESS: {Status.BLOCKED, Status.REVIEW, Status.FAILED, Status.DONE},
    Status.BLOCKED: {Status.IN_PROGRESS, Status.FAILED},
    Status.REVIEW: {Status.IN_PROGRESS, Status.DONE, Status.FAILED},
    Status.DONE: {Status.ARCHIVED},
    Status.FAILED: {Status.IN_PROGRESS, Status.ARCHIVED},
    Status.ARCHIVED: set(),
}


class GTSViolation(Exception):
    """Raised when an operation would break a GTS-1 invariant."""


@dataclass
class Attempt:
    by: str
    action: str
    result: str  # pending | pending_review | rejected | accepted | failed
    reason: str = ""
    at: str = field(default_factory=_now)


@dataclass
class Handoff:
    frm: str
    to: str
    note: str


@dataclass
class TaskState:
    """One unit of work. One owner at a time. The five invariants are enforced here."""
    id: str
    goal: str
    done_when: list[str]
    owner: str
    status: Status = Status.PENDING
    created_by: str = "orchestrator"
    created_at: str = field(default_factory=_now)
    updated_at: str = field(default_factory=_now)
    inputs: dict[str, Any] = field(default_factory=dict)
    outputs: dict[str, Any] = field(default_factory=dict)
    attempts: list[Attempt] = field(default_factory=list)
    decisions: list[dict] = field(default_factory=list)
    handoff: Handoff | None = None
    error: str | None = None
    human_gate: bool = False
    parent: str | None = None
    audit_ref: str = ""
    _done_checks: set[str] = field(default_factory=set)  # which done_when satisfied

    def __post_init__(self):
        if not self.id.startswith("TASK-"):
            raise GTSViolation("id must start with TASK-")
        if not self.done_when:
            raise GTSViolation("done_when must have at least one checkable item (invariant 3)")

    # --- invariant 2: append-only ---
    def add_attempt(self, by: str, action: str, result: str, reason: str = "") -> None:
        self.attempts.append(Attempt(by=by, action=action, result=result, reason=reason))
        self.updated_at = _now()

    def add_decision(self, by: str, choice: str, because: str) -> None:
        self.decisions.append({"by": by, "choice": choice, "because": because})
        self.updated_at = _now()

    # --- invariant 1 + 4: single owner, handoff carries a note ---
    def handoff_to(self, new_owner: str, note: str) -> None:
        if not note or not note.strip():
            raise GTSViolation("handoff requires a non-empty note (invariant 4)")
        self.handoff = Handoff(frm=self.owner, to=new_owner, note=note)
        self.owner = new_owner  # atomic single-owner change
        self.updated_at = _now()

    # --- status transitions are validated ---
    def set_status(self, new: Status) -> None:
        if new not in _TRANSITIONS[self.status]:
            raise GTSViolation(f"illegal transition {self.status.value} -> {new.value}")
        if new is Status.DONE and not self.is_done_satisfied():
            raise GTSViolation("cannot set done: done_when not fully satisfied (invariant 3)")
        self.status = new
        self.updated_at = _now()

    # --- invariant 3: explicit, checkable completion ---
    def mark_done_check(self, criterion: str) -> None:
        if criterion not in self.done_when:
            raise GTSViolation(f"'{criterion}' is not a declared done_when item")
        self._done_checks.add(criterion)

    def is_done_satisfied(self) -> bool:
        return set(self.done_when) <= self._done_checks

    # --- honest failure (ties to constitution law 16) ---
    def declare_blocked(self, by: str, reason: str) -> None:
        self.add_attempt(by=by, action="declared blocked", result="failed", reason=reason)
        self.set_status(Status.BLOCKED)

    def to_dict(self) -> dict:
        d = {k: v for k, v in self.__dict__.items() if not k.startswith("_")}
        d["status"] = self.status.value
        d["attempts"] = [a.__dict__ for a in self.attempts]
        if self.handoff:
            d["handoff"] = {"from": self.handoff.frm, "to": self.handoff.to, "note": self.handoff.note}
        return d
