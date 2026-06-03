"""
GPS-2 Permission — reference implementation.
Deny-by-default preventive gate. Runs BEFORE an action executes.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from fnmatch import fnmatch


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class Verdict(str, Enum):
    ALLOW = "ALLOW"
    DENY = "DENY"
    ESCALATE = "ESCALATE"


# global tool risk tiers; reversible=False means irreversible
TOOL_TIERS: dict[str, dict] = {
    "read:*":    {"tier": 0, "reversible": True},
    "write:*":   {"tier": 1, "reversible": True},
    "publish:*": {"tier": 2, "reversible": False},
    "send:*":    {"tier": 3, "reversible": False},
    "pay:*":     {"tier": 3, "reversible": False},
    "exec:*":    {"tier": 3, "reversible": False},
}


def _tier_for(action: str) -> dict:
    for pat, meta in TOOL_TIERS.items():
        if fnmatch(action, pat):
            return meta
    return {"tier": 3, "reversible": False}  # unknown = treat as dangerous


@dataclass
class Grant:
    agent: str
    allow: list[str] = field(default_factory=list)
    deny: list[str] = field(default_factory=list)
    escalate: list[str] = field(default_factory=list)


@dataclass
class Decision:
    agent: str
    action: str
    verdict: Verdict
    tier: int
    reversible: bool
    reason: str
    matched_rule: str
    at: str = field(default_factory=_now)


def _matches(action: str, patterns: list[str]) -> str | None:
    for p in patterns:
        if fnmatch(action, p):
            return p
    return None


def evaluate(grant: Grant, action: str, human_gate_passed: bool = False) -> Decision:
    """
    Decision order (first match wins) — invariant: deny-by-default.
    1. in deny            -> DENY
    2. irreversible & no human gate -> ESCALATE
    3. in escalate        -> ESCALATE
    4. in allow           -> ALLOW
    5. otherwise          -> DENY
    """
    meta = _tier_for(action)
    tier, rev = meta["tier"], meta["reversible"]

    def d(v: Verdict, reason: str, rule: str) -> Decision:
        return Decision(grant.agent, action, v, tier, rev, reason, rule)

    # 1. explicit deny — always wins
    m = _matches(action, grant.deny)
    if m:
        return d(Verdict.DENY, "explicitly denied", f"deny:{m}")

    in_escalate = _matches(action, grant.escalate)
    in_allow = _matches(action, grant.allow)

    # 2. deny-by-default FIRST: an action in no scope is denied,
    #    even (especially) if irreversible. Irreversibility never
    #    creates an escalation path that the grant didn't authorize.
    if not in_escalate and not in_allow:
        return d(Verdict.DENY, "not in any scope (deny-by-default)", "default:deny")

    # 3. irreversible in-scope action requires a human gate
    if not rev and not human_gate_passed:
        rule = f"escalate:{in_escalate}" if in_escalate else f"allow:{in_allow}"
        return d(Verdict.ESCALATE, "irreversible action requires human approval", f"{rule}+tier{tier}")

    # 4. explicit escalate (reversible, or human gate already passed)
    if in_escalate:
        if human_gate_passed:
            return d(Verdict.ALLOW, "escalated action approved by human", f"escalate:{in_escalate}+human")
        return d(Verdict.ESCALATE, "action requires human approval", f"escalate:{in_escalate}")

    # 5. explicit allow
    return d(Verdict.ALLOW, "in allow scope", f"allow:{in_allow}")
