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
    assert (tmp_path / "AGENTS.md").is_file()
    assert (tmp_path / "GEMINI.md").is_file()
    assert (tmp_path / "CLAUDE.md").is_file()


def test_offline_negative_caching(tmp_path: Path):
    """Test that upstream network failures write a negative cache to eliminate repeated latency."""
    import json
    from unittest.mock import patch
    from auto_context import config

    fake_cache_file = tmp_path / "update_check.json"

    with patch.object(config, "UPDATE_CACHE_FILE", fake_cache_file):
        with patch.object(update_cmd, "check_upstream_version", return_value=None) as mock_check:
            # 1. First run when offline: check_upstream_version returns None
            status = update_cmd.get_cached_update_status(force_check=True)
            assert status is not None
            assert status["source"] == "offline_cached"
            assert status["update_available"] is False
            assert fake_cache_file.exists(), "Negative cache file was not created!"

            # Verify contents of written cache
            disk_data = json.loads(fake_cache_file.read_text(encoding="utf-8"))
            assert disk_data["source"] == "offline_cached"
            assert mock_check.call_count == 1

            # 2. Subsequent run: must read from cache in 0ms without re-querying network
            cached_status = update_cmd.get_cached_update_status(force_check=False)
            assert cached_status is not None
            assert cached_status["source"] == "offline_cached"
            # mock_check must STILL be 1 (did not attempt network!)
            assert mock_check.call_count == 1

