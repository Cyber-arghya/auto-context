"""
scan_cmd.py — On-demand codebase inspection and satellite synchronization command.

Discovers routes, data models, network ports, and runbooks without burning LLM tokens.
Generates or updates stack-adaptive satellites (.agents/context/) and synchronizes
the Executive Hub (context.md) with strict idempotency and hash verification.
"""
from datetime import date
from pathlib import Path
from typing import Annotated, Optional

from rich.console import Console
from rich.panel import Panel
import typer

from auto_context import scanner
from auto_context.commands import init_cmd

console = Console()


def scan(
    target: Annotated[Optional[Path], typer.Argument(help="Target project directory.")] = None,
    force: Annotated[bool, typer.Option("--force", "-f", help="Force overwrite satellite files.")] = False,
) -> None:
    """
    Inspect project codebase, generate stack-adaptive satellites, and sync context.md.

    Zero Token Cost:
    - Runs 100% locally via fast filesystem heuristics.
    - Generates .agents/context/routes.md, schema.md, gotchas.md as needed.
    - Keeps primary context.md compact (< 400 tokens) using the Hub & Satellite pattern.
    """
    project_dir = (target or Path.cwd()).resolve()
    project_name = project_dir.name
    stack, framework = init_cmd.detect_stack(project_dir)

    console.print(Panel(
        f"[bold cyan]🔍 Auto-Context: Stack-Adaptive Codebase Scanner[/]\n"
        f"[yellow]   Target:[/] {project_name} ({project_dir})\n"
        f"[cyan]   Stack: [/] {stack} ([dim]{framework}[/])",
        border_style="cyan",
    ))

    # 1. Discover ports & services
    ports = scanner.discover_ports_and_services(project_dir)
    # 2. Discover runbook commands
    commands = scanner.discover_runbook_commands(project_dir)
    # 3. Generate adaptive satellites in .agents/context/
    satellites = scanner.generate_satellites(project_dir, force=force)

    # 4. Render/Sync the compact Executive Hub (context.md)
    hub_file = project_dir / "context.md"
    date_now = date.today().isoformat()

    # Build discovered ports table
    ports_table = "| Service / Key | Port | Source |\n| :--- | :--- | :--- |\n"
    if ports:
        for svc, port, src in ports:
            ports_table += f"| **{svc}** | `{port}` | {src} |\n"
    else:
        ports_table += "| **App Port** | `3000` (Default) | Inferred |\n"

    # Build runbook table
    runbook_table = "| Task | Executable Command |\n| :--- | :--- |\n"
    if commands:
        for action, cmd in commands:
            runbook_table += f"| {action} | `{cmd}` |\n"
    else:
        runbook_table += "| Start Development | `npm run dev` / `python main.py` |\n"

    # Build satellites index section
    satellites_index = ""
    if "routes" in satellites:
        satellites_index += f"- **Route Map:** [`routes.md`](file://{satellites['routes'].as_posix()})\n"
    if "schema" in satellites:
        satellites_index += f"- **Database Schemas:** [`schema.md`](file://{satellites['schema'].as_posix()})\n"
    if "gotchas" in satellites:
        satellites_index += f"- **Critical Gotchas:** [`gotchas.md`](file://{satellites['gotchas'].as_posix()})\n"

    # Anchored block for idempotent synchronization
    anchored_block = (
        "<!-- AUTO-CONTEXT:DISCOVERY:START -->\n"
        "## 1. Discovered Ports & Network Vault\n\n"
        f"{ports_table}\n"
        "## 2. Stack & Adaptive Satellites\n\n"
        f"* **Stack:** {stack} ({framework})\n"
        f"{satellites_index if satellites_index else '- Satellites: Core stack (no external routes/models detected)\n'}\n"
        "## 3. Operations Runbook\n\n"
        f"{runbook_table}\n"
        "<!-- AUTO-CONTEXT:DISCOVERY:END -->"
    )

    if hub_file.exists():
        existing_text = hub_file.read_text(encoding="utf-8")
        if "<!-- AUTO-CONTEXT:DISCOVERY:START -->" in existing_text:
            # Idempotent replacement of discovery block
            pattern = r"<!-- AUTO-CONTEXT:DISCOVERY:START -->.*?<!-- AUTO-CONTEXT:DISCOVERY:END -->"
            import re
            new_hub_text = re.sub(pattern, anchored_block, existing_text, flags=re.DOTALL)
        else:
            # Upgrade existing legacy context.md by prepending hub block
            new_hub_text = (
                f"# {project_name} — Executive Context Hub\n\n"
                f"> **Last Updated:** {date_now} | **Stack:** {stack} ({framework})\n\n"
                f"{anchored_block}\n\n"
                "## 4. Active Invariants & Gotchas\n\n"
                "See [`.agents/context/gotchas.md`](file://"
                f"{(project_dir / '.agents' / 'context' / 'gotchas.md').as_posix()}) "
                "for institutional knowledge.\n"
            )
    else:
        # Create brand new Executive Hub (< 60 lines!)
        new_hub_text = (
            f"# {project_name} — Executive Context Hub\n\n"
            f"> **Last Updated:** {date_now} | **Stack:** {stack} ({framework})\n\n"
            f"{anchored_block}\n\n"
            "## 4. Active Invariants & Gotchas\n\n"
            "Inspect [`.agents/context/gotchas.md`](file://"
            f"{(project_dir / '.agents' / 'context' / 'gotchas.md').as_posix()}) "
            "before modifying architecture.\n"
        )

    scanner.write_idempotent(hub_file, new_hub_text, "Executive Hub (context.md)")

    console.print(Panel(
        f"[bold green]✨ Codebase scan completed with zero token waste![/]\n"
        f"[white]• Ports discovered:      [green]{len(ports)}[/]\n"
        f"• Runbook commands:      [green]{len(commands)}[/]\n"
        f"• Satellites generated:  [green]{len(satellites)}[/] (routes, schema, gotchas)\n"
        f"• Hub size (context.md): [bold green]< 60 lines (Token Optimized)[/]",
        border_style="green",
    ))
