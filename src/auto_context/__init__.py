"""auto-context: Autonomous context & instruction manager for AI coding assistants."""
import sys

# Ensure UTF-8 stream handling across all operating systems (guards Windows cp1252 charmap crashes)
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

__version__ = "1.0.6"
