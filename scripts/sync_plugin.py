"""
sync_plugin.py — Canonical Single Source of Truth (SSOT) Synchronizer.

Enforces zero-drift between canonical package templates (src/auto_context/templates)
and the global plugin assets (plugin/).

Usage:
  python scripts/sync_plugin.py          # Synchronize templates -> plugin
  python scripts/sync_plugin.py --check  # Verify templates and plugin match (CI / tests)
"""
import argparse
import filecmp
from pathlib import Path
import shutil
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = REPO_ROOT / "src" / "auto_context" / "templates"
PLUGIN_DIR = REPO_ROOT / "plugin"


def get_sync_pairs() -> list[tuple[Path, Path]]:
    """Return all (source_template, target_plugin_file) pairs for domain rules and skills."""
    pairs = []

    # 1. templates/rules/* -> plugin/rules/*
    rules_tmpl = TEMPLATES_DIR / "rules"
    if rules_tmpl.is_dir():
        for f in rules_tmpl.rglob("*"):
            if f.is_file():
                rel = f.relative_to(rules_tmpl)
                pairs.append((f, PLUGIN_DIR / "rules" / rel))

    # 2. templates/skills/* -> plugin/skills/*
    skills_tmpl = TEMPLATES_DIR / "skills"
    if skills_tmpl.is_dir():
        for f in skills_tmpl.rglob("*"):
            if f.is_file():
                rel = f.relative_to(skills_tmpl)
                pairs.append((f, PLUGIN_DIR / "skills" / rel))

    return pairs


def sync(check_only: bool = False) -> int:
    pairs = get_sync_pairs()
    mismatches = []

    for src, dst in pairs:
        if not src.exists():
            mismatches.append(f"Missing source: {src}")
            continue

        if not dst.exists():
            mismatches.append(f"Missing destination: {dst}")
            if not check_only:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
                print(f"[SYNC] Created: {dst.relative_to(REPO_ROOT)}")
            continue

        if not filecmp.cmp(src, dst, shallow=False):
            mismatches.append(f"Content drift: {src.name} != {dst.relative_to(REPO_ROOT)}")
            if not check_only:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
                print(f"[SYNC] Mirrored: {src.relative_to(REPO_ROOT)} -> {dst.relative_to(REPO_ROOT)}")

    if check_only:
        if mismatches:
            print("[FAIL] SSOT Drift detected between templates/ and plugin/:")
            for m in mismatches:
                print(f"  - {m}")
            print("\nRun 'python scripts/sync_plugin.py' to reconcile automatically.")
            return 1
        print("[PASS] 100% SSOT match between templates/ and plugin/.")
        return 0

    if mismatches:
        print(f"[SUCCESS] Reconciled {len(mismatches)} files. Plugin is in sync with templates.")
    else:
        print("[SUCCESS] All plugin assets are already in sync with templates.")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Synchronize template SSOT into plugin directory")
    parser.add_argument("--check", action="store_true", help="Check for drift without modifying")
    args = parser.parse_args()
    sys.exit(sync(check_only=args.check))
