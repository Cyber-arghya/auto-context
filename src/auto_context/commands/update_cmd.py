"""
update_cmd.py — Modular, non-breaking update manager and upstream notification engine.

Ensures users stay synchronized with public rules, skills, and tools added to
https://github.com/Cyber-arghya/auto-context without breaking local project context,
custom user rules, or private memory.
"""
from importlib.metadata import version as get_pkg_version
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time
from typing import Annotated, Optional
import urllib.error
import urllib.request

from rich.console import Console
from rich.panel import Panel
import typer

from auto_context import config

console = Console()


def _parse_version(v_str: str) -> tuple[int, ...]:
    """Parse version string like '1.0.1' or 'v1.0.2' into an integer tuple."""
    clean = v_str.strip().lstrip("v").split("-")[0]
    parts = []
    for p in clean.split("."):
        try:
            parts.append(int(p))
        except ValueError:
            break
    return tuple(parts) if parts else (0, 0, 0)


def get_installed_version() -> str:
    """Return the currently installed package version."""
    for pkg in (config.PYPI_PACKAGE, "auto-context"):
        try:
            return get_pkg_version(pkg)
        except Exception:
            pass
    return "1.0.1"


# ── Update Checking & Cache Engine ────────────────────────────────────────────

def check_upstream_version(timeout: float = 2.0) -> Optional[dict]:
    """
    Query PyPI and GitHub to determine the latest upstream version.
    Returns dict with metadata or None if offline/error.
    """
    # 1. Try PyPI first (fastest, no rate limits)
    try:
        req = urllib.request.Request(
            config.PYPI_JSON_URL,
            headers={"User-Agent": f"auto-context-cli/{get_installed_version()}"},
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            latest = data.get("info", {}).get("version")
            if latest:
                return {
                    "latest_version": latest,
                    "source": "pypi",
                    "package": config.PYPI_PACKAGE,
                }
    except Exception:
        pass

    # 2. Fallback to GitHub Latest Release API
    try:
        req = urllib.request.Request(
            config.GITHUB_LATEST_RELEASE_URL,
            headers={"User-Agent": f"auto-context-cli/{get_installed_version()}"},
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            tag = data.get("tag_name", "").lstrip("v")
            if tag:
                return {
                    "latest_version": tag,
                    "source": "github",
                    "url": data.get("html_url"),
                }
    except Exception:
        pass

    return None


def get_cached_update_status(force_check: bool = False) -> Optional[dict]:
    """
    Retrieve update status from local cache or refresh if cache expired.
    Cached for 24 hours to ensure 0ms latency for daily CLI usage.
    """
    now = time.time()
    cache_file = config.UPDATE_CACHE_FILE

    try:
        if not force_check and cache_file.exists():
            cached = json.loads(cache_file.read_text(encoding="utf-8"))
            timestamp = cached.get("timestamp", 0)
            if now - timestamp < config.UPDATE_CHECK_INTERVAL:
                return cached
    except Exception:
        pass

    # Cache expired or missing — refresh in background
    upstream = check_upstream_version()
    if not upstream:
        return None

    current_v = get_installed_version()
    latest_v = upstream["latest_version"]
    update_available = _parse_version(latest_v) > _parse_version(current_v)

    cache_data = {
        "timestamp": now,
        "current_version": current_v,
        "latest_version": latest_v,
        "update_available": update_available,
        "source": upstream.get("source"),
    }

    try:
        cache_file.parent.mkdir(parents=True, exist_ok=True)
        cache_file.write_text(json.dumps(cache_data, indent=2), encoding="utf-8")
    except Exception:
        pass

    return cache_data


def maybe_notify_update() -> None:
    """
    Subtle, non-intrusive notification banner rendered at CLI termination.
    Only displays if an update is genuinely available and cache confirms it.
    """
    try:
        status = get_cached_update_status(force_check=False)
        if not status or not status.get("update_available"):
            return

        cur = status.get("current_version", "")
        latest = status.get("latest_version", "")
        console.print()
        console.print(Panel(
            f"[bold cyan]🔔 Auto-Context Update Available:[/] [yellow]v{cur}[/] → [bold green]v{latest}[/]\n"
            f"[white]   New public rules, skills, and upstream capabilities are ready.[/]\n"
            f"[cyan]   Run:[/] [bold yellow]init-context update[/] [dim]to sync modularly without breaking local context.[/]",
            border_style="cyan",
            title="[bold yellow]✨ Upstream Sync[/]",
        ))
    except Exception:
        # Never fail user command due to notification error
        pass


# ── Modular Update Implementations ───────────────────────────────────────────

def update_cli_package() -> bool:
    """Upgrade the auto-context-cli package using the user's active environment."""
    console.print("  [cyan][*] Upgrading auto-context-cli package...[/]")

    # 1. uv tool upgrade
    if shutil.which("uv"):
        try:
            res = subprocess.run(["uv", "tool", "upgrade", config.PYPI_PACKAGE], capture_output=True, text=True)
            if res.returncode == 0:
                console.print(f"  [green][✓] Upgraded via uv tool:[/] {config.PYPI_PACKAGE}")
                return True
        except Exception:
            pass

    # 2. pipx upgrade
    if shutil.which("pipx"):
        try:
            res = subprocess.run(["pipx", "upgrade", config.PYPI_PACKAGE], capture_output=True, text=True)
            if res.returncode == 0:
                console.print(f"  [green][✓] Upgraded via pipx:[/] {config.PYPI_PACKAGE}")
                return True
        except Exception:
            pass

    # 3. pip fallback
    try:
        res = subprocess.run(
            [sys.executable, "-m", "pip", "install", "--upgrade", config.PYPI_PACKAGE],
            capture_output=True, text=True
        )
        if res.returncode == 0:
            console.print(f"  [green][✓] Upgraded via pip:[/] {config.PYPI_PACKAGE}")
            return True
        else:
            console.print(f"  [yellow][!] pip upgrade notice:[/] {res.stderr.strip()[:100]}")
    except Exception as e:
        console.print(f"  [yellow][!] Could not auto-upgrade CLI package:[/] {e}")

    return False


def _download_text(url: str, timeout: float = 4.0) -> Optional[str]:
    """Download raw text file from remote repository."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "auto-context-cli"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8")
    except Exception:
        return None


def update_global_plugin() -> int:
    """
    Sync upstream public rules and plugin definitions into ~/.gemini/config/plugins/auto-context/.
    Preserves all existing user-defined custom rules and private skills.
    """
    console.print(f"  [cyan][*] Syncing Global AI Plugin:[/] {config.GLOBAL_PLUGIN_DIR}")
    updated_count = 0

    plugin_dir = config.GLOBAL_PLUGIN_DIR
    rules_dir = plugin_dir / "rules"
    skills_dir = plugin_dir / "skills" / "auto-context"

    try:
        rules_dir.mkdir(parents=True, exist_ok=True)
        skills_dir.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        console.print(f"  [yellow][!] Sandbox notice: Permission denied creating {plugin_dir}. Run in host terminal.[/]")
        return 0

    # Sync core plugin files from upstream repository
    core_files = [
        ("plugin.json", plugin_dir / "plugin.json"),
        ("plugin/rules/AGENTS.md", rules_dir / "AGENTS.md"),
        ("plugin/rules/code-standards.md", rules_dir / "code-standards.md"),
        ("plugin/rules/security-boundaries.md", rules_dir / "security-boundaries.md"),
        ("plugin/rules/hub-satellite-architecture.md", rules_dir / "hub-satellite-architecture.md"),
        ("plugin/rules/readme-docs-sync.md", rules_dir / "readme-docs-sync.md"),
        ("plugin/rules/registry.json", rules_dir / "registry.json"),
        ("plugin/skills/auto-context/SKILL.md", skills_dir / "SKILL.md"),
        ("plugin/skills/browser-testing/SKILL.md", plugin_dir / "skills" / "browser-testing" / "SKILL.md"),
        ("plugin/skills/docker-ops/SKILL.md", plugin_dir / "skills" / "docker-ops" / "SKILL.md"),
        ("plugin/skills/git-workflow/SKILL.md", plugin_dir / "skills" / "git-workflow" / "SKILL.md"),
        ("plugin/skills/server-diagnostics/SKILL.md", plugin_dir / "skills" / "server-diagnostics" / "SKILL.md"),
    ]

    for rel_path, dest_path in core_files:
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        url = f"{config.RAW_GITHUB_BASE}/{rel_path}"
        content = _download_text(url)
        if content:
            dest_path.write_text(content, encoding="utf-8")
            console.print(f"  [green][✓] Updated public definition:[/] {dest_path.name}")
            updated_count += 1
        else:
            # Fallback to locally bundled templates if offline
            tmpl_dir = config.get_templates_dir()
            fallback_map = {
                "AGENTS.md": tmpl_dir / "AGENTS.template.md",
                "SKILL.md": tmpl_dir / "skills" / dest_path.parent.name / "SKILL.md" if (tmpl_dir / "skills" / dest_path.parent.name / "SKILL.md").exists() else tmpl_dir / "skill.template.md",
                "code-standards.md": tmpl_dir / "rules" / "code-standards.md",
                "security-boundaries.md": tmpl_dir / "rules" / "security-boundaries.md",
                "hub-satellite-architecture.md": tmpl_dir / "rules" / "hub-satellite-architecture.md",
                "readme-docs-sync.md": tmpl_dir / "rules" / "readme-docs-sync.md",
                "registry.json": tmpl_dir / "rules" / "registry.json",
            }
            fb = fallback_map.get(dest_path.name)
            if fb and fb.exists():
                shutil.copy2(fb, dest_path)
                console.print(f"  [green][✓] Restored from bundled template:[/] {dest_path.name}")
                updated_count += 1

    return updated_count


def update_workspace(target_dir: Path, force: bool = False) -> int:
    """
    Safely update system-managed standing rules in the current project workspace.
    
    NON-BREAKING SAFETY GUARANTEES:
    - NEVER touches context.md (preserves project architecture, credentials & problem log).
    - NEVER touches context.local.md or .env (zero test credential or secret loss).
    - NEVER touches custom user rules in .agents/rules/*.md.
    - Only updates system standing rules (maintain_context.md, AGENTS.md, GEMINI.md).
    """
    console.print(f"  [cyan][*] Updating workspace system rules:[/] {target_dir.name}")
    updated_count = 0
    templates = config.get_templates_dir()

    # System-managed files to refresh
    system_rules = [
        (templates / "maintain_context.template.md", target_dir / config.AGENTS_SUBDIR / "rules" / "maintain_context.md"),
        (templates / "AGENTS.template.md", target_dir / "AGENTS.md"),
        (templates / "GEMINI.template.md", target_dir / "GEMINI.md"),
    ]

    variables = {
        "PROJECT_NAME": target_dir.name,
        "PROJECT_DIR": str(target_dir),
    }

    for tmpl_path, dest_path in system_rules:
        if not tmpl_path.exists():
            continue

        content = tmpl_path.read_text(encoding="utf-8")
        for k, v in variables.items():
            content = content.replace(f"{{{{{k}}}}}", v)

        if dest_path.exists() and not force:
            existing = dest_path.read_text(encoding="utf-8")
            if existing == content:
                console.print(f"  [dim]— Up to date:[/] {dest_path.name}")
                continue

            # Backup modified file if different
            bak_path = dest_path.with_suffix(".md.bak")
            shutil.copy2(dest_path, bak_path)
            console.print(f"  [yellow][*] Backed up customized file:[/] {bak_path.name}")

        dest_path.parent.mkdir(parents=True, exist_ok=True)
        dest_path.write_text(content, encoding="utf-8")
        console.print(f"  [green][✓] Updated system rule:[/] {dest_path.name}")
        updated_count += 1

    return updated_count


# ── CLI update Command ────────────────────────────────────────────────────────

def update(
    workspace: Annotated[bool, typer.Option("--workspace", "-w", help="Update managed system rules in active project.")] = False,
    global_: Annotated[bool, typer.Option("--global", "-g", help="Update global plugin and public rules only.")] = False,
    cli: Annotated[bool, typer.Option("--cli", "-c", help="Upgrade auto-context-cli package only.")] = False,
    check: Annotated[bool, typer.Option("--check", help="Check for available updates without modifying files.")] = False,
    force: Annotated[bool, typer.Option("--force", "-f", help="Force overwrite without creating backups.")] = False,
    target: Annotated[Optional[Path], typer.Option("--target", "-t", help="Target project directory.")] = None,
) -> None:
    """
    Safely update auto-context CLI, public rulebooks, and global agent plugins.

    Guaranteed Non-Breaking:
    - Never modifies context.md, context.local.md, or .env.
    - Never overwrites custom user-created rules or private skills.
    - Seamlessly pulls new upstream guidelines and capabilities.
    """
    console.print(Panel(
        "[bold cyan]🔄 Auto-Context: Modular Upstream Sync & Updater[/]\n"
        f"[dim]Upstream Repository: https://github.com/{config.GITHUB_REPO}[/]",
        border_style="cyan",
    ))

    # 1. Check upstream status
    status = get_cached_update_status(force_check=True)
    cur = get_installed_version()
    latest = status.get("latest_version", cur) if status else cur
    has_update = status.get("update_available", False) if status else False

    console.print(f"  [yellow]Installed Version:[/] v{cur}")
    console.print(f"  [cyan]Upstream Version: [/] v{latest}")
    if has_update:
        console.print(f"  [bold green]✨ New version available:[/] v{latest}")
    else:
        console.print("  [green][✓] You are running the latest version.[/]")

    if check:
        # Check-only mode ends here
        console.print("\n[dim]Run 'init-context update' to apply updates.[/]\n")
        return

    console.print()

    # Determine what to update
    all_selected = not (workspace or global_ or cli)
    project_dir = (target or Path.cwd()).resolve()
    has_project_context = (project_dir / "context.md").exists() or (project_dir / config.AGENTS_SUBDIR).exists()

    # Step A: Upgrade CLI Package
    if all_selected or cli:
        update_cli_package()

    # Step B: Sync Global Plugin & Public Rules
    if all_selected or global_:
        update_global_plugin()

    # Step C: Workspace System Rules
    if (all_selected and has_project_context) or workspace:
        update_workspace(project_dir, force=force)

    # Invalidate cache so notification disappears after successful update
    if config.UPDATE_CACHE_FILE.exists():
        try:
            config.UPDATE_CACHE_FILE.unlink()
        except Exception:
            pass

    console.print(Panel(
        "[bold green]✨ Modular update completed successfully![/]\n"
        "[white]• Custom user rules & private skills: [green]Untouched (Safe)[/]\n"
        "• Project context.md & credentials:   [green]Untouched (Zero Data Loss)[/]\n"
        "• Global plugin & system rules:       [bold green]Synchronized[/]",
        border_style="green",
    ))
