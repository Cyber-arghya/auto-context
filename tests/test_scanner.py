"""
Tests for scanner.py: port discovery, runbook command discovery, satellite generation, and gotchas safeguard.
"""
from pathlib import Path
from auto_context import scanner


def test_discover_ports_and_services(tmp_path: Path):
    # Create compose.yaml with port binding
    compose_file = tmp_path / "docker-compose.yml"
    compose_file.write_text(
        "services:\n  web:\n    ports:\n      - '8080:80'\n      - '5432:5432'\n",
        encoding="utf-8",
    )
    ports = scanner.discover_ports_and_services(tmp_path)
    assert len(ports) >= 2
    port_numbers = [p[1] for p in ports]
    assert "8080" in port_numbers
    assert "5432" in port_numbers


def test_discover_runbook_commands_pyproject(tmp_path: Path):
    pyproj = tmp_path / "pyproject.toml"
    pyproj.write_text(
        '[project]\nname = "demo"\nversion = "0.1.0"\n'
        '[project.scripts]\nrun-demo = "demo:main"\n'
        '[dependency-groups]\ndev = ["pytest>=8"]\n',
        encoding="utf-8",
    )
    commands = scanner.discover_runbook_commands(tmp_path)
    assert len(commands) >= 2
    cmd_strings = [c[1] for c in commands]
    assert "uv run run-demo" in cmd_strings
    assert "uv run pytest" in cmd_strings


def test_discover_runbook_commands_subproject(tmp_path: Path):
    sub = tmp_path / "backend"
    sub.mkdir(parents=True)
    pkg = sub / "package.json"
    pkg.write_text(
        '{"name": "backend", "scripts": {"dev": "next dev", "test": "jest"}}',
        encoding="utf-8",
    )
    commands = scanner.discover_runbook_commands(tmp_path)
    cmd_strings = [c[1] for c in commands]
    assert any("npm --prefix backend run dev" in s for s in cmd_strings)


def test_gotchas_not_overwritten_by_force(tmp_path: Path):
    satellites_dir = tmp_path / ".agents" / "context"
    satellites_dir.mkdir(parents=True)
    gotchas_file = satellites_dir / "gotchas.md"
    custom_content = "# Custom Architecture Trap\n1. Do not touch legacy auth server."
    gotchas_file.write_text(custom_content, encoding="utf-8")

    # Run generate_satellites with force=True
    scanner.generate_satellites(tmp_path, force=True)

    # Custom content must remain intact (never overwritten!)
    assert gotchas_file.read_text(encoding="utf-8") == custom_content
