"""
Tests for core package: domain exceptions and data models.
"""
from pathlib import Path
from auto_context.core import (
    AutoContextError,
    ConfigurationCorruptError,
    DuplicateRuleError,
    ItemNotFoundError,
    MemorySyncError,
    ResourceConflictError,
    SecurityViolationError,
    RuleDefinition,
    SkillDefinition,
    SubagentDefinition,
    UpdateStatus,
    ValidationReport,
)


def test_domain_exception_hierarchy():
    """Verify that all domain exceptions inherit from AutoContextError."""
    sec_err = SecurityViolationError(violations=[{"type": "secret"}])
    assert isinstance(sec_err, AutoContextError)
    assert len(sec_err.violations) == 1
    assert "1 violation" in str(sec_err)

    dup_err = DuplicateRuleError(title="No Dups", domain="code-standards", file_name="code-standards.md")
    assert isinstance(dup_err, AutoContextError)
    assert dup_err.title == "No Dups"
    assert "code-standards" in str(dup_err)

    mem_err = MemorySyncError("Git pull failed")
    assert isinstance(mem_err, AutoContextError)
    assert "Git pull failed" in str(mem_err)

    cfg_err = ConfigurationCorruptError(Path("/tmp/mcp.json"), "invalid syntax")
    assert isinstance(cfg_err, AutoContextError)
    assert "invalid syntax" in str(cfg_err)

    item_err = ItemNotFoundError("my-rule", item_type="Rule")
    assert isinstance(item_err, AutoContextError)
    assert "Rule 'my-rule' not found." == str(item_err)

    res_err = ResourceConflictError(Path("/tmp/rule.md"), resource_type="Rule")
    assert isinstance(res_err, AutoContextError)
    assert "--force" in str(res_err)


def test_rule_definition_model():
    """Verify RuleDefinition model attributes and serialization."""
    rule = RuleDefinition(
        name="test-rule",
        title="Test Rule",
        file_name="test-rule.md",
        domain="testing",
        description="Guidelines for testing",
        keywords=["test", "unit", "pytest"],
        content="# Test Rule Content",
    )
    assert rule.name == "test-rule"
    d = rule.to_dict()
    assert d["name"] == "test-rule"
    assert d["keywords"] == ["test", "unit", "pytest"]
    assert d["domain"] == "testing"


def test_skill_and_agent_models(tmp_path: Path):
    """Verify SkillDefinition and SubagentDefinition models."""
    skill = SkillDefinition(
        name="docker-build",
        path=tmp_path / "skills" / "docker-build",
        triggers=["docker", "container"],
    )
    assert skill.name == "docker-build"
    assert len(skill.triggers) == 2

    agent = SubagentDefinition(
        name="architect",
        role="System Architect",
        file_name="architect.md",
        path=tmp_path / "agents" / "architect.md",
    )
    assert agent.role == "System Architect"
    assert agent.file_name == "architect.md"


def test_validation_report_and_update_status():
    """Verify ValidationReport and UpdateStatus models."""
    report_clean = ValidationReport(success=True, files_scanned=12)
    assert report_clean.success is True
    assert report_clean.has_violations is False

    report_dirty = ValidationReport(
        success=False,
        violations=[{"file": "secret.txt", "type": "leak"}],
        files_scanned=12,
    )
    assert report_dirty.success is False
    assert report_dirty.has_violations is True

    status = UpdateStatus(
        needs_update=True,
        local_version="0.3.0",
        upstream_version="0.4.0",
        checked_at="2026-11-09T00:00:00Z",
        is_cached=True,
    )
    assert status.needs_update is True
    assert status.local_version == "0.3.0"
    assert status.is_cached is True
