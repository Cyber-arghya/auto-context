"""
commands/memory.py — Central memory brain management.

Wraps git CLI via subprocess.run. Runs security.audit_path()
before every commit or push — zero-bypass hard-block.

Subcommands: init, push, pull, status
"""
from __future__ import annotations

import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Annotated, Optional

import typer
from rich.console import Console
from rich.panel import Panel

from auto_context import config, security

app = typer.Typer(help="Central memory brain management.")
console = Console()

MEMORY_DIR = config.MEMORY_DIR

_GITIGNORE_ENTRIES = """\
# Security: Prohibit credentials and environment files from central memory
.env
.env.*
*.local.md
context.local.md
*.key
*.pem
*.p12
*.pfx
*.kdbx
id_rsa*
id_ed25519*
id_ecdsa*
id_dsa*
authorized_keys
known_hosts
"""


def _git(cwd: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    """Run a git command in *cwd*, capturing output."""
    return subprocess.run(
        ["git", "-C", str(cwd), *args],
        capture_output=True,
        text=True,
        check=check,
    )


def _has_gh() -> bool:
    return shutil.which("gh") is not None


# ── init ──────────────────────────────────────────────────────────────────────

@app.command("init")
def memory_init(
    repo_name: Annotated[str, typer.Argument(help="GitHub repo name.")] = "auto-context-memory",
) -> None:
    """Initialize a private central memory brain repository."""
    console.print(Panel(
        f"[bold green]🧠 Initializing Private Central Memory Brain[/]\n"
        f"[yellow]   Directory:[/] {MEMORY_DIR}\n"
        f"[cyan]   Repo:     [/] {repo_name} (Strictly Private)",
        border_style="cyan",
    ))

    (MEMORY_DIR / "rules").mkdir(parents=True, exist_ok=True)
    (MEMORY_DIR / "skills").mkdir(parents=True, exist_ok=True)

    # Init git repo
    if not (MEMORY_DIR / ".git").exists():
        _git(MEMORY_DIR, "init")
        console.print("  [green][✓] Initialized Git repository[/]")

    # Hardened .gitignore
    (MEMORY_DIR / ".gitignore").write_text(_GITIGNORE_ENTRIES, encoding="utf-8")
    console.print("  [green][✓] Hardened .gitignore written[/]")

    # profile.md
    _write_profile(repo_name)

    # Security audit before first commit
    console.print("  [cyan][*] Running pre-commit security audit...[/]")
    violations = security.audit_path(MEMORY_DIR)
    security.abort_if_violations(violations)

    _git(MEMORY_DIR, "add", "-A", check=False)
    _git(MEMORY_DIR, "commit", "-m", config.GIT_COMMIT_INIT, check=False)
    _git(MEMORY_DIR, "branch", "-M", "main", check=False)

    if _has_gh():
        console.print("  [cyan][*] Creating strictly private GitHub repository via gh...[/]")
        result = subprocess.run(
            ["gh", "repo", "create", repo_name,
             "--private", f"--source={MEMORY_DIR}", "--remote=origin", "--push"],
            capture_output=True, text=True,
        )
        if result.returncode == 0:
            console.print("  [green][✓] Private GitHub memory repository created and pushed![/]")
        else:
            _print_manual_push(repo_name)
    else:
        console.print("  [yellow][!] GitHub CLI ('gh') not found. Install it or connect manually:[/]")
        _print_manual_push(repo_name)

    console.print(f"\n[bold green]🎉 Central Memory Initialized![/]")
    console.print(f"   [yellow]Local Brain:[/]  {MEMORY_DIR}")
    console.print(f"   [green]Sync Command:[/] init-context memory push\n")


def _print_manual_push(repo_name: str) -> None:
    console.print(f"   [dim]git -C \"{MEMORY_DIR}\" remote add origin git@github.com:<username>/{repo_name}.git[/]")
    console.print(f"   [dim]git -C \"{MEMORY_DIR}\" push -u origin main[/]")


def _write_profile(repo_name: str) -> None:
    profile = MEMORY_DIR / "profile.md"
    if profile.exists():
        return
    import getpass
    username = getpass.getuser()
    date_now = datetime.now().strftime("%Y-%m-%d")
    profile.write_text(
        f"# Agent Memory & Developer Profile\n\n"
        f"> **Owner:** {username}  \n"
        f"> **Initialized:** {date_now}  \n"
        f"> **Repository:** {repo_name}  \n"
        f"> **Visibility:** Private Central Agent Brain  \n\n---\n\n"
        f"## 1. Developer Preferences\n- Edit this file to personalise agent behaviour.\n\n"
        f"## 2. Central Knowledge Base Index\n"
        f"- **Global Rules:** `rules/`\n"
        f"- **Reusable Skills:** `skills/`\n",
        encoding="utf-8",
    )
    console.print("  [green][✓] Generated Developer Profile: profile.md[/]")


# ── local harvester ─────────────────────────────────────────────────────────

LOCAL_SYSTEM_RULES: frozenset[str] = frozenset({
    "maintain_context.md",
    "AGENTS.md",
    "GEMINI.md",
    "context.local.md",
})


def _sync_local_to_memory(project_dir: Path) -> int:
    """Harvest newly created local project rules & skills into central memory."""
    harvested = 0
    try:
        local_rules = project_dir / config.AGENTS_SUBDIR / "rules"
        if local_rules.exists():
            (MEMORY_DIR / "rules").mkdir(parents=True, exist_ok=True)
            for rfile in local_rules.glob("*.md"):
                # Exclude project-specific local instructions from polluting central memory
                if rfile.name in LOCAL_SYSTEM_RULES or rfile.name.endswith(".local.md"):
                    continue

                dest = MEMORY_DIR / "rules" / rfile.name
                if not dest.exists():
                    shutil.copy2(rfile, dest)
                    harvested += 1
                    console.print(f"  [green][✓] Harvested local rule to Central Memory:[/] {rfile.name}")
                elif rfile.stat().st_mtime > dest.stat().st_mtime:
                    shutil.copy2(rfile, dest)
                    harvested += 1
                    console.print(f"  [green][✓] Updated local rule in Central Memory:[/] {rfile.name}")

        local_skills = project_dir / config.AGENTS_SUBDIR / "skills"
        if local_skills.exists():
            (MEMORY_DIR / "skills").mkdir(parents=True, exist_ok=True)
            for sdir in local_skills.iterdir():
                if sdir.is_dir() and (sdir / "SKILL.md").exists():
                    dest_dir = MEMORY_DIR / "skills" / sdir.name
                    dest_file = dest_dir / "SKILL.md"
                    src_file = sdir / "SKILL.md"
                    if not dest_file.exists() or src_file.stat().st_mtime > dest_file.stat().st_mtime:
                        dest_dir.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(src_file, dest_file)
                        harvested += 1
                        console.print(f"  [green][✓] Harvested local skill to Central Memory:[/] {sdir.name}")
    except OSError:
        pass
    return harvested


# ── push ──────────────────────────────────────────────────────────────────────

@app.command("push")
def memory_push(
    harvest: Annotated[bool, typer.Option("--harvest/--no-harvest", "-h/-n", help="Auto-harvest local workspace rules/skills into central memory.")] = True,
) -> None:
    """Audit secrets and push memory brain to private GitHub repo."""
    console.print(Panel(
        "[bold green]🧠 Synchronizing Central Memory Brain[/]\n"
        f"[yellow]   Location:[/] {MEMORY_DIR}",
        border_style="cyan",
    ))

    try:
        if not MEMORY_DIR.exists():
            console.print(f"[red][✗] Memory directory not found:[/] {MEMORY_DIR}")
            console.print("    Run: [cyan]init-context memory init[/]")
            raise typer.Exit(1)

        # Harvest local rules/skills if in a project directory
        if harvest:
            _sync_local_to_memory(Path.cwd().resolve())

        console.print("  [cyan][*] Running Zero-Bypass Security Auditor...[/]")
        violations = security.audit_path(MEMORY_DIR)
        security.abort_if_violations(violations)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        _git(MEMORY_DIR, "add", "-A", check=False)
        _git(MEMORY_DIR, "commit", "-m", f"{config.GIT_COMMIT_SYNC} [{timestamp}]", check=False)

        remote = _git(MEMORY_DIR, "remote", "get-url", "origin", check=False).stdout.strip()
        if remote:
            console.print("  [cyan][*] Pushing to private remote repository...[/]")
            result = _git(MEMORY_DIR, "push", "origin", "main", check=False)
            if result.returncode == 0:
                console.print("  [green][✓] Memory brain pushed successfully![/]")
            else:
                console.print(f"  [red][✗] Push failed:[/] {result.stderr.strip()}")
        else:
            console.print("  [yellow][!] No remote 'origin' configured. Run memory init first.[/]")

        console.print("\n[bold green]✨ Memory synchronization complete![/]\n")

    except PermissionError as pe:
        console.print(Panel(
            f"[bold red][✗] Permission Denied Accessing Central Memory[/]\n"
            f"[yellow]   Path:[/] {MEMORY_DIR}\n\n"
            f"[white]   Cause:[/] Running inside a restricted sandbox without host filesystem access.\n"
            f"[cyan]   Fix:[/] Run this command in your external terminal (PowerShell / Bash), or enable unsandboxed mode.",
            border_style="red",
        ))
        raise typer.Exit(1)
    except OSError as err:
        console.print(f"[red][✗] Central memory error:[/] {err}")
        raise typer.Exit(1)


# ── pull ──────────────────────────────────────────────────────────────────────

@app.command("pull")
def memory_pull(
    repo_url: Annotated[Optional[str], typer.Argument(help="Remote repo URL (required for first pull).")] = None,
) -> None:
    """Pull and sync the central memory brain from remote."""
    console.print(Panel(
        "[bold green]🧠 Pulling Central Memory Brain[/]",
        border_style="cyan",
    ))

    try:
        if not MEMORY_DIR.exists():
            if not repo_url:
                console.print("[red][✗] Memory directory not found. Provide a repo URL:[/]")
                console.print("    [cyan]init-context memory pull <url>[/]")
                raise typer.Exit(1)
            subprocess.run(["git", "clone", repo_url, str(MEMORY_DIR)], check=True)
        else:
            _git(MEMORY_DIR, "pull", "origin", "main")

        console.print("  [cyan][*] Running post-pull security audit...[/]")
        violations = security.audit_path(MEMORY_DIR)
        security.abort_if_violations(violations)
        console.print("\n[bold green]✨ Central memory updated successfully![/]\n")

    except PermissionError as pe:
        console.print(Panel(
            f"[bold red][✗] Permission Denied Accessing Central Memory[/]\n"
            f"[yellow]   Path:[/] {MEMORY_DIR}\n\n"
            f"[white]   Fix:[/] Run in external terminal or enable unsandboxed execution mode.",
            border_style="red",
        ))
        raise typer.Exit(1)


# ── status ────────────────────────────────────────────────────────────────────

@app.command("status")
def memory_status() -> None:
    """Show status of the central memory brain."""
    console.print(Panel(
        "[bold green]🧠 Central Memory Status[/]",
        border_style="cyan",
    ))

    try:
        if not MEMORY_DIR.exists():
            console.print("  [yellow][!] Central memory not initialized.[/]")
            console.print("      Run: [cyan]init-context memory init[/]")
            return

        remote = _git(MEMORY_DIR, "remote", "get-url", "origin", check=False).stdout.strip()
        rules_path = MEMORY_DIR / "rules"
        skills_path = MEMORY_DIR / "skills"

        rules_count = len(list(rules_path.glob("*.md"))) if rules_path.exists() else 0
        skills_count = len([d for d in skills_path.iterdir() if d.is_dir()]) if skills_path.exists() else 0

        console.print(f"  [yellow]Location:[/] {MEMORY_DIR}")
        console.print(f"  [cyan]Remote:  [/] {remote or '(none)'}")
        console.print(f"  [green]Rules:   [/] {rules_count} registered")
        console.print(f"  [green]Skills:  [/] {skills_count} registered")
        console.print()

    except PermissionError:
        console.print(Panel(
            f"[bold red][✗] Permission Denied Accessing Central Memory[/]\n"
            f"[yellow]   Path:[/] {MEMORY_DIR}\n\n"
            f"[white]   Cause:[/] Sandboxed IDE terminal lacks access to host directory ~/.auto-context.\n"
            f"[cyan]   Fix:[/] Run 'init-context memory status' in your host terminal (PowerShell / Bash), or grant filesystem access.",
            border_style="red",
        ))
    except OSError as err:
        console.print(f"  [yellow][!] Central memory status warning:[/] {err}")

