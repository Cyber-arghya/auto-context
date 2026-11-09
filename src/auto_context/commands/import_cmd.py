"""
commands/import_cmd.py — Fetch and install a skill or rule from a Gist or URL.

1. Resolves GitHub Gist HTML URLs to raw content URLs.
2. Downloads content (httpx with urllib fallback).
3. Runs security audit on downloaded content.
4. Detects skill vs rule from frontmatter.
5. Handles file collisions with interactive overwrite / rename / cancel prompt.
"""
from __future__ import annotations

import logging
import re
import tempfile
import time
import urllib.request
from pathlib import Path
from typing import Annotated
from urllib.error import URLError
from urllib.parse import urlparse

import typer
from rich.console import Console

from auto_context import config, security
from auto_context.config import AGENTS_SUBDIR

logger = logging.getLogger(__name__)
console = Console()

# Regex: https://gist.github.com/<user>/<id>
_GIST_HTML_RE = re.compile(r"^https?://gist\.github\.com/([^/]+)/([a-f0-9]+)", re.IGNORECASE)
_GIST_ID_RE = re.compile(r"^[a-f0-9]+$", re.IGNORECASE)
# Frontmatter field matchers
_NAME_RE   = re.compile(r"(?m)^name:\s*[\"']?([a-zA-Z0-9_\-]+)")
_SKILL_RE  = re.compile(r"(?m)^triggers\s*:")


def _resolve_url(url: str) -> str:
    """Convert a Gist HTML URL to its raw content URL, stripping fragments, query params, and trailing slashes."""
    stripped = url.strip()
    try:
        parsed = urlparse(stripped)
        if parsed.netloc.lower() in ("gist.github.com", "www.gist.github.com"):
            parts = [p for p in parsed.path.strip("/").split("/") if p]
            if len(parts) >= 2 and _GIST_ID_RE.match(parts[1]):
                if len(parts) == 2 or (len(parts) >= 3 and parts[2].lower() == "raw"):
                    return f"https://gist.githubusercontent.com/{parts[0]}/{parts[1]}/raw"
    except (ValueError, TypeError) as exc:
        logger.debug("Failed to parse URL %s: %s", url, exc)
    return stripped


def _fetch(url: str) -> str:
    """Download URL content as a string. Tries httpx first, falls back to urllib."""
    try:
        import httpx
        resp = httpx.get(url, follow_redirects=True, timeout=30)
        resp.raise_for_status()
        return resp.text
    except Exception as exc:
        logger.debug("httpx fetch failed for %s, falling back to urllib: %s", url, exc)

    try:
        with urllib.request.urlopen(url, timeout=30) as resp:  # noqa: S310
            return resp.read().decode("utf-8")
    except URLError as exc:
        raise typer.BadParameter(f"Failed to download content from: {url}\n{exc}") from exc


def _detect_type(content: str) -> str:
    """Return 'skill' or 'rule' based on frontmatter inspection."""
    if _SKILL_RE.search(content) or "# Skill:" in content:
        return "skill"
    return "rule"


def _dest_path(clean_name: str, item_type: str, project_dir: Path, global_: bool) -> Path:
    if global_:
        if item_type == "skill":
            return config.GLOBAL_PLUGIN_DIR / "skills" / clean_name / "SKILL.md"
        return config.GLOBAL_PLUGIN_DIR / "rules" / f"{clean_name}.md"
    else:
        if item_type == "skill":
            return project_dir / AGENTS_SUBDIR / "skills" / clean_name / "SKILL.md"
        return project_dir / AGENTS_SUBDIR / "rules" / f"{clean_name}.md"


def import_item(
    url: Annotated[str, typer.Argument(help="Gist URL or raw content URL to import.")],
    target: Annotated[Path | None, typer.Option("--target", "-t")] = None,
    as_name: Annotated[str | None, typer.Option("--as", help="Override imported item name.")] = None,
    global_: Annotated[bool, typer.Option("--global", "-g")] = False,
    force: Annotated[bool, typer.Option("--force", "-f")] = False,
) -> None:
    """Audit and import a skill or rule from a GitHub Gist or URL."""
    project_dir = (target or Path.cwd()).resolve()
    raw_url = _resolve_url(url)

    console.print("\n[bold cyan]📥 Importing External Instruction[/]")
    console.print(f"   [cyan][*] Fetching:[/] {raw_url}")
    content = _fetch(raw_url)

    # Write to a temp file so the security scanner can work on it
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", encoding="utf-8", delete=False
    ) as tmp:
        tmp.write(content)
        tmp_path = Path(tmp.name)

    try:
        console.print("   [cyan][*] Running pre-import security audit...[/]")
        violations = security.audit_path(tmp_path, single_file=True)
        security.abort_if_violations(violations)

        # Detect metadata
        name_match = _NAME_RE.search(content)
        detected_name = name_match.group(1).strip() if name_match else ""
        item_type = _detect_type(content)
        ts_fallback = f"imported-{int(time.time())}"
        final_name = (as_name or detected_name or ts_fallback).lower().replace(" ", "-").replace("_", "-").removesuffix(".md")

        scope = "GLOBAL Plugin" if global_ else "LOCAL Project"
        dest = _dest_path(final_name, item_type, project_dir, global_)

        # Collision guard
        if dest.exists() and not force:
            console.print(f"\n[yellow][!] Collision:[/] '{final_name}' already exists at:\n    {dest}")
            choice = typer.prompt("Action? [O]verwrite / [R]ename / [C]ancel", default="C")

            if choice.strip().upper().startswith("O"):
                console.print("    [yellow]Overwriting...[/]")
            elif choice.strip().upper().startswith("R"):
                new_name = typer.prompt("New name").strip()
                if not new_name:
                    console.print("[red][✗] Name cannot be empty. Import cancelled.[/]")
                    raise typer.Exit(1)
                final_name = new_name.lower().replace(" ", "-").replace("_", "-").removesuffix(".md")
                dest = _dest_path(final_name, item_type, project_dir, global_)
            else:
                console.print("[cyan][*] Import cancelled.[/]\n")
                raise typer.Exit(0)

        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content, encoding="utf-8")

    finally:
        tmp_path.unlink(missing_ok=True)

    console.print("\n[bold green]✨ Imported Successfully![/]")
    console.print(f"   [yellow]Type: [/] {item_type.upper()}")
    console.print(f"   [yellow]Name: [/] {final_name}")
    console.print(f"   [cyan]Scope:[/] {scope}")
    console.print(f"   [green]File: [/] {dest}\n")

