"""
main.py — Root Typer app and CLI entrypoint.

Supports both modern subcommands (rule, skill, mcp, memory, share, import)
and legacy flag compatibility (-r, -s, --add-mcp, --list-mcp, --remove-mcp).
"""
from importlib.metadata import version as pkg_version
from pathlib import Path
from typing import Annotated, Optional

import typer
from rich.console import Console

from auto_context.commands import init_cmd, memory, mcp, share, import_cmd

app = typer.Typer(
    name="init-context",
    help="Autonomous context & instruction manager for AI coding assistants.",
    no_args_is_help=False,
    add_completion=False,
)
console = Console()

# ── Sub-routers ────────────────────────────────────────────────────────────────
app.add_typer(memory.app, name="memory", help="Central memory brain management.")
app.add_typer(mcp.app, name="mcp", help="MCP tool registry management.")

# ── Inline subcommands ────────────────────────────────────────────────────────
app.command("init")(init_cmd.init)
app.command("rule")(init_cmd.new_rule)
app.command("skill")(init_cmd.new_skill)
app.command("share")(share.share)
app.command("import")(import_cmd.import_item)


@app.callback(invoke_without_command=True)
def root(
    ctx: typer.Context,
    target: Annotated[Optional[Path], typer.Option("--target", "-t", help="Target project directory.")] = None,
    new_rule: Annotated[Optional[str], typer.Option("--new-rule", "-r", help="Scaffold a new agent rule.")] = None,
    new_skill: Annotated[Optional[str], typer.Option("--new-skill", "-s", help="Scaffold a new agent skill.")] = None,
    add_mcp: Annotated[Optional[str], typer.Option("--add-mcp", help="Add or update an MCP server.")] = None,
    remove_mcp: Annotated[Optional[str], typer.Option("--remove-mcp", help="Remove an MCP server.")] = None,
    list_mcp: Annotated[bool, typer.Option("--list-mcp", help="List registered MCP servers.")] = False,
    preset: Annotated[Optional[str], typer.Option("--preset", "-p", help="MCP preset name.")] = None,
    runtime: Annotated[Optional[str], typer.Option("--runtime", "--runner", help="Package runner (uvx vs npx).")] = None,
    command: Annotated[Optional[str], typer.Option("--command", "-c", help="Executable command for MCP server.")] = None,
    args: Annotated[Optional[str], typer.Option("--args", "-a", help="Arguments to pass to MCP command.")] = None,
    url: Annotated[Optional[str], typer.Option("--url", help="HTTP endpoint URL for remote MCP server.")] = None,
    env_var: Annotated[Optional[str], typer.Option("--env-var", help="Secret environment variable name.")] = None,
    env: Annotated[Optional[str], typer.Option("--env", help="Environment variables (KEY=val,KEY2=val2).")] = None,
    global_: Annotated[bool, typer.Option("--global", "-g", help="Target global plugin scope.")] = False,
    force: Annotated[bool, typer.Option("--force", "-f", help="Overwrite existing files.")] = False,
    dry_run: Annotated[bool, typer.Option("--dry-run", "-d", help="Preview without writing.")] = False,
    version: bool = typer.Option(False, "--version", "-v", help="Show version and exit."),
) -> None:
    """
    Run without a subcommand to scaffold project context, or use flags for
    rules (-r), skills (-s), MCP (--add-mcp), and options.
    """
    if version:
        try:
            v = pkg_version("auto-context")
        except Exception:
            v = "1.0.0"
        console.print(f"init-context v{v}")
        raise typer.Exit()

    if ctx.invoked_subcommand is not None:
        return

    # ── Legacy flag routing ────────────────────────────────────────────────────
    if new_rule:
        init_cmd.new_rule(name=new_rule, target=target, global_=global_, force=force, dry_run=dry_run)
        return

    if new_skill:
        init_cmd.new_skill(name=new_skill, target=target, global_=global_, force=force, dry_run=dry_run)
        return

    if list_mcp:
        mcp.list_mcp(target=target, global_=global_)
        return

    if remove_mcp:
        mcp.remove_mcp(name=remove_mcp, target=target, global_=global_)
        return

    if add_mcp:
        mcp.add_mcp(
            name=add_mcp,
            target=target,
            global_=global_,
            preset=preset,
            runtime=runtime,
            command=command,
            args=args,
            url=url,
            env_var=env_var,
            env=env,
        )
        return

    # Default action: scaffold workspace
    init_cmd.init(target=target, force=force, dry_run=dry_run)


def main() -> None:  # pragma: no cover
    import os, sys
    # Ensure UTF-8 output on all platforms (Windows CP1252 fix)
    if sys.platform == "win32":
        os.environ.setdefault("PYTHONIOENCODING", "utf-8")
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
        except AttributeError:
            pass
    app()
