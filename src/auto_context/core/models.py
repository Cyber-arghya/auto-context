"""
core/models.py — Domain entities and data models for auto-context.

Defines type-safe, immutable/validated dataclasses for rules, skills, subagents,
validation reports, and update statuses.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional


@dataclass
class RuleDefinition:
    """Represents a managed domain rule or guideline."""
    name: str
    title: str
    file_name: str
    domain: str
    description: str = ""
    keywords: list[str] = field(default_factory=list)
    content: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "title": self.title,
            "file_name": self.file_name,
            "domain": self.domain,
            "description": self.description,
            "keywords": list(self.keywords),
        }


@dataclass
class SkillDefinition:
    """Represents an operational skill runbook directory."""
    name: str
    path: Path
    triggers: list[str] = field(default_factory=list)
    content: str = ""


@dataclass
class SubagentDefinition:
    """Represents a specialized Antigravity subagent persona."""
    name: str
    role: str
    file_name: str
    path: Optional[Path] = None
    content: str = ""


@dataclass
class ValidationReport:
    """Represents the outcome of a security, lint, or health audit."""
    success: bool
    violations: list[dict[str, Any]] = field(default_factory=list)
    files_scanned: int = 0
    summary: str = ""

    @property
    def has_violations(self) -> bool:
        return len(self.violations) > 0


@dataclass
class UpdateStatus:
    """Represents upstream package update status and caching metadata."""
    needs_update: bool
    local_version: str
    upstream_version: str
    checked_at: str
    is_cached: bool = False

