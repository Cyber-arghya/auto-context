"""
core/exceptions.py — Domain exception hierarchy for auto-context.

Provides structured, domain-specific exception types to eliminate raw sys.exit calls,
unhandled crashes, and unstructured error strings.
"""
from __future__ import annotations

from typing import Any, Optional


class AutoContextError(Exception):
    """Base exception for all auto-context domain errors."""

    def __init__(self, message: str = "An auto-context error occurred."):
        super().__init__(message)
        self.message = message


class SecurityViolationError(AutoContextError):
    """Raised when security audit detects secret patterns, prohibited files, or permissions issues."""

    def __init__(self, violations: list[Any], message: Optional[str] = None):
        self.violations = violations
        count = len(violations)
        msg = message or f"Security audit blocked execution: {count} violation(s) found."
        super().__init__(msg)


class DuplicateRuleError(AutoContextError):
    """Raised when rule guideline or title collides with an existing domain rule."""

    def __init__(self, title: str, domain: str, file_name: str):
        self.title = title
        self.domain = domain
        self.file_name = file_name
        super().__init__(f"Duplicate rule conflict in '{domain}' ({file_name}): '{title}'")


class MemorySyncError(AutoContextError):
    """Raised when git push, pull, status, or init operations fail in Central Memory."""

    def __init__(self, message: str = "Central memory operation failed."):
        super().__init__(message)


class ConfigurationCorruptError(AutoContextError):
    """Raised when mcp_config.json or registry.json contains malformed or unparseable structures."""

    def __init__(self, path: Any, reason: str = "malformed JSON structure"):
        self.path = path
        self.reason = reason
        super().__init__(f"Configuration file corrupted or invalid ({path}): {reason}")


class ItemNotFoundError(AutoContextError):
    """Raised when a rule, skill, or agent cannot be found in workspace or global scope."""

    def __init__(self, name: str, item_type: str = "Item"):
        self.name = name
        self.item_type = item_type
        super().__init__(f"{item_type} '{name}' not found.")


class ResourceConflictError(AutoContextError):
    """Raised when trying to overwrite an existing resource without force flag."""

    def __init__(self, path: Any, resource_type: str = "Resource"):
        self.path = path
        self.resource_type = resource_type
        super().__init__(f"{resource_type} already exists: {path}. Use --force to overwrite.")

