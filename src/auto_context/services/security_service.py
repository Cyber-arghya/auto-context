"""
services/security_service.py — Service layer for secret scanning and security audits.
"""
from __future__ import annotations

from pathlib import Path

from auto_context import security
from auto_context.core.exceptions import SecurityViolationError
from auto_context.core.models import ValidationReport


class SecurityService:
    """Service providing secret scanning, prohibited file detection, and audit reporting."""

    def __init__(self, default_target: Path | None = None):
        self.default_target = (default_target or Path.cwd()).resolve()

    def audit(self, path: Path | None = None, *, single_file: bool = False) -> ValidationReport:
        """
        Audit *path* (or default_target) for security violations.
        Returns a structured ValidationReport.
        """
        target = path or self.default_target
        violations = security.audit_path(target, single_file=single_file)
        
        violation_dicts = [
            {
                "file": str(v.file),
                "line": v.line,
                "pattern": v.pattern,
                "preview": v.preview,
            }
            for v in violations
        ]
        
        success = len(violations) == 0
        summary = (
            f"Audit passed: 0 sensitive credentials detected."
            if success
            else f"Audit failed: {len(violations)} security violation(s) found."
        )

        return ValidationReport(
            success=success,
            violations=violation_dicts,
            files_scanned=1 if single_file else -1,
            summary=summary,
        )

    def audit_and_abort(self, path: Path | None = None, *, single_file: bool = False) -> None:
        """
        Audit *path*. If violations are found, print rich report to stderr
        and raise SecurityViolationError.
        """
        target = path or self.default_target
        violations = security.audit_path(target, single_file=single_file)
        if violations:
            security.print_report(violations)
            raise SecurityViolationError(violations)

