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

    # 4. Standard docs/ Layout Templates
    docs_dir = TEMPLATES_DIR / "docs"
    assert docs_dir.is_dir(), "templates/docs/ directory must exist"
    expected_docs = [
        "architecture/system-design.md",
        "architecture/database-schema.md",
        "architecture/api-design.md",
        "development/development-guide.md",
        "decisions/ADR-001.md",
    ]
    for doc_rel in expected_docs:
        doc_path = docs_dir / doc_rel
        assert doc_path.exists(), f"Missing required docs template: {doc_rel}"

    # 5. Antigravity Subagent Personas
    agents_dir = TEMPLATES_DIR / "agents"
    assert agents_dir.is_dir(), "templates/agents/ directory must exist"
    assert (TEMPLATES_DIR / "agent.template.md").exists(), "templates/agent.template.md must exist"
    for expected in ("architect.md", "code-reviewer.md", "security-auditor.md"):
        agent_file = agents_dir / expected
        assert agent_file.exists(), f"Missing required subagent persona: {expected}"

    # 6. Deterministic Lifecycle Hooks
    hooks_dir = TEMPLATES_DIR / "hooks"
    assert hooks_dir.is_dir(), "templates/hooks/ directory must exist"
    for expected in ("format.sh", "format.ps1", "validate.sh", "validate.ps1"):
        hook_file = hooks_dir / expected
        assert hook_file.exists(), f"Missing required lifecycle hook template: {expected}"


def test_template_variable_rendering():
    """Ensure all core markdown templates render cleanly without unpopulated placeholders."""
    dummy_vars = {
        "PROJECT_NAME": "my-test-app",
        "PROJECT_DIR": "/path/to/my-test-app",
        "STACK": "Python 3.12",
        "FRAMEWORK": "FastAPI",
        "DATE_NOW": "2026-11-03",
        "AGENT_NAME": "custom-agent",
        "AGENT_ROLE": "Custom Agent",
        "AGENT_DESCRIPTION": "A custom test agent persona",
    }
    placeholder_pattern = re.compile(r"\{\{[A-Z0-9_]+\}\}")

    template_files = [
        TEMPLATES_DIR / "context.template.md",
        TEMPLATES_DIR / "AGENTS.template.md",
        TEMPLATES_DIR / "project-goal.template.md",
        TEMPLATES_DIR / "agent.template.md",
    ]
    docs_dir = TEMPLATES_DIR / "docs"
    if docs_dir.exists():
        template_files.extend(docs_dir.rglob("*.md"))
    agents_dir = TEMPLATES_DIR / "agents"
    if agents_dir.exists():
        template_files.extend(agents_dir.rglob("*.md"))
    hooks_dir = TEMPLATES_DIR / "hooks"
    if hooks_dir.exists():
        template_files.extend(f for f in hooks_dir.iterdir() if f.is_file())

    for tmpl_file in template_files:
        assert tmpl_file.exists(), f"{tmpl_file.name} must exist"
        rendered = _render(tmpl_file, dummy_vars)

        leftovers = placeholder_pattern.findall(rendered)
        assert not leftovers, f"{tmpl_file.name} contains unrendered placeholders: {leftovers}"
        assert "my-test-app" in rendered
