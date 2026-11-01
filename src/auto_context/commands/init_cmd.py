"""
commands/init_cmd.py — Workspace scaffolding, stack detection,
rule and skill scaffolding commands.

Commands exposed:
    init      — scaffold the current (or target) project directory
    rule      — scaffold a new agent rule file
    skill     — scaffold a new agent skill directory
"""
from __future__ import annotations

import json
import shutil
from datetime import date
from pathlib import Path
from typing import Annotated, Optional

import typer
from rich.console import Console
from rich.panel import Panel

from auto_context import config
from auto_context.config import AGENTS_SUBDIR, GEMINI_SUBDIR, get_templates_dir

import sys

console = Console()

# ── Template variable substitution ────────────────────────────────────────────

def _render(template_path: Path, variables: dict[str, str]) -> str:
    """Read a template file and replace {{KEY}} placeholders."""
    text = template_path.read_text(encoding="utf-8")
    for key, val in variables.items():
        text = text.replace("{{" + key + "}}", val)
    return text


def _write_if_missing(dest: Path, content: str, *, force: bool, dry_run: bool) -> bool:
    """Write *content* to *dest*. Return True if a file was written."""
    if dest.exists() and not force:
        console.print(f"  [yellow][*] Preserved:[/] {dest.relative_to(dest.anchor)} (use --force to overwrite)")
        return False
    if dry_run:
        console.print(f"  [yellow][!] Dry-run:[/] Would write → {dest}")
        return False
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(content, encoding="utf-8")
    console.print(f"  [green][✓] Generated:[/] {dest}")
    return True


def _copy_if_missing(src: Path, dest: Path, *, force: bool, dry_run: bool) -> bool:
    """Copy *src* to *dest*. Return True if a file was written."""
    if dest.exists() and not force:
        console.print(f"  [yellow][*] Preserved:[/] {dest}")
        return False
    if dry_run:
        console.print(f"  [yellow][!] Dry-run:[/] Would copy {src.name} → {dest}")
        return False
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)
    console.print(f"  [green][✓] Copied:[/] {dest}")
    return True


# ── Stack detection ───────────────────────────────────────────────────────────

_JS_FRAMEWORKS = {
    "next": "Next.js", "react": "React", "vue": "Vue.js",
    "express": "Express.js", "fastify": "Fastify", "nest": "NestJS",
}
_PY_FRAMEWORKS = {
    "fastapi": "FastAPI", "flask": "Flask", "django": "Django",
}


def detect_stack(project_dir: Path) -> tuple[str, str]:
    """Return (stack_label, framework_label) for the project directory."""
    for filename, stack, kind in config.STACK_INDICATORS:
        indicator = project_dir / filename
        if not indicator.exists():
            continue

        if kind == "js":
            content = indicator.read_text(encoding="utf-8", errors="ignore").lower()
            fw = next((fw for key, fw in _JS_FRAMEWORKS.items() if key in content), "Not detected")
            return stack, fw

        if kind == "py":
            # Check manage.py for Django first
            if (project_dir / "manage.py").exists():
                return stack, "Django"
            # scan all py indicator files
            combined = ""
            for py_file in ("requirements.txt", "pyproject.toml", "Pipfile"):
                p = project_dir / py_file
                if p.exists():
                    combined += p.read_text(encoding="utf-8", errors="ignore").lower()
            fw = next((fw for key, fw in _PY_FRAMEWORKS.items() if key in combined), "Not detected")
            return stack, fw

        return stack, "Standard"

    # Fallback: check immediate child directories if current folder has no manifest
    try:
        for child in project_dir.iterdir():
            if child.is_dir() and not child.name.startswith((".", "node_modules", "venv", "__pycache__")):
                for filename, stack, kind in config.STACK_INDICATORS:
                    if (child / filename).exists():
                        sub_stack, sub_fw = detect_stack(child)
                        return f"{sub_stack} (in {child.name}/)", sub_fw
    except Exception:
        pass

    return "General / Multi-stack", "Not detected"


# ── .gitignore helper ─────────────────────────────────────────────────────────

def _ensure_gitignore_entries(project_dir: Path, entries: list[str]) -> None:
    """Append *entries* to .gitignore if not already present."""
    gitignore = project_dir / ".gitignore"
    existing = gitignore.read_text(encoding="utf-8") if gitignore.exists() else ""
    missing = [e for e in entries if e not in existing]
    if missing:
        with gitignore.open("a", encoding="utf-8") as fh:
            fh.write("\n# auto-context: protected files\n")
            fh.write("\n".join(missing) + "\n")
        console.print(f"  [green][✓] Updated:[/] .gitignore ({', '.join(missing)})")


# ── init command ──────────────────────────────────────────────────────────────

def init(
    target: Annotated[Optional[Path], typer.Argument(help="Target project directory.")] = None,
    force: Annotated[bool, typer.Option("--force", "-f", help="Overwrite existing files.")] = False,
    dry_run: Annotated[bool, typer.Option("--dry-run", "-d", help="Preview without writing.")] = False,
) -> None:
    """Scaffold autonomous context files into a project directory."""
    project_dir = (target or Path.cwd()).resolve()
    project_name = project_dir.name
    stack, framework = detect_stack(project_dir)
    date_now = date.today().isoformat()
    templates = get_templates_dir()   # importlib.resources-safe path

    console.print(Panel(
        f"[bold cyan]🚀 Auto-Context: Initializing Autonomous Context Manager[/]\n"
        f"[yellow]   Target:[/] {project_name} ({project_dir})\n"
        f"[cyan]   Stack: [/] {stack} ([dim]{framework}[/])",
        border_style="cyan",
    ))

    if dry_run:
        console.print("[yellow][!] Dry-run mode: No files will be written.\n")

    variables = {
        "PROJECT_NAME": project_name,
        "PROJECT_DIR":  str(project_dir),
        "STACK":        stack,
        "FRAMEWORK":    framework,
        "DATE_NOW":     date_now,
    }

    # ── Rules ────────────────────────────────────────────────────────────────
    rules_dest = project_dir / AGENTS_SUBDIR / "rules"
    for rule_file in (templates / "rules").glob("*.md"):
        _copy_if_missing(rule_file, rules_dest / rule_file.name, force=force, dry_run=dry_run)

    maintain_tmpl = templates / "maintain_context.template.md"
    if maintain_tmpl.exists():
        content = _render(maintain_tmpl, variables)
        _write_if_missing(rules_dest / "maintain_context.md", content, force=force, dry_run=dry_run)

    # ── Skills ───────────────────────────────────────────────────────────────
    skills_dest = project_dir / AGENTS_SUBDIR / "skills"
    for skill_dir in (templates / "skills").iterdir():
        if skill_dir.is_dir():
            skill_md = skill_dir / "SKILL.md"
            if skill_md.exists():
                _copy_if_missing(
                    skill_md,
                    skills_dest / skill_dir.name / "SKILL.md",
                    force=force, dry_run=dry_run,
                )

    # ── Root context files ────────────────────────────────────────────────────
    for tmpl_name, dest_name in [
        ("context.template.md",       "context.md"),
        ("context.local.template.md", "context.local.md"),
        ("GEMINI.template.md",        "GEMINI.md"),
        ("AGENTS.template.md",        "AGENTS.md"),
    ]:
        tmpl = templates / tmpl_name
        if tmpl.exists():
            content = _render(tmpl, variables)
            _write_if_missing(project_dir / dest_name, content, force=force, dry_run=dry_run)

    # ── MCP config stub ───────────────────────────────────────────────────────
    mcp_tmpl = templates / "mcp_config.template.json"
    if mcp_tmpl.exists():
        for mcp_dir in [
            project_dir / GEMINI_SUBDIR,
            project_dir / AGENTS_SUBDIR,
        ]:
            _copy_if_missing(
                mcp_tmpl,
                mcp_dir / "mcp_config.json",
                force=force, dry_run=dry_run,
            )

    # ── .gitignore ────────────────────────────────────────────────────────────
    if not dry_run:
        _ensure_gitignore_entries(project_dir, [
            "context.local.md",
            ".env",
            ".env.local",
            ".env.*.local",
        ])

        # ── Stack-Adaptive Satellites (.agents/context/) ───────────────────────
        try:
            from auto_context import scanner
            scanner.generate_satellites(project_dir, force=force)
        except Exception:
            pass

    console.print(Panel(
        "[bold green]✨ Project scaffold complete![/]\n"
        "Edit [cyan]context.md[/] and [cyan]GEMINI.md[/] to customise your AI workspace.",
        border_style="green",
    ))


# ── rule command ──────────────────────────────────────────────────────────────

def new_rule(
    name: Annotated[str, typer.Argument(help="Rule name (e.g. code-standards).")],
    target: Annotated[Optional[Path], typer.Option("--target", "-t")] = None,
    global_: Annotated[bool, typer.Option("--global", "-g", help="Install into global plugin.")] = False,
    force: Annotated[bool, typer.Option("--force", "-f")] = False,
    dry_run: Annotated[bool, typer.Option("--dry-run", "-d")] = False,
) -> None:
    """Scaffold a new agent rule file."""
    clean_name = name.lower().replace(" ", "-").replace("_", "-").removesuffix(".md")
    title = clean_name.replace("-", " ").title()

    dest_dir = (
        config.GLOBAL_PLUGIN_DIR / "rules"
        if global_
        else (target or Path.cwd()).resolve() / AGENTS_SUBDIR / "rules"
    )
    dest_file = dest_dir / f"{clean_name}.md"

    if dest_file.exists() and not force:
        console.print(f"[yellow][!] Rule already exists:[/] {dest_file}\n    Use --force to overwrite.")
        raise typer.Exit(1)

    tmpl = get_templates_dir() / "rule.template.md"
    if tmpl.exists():
        content = _render(tmpl, {"RULE_NAME": clean_name, "RULE_TITLE": title})
    else:
        content = (
            f"---\nname: {clean_name}\ndescription: Guidelines for {title}.\ntrigger: always_on\n---\n\n"
            f"# Rule: {title}\n\n## Objective\n\n## Guidelines & Constraints\n"
        )

    _write_if_missing(dest_file, content, force=force, dry_run=dry_run)
    if global_ and config.MEMORY_DIR.exists():
        mem_dest = config.MEMORY_DIR / "rules" / f"{clean_name}.md"
        _write_if_missing(mem_dest, content, force=force, dry_run=dry_run)
    scope = "GLOBAL Plugin & Central Memory" if global_ else f"LOCAL ({dest_dir})"
    console.print(Panel(
        f"[bold green]✨ New Rule Created![/]\n"
        f"[yellow]   Name:[/]  {clean_name}\n"
        f"[cyan]   Scope:[/] {scope}\n"
        f"[green]   File: [/] {dest_file}",
        border_style="cyan",
    ))


# ── skill command ─────────────────────────────────────────────────────────────

def new_skill(
    name: Annotated[str, typer.Argument(help="Skill name (e.g. deploy-docker).")],
    target: Annotated[Optional[Path], typer.Option("--target", "-t")] = None,
    global_: Annotated[bool, typer.Option("--global", "-g")] = False,
    force: Annotated[bool, typer.Option("--force", "-f")] = False,
    dry_run: Annotated[bool, typer.Option("--dry-run", "-d")] = False,
) -> None:
    """Scaffold a new agent skill directory."""
    clean_name = name.lower().replace(" ", "-").replace("_", "-")
    title = clean_name.replace("-", " ").title()

    dest_dir = (
        config.GLOBAL_PLUGIN_DIR / "skills" / clean_name
        if global_
        else (target or Path.cwd()).resolve() / AGENTS_SUBDIR / "skills" / clean_name
    )
    dest_file = dest_dir / "SKILL.md"

    if dest_file.exists() and not force:
        console.print(f"[yellow][!] Skill already exists:[/] {dest_file}\n    Use --force to overwrite.")
        raise typer.Exit(1)

    tmpl = get_templates_dir() / "skill.template.md"
    if tmpl.exists():
        content = _render(tmpl, {"SKILL_NAME": clean_name, "SKILL_TITLE": title})
    else:
        content = (
            f"---\nname: {clean_name}\nversion: 1.0.0\n"
            f"description: Skill for {title}.\ntriggers: [\"{clean_name}\"]\n---\n\n"
            f"# Skill: {title}\n\n## Overview\n\n## When to Activate\n\n## Workflow\n"
        )

    _write_if_missing(dest_file, content, force=force, dry_run=dry_run)
    if global_ and config.MEMORY_DIR.exists():
        mem_dest = config.MEMORY_DIR / "skills" / clean_name / "SKILL.md"
        _write_if_missing(mem_dest, content, force=force, dry_run=dry_run)
    scope = "GLOBAL Plugin & Central Memory" if global_ else f"LOCAL ({dest_dir})"
    console.print(Panel(
        f"[bold green]🎯 New Skill Created![/]\n"
        f"[yellow]   Name:[/]  {clean_name}\n"
        f"[cyan]   Scope:[/] {scope}\n"
        f"[green]   File: [/] {dest_file}",
        border_style="cyan",
    ))


# ── promote command ───────────────────────────────────────────────────────────

def promote(
    name: Annotated[str, typer.Argument(help="Rule or skill name to promote to Central Memory.")],
    target: Annotated[Optional[Path], typer.Option("--target", "-t")] = None,
) -> None:
    """Promote a local workspace rule or skill to Central Memory and global scope."""
    project_dir = (target or Path.cwd()).resolve()
    clean_name = name.lower().replace(" ", "-").replace("_", "-").removesuffix(".md")

    local_rule = project_dir / AGENTS_SUBDIR / "rules" / f"{clean_name}.md"
    local_skill = project_dir / AGENTS_SUBDIR / "skills" / clean_name / "SKILL.md"

    promoted = False
    if local_rule.exists():
        content = local_rule.read_text(encoding="utf-8")
        (config.GLOBAL_PLUGIN_DIR / "rules").mkdir(parents=True, exist_ok=True)
        (config.GLOBAL_PLUGIN_DIR / "rules" / f"{clean_name}.md").write_text(content, encoding="utf-8")
        if config.MEMORY_DIR.exists():
            (config.MEMORY_DIR / "rules").mkdir(parents=True, exist_ok=True)
            (config.MEMORY_DIR / "rules" / f"{clean_name}.md").write_text(content, encoding="utf-8")
        console.print(f"[bold green][✓] Promoted local rule '{clean_name}' to Global Plugin and Central Memory![/]")
        promoted = True

    if local_skill.exists():
        content = local_skill.read_text(encoding="utf-8")
        (config.GLOBAL_PLUGIN_DIR / "skills" / clean_name).mkdir(parents=True, exist_ok=True)
        (config.GLOBAL_PLUGIN_DIR / "skills" / clean_name / "SKILL.md").write_text(content, encoding="utf-8")
        if config.MEMORY_DIR.exists():
            (config.MEMORY_DIR / "skills" / clean_name).mkdir(parents=True, exist_ok=True)
            (config.MEMORY_DIR / "skills" / clean_name / "SKILL.md").write_text(content, encoding="utf-8")
        console.print(f"[bold green][✓] Promoted local skill '{clean_name}' to Global Plugin and Central Memory![/]")
        promoted = True

    if not promoted:
        console.print(f"[red][✗] Rule or skill '{clean_name}' not found in local workspace ({project_dir}).[/]")
        raise typer.Exit(1)

    console.print("   [cyan]💡 Run 'init-context memory push' to push changes to your private GitHub repo.[/]\n")
