"""
Tests for security.py: secret detection, prohibited files, ignore filters, and false-positive guards.
"""
from pathlib import Path
from auto_context import security


def test_clean_file_passes_audit(tmp_path: Path):
    clean_file = tmp_path / "main.py"
    clean_file.write_text("def hello():\n    return 'world'\n", encoding="utf-8")
    violations = security.audit_path(clean_file, single_file=True)
    assert len(violations) == 0


def test_prohibited_filename_caught(tmp_path: Path):
    env_file = tmp_path / ".env"
    env_file.write_text("FOO=BAR\n", encoding="utf-8")
    violations = security.audit_path(env_file, single_file=True)
    assert len(violations) == 1
    assert violations[0].pattern == "Prohibited Sensitive File"


def test_prohibited_extension_caught(tmp_path: Path):
    key_file = tmp_path / "server.key"
    key_file.write_text("dummy key content", encoding="utf-8")
    violations = security.audit_path(key_file, single_file=True)
    assert len(violations) == 1
    assert violations[0].pattern == "Prohibited Key/Certificate Extension"


def test_secret_patterns_detected(tmp_path: Path):
    # Dynamically constructed to prevent VCS push-protection static alarms on test fixtures
    test_cases = [
        ("ghp_" + "1234567890abcdefghijklmnopqrstuvwxyzAB", "GitHub Token"),
        ("sk_live_" + "1234567890abcdefghijklmn", "Stripe Live Key"),
        ("sk-proj-" + "1234567890abcdefghijklmnopqrstuvwxyz12345678", "OpenAI Project Key"),
        ("AIza" + "SyA1234567890abcdefghijklmnopqrstuv", "Google API Key"),
        ("AKIA" + "1234567890ABCDEF", "AWS Access Key ID"),
    ]
    for token, pattern_name in test_cases:
        f = tmp_path / f"test_{pattern_name.replace(' ', '_')}.txt"
        f.write_text(f"API_KEY = \"{token}\"\n", encoding="utf-8")
        violations = security.audit_path(f, single_file=True)
        assert len(violations) >= 1
        assert any(v.pattern == pattern_name for v in violations)


def test_template_env_var_not_flagged(tmp_path: Path):
    tmpl_file = tmp_path / "config.json"
    tmpl_file.write_text(
        '{"env": {"GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_PERSONAL_ACCESS_TOKEN}"}}',
        encoding="utf-8",
    )
    violations = security.audit_path(tmpl_file, single_file=True)
    assert len(violations) == 0


def test_node_modules_and_venv_ignored(tmp_path: Path):
    # Simulate bulky dependency tree with fake secrets
    node_dir = tmp_path / "node_modules" / "some-pkg"
    node_dir.mkdir(parents=True)
    fake_pkg_file = node_dir / "index.js"
    fake_pkg_file.write_text('const token = "ghp_1234567890abcdefghijklmnopqrstuvwxyzAB";\n', encoding="utf-8")

    venv_dir = tmp_path / ".venv" / "Lib"
    venv_dir.mkdir(parents=True)
    fake_venv_file = venv_dir / "lib.py"
    fake_venv_file.write_text('KEY = "sk-proj-1234567890abcdefghijklmnopqrstuvwxyz12345678"\n', encoding="utf-8")

    # Clean file in source root
    src_file = tmp_path / "src" / "app.py"
    src_file.parent.mkdir(parents=True)
    src_file.write_text("print('clean source')", encoding="utf-8")

    violations = security.audit_path(tmp_path)
    # Both node_modules and .venv must be completely ignored
    assert len(violations) == 0
