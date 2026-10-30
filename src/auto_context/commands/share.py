"""
commands/share.py — Publish a skill or rule via GitHub Gist.

Primary:  gh gist create (if gh CLI available and authenticated)
Fallback: httpx + GITHUB_TOKEN env var → POST /gists
"""
from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path
from typing import Annotated, Optional

import typer
from rich.console import Console

from auto_context import config, security

console = Console()


def _find_item(name: str, project_dir: Path) -> Optional[Path]:
    """Search local, memory, and global scopes for a named skill or rule."""
    clean = name.lower().replace(" ", "-").replace("_", "-").removesuffix(".md")
    candidates = [
        project_dir / ".agents" / "skills" / clean / "SKILL.md",
        project_dir / ".agents" / "rules" / f"{clean}.md",
        config.MEMORY_DIR / "skills" / clean / "SKILL.md",
        config.MEMORY_DIR / "rules" / f"{clean}.md",
        config.GLOBAL_PLUGIN_DIR / "skills" / clean / "SKILL.md",
        config.GLOBAL_PLUGIN_DIR / "rules" / f"{clean}.md",
    ]
    return next((p for p in candidates if p.exists()), None)


def _gh_gist_create(file_path: Path, public: bool, description: str) -> Optional[str]:
    """Create a Gist via gh CLI. Returns the Gist URL or None on failure."""
    if not shutil.which("gh"):
        return None
    cmd = ["gh", "gist", "create", str(file_path), "--desc", description]
    if public:
        cmd.append("--public")
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        for line in result.stdout.splitlines():
            clean_line = line.strip()
            if "gist.github.com" in clean_line:
                return clean_line
        return result.stdout.strip()
    return None


def _httpx_gist_create(file_path: Path, public: bool, description: str) -> Optional[str]:
    """Fallback: create a Gist via GitHub REST API using GITHUB_TOKEN."""
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        return None
    try:
        import httpx
    except ImportError:
        return None

    content = file_path.read_text(encoding="utf-8")
    payload = {
        "description": description,
        "public": public,
        "files": {file_path.name: {"content": content}},
    }
    resp = httpx.post(
        "https://api.github.com/gists",
        headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"},
        json=payload,
        timeout=30,
    )
    if resp.status_code == 201:
        return resp.json().get("html_url")
    return None


def share(
    name: Annotated[str, typer.Argument(help="Skill or rule name to share.")],
    target: Annotated[Optional[Path], typer.Option("--target", "-t")] = None,
    public: Annotated[bool, typer.Option("--public", help="Publish as public Gist (default: secret).")] = False,
) -> None:
    """Audit and publish a skill or rule via GitHub Gist."""
    project_dir = (target or Path.cwd()).resolve()
    target_file = _find_item(name, project_dir)

    if not target_file:
        console.print(f"[red][✗] Item '{name}' not found in local, memory, or global scopes.[/]")
        raise typer.Exit(1)

    clean_name = name.lower().replace(" ", "-").replace("_", "-").removesuffix(".md")
    console.print(f"\n[bold cyan]📤 Publishing:[/] {clean_name}\n   [dim]{target_file}[/]")

    console.print("  [cyan][*] Running pre-share security audit...[/]")
    violations = security.audit_path(target_file, single_file=True)
    security.abort_if_violations(violations)

    description = f"auto-context: {clean_name}"
    gist_url = _gh_gist_create(target_file, public, description)
    if not gist_url:
        gist_url = _httpx_gist_create(target_file, public, description)

    if not gist_url:
        console.print(
            "[red][✗] Could not publish Gist.[/]\n"
            "    Install [cyan]gh[/] CLI and run [cyan]gh auth login[/], "
            "or set the [cyan]GITHUB_TOKEN[/] environment variable."
        )
        raise typer.Exit(1)

    console.print(f"\n[bold green]✨ Published successfully![/]")
    console.print(f"   [cyan]Gist URL:[/] {gist_url}")
    console.print(f"\n[yellow]💡 Anyone can import this with:[/]")
    console.print(f"   [green]init-context import {gist_url}[/]\n")

