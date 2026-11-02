"""
test_ssot.py — Single Source of Truth & Zero-Drift Invariant Tests.

Verifies that bundled plugin rules and skills in plugin/ never drift from
the canonical templates in src/auto_context/templates.
"""
import filecmp
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = REPO_ROOT / "src" / "auto_context" / "templates"
PLUGIN_DIR = REPO_ROOT / "plugin"


def test_rules_and_skills_ssot_sync():
    """Ensure all rules and skills in templates/ match plugin/ exactly."""
    # 1. Rules
    rules_tmpl = TEMPLATES_DIR / "rules"
    assert rules_tmpl.is_dir(), "templates/rules directory must exist"
    for src in rules_tmpl.rglob("*.md"):
        rel = src.relative_to(rules_tmpl)
        dst = PLUGIN_DIR / "rules" / rel
        assert dst.exists(), f"Plugin rule missing: {dst}"
        assert filecmp.cmp(src, dst, shallow=False), f"Drift detected between {src} and {dst}. Run scripts/sync_plugin.py"

    # 2. Skills
    skills_tmpl = TEMPLATES_DIR / "skills"
    assert skills_tmpl.is_dir(), "templates/skills directory must exist"
    for src in skills_tmpl.rglob("*.md"):
        rel = src.relative_to(skills_tmpl)
        dst = PLUGIN_DIR / "skills" / rel
        assert dst.exists(), f"Plugin skill missing: {dst}"
        assert filecmp.cmp(src, dst, shallow=False), f"Drift detected between {src} and {dst}. Run scripts/sync_plugin.py"


def test_no_redundant_gemini_template():
    """Ensure GEMINI.template.md is not duplicated (AGENTS.template.md is SSOT)."""
    gemini_tmpl = TEMPLATES_DIR / "GEMINI.template.md"
    assert not gemini_tmpl.exists(), "GEMINI.template.md must not exist; AGENTS.template.md is the single canonical template."

