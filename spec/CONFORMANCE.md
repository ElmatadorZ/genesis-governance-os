# Genesis Governance OS — Conformance Specification

**Status:** Normative · **Version:** 2.0 · **Applies to:** GTS-1, GPS-2, GOP-3, GOS-0

This document is the single normative authority for what it means to *claim conformance* with
Genesis Governance OS. It restates the invariants defined in the individual specifications using
formal requirement language, assigns each a stable identifier, defines conformance levels, and
states honestly which requirements are machine-verified and which require attestation.

It introduces **no new requirements.** Where this document and an individual specification appear
to disagree, that is a defect — please [open an issue](https://github.com/ElmatadorZ/genesis-governance-os/issues).

---

## 1. Normative language

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**, **SHOULD**,
**SHOULD NOT**, **RECOMMENDED**, **MAY**, and **OPTIONAL** in this document and in the
specifications it governs are to be interpreted as described in
[RFC 2119](https://www.rfc-editor.org/rfc/rfc2119) and
[RFC 8174](https://www.rfc-editor.org/rfc/rfc8174), and only when they appear in all capitals.

## 2. Terminology

| Term | Meaning |
|---|---|
| **Implementation** | Any system claiming to implement one or more Genesis Governance OS standards. |
| **Agent** | An autonomous actor that may hold a task, request permission, and act. |
| **Governance layer** | The human or Legislative branch authority that issues and edits grants. |
| **Irreversible action** | An action whose effects cannot be undone by the implementation itself (`reversible: false`). |
| **Human gate** | An explicit, recorded approval by a human before a specific action proceeds. |
| **Audit log** | An append-only, tamper-evident record external to the agent being audited. |

## 3. Conformance levels

An implementation MUST declare exactly one level.

| Level | Name | Requires |
|---|---|---|
| **L1** | **Core** | All **GTS-1** and **GPS-2** requirements. The minimum that prevents the worst failures. |
| **L2** | **Full** | L1 **plus** all **GOP-3** requirements. |
| **L3** | **Governed** | L2 **plus** **GOS-0** — separation of powers and the constitutional laws. |

- An implementation claiming **L3** MUST enforce, at minimum, constitutional laws 01, 02, 15, 16,
  and 17 (separation of powers · accountability · human-decides · honest-failure ·
  capability-as-constitutional-act). All remaining laws are **RECOMMENDED**, and are **REQUIRED**
  for the *governmental-scale* profile.
- An implementation that satisfies some but not all requirements of a level MUST NOT claim that
  level. It MAY describe itself as "partially conformant" and MUST enumerate the unmet requirements.

## 4. Normative requirements

Requirement IDs are stable and MUST be cited when claiming or disputing conformance.

### 4.1 GTS-1 · Task State

| ID | Requirement |
|---|---|
| **GTS-1.1** | A task **MUST** have at most one `owner` at any instant. A handoff **MUST** change ownership atomically. |
| **GTS-1.2** | `attempts` and `decisions` **MUST** be append-only. An implementation **MUST NOT** edit or delete a recorded attempt. |
| **GTS-1.3** | A task **MUST NOT** reach `done` unless every `done_when` item is checkable and has been checked. Implicit completion **MUST NOT** occur. |
| **GTS-1.4** | A change of owner **MUST** carry a non-empty `handoff.note`. A task **MUST NOT** move silently. |
| **GTS-1.5** | Every state change **MUST** be referenced in an external tamper-evident audit log (`audit_ref`). |

### 4.2 GPS-2 · Permission

| ID | Requirement |
|---|---|
| **GPS-2.1** | Any action not explicitly allowed **MUST** be denied (deny-by-default). An explicit deny **MUST** take precedence over an allow. |
| **GPS-2.2** | The permission gate **MUST** execute *before* the tool call. An implementation **MUST NOT** evaluate permission after the effect. |
| **GPS-2.3** | An irreversible action **MUST** require both an explicit grant **and** a passed human gate; otherwise it **MUST** be denied or escalated. An action of unknown reversibility **MUST** be treated as irreversible. |
| **GPS-2.4** | Every decision — ALLOW, DENY, and ESCALATE alike — **MUST** be written to the audit log. |
| **GPS-2.5** | An agent **MUST NOT** widen its own scope. Only the governance layer **MAY** edit grants. Self-modification of permissions is a constitutional violation. |

### 4.3 GOP-3 · Orchestration

| ID | Requirement |
|---|---|
| **GOP-3.1** | Every sub-task **MUST** be created with checkable `done_when` criteria. |
| **GOP-3.2** | Assignment **MUST** be by capability fit. An implementation **MUST NOT** route solely by availability. |
| **GOP-3.3** | Hard ceilings on attempts, handoffs, and total steps **MUST** be enforced. On trip, the workflow **MUST** escalate to a human and **MUST NOT** retry unboundedly. |
| **GOP-3.4** | The orchestrator **MUST NOT** override a GPS-2 DENY, a GTS-1 `done_when`, or a human gate. The coordinator is not a superuser. |
| **GOP-3.5** | Every workflow **MUST** terminate with a human-auditable summary. |

### 4.4 GOS-0 · Constitution (L3)

| ID | Requirement |
|---|---|
| **GOS-0.01** | No component **MUST** simultaneously legislate, execute, and judge (separation of powers). |
| **GOS-0.02** | Every consequential action **MUST** be attributable to an accountable actor. |
| **GOS-0.15** | Irreversible decisions **MUST** rest with a human. |
| **GOS-0.16** | A blocked agent **MUST** report the block. It **MUST NOT** fake completion (honest failure). |
| **GOS-0.17** | Acquiring a new capability **MUST** proceed as a constitutional act; the system **MUST NOT** rewrite its own rules. |

## 5. Verification

### 5.1 Machine-verified requirements

The reference conformance suite ([`reference/python/conformance_test.py`](../reference/python/conformance_test.py))
executes **18 checks**. It runs dependency-free and under `pytest`, and is exercised in CI across
Linux, macOS, and Windows on Python 3.9 / 3.11 / 3.12.

```bash
cd reference/python
python conformance_test.py     # -> CONFORMANCE: 18/18 passed
python -m pytest -q            # every check asserts; a violation fails the run
```

| Requirement | Automated coverage |
|---|---|
| GTS-1.1 | ✅ owner changes atomically on handoff |
| GTS-1.2 | ✅ attempts append-only |
| GTS-1.3 | ✅ 4 checks — empty `done_when` rejected, early `done` blocked, `done` allowed when satisfied, illegal transition rejected |
| GTS-1.4 | ✅ empty handoff note rejected |
| GTS-1.5 | ⚠️ **attestation** — external log integrity cannot be proven in-process |
| GPS-2.1 | ✅ 3 checks — unlisted denied, explicit deny wins, allow scope honoured |
| GPS-2.2 | ⚠️ **attestation** — call ordering is a property of the host integration |
| GPS-2.3 | ✅ 3 checks — escalate without human, allow with human gate, unknown treated as irreversible |
| GPS-2.4 | ⚠️ **attestation** — audit completeness is host-dependent |
| GPS-2.5 | ⚠️ **attestation** — requires inspecting the grant-editing path |
| GOP-3.1 | ✅ covered via workflow construction |
| GOP-3.2 | ⚠️ **not yet automated** — routing-by-fit test is an open item |
| GOP-3.3 | ✅ 2 checks — guard escalates, trip event logged |
| GOP-3.4 | ✅ covered indirectly by the gate tests |
| GOP-3.5 | ⚠️ **not yet automated** |
| GOS-0.16 | ✅ blocked status, not fake-done |
| GOS-0.01/.02/.15/.17 | ⚠️ **attestation** — organisational properties |

### 5.2 Attestation

Requirements marked ⚠️ cannot be proven by an in-process test suite; they are properties of how the
implementation is *integrated and operated*. An implementation claiming conformance for these
**MUST** publish a short attestation describing how each is enforced, and **SHOULD** link to the
code path or control that enforces it.

Stating this openly is deliberate: a standard that claims full automated coverage it does not have
would violate its own honest-failure law (GOS-0.16).

## 6. Claiming conformance

An implementation claiming conformance **MUST** publish:

1. the **level** claimed (L1 / L2 / L3);
2. the **version** of this specification (2.0);
3. the **result** of the conformance suite, or of an equivalent suite in the implementation language;
4. an **attestation** for every ⚠️ requirement at the claimed level;
5. any **unmet** requirements, by ID.

Recommended wording:

> *"<name> is Genesis Governance OS **L2 (Full)** conformant against CONFORMANCE 2.0.
> Automated: 18/18. Attested: GTS-1.5, GPS-2.2, GPS-2.4, GPS-2.5, GOP-3.5. Unmet: none."*

An implementation that strips safety invariants (separation of powers, honest-failure,
human-in-the-loop) **MUST NOT** claim conformance and **MUST** be renamed so as not to imply
endorsement — see [LICENSE](../LICENSE.md) §3.

## 7. Versioning & stability

- This specification follows **semantic versioning**. Within a major version, requirement IDs are
  **stable** and their meaning **MUST NOT** change.
- A **MINOR** bump **MAY** add RECOMMENDED or OPTIONAL requirements, or add automated coverage.
- Promoting a requirement to MUST, or adding a new MUST, **REQUIRES** a **MAJOR** bump.
- Retired requirement IDs **MUST NOT** be reused.
- Changes are recorded in [CHANGELOG.md](../CHANGELOG.md).

---

*Genesis Governance OS · CONFORMANCE 2.0 · Bunyawat Dechanon (ElmatadorZ)*
