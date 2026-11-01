"""
Tests for init_cmd.py: project scaffolding, rule & skill creation, and collision guards.
"""
from pathlib import Path
import typer
from auto_context.commands import init_cmd


def test_init_scaffolds_complete_workspace(tmp_path: Path):
    init_cmd.init(target=tmp_path)

    assert (tmp_path / "context.md").exists()
    assert (tmp_path / "context.local.md").exists()
    assert (tmp_path / "AGENTS.md").exists()
    assert (tmp_path / "GEMINI.md").exists()
    assert (tmp_path / ".agents" / "rules" / "maintain_context.md").exists()
    assert (tmp_path / ".agents" / "skills" / "docker-ops" / "SKILL.md").exists()
    assert (tmp_path / ".gitignore").exists()


def test_rule_creation_and_collision_guard(tmp_path: Path):
    # Create rule first time
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


def test_skill_creation_and_collision_guard(tmp_path: Path):
    # Create skill first time
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
