"""
security.py — Zero-bypass secret scanner and key auditor.

Pure-Python port of the PowerShell Test-SecretSafety function.
Uses rich for coloured terminal output instead of raw ANSI codes.

Public API:
    audit_path(path, single_file=False) -> list[Violation]
    print_report(violations)            -> None  (prints via rich)
    abort_if_violations(violations)     -> None  (sys.exit(1) on findings)
"""
from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

from rich.console import Console
from rich.text import Text

console = Console(stderr=True)

# ── Prohibited filenames & extensions ────────────────────────────────────────
PROHIBITED_FILES: frozenset[str] = frozenset({
    ".env", ".env.local", ".env.production", ".env.development",
    ".env.test", ".env.staging", "id_rsa", "id_rsa.pub",
    "id_ed25519", "id_ed25519.pub", "id_ecdsa", "id_ecdsa.pub",
    "id_dsa", "id_dsa.pub", "authorized_keys", "known_hosts",
})

PROHIBITED_EXTENSIONS: frozenset[str] = frozenset({
    ".pem", ".key", ".pkcs12", ".p12", ".pfx", ".kdbx",
})

# ── Secret patterns (name → compiled regex) ──────────────────────────────────
_RAW_PATTERNS: list[tuple[str, str]] = [
    ("GitHub Token",               r"(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9_]{36,}"),
    ("GitHub Fine-grained PAT",    r"github_pat_[A-Za-z0-9_]{50,}"),
    ("Stripe Live Key",            r"sk_live_[0-9a-zA-Z]{24,}"),
    ("OpenAI API Key",             r"sk-[a-zA-Z0-9_\-]{32,}"),
    ("Anthropic API Key",          r"sk-ant-[a-zA-Z0-9_\-]{32,}"),
    ("OpenAI Project Key",         r"sk-proj-[a-zA-Z0-9_\-]{40,}"),
    ("Google API Key",             r"AIza[0-9A-Za-z\-_]{35}"),
    ("AWS Access Key ID",          r"AKIA[0-9A-Z]{16}"),
    ("Private Key Block",          r"-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----"),
    ("Hardcoded Secret/Password",
     r'(?i)(?:password|secret|api[_-]?key|access[_-]?token)\s*[:=]\s*[\'"]'
     r'(?!(?:YOUR_|REPLACE_|MOCK_|TEST_|DUMMY_|\{\{|<))'
     r'[A-Za-z0-9_\-\.\$\!\@\#\%\^\&\*\(\)\+]{8,}[\'"]'),
]

PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    (name, re.compile(pattern)) for name, pattern in _RAW_PATTERNS
]


@dataclass(slots=True)
class Violation:
    """A single security finding."""
    file: Path
    line: int          # 0 = filename-level violation
    pattern: str
    preview: str       # masked token preview


# ── Core scanner ─────────────────────────────────────────────────────────────

def _mask(token: str) -> str:
    """Return a partially-masked token for safe display."""
    if len(token) <= 8:
        return "****"
    return token[:4] + "*" * (len(token) - 8) + token[-4:]


def _scan_file(path: Path) -> list[Violation]:
    """Return violations found in a single file."""
    violations: list[Violation] = []
    name = path.name
    suffix = path.suffix.lower()

    # Filename-level checks
    if name in PROHIBITED_FILES or name.startswith(".env."):
        return [Violation(path, 0, "Prohibited Sensitive File", name)]
    if suffix in PROHIBITED_EXTENSIONS:
        return [Violation(path, 0, "Prohibited Key/Certificate Extension", name)]

    # Content scan (skip binary-looking files gracefully)
    try:
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    except OSError:
        return violations

    for lineno, line in enumerate(lines, start=1):
        for pattern_name, regex in PATTERNS:
            m = regex.search(line)
            if m:
                violations.append(Violation(path, lineno, pattern_name, _mask(m.group())))
                break  # one finding per line is enough

    return violations


def audit_path(path: Path, *, single_file: bool = False) -> list[Violation]:
    """
    Scan *path* for secrets and prohibited files.

    Args:
        path:        File or directory to scan.
        single_file: When True, treat *path* as a single file even if it is
                     a directory (mirrors the original -Mode "File" flag).

    Returns:
        List of Violation objects (empty = clean).
    """
    violations: list[Violation] = []

    if single_file or path.is_file():
        if path.exists():
            violations.extend(_scan_file(path))
    else:
        for child in path.rglob("*"):
            # Skip .git internals
            if ".git" in child.parts:
                continue
            if child.is_file():
                violations.extend(_scan_file(child))

    return violations


# ── Rich reporter ─────────────────────────────────────────────────────────────

def print_report(violations: list[Violation]) -> None:
    """Print a rich-formatted security report to stderr."""
    if not violations:
        console.print("[bold green][✓] Security Audit Passed:[/] 0 sensitive credentials detected.")
        return

    console.print(
        f"\n[bold red][✗] SECURITY AUDIT VIOLATION — {len(violations)} finding(s):[/]"
    )
    for v in violations:
        loc = f"Line {v.line}" if v.line > 0 else "Filename"
        line = Text()
        line.append("   • ", style="yellow")
        line.append(str(v.file), style="cyan")
        line.append(f" [{loc}]: ", style="white")
        line.append(v.pattern, style="bold red")
        line.append(f" (preview: {v.preview})", style="dim")
        console.print(line)


def abort_if_violations(violations: list[Violation]) -> None:
    """Print the report and exit with code 1 if any violations exist."""
    print_report(violations)
    if violations:
        console.print(
            "\n[bold red][✗] ABORT:[/] Remove credentials before committing or sharing.\n"
        )
        sys.exit(1)

