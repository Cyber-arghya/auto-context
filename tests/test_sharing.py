"""
Tests for share.py and import_cmd.py: item discovery, Gist URL resolution, and type detection.
"""
from pathlib import Path
from auto_context.commands import share, import_cmd, init_cmd


def test_find_item_resolution(tmp_path: Path):
    """Test locating a local skill or rule for sharing."""
    # Create local rule and skill
    init_cmd.new_rule(name="my-shared-rule", target=tmp_path)
    init_cmd.new_skill(name="my-shared-skill", target=tmp_path)

    rule_path = share._find_item("my-shared-rule", tmp_path)
    assert rule_path is not None
    assert rule_path.exists()
    assert rule_path.name == "my-shared-rule.md"

    skill_path = share._find_item("my-shared-skill", tmp_path)
    assert skill_path is not None
    assert skill_path.exists()
    assert skill_path.name == "SKILL.md"

    # Non-existent item returns None
    assert share._find_item("non-existent-item", tmp_path) is None


def test_resolve_gist_url():
    """Test converting GitHub Gist web URL to raw content endpoint."""
    web_url = "https://gist.github.com/myuser/1234567890abcdef"
    raw_url = import_cmd._resolve_url(web_url)
    assert raw_url == "https://gist.githubusercontent.com/myuser/1234567890abcdef/raw"

    direct_url = "https://example.com/raw/rule.md"
    assert import_cmd._resolve_url(direct_url) == direct_url


def test_detect_type_from_frontmatter():
    """Test detecting whether downloaded content is a skill or rule."""
    skill_content = (
        "---\n"
        "name: my-skill\n"
        "triggers: [\"deploy\"]\n"
        "---\n"
        "# Skill: My Skill\n"
    )
    assert import_cmd._detect_type(skill_content) == "skill"

    rule_content = (
        "---\n"
        "name: my-rule\n"
        "trigger: always_on\n"
        "---\n"
        "# Rule: My Rule\n"
    )
    assert import_cmd._detect_type(rule_content) == "rule"

