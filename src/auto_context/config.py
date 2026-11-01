"""
config.py — Global path constants and runtime configuration.

All path logic is centralised here so every other module can import
a single named constant rather than re-computing home directories.
"""
import importlib.resources as _pkg_resources
from pathlib import Path


def get_templates_dir() -> Path:
    """
    Return the templates directory in a crash-proof, persistent way
    that works during development, wheel installs, and virtual environments.
    """
    pkg_tmpl = Path(__file__).parent / "templates"
    if pkg_tmpl.is_dir():
        return pkg_tmpl

    try:
        ref = _pkg_resources.files("auto_context").joinpath("templates")
        if isinstance(ref, Path) and ref.is_dir():
            return ref
    except Exception:
        pass

    return pkg_tmpl


# ── User home-relative roots ───────────────────────────────────────────────────
HOME = Path.home()

# Central memory brain (~/.auto-context/memory)
MEMORY_DIR: Path = HOME / ".auto-context" / "memory"

# Global plugin scope consumed by Antigravity / Gemini CLI
GLOBAL_PLUGIN_DIR: Path = HOME / ".gemini" / "config" / "plugins" / "auto-context"
GLOBAL_GEMINI_DIR: Path = HOME / ".gemini" / "config"

# Subdirectory conventions (relative to any project or plugin root)
RULES_SUBDIR = "rules"
SKILLS_SUBDIR = "skills"
AGENTS_SUBDIR = ".agents"
GEMINI_SUBDIR = ".gemini"

# ── Stack detection: indicator files → (stack_label, framework_hint_key) ──────
STACK_INDICATORS: list[tuple[str, str, str]] = [
    # (filename, stack_label, framework_key_for_content_scan)
    ("package.json", "Node.js / JavaScript / TypeScript", "js"),
    ("pyproject.toml", "Python", "py"),
    ("requirements.txt", "Python", "py"),
    ("Pipfile", "Python", "py"),
    ("go.mod", "Go (Golang)", "go"),
    ("Cargo.toml", "Rust", "rust"),
    ("pom.xml", "Java / Kotlin", "jvm"),
    ("build.gradle", "Java / Kotlin", "jvm"),
    ("docker-compose.yml", "Dockerized Container", "docker"),
    ("Dockerfile", "Dockerized Container", "docker"),
]

# ── Git commit message templates ───────────────────────────────────────────────
GIT_COMMIT_INIT = "feat(memory): initialize central agent brain knowledge base"
GIT_COMMIT_SYNC = "chore(memory): sync agent brain knowledge base"

# ── Update & Upstream Configuration ──────────────────────────────────────────
GITHUB_REPO = "Cyber-arghya/auto-context"
PYPI_PACKAGE = "auto-context-cli"
RAW_GITHUB_BASE = "https://raw.githubusercontent.com/Cyber-arghya/auto-context/main"
PYPI_JSON_URL = f"https://pypi.org/pypi/{PYPI_PACKAGE}/json"
GITHUB_LATEST_RELEASE_URL = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"

import tempfile

def get_cache_dir() -> Path:
    """Return user cache directory, falling back to tempdir if permission restricted."""
    try:
        p = HOME / ".auto-context" / "cache"
        p.mkdir(parents=True, exist_ok=True)
        return p
    except Exception:
        p = Path(tempfile.gettempdir()) / "auto-context-cache"
        try:
            p.mkdir(parents=True, exist_ok=True)
        except Exception:
            pass
        return p

CACHE_DIR: Path = get_cache_dir()
UPDATE_CACHE_FILE: Path = CACHE_DIR / "update_check.json"
UPDATE_CHECK_INTERVAL: int = 86400  # 24 hours in seconds


