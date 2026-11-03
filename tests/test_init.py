"""
Tests for init_cmd.py: project scaffolding, rule & skill lifecycle, appending guidelines, and promotion.
"""
from pathlib import Path
import typer
from auto_context import config
from auto_context.commands import init_cmd


def test_init_scaffolds_complete_workspace(tmp_path: Path):
    """Verify that init-context creates all required core files and directories."""
    init_cmd.init(target=tmp_path)

    assert (tmp_path / ".agents" / "context.md").exists(), "context.md must be scaffolded"
    assert (tmp_path / ".agents" / "project-goal.md").exists(), "project-goal.md must be scaffolded"
    assert (tmp_path / "AGENTS.md").exists(), "AGENTS.md must be scaffolded"
    assert (tmp_path / "GEMINI.md").exists(), "GEMINI.md must be scaffolded"
    assert (tmp_path / ".agents" / "rules" / "code-standards.md").exists(), "code-standards rule must exist"
    assert (tmp_path / ".agents" / "skills" / "docker-ops" / "SKILL.md").exists(), "docker-ops skill must exist"
    assert (tmp_path / ".gitignore").exists(), ".gitignore must exist"


def test_rule_creation_and_collision_guard(tmp_path: Path):
    """Test creating a rule and verifying duplicate collision prevention."""
    init_cmd.new_rule(name="api-conventions", target=tmp_path)
    rule_file = tmp_path / ".agents" / "rules" / "api-conventions.md"
    assert rule_file.exists()

    # Attempting to recreate without --force must raise typer.Exit
    raised = False
    try:
        init_cmd.new_rule(name="api-conventions", target=tmp_path)
    except typer.Exit:
        raised = True
    assert raised, "Expected typer.Exit when recreating existing rule without --force"


def test_rule_append_guideline(tmp_path: Path):
    """Test appending a new guideline to an existing rule domain."""
    init_cmd.new_rule(name="code-standards", target=tmp_path)
    rule_file = tmp_path / ".agents" / "rules" / "code-standards.md"
    assert rule_file.exists()

    init_cmd.new_rule(
        name="code-standards",
        target=tmp_path,
        append=True,
        guideline="Always use type annotations for public APIs.",
    )
    content = rule_file.read_text(encoding="utf-8")
    assert "Always use type annotations for public APIs." in content


def test_skill_creation_and_collision_guard(tmp_path: Path):
    """Test creating an operational skill and verifying duplicate collision prevention."""
    init_cmd.new_skill(name="deploy-k8s", target=tmp_path)
    skill_file = tmp_path / ".agents" / "skills" / "deploy-k8s" / "SKILL.md"
    assert skill_file.exists()

    # Attempting to recreate without --force must raise typer.Exit
    raised = False
    try:
        init_cmd.new_skill(name="deploy-k8s", target=tmp_path)
    except typer.Exit:
        raised = True
    assert raised, "Expected typer.Exit when recreating existing skill without --force"


def test_promote_local_rule_and_skill(tmp_path: Path):
    """Test promoting local workspace rule and skill to Global Plugin scope."""
    fake_global = tmp_path / "fake_global"
    fake_memory = tmp_path / "fake_memory"
    orig_global = config.GLOBAL_PLUGIN_DIR
    orig_memory = config.MEMORY_DIR
    try:
        config.GLOBAL_PLUGIN_DIR = fake_global
        config.MEMORY_DIR = fake_memory

        # 1. Create local rule and skill
        init_cmd.new_rule(name="custom-db-rule", target=tmp_path)
        init_cmd.new_skill(name="custom-deploy", target=tmp_path)

        # 2. Promote both
        init_cmd.promote(name="custom-db-rule", target=tmp_path)
        init_cmd.promote(name="custom-deploy", target=tmp_path)

        # 3. Verify copied to global plugin directory
        assert (fake_global / "rules" / "custom-db-rule.md").exists()
        assert (fake_global / "skills" / "custom-deploy" / "SKILL.md").exists()
    finally:
        config.GLOBAL_PLUGIN_DIR = orig_global
        config.MEMORY_DIR = orig_memory
