"""
Tests for commands/memory.py: memory status, memory reset, and remote error recovery.
"""
from pathlib import Path
from unittest.mock import patch
import typer
from auto_context.commands import memory
from auto_context import config


def test_memory_status_uninitialized(tmp_path: Path):
    with patch.object(memory, "MEMORY_DIR", tmp_path / "non_existent_memory"):
        # Should not raise exception
        memory.memory_status()


def test_memory_reset_with_force(tmp_path: Path):
    fake_mem = tmp_path / "fake_memory"
    fake_mem.mkdir(parents=True)
    (fake_mem / "dirty.txt").write_text("temporary data", encoding="utf-8")

    with patch.object(memory, "MEMORY_DIR", fake_mem):
        # Reset with force=True, harvest=False
        memory.memory_reset(force=True, harvest=False)

        assert (fake_mem / "rules").is_dir()
        assert (fake_mem / "skills").is_dir()
        assert (fake_mem / "profile.md").is_file()
        assert not (fake_mem / "dirty.txt").exists()


def test_repo_name_extraction():
    import re
    url = "git@github.com:Cyber-arghya/custom-memory-brain.git"
    m = re.search(r"[:/]([^/:]+?)(?:\.git)?$", url)
    assert m is not None
    assert m.group(1) == "custom-memory-brain"


def test_memory_remote_url(tmp_path: Path):
    fake_mem = tmp_path / "fake_mem_remote"
    fake_mem.mkdir(parents=True)
    memory._git(fake_mem, "init")

    with patch.object(memory, "MEMORY_DIR", fake_mem):
        memory.memory_remote("git@github.com:myuser/test-remote.git")
        rem = memory._git(fake_mem, "remote", "get-url", "origin").stdout.strip()
        assert rem == "git@github.com:myuser/test-remote.git"


def test_memory_pull_git_error_graceful(tmp_path: Path):
    fake_mem = tmp_path / "fake_mem"
    fake_mem.mkdir(parents=True)
    with patch.object(memory, "MEMORY_DIR", fake_mem):
        with patch.object(memory, "_git", side_effect=memory.subprocess.CalledProcessError(1, ["git", "pull"], stderr="fatal: remote error")):
            try:
                memory.memory_pull()
                assert False, "Should have raised typer.Exit"
            except typer.Exit as e:
                assert e.exit_code == 1


def test_memory_harvest_recursive_skill_tree(tmp_path: Path):
    fake_mem = tmp_path / "fake_mem_tree"
    fake_mem.mkdir(parents=True)
    fake_proj = tmp_path / "fake_project"
    fake_proj.mkdir(parents=True)

    local_skill_dir = fake_proj / config.AGENTS_SUBDIR / "skills" / "custom-deploy"
    scripts_dir = local_skill_dir / "scripts"
    scripts_dir.mkdir(parents=True)
    (local_skill_dir / "SKILL.md").write_text("# Deploy Skill", encoding="utf-8")
    (scripts_dir / "deploy.sh").write_text("#!/bin/bash\necho deploy", encoding="utf-8")

    with patch.object(memory, "MEMORY_DIR", fake_mem):
        harvested = memory._sync_local_to_memory(fake_proj)
        assert harvested >= 1
        assert (fake_mem / "skills" / "custom-deploy" / "SKILL.md").is_file()
        assert (fake_mem / "skills" / "custom-deploy" / "scripts" / "deploy.sh").is_file()
        assert (fake_mem / "skills" / "custom-deploy" / "scripts" / "deploy.sh").read_text(encoding="utf-8") == "#!/bin/bash\necho deploy"


def test_memory_status_json_output(tmp_path: Path):
    """Test machine-readable JSON output for memory status."""
    import json
    from typer.testing import CliRunner
    from auto_context.main import app

    runner = CliRunner()
    # 1. Uninitialized memory status as JSON
    with patch.object(memory, "MEMORY_DIR", tmp_path / "non_existent"):
        result = runner.invoke(app, ["memory", "status", "--json"])
        assert result.exit_code == 0
        parsed = json.loads(result.output)
        assert parsed["initialized"] is False
        assert parsed["rules_count"] == 0

    # 2. Initialized memory status as JSON
    fake_mem = tmp_path / "active_memory"
    (fake_mem / "rules").mkdir(parents=True)
    (fake_mem / "skills" / "my-skill").mkdir(parents=True)
    (fake_mem / "rules" / "rule1.md").write_text("# Rule 1", encoding="utf-8")

    with patch.object(memory, "MEMORY_DIR", fake_mem):
        result = runner.invoke(app, ["memory", "status", "--json"])
        assert result.exit_code == 0
        parsed = json.loads(result.output)
        assert parsed["initialized"] is True
        assert parsed["rules_count"] == 1
        assert parsed["skills_count"] == 1
        assert "rule1.md" in parsed["rules"]
        assert "my-skill" in parsed["skills"]





