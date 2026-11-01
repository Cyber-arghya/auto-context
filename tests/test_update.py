"""
Tests for update_cmd.py: version parsing, non-breaking safety guarantees.
"""
from pathlib import Path
from auto_context.commands import update_cmd


def test_version_parsing():
    assert update_cmd._parse_version("1.0.5") == (1, 0, 5)
    assert update_cmd._parse_version("v1.0.6") == (1, 0, 6)
    assert update_cmd._parse_version("2.1.0-beta") == (2, 1, 0)
    assert update_cmd._parse_version("1.0.6") > update_cmd._parse_version("1.0.5")
    assert update_cmd._parse_version("1.1.0") > update_cmd._parse_version("1.0.9")


def test_update_workspace_preserves_custom_rules_and_context(tmp_path: Path):
    agents_dir = tmp_path / ".agents" / "rules"
    agents_dir.mkdir(parents=True)
    custom_rule = agents_dir / "my-custom-rule.md"
    custom_rule.write_text("# Custom Rule Content", encoding="utf-8")

    context_file = tmp_path / "context.md"
    context_file.write_text("# Custom Project Hub", encoding="utf-8")

    # Run workspace update
    update_cmd.update_workspace(target_dir=tmp_path)

    # Custom rule and context.md must remain 100% untouched
    assert custom_rule.read_text(encoding="utf-8") == "# Custom Rule Content"
    assert context_file.read_text(encoding="utf-8") == "# Custom Project Hub"
