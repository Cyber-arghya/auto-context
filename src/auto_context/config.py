"""
config.py — Global path constants and runtime configuration.

All path logic is centralised here so every other module can import
a single named constant rather than re-computing home directories.
"""
import importlib.resources as _pkg_resources
from pathlib import Path


def get_templates_dir() -> Path:
    """
    Return the templates directory in a way that works both during development
    (uv run / editable install) and after a wheel install (uv tool install .).

    importlib.resources.files() is the PEP 451-compliant way to locate data
    files that are bundled inside a Python package, regardless of whether the
    package is installed as a wheel, a zip, or an editable source tree.
    """
    try:
        # Python 3.9+ path — works in wheel and editable installs
        ref = _pkg_resources.files("auto_context").joinpath("templates")
        # Materialise to a real Path so callers can use glob(), iterdir(), etc.
        with _pkg_resources.as_file(ref) as p:
            return p
    except Exception:
        # Hard fallback: source-tree layout (should never be reached in practice)
        return Path(__file__).parent / "templates"


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

