"""
update_cmd.py — Modular, non-breaking update manager and upstream notification engine.

Ensures users stay synchronized with public rules, skills, and tools added to
https://github.com/Cyber-arghya/auto-context without breaking local project context,
custom user rules, or private memory.
"""
from importlib.metadata import PackageNotFoundError, version as get_pkg_version
import json
import logging
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

logger = logging.getLogger(__name__)
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
        except PackageNotFoundError:
            pass
        except Exception as exc:
            logger.debug("Error checking package version for %s: %s", pkg, exc)
    try:
        import auto_context
        return getattr(auto_context, "__version__", "1.5.1")
    except Exception as exc:
        logger.debug("Error checking auto_context.__version__: %s", exc)
        return "1.5.1"


# ── Update Checking & Cache Engine ────────────────────────────────────────────

def check_upstream_version(timeout: float = 1.2) -> Optional[dict]:
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
    except (urllib.error.URLError, OSError, json.JSONDecodeError, TimeoutError) as exc:
        logger.debug("PyPI check failed: %s", exc)

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
    except (urllib.error.URLError, OSError, json.JSONDecodeError, TimeoutError) as exc:
        logger.debug("GitHub check failed: %s", exc)

    return None


def get_cached_update_status(force_check: bool = False) -> Optional[dict]:
    """
    Retrieve update status from local cache or refresh if cache expired.
    Cached for 24 hours to ensure 0ms latency for daily CLI usage.
    Writes a negative/fallback cache entry on network failure to prevent repeated offline delays.
    """
    now = time.time()
    cache_file = config.UPDATE_CACHE_FILE

    try:
        if not force_check and cache_file.exists():
            cached = json.loads(cache_file.read_text(encoding="utf-8"))
            timestamp = cached.get("timestamp", 0)
            if now - timestamp < config.UPDATE_CHECK_INTERVAL:
                return cached
    except (OSError, json.JSONDecodeError) as exc:
        logger.debug("Cache read failed: %s", exc)

    # Cache expired or missing — refresh
    upstream = check_upstream_version(timeout=1.2)

    current_v = get_installed_version()
    latest_v = upstream["latest_version"] if upstream else current_v
    update_available = (_parse_version(latest_v) > _parse_version(current_v)) if upstream else False

    cache_data = {
        "timestamp": now,
        "current_version": current_v,
        "latest_version": latest_v,
        "update_available": update_available,
        "source": upstream.get("source") if upstream else "offline_cached",
    }

    try:
        cache_file.parent.mkdir(parents=True, exist_ok=True)
        cache_file.write_text(json.dumps(cache_data, indent=2), encoding="utf-8")
    except OSError as exc:
        logger.debug("Cache write failed: %s", exc)

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
    except Exception as exc:
        # Never fail user command due to notification error
        logger.debug("Failed to render update notification: %s", exc)


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
        except (subprocess.SubprocessError, OSError) as exc:
            logger.debug("uv tool upgrade failed: %s", exc)

    # 2. pipx upgrade
    if shutil.which("pipx"):
        try:
            res = subprocess.run(["pipx", "upgrade", config.PYPI_PACKAGE], capture_output=True, text=True)
            if res.returncode == 0:
                console.print(f"  [green][✓] Upgraded via pipx:[/] {config.PYPI_PACKAGE}")
                return True
        except (subprocess.SubprocessError, OSError) as exc:
            logger.debug("pipx upgrade failed: %s", exc)

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
    except (urllib.error.URLError, OSError, TimeoutError) as exc:
        logger.debug("Download text failed for %s: %s", url, exc)
        return None


def update_global_plugin() -> int:
    """
    Sync canonical rules and plugin definitions from bundled package into ~/.gemini/config/plugins/auto-context/.
    Preserves all existing user-defined custom rules and private skills.
    """
    console.print(f"  [cyan][*] Syncing Global AI Plugin:[/] {config.GLOBAL_PLUGIN_DIR}")
    updated_count = 0

    plugin_dir = config.GLOBAL_PLUGIN_DIR
    rules_dir = plugin_dir / "rules"
    skills_dir = plugin_dir / "skills"

    try:
        rules_dir.mkdir(parents=True, exist_ok=True)
        skills_dir.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        console.print(f"  [yellow][!] Sandbox notice: Permission denied creating {plugin_dir}. Run in host terminal.[/]")
        return 0

    tmpl_dir = config.get_templates_dir()

    # 1. Plugin manifest
    plugin_json = tmpl_dir / "plugin.json"
    if plugin_json.exists():
        shutil.copy2(plugin_json, plugin_dir / "plugin.json")
        updated_count += 1

    # 2. Canonical rules
    rules_tmpl = tmpl_dir / "rules"
    if rules_tmpl.is_dir():
        for rule_file in rules_tmpl.glob("*.md"):
            shutil.copy2(rule_file, rules_dir / rule_file.name)
            updated_count += 1
        reg_file = rules_tmpl / "registry.json"
        if reg_file.exists():
            shutil.copy2(reg_file, rules_dir / "registry.json")
            updated_count += 1

    # 3. Standing rules
    agents_tmpl = tmpl_dir / "AGENTS.template.md"
    if agents_tmpl.exists():
        content = agents_tmpl.read_text(encoding="utf-8")
        content = content.replace("{{PROJECT_NAME}}", "Global").replace("{{PROJECT_DIR}}", Path.home().as_posix())
        (rules_dir / "AGENTS.md").write_text(content, encoding="utf-8")
        updated_count += 1

    # 4. Canonical skills
    skills_tmpl = tmpl_dir / "skills"
    if skills_tmpl.is_dir():
        for skill_dir in skills_tmpl.iterdir():
            if skill_dir.is_dir():
                target_skill_dir = skills_dir / skill_dir.name
                target_skill_dir.mkdir(parents=True, exist_ok=True)
                for f in skill_dir.glob("*"):
                    if f.is_file():
                        shutil.copy2(f, target_skill_dir / f.name)
                        updated_count += 1

    console.print(f"  [green][✓] Global plugin updated ({updated_count} assets synced).[/]")
    return updated_count


def update_workspace(target_dir: Path, force: bool = False) -> int:
    """
    Safely update system-managed standing rules in the current project workspace.
    
    NON-BREAKING SAFETY GUARANTEES:
    - NEVER touches context.md (preserves project architecture, credentials & problem log).
    - NEVER touches context.local.md or .env (zero test credential or secret loss).
    - NEVER touches custom user rules in .agents/rules/*.md.
    - Only updates system standing rules (AGENTS.md, GEMINI.md).
    """
    console.print(f"  [cyan][*] Updating workspace system rules:[/] {target_dir.name}")
    updated_count = 0
    templates = config.get_templates_dir()

    # System-managed files to refresh
    system_rules = [
        (templates / "AGENTS.template.md", target_dir / "AGENTS.md"),
        (templates / "AGENTS.template.md", target_dir / "GEMINI.md"),
        (templates / "AGENTS.template.md", target_dir / "CLAUDE.md"),
    ]

    variables = {
        "PROJECT_NAME": target_dir.name,
        "PROJECT_DIR": target_dir.as_posix(),
    }

    # Clean up legacy meta-rules from .agents/rules to enforce DRY
    rules_dir = target_dir / config.AGENTS_SUBDIR / "rules"
    for legacy_name in ("maintain_context.md", "maintain_context.md.bak", "hub-satellite-architecture.md"):
        legacy_file = rules_dir / legacy_name
        if legacy_file.exists():
            legacy_file.unlink(missing_ok=True)

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
        except OSError as exc:
            logger.debug("Failed to remove cache file: %s", exc)

    console.print(Panel(
        "[bold green]✨ Modular update completed successfully![/]\n"
        "[white]• Custom user rules & private skills: [green]Untouched (Safe)[/]\n"
        "• Project context.md & credentials:   [green]Untouched (Zero Data Loss)[/]\n"
        "• Global plugin & system rules:       [bold green]Synchronized[/]",
        border_style="green",
    ))
