"""SKILL.md contract for Genesis Governance OS.

conformance_test.py exercises the standards themselves (GTS-1, GPS-2, GOP-3).
This holds the installable SKILL.md to its own frontmatter contract, so the file
a model loads stays valid and its license keeps agreeing with the LICENSE file.
"""
from __future__ import annotations

import re
from pathlib import Path

import yaml

# reference/python/ -> repo root
ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "skills" / "genesis-governance-os" / "SKILL.md"


def _split():
    text = SKILL.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    assert m, "frontmatter must be present and delimited"
    return yaml.safe_load(m.group(1)), text[m.end():]


def test_canonical_filename():
    assert SKILL.exists() and SKILL.name == "SKILL.md"


def test_frontmatter_and_license():
    fm, _ = _split()
    for f in ("name", "description", "license"):
        assert f in fm
    assert str(fm["license"]).lower().replace(" ", "-") == "apache-2.0"
    assert "Apache License" in (ROOT / "LICENSE").read_text(encoding="utf-8")


def test_name_slug_safe():
    fm, _ = _split()
    assert re.fullmatch(r"[a-z0-9][a-z0-9-]*", str(fm["name"]))


def test_metadata_bounds_scope():
    fm, _ = _split()
    meta = fm.get("metadata", {})
    assert meta.get("compatibility")
    assert meta.get("not_for")


def test_four_standards_named_in_body():
    _, body = _split()
    for std in ("GTS-1", "GPS-2", "GOP-3", "GOS-0"):
        assert std in body, f"the {std} standard must be named in SKILL.md"
