## What does this change?

<!-- One paragraph. What problem does it solve? -->

## Type

- [ ] Specification change (touches `spec/` — see below)
- [ ] Reference implementation
- [ ] Documentation / examples
- [ ] Tooling / CI

## If this touches a specification

Specification changes are governed by [CONFORMANCE.md §7](../spec/CONFORMANCE.md).

- [ ] Requirement IDs affected: `________`
- [ ] This change is: `[ ] editorial  [ ] MINOR (adds SHOULD/MAY or coverage)  [ ] MAJOR (adds or promotes a MUST)`
- [ ] `CHANGELOG.md` updated
- [ ] No existing requirement ID changed meaning within this major version
- [ ] No retired requirement ID reused

## Safety invariants

- [ ] This change does **not** weaken separation of powers, honest-failure, or human-in-the-loop
- [ ] If it adds a requirement, conformance coverage is stated (automated or attestation)

## Verification

```bash
cd reference/python
python conformance_test.py   # must print 18/18 (or the new total)
python -m pytest -q
python demo.py
```

- [ ] Conformance suite passes locally
- [ ] CI is green on all platforms
