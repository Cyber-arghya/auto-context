"""
commands/memory.py — Central memory brain management.

Wraps git CLI via subprocess.run. Runs security.audit_path()
before every commit or push — zero-bypass hard-block.

Subcommands: init, push, pull, status
"""
from __future__ import annotations

import re
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


def _ensure_global_gitignore(entries: list[str]) -> None:
    """Ensure protected auto-context patterns exist in user's global gitignore."""
    import subprocess
    try:
        res = subprocess.run(
            ["git", "config", "--global", "core.excludesfile"],
            capture_output=True, text=True, check=False,
        )
        global_path_str = res.stdout.strip()
        if not global_path_str:
            global_path = Path.home() / ".gitignore_global"
            subprocess.run(
                ["git", "config", "--global", "core.excludesfile", str(global_path)],
                capture_output=True, text=True, check=False,
            )
        else:
            global_path = Path(global_path_str).expanduser()

        existing = global_path.read_text(encoding="utf-8") if global_path.exists() else ""
        missing = [e for e in entries if e not in existing]
        if missing:
            with global_path.open("a", encoding="utf-8") as fh:
                if "# auto-context: global protected files" not in existing:
                    fh.write("\n# auto-context: global protected files\n")
                fh.write("\n".join(missing) + "\n")
            console.print(f"  [green][✓] Registered Global Git Ignore:[/] {global_path.name} ({', '.join(missing)})")
    except Exception:
        pass


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

    # Local repository exclude (keeps remote test-memory repository clean without committing a .gitignore)
    exclude_file = MEMORY_DIR / ".git" / "info" / "exclude"
    if exclude_file.parent.exists():
        exclude_file.write_text(_GITIGNORE_ENTRIES, encoding="utf-8")

    # Global zero-footprint gitignore registration
    _ensure_global_gitignore(config.ZERO_FOOTPRINT_PATTERNS)

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
                        dest_dir.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copytree(sdir, dest_dir, dirs_exist_ok=True)
                        harvested += 1
                        console.print(f"  [green][✓] Harvested local skill tree to Central Memory:[/] {sdir.name}")
    except OSError:
        pass
    return harvested


# ── push ──────────────────────────────────────────────────────────────────────

@app.command("push")
def memory_push(
    harvest: Annotated[bool, typer.Option("--harvest/--no-harvest", "-h/-n", help="Auto-harvest local workspace rules/skills into central memory.")] = True,
    repo: Annotated[Optional[str], typer.Option("--repo", "-r", help="Specify private GitHub repo name if remote needs creation.")] = None,
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

        # Ensure global zero-footprint gitignore protection across all machine projects
        _ensure_global_gitignore(config.ZERO_FOOTPRINT_PATTERNS)

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
                stderr = result.stderr.strip()
                not_found_signals = (
                    "repository not found",
                    "does not appear to be a git repository",
                    "could not read from remote repository",
                    "fatal: remote error",
                    "404",
                )
                if any(sig in stderr.lower() for sig in not_found_signals):
                    console.print(f"  [yellow][!] Remote repository not found or deleted:[/] {remote}")

                    if _has_gh():
                        console.print("  [cyan]Create a new dedicated private GitHub repository now.[/]")
                        try:
                            chosen_name = repo or typer.prompt(
                                "  [?] Enter private GitHub repository name",
                                default="auto-context-memory",
                            ).strip()
                        except Exception:
                            chosen_name = repo or "auto-context-memory"

                        console.print(f"  [cyan][*] Creating private GitHub repository '{chosen_name}' via gh...[/]")
                        _git(MEMORY_DIR, "remote", "remove", "origin", check=False)
                        gh_res = subprocess.run(
                            ["gh", "repo", "create", chosen_name, "--private", f"--source={MEMORY_DIR}", "--remote=origin", "--push"],
                            capture_output=True, text=True,
                        )
                        if gh_res.returncode == 0:
                            console.print(f"  [green][✓] New private repository '{chosen_name}' created and memory pushed successfully![/]")
                            _write_profile(chosen_name)
                        else:
                            _git(MEMORY_DIR, "remote", "add", "origin", remote, check=False)
                            console.print(f"  [red][✗] Failed to create repo via gh:[/] {gh_res.stderr.strip()}")
                            _print_manual_push(chosen_name)
                    else:
                        console.print("  [yellow][!] GitHub CLI ('gh') not found. Reconnect a new private repository manually:[/]")
                        try:
                            chosen_url = typer.prompt("  [?] Enter new remote Git repository URL (e.g. git@github.com:user/new-repo.git)").strip()
                        except Exception:
                            chosen_url = ""
                        if chosen_url:
                            _git(MEMORY_DIR, "remote", "set-url", "origin", chosen_url, check=False)
                            console.print(f"  [green][✓] Remote updated to:[/] {chosen_url}")
                            _git(MEMORY_DIR, "push", "origin", "main", check=False)
                        else:
                            _print_manual_push("new-repo-name")
                else:
                    console.print(f"  [red][✗] Push failed:[/] {stderr}")
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
            subprocess.run(["git", "clone", repo_url, str(MEMORY_DIR)], check=True, capture_output=True, text=True)
        else:
            _git(MEMORY_DIR, "pull", "origin", "main")

        console.print("  [cyan][*] Running post-pull security audit...[/]")
        violations = security.audit_path(MEMORY_DIR)
        security.abort_if_violations(violations)
        console.print("\n[bold green]✨ Central memory updated successfully![/]\n")

    except subprocess.CalledProcessError as cpe:
        stderr = (cpe.stderr or "").strip() if getattr(cpe, "stderr", None) else str(cpe)
        cmd_str = " ".join(cpe.cmd) if isinstance(cpe.cmd, (list, tuple)) else str(cpe.cmd)
        console.print(Panel(
            f"[bold red][✗] Git Pull Failed[/]\n"
            f"[yellow]   Command:[/] {cmd_str}\n"
            f"[white]   Error:[/] {stderr}\n\n"
            f"[cyan]   Fix:[/] Check network connectivity, git credentials, or resolve conflicts in {MEMORY_DIR}.",
            border_style="red",
        ))
        raise typer.Exit(1)
    except PermissionError as pe:
        console.print(Panel(
            f"[bold red][✗] Permission Denied Accessing Central Memory[/]\n"
            f"[yellow]   Path:[/] {MEMORY_DIR}\n\n"
            f"[white]   Fix:[/] Run in external terminal or enable unsandboxed execution mode.",
            border_style="red",
        ))
        raise typer.Exit(1)
    except OSError as err:
        console.print(f"[red][✗] Central memory error:[/] {err}")
        raise typer.Exit(1)


# ── remote ───────────────────────────────────────────────────────────────────

@app.command("remote")
def memory_remote(
    repo_name_or_url: Annotated[Optional[str], typer.Argument(help="New private repository name or git URL.")] = None,
    create: Annotated[bool, typer.Option("--create/--no-create", "-c/-n", help="Create the repository on GitHub via gh if it does not exist.")] = True,
) -> None:
    """View or switch the remote private GitHub repository for central memory."""
    console.print(Panel(
        "[bold green]🧠 Central Memory Remote Management[/]\n"
        f"[yellow]   Location:[/] {MEMORY_DIR}",
        border_style="cyan",
    ))

    try:
        current_remote = _git(MEMORY_DIR, "remote", "get-url", "origin", check=False).stdout.strip()
        console.print(f"  [cyan]Current Remote:[/] {current_remote or '(none)'}\n")

        target = repo_name_or_url
        if not target:
            target = typer.prompt(
                "  [?] Enter new private repository name (e.g. 'my-agent-brain') or full Git URL",
                default="auto-context-memory",
            ).strip()

        if not target:
            console.print("  [yellow][*] No repository specified. Aborting.[/]")
            return

        if target.startswith(("git@", "https://", "http://")):
            _git(MEMORY_DIR, "remote", "remove", "origin", check=False)
            _git(MEMORY_DIR, "remote", "add", "origin", target, check=False)
            console.print(f"  [green][✓] Updated remote origin to:[/] {target}")
            return

        repo_name = target.replace(".git", "")
        if create and _has_gh():
            console.print(f"  [cyan][*] Creating private GitHub repository '{repo_name}' via gh...[/]")
            _git(MEMORY_DIR, "remote", "remove", "origin", check=False)
            gh_res = subprocess.run(
                ["gh", "repo", "create", repo_name, "--private", f"--source={MEMORY_DIR}", "--remote=origin", "--push"],
                capture_output=True, text=True,
            )
            if gh_res.returncode == 0:
                console.print(f"  [green][✓] Private repository '{repo_name}' created and connected![/]")
                _write_profile(repo_name)
            else:
                console.print(f"  [red][✗] gh repo create error:[/] {gh_res.stderr.strip()}")
                _print_manual_push(repo_name)
        else:
            _git(MEMORY_DIR, "remote", "remove", "origin", check=False)
            console.print(f"  [yellow][!] Set remote URL manually or install gh CLI:[/]")
            _print_manual_push(repo_name)

    except PermissionError:
        console.print(Panel(
            f"[bold red][✗] Permission Denied Accessing Central Memory[/]\n"
            f"[yellow]   Path:[/] {MEMORY_DIR}\n\n"
            f"[white]   Fix:[/] Run in external host terminal (PowerShell / Bash).",
            border_style="red",
        ))
        raise typer.Exit(1)


# ── reset ────────────────────────────────────────────────────────────────────

@app.command("reset")
def memory_reset(
    force: Annotated[bool, typer.Option("--force", "-f", help="Force reset without confirmation prompt.")] = False,
    harvest: Annotated[bool, typer.Option("--harvest/--no-harvest", "-h/-n", help="Auto-harvest local workspace rules/skills after reset.")] = True,
) -> None:
    """Reset and re-initialize local central memory brain cache."""
    console.print(Panel(
        "[bold yellow]⚠️ Resetting Central Memory Brain[/]\n"
        f"[yellow]   Location:[/] {MEMORY_DIR}",
        border_style="yellow",
    ))

    try:
        if not force:
            confirmed = typer.confirm(
                "Are you sure you want to reset the local central memory cache? (Remote repository will remain untouched)",
                default=False,
            )
            if not confirmed:
                console.print("  [yellow][*] Reset aborted by user.[/]")
                return

        existing_remote = ""
        if (MEMORY_DIR / ".git").exists():
            res = _git(MEMORY_DIR, "remote", "get-url", "origin", check=False)
            if res.returncode == 0:
                existing_remote = res.stdout.strip()

        if MEMORY_DIR.exists():
            for item in MEMORY_DIR.iterdir():
                if item.is_dir():
                    shutil.rmtree(item, ignore_errors=True)
                else:
                    item.unlink(missing_ok=True)
        else:
            MEMORY_DIR.mkdir(parents=True, exist_ok=True)

        (MEMORY_DIR / "rules").mkdir(parents=True, exist_ok=True)
        (MEMORY_DIR / "skills").mkdir(parents=True, exist_ok=True)

        _git(MEMORY_DIR, "init")
        _git(MEMORY_DIR, "branch", "-M", "main", check=False)

        exclude_file = MEMORY_DIR / ".git" / "info" / "exclude"
        if exclude_file.parent.exists():
            exclude_file.write_text(_GITIGNORE_ENTRIES, encoding="utf-8")
        _ensure_global_gitignore(config.ZERO_FOOTPRINT_PATTERNS)

        repo_label = existing_remote.split("/")[-1].replace(".git", "") if existing_remote else "auto-context-memory"
        _write_profile(repo_label)

        if existing_remote:
            _git(MEMORY_DIR, "remote", "add", "origin", existing_remote, check=False)
            console.print(f"  [green][✓] Restored Remote Origin:[/] {existing_remote}")

        if harvest:
            harvested = _sync_local_to_memory(Path.cwd().resolve())
            if harvested:
                console.print(f"  [green][✓] Re-harvested {harvested} rules/skills from current workspace[/]")

        _git(MEMORY_DIR, "add", "-A", check=False)
        _git(MEMORY_DIR, "commit", "-m", f"{config.GIT_COMMIT_INIT} [reset]", check=False)

        console.print("\n[bold green]✨ Central memory reset completed successfully![/]\n")

    except PermissionError:
        console.print(Panel(
            f"[bold red][✗] Permission Denied Accessing Central Memory[/]\n"
            f"[yellow]   Path:[/] {MEMORY_DIR}\n\n"
            f"[white]   Cause:[/] Sandboxed IDE terminal lacks access to host directory ~/.auto-context.\n"
            f"[cyan]   Fix:[/] Run 'init-context memory reset' in your host terminal (PowerShell / Bash), or grant filesystem access.",
            border_style="red",
        ))
        raise typer.Exit(1)
    except OSError as err:
        console.print(f"[red][✗] Central memory reset error:[/] {err}")
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

