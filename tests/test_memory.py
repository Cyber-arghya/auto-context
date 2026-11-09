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



