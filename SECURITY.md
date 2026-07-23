# Security Policy

Genesis Governance OS is a **specification** plus a small reference implementation. Security issues
therefore fall into two distinct classes, and both matter.

## 1. Specification vulnerabilities

A flaw in the standard itself — a way to satisfy every stated invariant while still producing an
unsafe or unaccountable system. Examples: a permission-gate bypass that conformance would not
detect, a loop-guard evasion, a path that lets an agent widen its own scope while remaining
"conformant".

**These are the most serious issues this project can receive.** A specification flaw propagates to
every implementation.

## 2. Reference implementation vulnerabilities

A defect in `reference/python/` that does not reflect a flaw in the specification.

## Supported versions

| Version | Supported |
|---|---|
| 2.0.x | ✅ |
| < 2.0 | ❌ |

## Reporting

Please report privately first, via
[GitHub Security Advisories](https://github.com/ElmatadorZ/genesis-governance-os/security/advisories/new).
Do not open a public issue for an unpatched specification flaw.

Include: the requirement ID(s) affected (e.g. `GPS-2.3`), a concrete scenario that satisfies the
letter of the requirement while violating its intent, and the impact.

**Response targets:** acknowledgement within 7 days · initial assessment within 30 days.

## Disclosure

Confirmed specification flaws are published as a `MAJOR` or `MINOR` spec revision with an entry in
[CHANGELOG.md](CHANGELOG.md) and, where a requirement changes meaning, a migration note. Credit is
given unless the reporter requests otherwise.

## Scope

Out of scope: vulnerabilities in third-party implementations of this standard (report to that
project), and issues in models or runtimes the standard is applied to.
