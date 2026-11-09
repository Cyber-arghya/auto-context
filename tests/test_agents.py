"""
Tests for subagent persona directory support (.agents/agents/) and init-context agent command.
"""
from pathlib import Path
from unittest.mock import patch
import typer

from auto_context.commands import init_cmd
from auto_context import config


def test_init_scaffolds_default_subagents(tmp_path: Path):
    init_cmd.init(target=tmp_path)
    agents_dir = tmp_path / ".agents" / "agents"
    assert agents_dir.is_dir()
    for role in ("architect.md", "code-reviewer.md", "security-auditor.md"):
        role_file = agents_dir / role
        assert role_file.is_file(), f"Expected default subagent {role} to be scaffolded"
        content = role_file.read_text(encoding="utf-8")
        assert tmp_path.name in content


def test_new_agent_predefined_role(tmp_path: Path):
    init_cmd.new_agent(name="architect", target=tmp_path)
    agent_file = tmp_path / ".agents" / "agents" / "architect.md"
    assert agent_file.is_file()
    content = agent_file.read_text(encoding="utf-8")
    assert "Software Architect" in content
    assert tmp_path.name in content


def test_new_agent_custom_role(tmp_path: Path):
    init_cmd.new_agent(
        name="database-engineer",
        description="PostgreSQL schema and query performance specialist",
        target=tmp_path,
    )
    agent_file = tmp_path / ".agents" / "agents" / "database-engineer.md"
    assert agent_file.is_file()
    content = agent_file.read_text(encoding="utf-8")
    assert "Database Engineer" in content
    assert "PostgreSQL schema" in content


def test_new_agent_collision_guard_and_force(tmp_path: Path):
    init_cmd.new_agent(name="tester", target=tmp_path)
    agent_file = tmp_path / ".agents" / "agents" / "tester.md"
    assert agent_file.is_file()

    # Re-running without force should raise typer.Exit(1)
    try:
        init_cmd.new_agent(name="tester", target=tmp_path)
        assert False, "Should raise typer.Exit when subagent exists without --force"
    except typer.Exit as e:
        assert e.exit_code == 1

    # Re-running with force=True should succeed
    init_cmd.new_agent(name="tester", target=tmp_path, force=True, description="Updated tester description")
    assert "Updated tester description" in agent_file.read_text(encoding="utf-8")


def test_promote_subagent(tmp_path: Path):
    fake_global = tmp_path / "fake_global"
    fake_memory = tmp_path / "fake_memory"
    fake_global.mkdir(parents=True)
    fake_memory.mkdir(parents=True)

    with patch.object(config, "GLOBAL_PLUGIN_DIR", fake_global), patch.object(config, "MEMORY_DIR", fake_memory):
        init_cmd.new_agent(name="release-manager", target=tmp_path)
        init_cmd.promote("release-manager", target=tmp_path)

        assert (fake_global / "agents" / "release-manager.md").is_file()
        assert (fake_memory / "agents" / "release-manager.md").is_file()
