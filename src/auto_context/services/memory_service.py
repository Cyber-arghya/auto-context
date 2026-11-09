"""
services/memory_service.py — Service layer for Central Memory brain synchronization.
"""
from __future__ import annotations

import re
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from auto_context import config, security
from auto_context.core.exceptions import MemorySyncError, SecurityViolationError


class MemoryService:
    """Service orchestrating Central Memory git synchronization and asset harvesting."""

    def __init__(self, memory_dir: Optional[Path] = None):
        self.memory_dir = memory_dir or config.MEMORY_DIR

    def _git(self, *args: str, check: bool = True) -> subprocess.CompletedProcess:
        """Execute a git command inside the central memory repository."""
        try:
            return subprocess.run(
                ["git", "-C", str(self.memory_dir), *args],
                capture_output=True,
                text=True,
                check=check,
            )
        except subprocess.CalledProcessError as err:
            raise MemorySyncError(f"Git command failed: git {' '.join(args)}\n{err.stderr or err.stdout}") from err

    def is_initialized(self) -> bool:
        """Check if central memory repository is initialized."""
        return (self.memory_dir / ".git").is_dir()

    def audit_memory(self) -> None:
        """Run zero-bypass security audit on memory directory before sync."""
        violations = security.audit_path(self.memory_dir)
        if violations:
            security.print_report(violations)
            raise SecurityViolationError(violations)

    def harvest_from_workspace(self, workspace_dir: Path) -> int:
        """Harvest rules, skills, and agents from workspace into central memory."""
        if not self.is_initialized():
            raise MemorySyncError("Central memory not initialized. Run 'init-context memory init' first.")

        agents_dir = workspace_dir / config.AGENTS_SUBDIR
        harvested = 0

        # 1. Rules
        rules_src = agents_dir / "rules"
        if rules_src.is_dir():
            dest = self.memory_dir / "rules"
            dest.mkdir(parents=True, exist_ok=True)
            for f in rules_src.glob("*.md"):
                shutil.copy2(f, dest / f.name)
                harvested += 1

        # 2. Skills
        skills_src = agents_dir / "skills"
        if skills_src.is_dir():
            dest = self.memory_dir / "skills"
            dest.mkdir(parents=True, exist_ok=True)
            for d in skills_src.iterdir():
                if d.is_dir():
                    shutil.copytree(d, dest / d.name, dirs_exist_ok=True)
                    harvested += 1

        # 3. Agents
        agents_src = agents_dir / "agents"
        if agents_src.is_dir():
            dest = self.memory_dir / "agents"
            dest.mkdir(parents=True, exist_ok=True)
            for f in agents_src.glob("*.md"):
                shutil.copy2(f, dest / f.name)
                harvested += 1

        return harvested

    def commit_and_push(self, message: str) -> None:
        """Stage, commit, and push memory assets to remote repository."""
        self.audit_memory()
        self._git("add", "-A")
        
        status = self._git("status", "--porcelain", check=False)
        if not status.stdout.strip():
            return  # Nothing to commit

        self._git("commit", "-m", message)
        self._git("push", "-u", "origin", "main", check=False)

    def pull(self) -> str:
        """Pull latest changes from remote repository."""
        if not self.is_initialized():
            raise MemorySyncError("Central memory not initialized.")
        res = self._git("pull", "--rebase", check=False)
        return res.stdout

