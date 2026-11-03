"""
test_ssot.py — Single Source of Truth & Template Integrity Verification.

Enforces zero-duplicate-directory policy, canonical template integrity,
and clean template placeholder substitution.
"""
import json
import re
from pathlib import Path
from auto_context.commands.init_cmd import _render

REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = REPO_ROOT / "src" / "auto_context" / "templates"


def test_no_duplicate_plugin_directory():
    """Ensure duplicate 'plugin/' folder does NOT exist at repo root."""
    plugin_dir = REPO_ROOT / "plugin"
    assert not plugin_dir.exists(), "Duplicate 'plugin/' folder must not exist at repo root. All assets live in src/auto_context/templates/."


def test_no_redundant_gemini_template():
    """Ensure GEMINI.template.md is not duplicated (AGENTS.template.md is SSOT)."""
    gemini_tmpl = TEMPLATES_DIR / "GEMINI.template.md"
    assert not gemini_tmpl.exists(), "GEMINI.template.md must not exist; AGENTS.template.md is the single canonical template."


def test_canonical_templates_integrity():
    """Verify all canonical rules, skills, and plugin manifest exist in templates."""
    # 1. Plugin Manifest
    manifest = TEMPLATES_DIR / "plugin.json"
    assert manifest.exists(), "templates/plugin.json must exist"
    data = json.loads(manifest.read_text(encoding="utf-8"))
    assert data.get("name") == "auto-context"

    # 2. Domain Rules
    rules_dir = TEMPLATES_DIR / "rules"
    assert rules_dir.is_dir(), "templates/rules/ directory must exist"
    for expected in ("code-standards.md", "security-boundaries.md", "readme-docs-sync.md", "registry.json"):
        rule_path = rules_dir / expected
        assert rule_path.exists(), f"Missing required domain rule: {expected}"

    # 3. Operational Skills
    skills_dir = TEMPLATES_DIR / "skills"
    assert skills_dir.is_dir(), "templates/skills/ directory must exist"
    for expected in ("docker-ops", "git-workflow", "server-diagnostics", "feature-verification", "auto-context", "browser-testing"):
        skill_file = skills_dir / expected / "SKILL.md"
        assert skill_file.exists(), f"Missing required operational skill: {expected}/SKILL.md"


def test_template_variable_rendering():
    """Ensure all core markdown templates render cleanly without unpopulated placeholders."""
    dummy_vars = {
        "PROJECT_NAME": "my-test-app",
        "PROJECT_DIR": "/path/to/my-test-app",
        "STACK": "Python 3.12",
        "FRAMEWORK": "FastAPI",
        "DATE_NOW": "2026-11-03",
    }
    placeholder_pattern = re.compile(r"\{\{[A-Z0-9_]+\}\}")

    for template_name in ("context.template.md", "AGENTS.template.md", "project-goal.template.md"):
        tmpl_file = TEMPLATES_DIR / template_name
        assert tmpl_file.exists(), f"{template_name} must exist"
        rendered = _render(tmpl_file, dummy_vars)

        leftovers = placeholder_pattern.findall(rendered)
        assert not leftovers, f"{template_name} contains unrendered placeholders: {leftovers}"
        assert "my-test-app" in rendered
