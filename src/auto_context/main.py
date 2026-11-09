"""
main.py — Root Typer app and CLI entrypoint.

Supports both modern subcommands (rule, skill, mcp, memory, share, import)
and legacy flag compatibility (-r, -s, --add-mcp, --list-mcp, --remove-mcp).
"""
from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version as pkg_version
import logging
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from auto_context.commands import init_cmd, memory, mcp, share, import_cmd, update_cmd
from auto_context.core.exceptions import AutoContextError

logger = logging.getLogger(__name__)

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
app.command("agent")(init_cmd.new_agent)
app.command("promote")(init_cmd.promote)
app.command("share")(share.share)
app.command("import")(import_cmd.import_item)
app.command("update")(update_cmd.update)


def audit(
    target: Annotated[Path | None, typer.Option("--target", "-t", help="Directory or file to audit.")] = None,
    json_output: Annotated[bool, typer.Option("--json", help="Output audit findings as JSON.")] = False,
) -> None:
    """Scan workspace or files for leaked credentials, secrets, and sensitive tokens."""
    from auto_context import security
    target_path = (target or Path.cwd()).resolve()
    violations = security.audit_path(target_path, single_file=target_path.is_file())
    if json_output:
        import json
        payload = {
            "target": str(target_path),
            "clean": len(violations) == 0,
            "violations_count": len(violations),
            "violations": [
                {
                    "file": str(v.file),
                    "line": v.line,
                    "pattern": v.pattern,
                    "preview": v.preview,
                }
                for v in violations
            ],
        }
        print(json.dumps(payload, indent=2))
        if violations:
            raise typer.Exit(1)
        return

    if not violations:
        console.print(f"[bold green]✨ Security audit passed:[/] No secrets detected in {target_path}")
        return

    security.print_report(violations)
    raise typer.Exit(1)


app.command("audit")(audit)


@app.callback(invoke_without_command=True)
def root(
    ctx: typer.Context,
    target: Annotated[Path | None, typer.Option("--target", "-t", help="Target project directory.")] = None,
    new_rule: Annotated[str | None, typer.Option("--new-rule", "-r", help="Scaffold a new agent rule.")] = None,
    new_skill: Annotated[str | None, typer.Option("--new-skill", "-s", help="Scaffold a new agent skill.")] = None,
    new_agent: Annotated[str | None, typer.Option("--new-agent", help="Scaffold a new agent persona.")] = None,
    add_mcp: Annotated[str | None, typer.Option("--add-mcp", help="Add or update an MCP server.")] = None,
    remove_mcp: Annotated[str | None, typer.Option("--remove-mcp", help="Remove an MCP server.")] = None,
    list_mcp: Annotated[bool, typer.Option("--list-mcp", help="List registered MCP servers.")] = False,
    preset: Annotated[str | None, typer.Option("--preset", "-p", help="MCP preset name.")] = None,
    runtime: Annotated[str | None, typer.Option("--runtime", "--runner", help="Package runner (uvx vs npx).")] = None,
    command: Annotated[str | None, typer.Option("--command", "-c", help="Executable command for MCP server.")] = None,
    args: Annotated[str | None, typer.Option("--args", "-A", help="Arguments to pass to MCP command.")] = None,
    url: Annotated[str | None, typer.Option("--url", help="HTTP endpoint URL for remote MCP server.")] = None,
    env_var: Annotated[str | None, typer.Option("--env-var", help="Secret environment variable name.")] = None,
    env: Annotated[str | None, typer.Option("--env", help="Environment variables (KEY=val,KEY2=val2).")] = None,
    global_: Annotated[bool, typer.Option("--global", "-g", help="Target global plugin scope.")] = False,
    force: Annotated[bool, typer.Option("--force", "-f", help="Overwrite existing files.")] = False,
    append: Annotated[bool, typer.Option("--append", "-a", help="Append to existing domain rule.")] = False,
    guideline: Annotated[str | None, typer.Option("--guideline", help="Guideline text to append to rule.")] = None,
    dry_run: Annotated[bool, typer.Option("--dry-run", "-d", help="Preview without writing.")] = False,
    json_output: Annotated[bool, typer.Option("--json", help="Output machine-readable JSON format.")] = False,
    version: bool = typer.Option(False, "--version", "-v", help="Show version and exit."),
) -> None:
    """
    Run without a subcommand to scaffold project context, or use flags for
    rules (-r), skills (-s), MCP (--add-mcp), and options.
    """
    if version:
        try:
            v = pkg_version("auto-context-cli")
        except PackageNotFoundError:
            try:
                v = pkg_version("auto-context")
            except PackageNotFoundError:
                v = "1.5.1"
        console.print(f"init-context v{v}")
        raise typer.Exit()

    if ctx.invoked_subcommand is not None:
        return

    # ── Legacy flag routing ────────────────────────────────────────────────────
    if new_rule:
        init_cmd.new_rule(name=new_rule, target=target, global_=global_, force=force, append=append, guideline=guideline, dry_run=dry_run)
        return

    if new_skill:
        init_cmd.new_skill(name=new_skill, target=target, global_=global_, force=force, dry_run=dry_run)
        return

    if new_agent:
        init_cmd.new_agent(name=new_agent, target=target, global_=global_, force=force, dry_run=dry_run)
        return

    if list_mcp:
        mcp.list_mcp(target=target, global_=global_, json_output=json_output)
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

    try:
        app()
    except AutoContextError as err:
        console.print(f"[bold red][✗] Error:[/] {err}")
        sys.exit(1)
    except SystemExit as e:
        if e.code == 0 and not any(arg in sys.argv for arg in ("--version", "-v", "update", "--help", "-h")):
            update_cmd.maybe_notify_update()
        raise
    except Exception:
        raise
    else:
        if not any(arg in sys.argv for arg in ("--version", "-v", "update", "--help", "-h")):
            update_cmd.maybe_notify_update()
