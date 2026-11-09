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

