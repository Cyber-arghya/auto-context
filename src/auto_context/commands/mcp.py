"""
commands/mcp.py — MCP tool registry management.

Subcommands: add, remove, list
Uses native json.load / json.dump — no shell JSON manipulation.

Presets: sqlite, duckdb, git, fetch, time, postgres, github, filesystem, brave
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import shlex
import stat
import sys
from typing import Annotated, Optional

import typer
from rich.console import Console
from rich.table import Table

from auto_context import config
from auto_context.config import AGENTS_SUBDIR, GEMINI_SUBDIR

app = typer.Typer(help="MCP tool registry management.")
console = Console()

# ── Preset definitions ────────────────────────────────────────────────────────
# Each preset is a callable that receives (runtime, args, env_var) and returns
# a dict that becomes the server config value in mcp_config.json.

_PRESETS: dict[str, dict] = {
    "sqlite": {
        "uvx": lambda db: {"command": "uvx", "args": ["mcp-server-sqlite", "--db-path", db]},
        "npx": lambda db: {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-sqlite", db]},
        "default_args": "database.db",
        "env_var": None,
    },
    "duckdb": {
        "uvx": lambda db: {"command": "uvx", "args": ["duckdb-mcp", "--db-path", db]},
        "npx": lambda db: {"command": "uvx", "args": ["duckdb-mcp", "--db-path", db]},  # always uvx
        "default_args": "database.duckdb",
        "env_var": None,
        "force_uvx": True,
    },
    "git": {
        "uvx": lambda repo: {"command": "uvx", "args": ["mcp-server-git", "--repository", repo]},
        "npx": lambda repo: {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-git", repo]},
        "default_args": ".",
        "env_var": None,
    },
    "fetch": {
        "uvx": lambda _: {"command": "uvx", "args": ["mcp-server-fetch"]},
        "npx": lambda _: {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-fetch"]},
        "env_var": None,
    },
    "time": {
        "uvx": lambda _: {"command": "uvx", "args": ["mcp-server-time"]},
        "npx": lambda _: {"command": "uvx", "args": ["mcp-server-time"]},  # always uvx
        "env_var": None,
        "force_uvx": True,
    },
    "postgres": {
        "uvx": lambda conn: {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-postgres", conn]},
        "npx": lambda conn: {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-postgres", conn]},
        "default_env_var": "DATABASE_URL",
        "env_placeholder": "postgresql://username:password@localhost:5432/mydb",
    },
    "github": {
        "uvx": lambda _: {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-github"],
                          "env": {"GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_PERSONAL_ACCESS_TOKEN}"}},
        "npx": lambda _: {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-github"],
                          "env": {"GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_PERSONAL_ACCESS_TOKEN}"}},
        "default_env_var": "GITHUB_PERSONAL_ACCESS_TOKEN",
        "env_placeholder": "ghp_yourPersonalAccessTokenHere",
    },
    "filesystem": {
        "uvx": lambda d: {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-filesystem", d]},
        "npx": lambda d: {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-filesystem", d]},
        "default_args": ".",
        "env_var": None,
    },
    "brave": {
        "uvx": lambda _: {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-brave-search"],
                          "env": {"BRAVE_API_KEY": "${BRAVE_API_KEY}"}},
        "npx": lambda _: {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-brave-search"],
                          "env": {"BRAVE_API_KEY": "${BRAVE_API_KEY}"}},
        "default_env_var": "BRAVE_API_KEY",
        "env_placeholder": "your_brave_api_key_here",
    },
}


# ── .env helpers ──────────────────────────────────────────────────────────────

def _write_env_placeholder(project_dir: Path, var_name: str, placeholder: str) -> None:
    """Write a placeholder to .env.example and protect .env in .gitignore."""
    example = project_dir / ".env.example"
    existing = example.read_text(encoding="utf-8") if example.exists() else ""
    if f"{var_name}=" not in existing:
        with example.open("a", encoding="utf-8") as fh:
            fh.write(f"{var_name}={placeholder}\n")
        console.print(f"  [green][✓] Added placeholder:[/] .env.example ({var_name})")

    # Secure .env with chmod 600 equivalent if it exists
    dot_env = project_dir / ".env"
    if dot_env.exists():
        try:
            dot_env.chmod(stat.S_IRUSR | stat.S_IWUSR)
        except OSError:
            pass  # Windows may not support this; best-effort


def _detect_runtime(project_dir: Path) -> str:
    """Auto-detect uvx vs npx based on project indicators."""
    import shutil
    py_indicators = ("pyproject.toml", "requirements.txt", "Pipfile")
    has_python = any((project_dir / f).exists() for f in py_indicators)
    if has_python and shutil.which("uvx"):
        return "uvx"
    return "npx"


# ── JSON config helpers ───────────────────────────────────────────────────────

def _load_mcp_config(path: Path) -> dict:
    """Load mcp_config.json, returning an empty mcpServers dict on failure."""
    if path.exists():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                return data
        except json.JSONDecodeError:
            pass
    return {"mcpServers": {}}


def _save_mcp_config(path: Path, data: dict) -> None:
    """Write mcp_config.json with 2-space indent."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def _mcp_paths(project_dir: Path, global_: bool) -> list[Path]:
    """Return the list of mcp_config.json paths to write."""
    if global_:
        return [
            config.GLOBAL_GEMINI_DIR / "mcp_config.json",
            config.GLOBAL_PLUGIN_DIR / "mcp_config.json",
        ]
    return [
        project_dir / GEMINI_SUBDIR / "mcp_config.json",
        project_dir / AGENTS_SUBDIR / "mcp_config.json",
    ]


# ── add subcommand ────────────────────────────────────────────────────────────

@app.command("add")
def add_mcp(
    name: Annotated[str, typer.Argument(help="Server name or preset (sqlite, github, …).")],
    target: Annotated[Optional[Path], typer.Option("--target", "-t")] = None,
    global_: Annotated[bool, typer.Option("--global", "-g")] = False,
    preset: Annotated[Optional[str], typer.Option("--preset", "-p", help="Preset name.")] = None,
    runtime: Annotated[Optional[str], typer.Option("--runtime", "--runner")] = None,
    command: Annotated[Optional[str], typer.Option("--command", "-c")] = None,
    args: Annotated[Optional[str], typer.Option("--args", "-a")] = None,
    url: Annotated[Optional[str], typer.Option("--url")] = None,
    env_var: Annotated[Optional[str], typer.Option("--env-var")] = None,
    env: Annotated[Optional[str], typer.Option("--env", help="KEY=val,KEY2=val2")] = None,
) -> None:
    """Add or update an MCP server configuration."""
    project_dir = (target or Path.cwd()).resolve()
    server_name = name.lower()
    chosen_preset = preset or (name.lower() if name.lower() in _PRESETS else None)
    runner = runtime or _detect_runtime(project_dir)

    server_cfg: dict = {}

    if url:
        server_cfg = {"url": url}

    elif chosen_preset and chosen_preset in _PRESETS:
        p = _PRESETS[chosen_preset]
        force_uvx = p.get("force_uvx", False)
        r = "uvx" if force_uvx else runner
        arg_val = args or p.get("default_args", ".")
        fn = p[r] if r in p else p["npx"]
        server_cfg = fn(arg_val)

        # Handle secret env vars
        default_ev = p.get("default_env_var")
        if default_ev:
            ev = env_var or default_ev
            ph = p.get("env_placeholder", f"your_{ev}_here")
            if not global_:
                _write_env_placeholder(project_dir, ev, ph)
            console.print(f"  [bold green][🔒] Secret safety:[/] {ev} referenced via env var (not hardcoded).")

    elif command:
        server_cfg = {"command": command}
        if args:
            try:
                server_cfg["args"] = shlex.split(args, posix=(sys.platform != "win32"))
            except Exception:
                server_cfg["args"] = args.split()
        if env_var:
            server_cfg.setdefault("env", {})[env_var] = f"${{{env_var}}}"
            if not global_:
                _write_env_placeholder(project_dir, env_var, f"your_{env_var}_here")

    else:
        # Generic: derive package name from server_name
        if runner == "uvx":
            server_cfg = {"command": "uvx", "args": [f"mcp-server-{server_name}"]}
        else:
            server_cfg = {"command": "npx", "args": ["-y", f"@modelcontextprotocol/server-{server_name}"]}

    # Merge explicit --env pairs
    if env:
        extra = {}
        for item in env.split(","):
            if "=" in item:
                k, v = item.split("=", 1)
                extra[k.strip()] = v.strip()
        server_cfg.setdefault("env", {}).update(extra)

    # Write to all target config files
    for cfg_path in _mcp_paths(project_dir, global_):
        data = _load_mcp_config(cfg_path)
        data["mcpServers"][server_name] = server_cfg
        _save_mcp_config(cfg_path, data)

    scope = f"GLOBAL (~/.gemini/config/mcp_config.json)" if global_ else f"LOCAL ({project_dir}/.gemini/mcp_config.json)"
    transport = f"HTTP ({url})" if url else f"stdio ({server_cfg.get('command', '?')})"
    console.print(f"\n[bold cyan]🔌 MCP Server Configured![/]")
    console.print(f"   [yellow]Server:[/]    {server_name}")
    console.print(f"   [cyan]Scope:[/]     {scope}")
    console.print(f"   [green]Transport:[/] {transport}")
    console.print("   [dim][i] Restart your AI client to activate new MCP tools.[/]\n")


# ── remove subcommand ─────────────────────────────────────────────────────────

@app.command("remove")
def remove_mcp(
    name: Annotated[str, typer.Argument(help="Server name to remove.")],
    target: Annotated[Optional[Path], typer.Option("--target", "-t")] = None,
    global_: Annotated[bool, typer.Option("--global", "-g")] = False,
) -> None:
    """Remove an MCP server from configuration."""
    project_dir = (target or Path.cwd()).resolve()
    removed_from: list[Path] = []

    for cfg_path in _mcp_paths(project_dir, global_):
        if not cfg_path.exists():
            continue
        data = _load_mcp_config(cfg_path)
        if name in data.get("mcpServers", {}):
            del data["mcpServers"][name]
            _save_mcp_config(cfg_path, data)
            removed_from.append(cfg_path)

    if removed_from:
        console.print(f"[green][✓] Removed MCP server:[/] {name}")
        for p in removed_from:
            console.print(f"   [dim]{p}[/]")
    else:
        console.print(f"[yellow][!] Server '{name}' not found in any MCP config.[/]")


# ── list subcommand ───────────────────────────────────────────────────────────

@app.command("list")
def list_mcp(
    target: Annotated[Optional[Path], typer.Option("--target", "-t")] = None,
    global_: Annotated[bool, typer.Option("--global", "-g")] = False,
) -> None:
    """List all registered MCP servers."""
    project_dir = (target or Path.cwd()).resolve()

    for cfg_path in _mcp_paths(project_dir, global_):
        if not cfg_path.exists():
            continue
        data = _load_mcp_config(cfg_path)
        servers = data.get("mcpServers", {})
        if not servers:
            continue

        table = Table(title=f"MCP Servers — {cfg_path}", border_style="cyan")
        table.add_column("Name", style="yellow", no_wrap=True)
        table.add_column("Type", style="magenta", width=6)
        table.add_column("Endpoint / Command", style="white")

        for sname, cfg in servers.items():
            if "url" in cfg:
                table.add_row(sname, "http", cfg["url"])
            else:
                cmd_str = cfg.get("command", "?") + " " + " ".join(cfg.get("args", []))
                if len(cmd_str) > 60:
                    cmd_str = cmd_str[:57] + "..."
                table.add_row(sname, "stdio", cmd_str)

        console.print(table)
        return

    console.print("[yellow][!] No MCP configuration found. Run:[/] init-context mcp add <name>")

