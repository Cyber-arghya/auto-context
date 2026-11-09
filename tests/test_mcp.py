"""
Tests for mcp.py: preset resolution, shlex quoted arguments handling, configuration persistence.
"""
from pathlib import Path
import json
import typer
from auto_context.commands import mcp


def test_add_mcp_preset_sqlite(tmp_path: Path):
    cfg_file = tmp_path / ".gemini" / "mcp_config.json"
    cfg_file.parent.mkdir(parents=True)
    cfg_file.write_text('{"mcpServers": {}}', encoding="utf-8")

    mcp.add_mcp(
        name="sqlite",
        target=tmp_path,
        args="data/app.db",
        runtime="uvx",
    )

    data = json.loads(cfg_file.read_text(encoding="utf-8"))
    assert "sqlite" in data["mcpServers"]
    server = data["mcpServers"]["sqlite"]
    assert server["command"] == "uvx"
    assert "data/app.db" in server["args"]


def test_add_mcp_quoted_arguments_with_spaces(tmp_path: Path):
    cfg_file = tmp_path / ".gemini" / "mcp_config.json"
    cfg_file.parent.mkdir(parents=True)
    cfg_file.write_text('{"mcpServers": {}}', encoding="utf-8")

    mcp.add_mcp(
        name="custom-server",
        target=tmp_path,
        command="python",
        args="--db 'C:/Program Files/My App/db.sqlite' --verbose",
    )

    data = json.loads(cfg_file.read_text(encoding="utf-8"))
    assert "custom-server" in data["mcpServers"]
    server = data["mcpServers"]["custom-server"]
    # Argument with spaces inside quotes must not be broken into multiple tokens
    assert any("C:/Program Files/My App/db.sqlite" in arg for arg in server["args"])


def test_cli_flag_args_capital_a(tmp_path: Path):
    """Test that -A sets args without conflicting with -a (append)."""
    from typer.testing import CliRunner
    from auto_context.main import app

    runner = CliRunner()
    result = runner.invoke(app, ["--add-mcp", "custom-flag", "--command", "runner", "-A", "--port 8080", "--target", str(tmp_path)])
    assert result.exit_code == 0
    cfg_file = tmp_path / ".gemini" / "mcp_config.json"
    assert cfg_file.exists()
    data = json.loads(cfg_file.read_text(encoding="utf-8"))
    assert "custom-flag" in data["mcpServers"]
    assert "--port" in data["mcpServers"]["custom-flag"]["args"]


def test_mcp_config_guards_null_and_empty(tmp_path: Path):
    """Test that _load_mcp_config, add_mcp, and remove_mcp handle empty and null mcpServers safely."""
    gemini_cfg = tmp_path / ".gemini" / "mcp_config.json"
    agents_cfg = tmp_path / ".agents" / "mcp_config.json"
    gemini_cfg.parent.mkdir(parents=True)
    agents_cfg.parent.mkdir(parents=True)

    # 1. Config with empty dict {}
    gemini_cfg.write_text("{}", encoding="utf-8")
    # 2. Config with {"mcpServers": null}
    agents_cfg.write_text('{"mcpServers": null}', encoding="utf-8")

    # Loading both must yield a safe dict with mcpServers as dict
    assert isinstance(mcp._load_mcp_config(gemini_cfg)["mcpServers"], dict)
    assert isinstance(mcp._load_mcp_config(agents_cfg)["mcpServers"], dict)

    # Adding an MCP server must succeed without KeyError or TypeError
    mcp.add_mcp(
        name="test-server",
        target=tmp_path,
        command="test-cmd",
    )
    data1 = json.loads(gemini_cfg.read_text(encoding="utf-8"))
    data2 = json.loads(agents_cfg.read_text(encoding="utf-8"))
    assert "test-server" in data1["mcpServers"]
    assert "test-server" in data2["mcpServers"]

    # Removing an MCP server must succeed safely
    mcp.remove_mcp(name="test-server", target=tmp_path)
    data1_after = json.loads(gemini_cfg.read_text(encoding="utf-8"))
    assert "test-server" not in data1_after["mcpServers"]


def test_posix_path_normalization_in_scaffolding(tmp_path: Path):
    """Test that project_dir in AGENTS.md uses POSIX forward slashes instead of Windows backslashes."""
    from auto_context.commands import init_cmd
    init_cmd.init(target=tmp_path)
    agents_md = tmp_path / "AGENTS.md"
    assert agents_md.exists()
    content = agents_md.read_text(encoding="utf-8")
    # Must use forward slash file:// URI format without unescaped Windows backslashes
    assert f"file://{tmp_path.as_posix()}/" in content
    assert "\\" not in content.split("file://")[1].split()[0]


