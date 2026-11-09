"""
auto_context.core — Core models, domain entities, and exceptions.
"""
from __future__ import annotations

from auto_context.core.exceptions import (
    AutoContextError,
    ConfigurationCorruptError,
    DuplicateRuleError,
    ItemNotFoundError,
    MemorySyncError,
    ResourceConflictError,
    SecurityViolationError,
)
from auto_context.core.models import (
    RuleDefinition,
    SkillDefinition,
    SubagentDefinition,
    UpdateStatus,
    ValidationReport,
)

__all__ = [
    "AutoContextError",
    "ConfigurationCorruptError",
    "DuplicateRuleError",
    "ItemNotFoundError",
    "MemorySyncError",
    "ResourceConflictError",
    "SecurityViolationError",
    "RuleDefinition",
    "SkillDefinition",
    "SubagentDefinition",
    "UpdateStatus",
    "ValidationReport",
]

