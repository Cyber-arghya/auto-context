"""
Tests for auto_context.services package: ScaffoldService, RegistryService, SecurityService, MemoryService.
"""
from pathlib import Path

from auto_context.core.exceptions import (
    DuplicateRuleError,
    MemorySyncError,
    ResourceConflictError,
    SecurityViolationError,
)
from auto_context.services import (
    MemoryService,
    RegistryService,
    ScaffoldService,
    SecurityService,
)


def test_registry_service_lifecycle(tmp_path: Path):
    """Test RegistryService loading, duplicate checking, and registration."""
    service = RegistryService(target_dir=tmp_path)
    reg = service.load_registry()
    assert "version" in reg

    # Register a new rule
    service.register_rule("custom-db", "Custom Database Optimization", "custom-db.md")
    reg_after = service.load_registry()
    assert "custom-db" in reg_after["domains"]

    # Duplicate check: should detect collision
    dup = service.find_duplicate("Custom Database Optimization techniques")
    assert dup is not None
    assert dup[0] == "custom-db"

    # Unrelated guideline: should NOT collide
    no_dup = service.find_duplicate("Completely unrelated frontend design pattern")
    assert no_dup is None


def test_scaffold_service_components(tmp_path: Path):
    """Test ScaffoldService for docs, subagents, and hooks."""
    service = ScaffoldService(project_dir=tmp_path)
    vars = {"PROJECT_NAME": "test-project", "PROJECT_DIR": tmp_path.as_posix()}

    # Scaffold docs layout
    docs = service.scaffold_docs_layout(vars)
    assert (tmp_path / "docs" / "architecture").exists()
    assert (tmp_path / "docs" / "development").exists()
    assert (tmp_path / "docs" / "decisions").exists()

    # Scaffold single subagent
    agent = service.scaffold_single_subagent("data-engineer")
    assert agent.name == "data-engineer"
    assert (tmp_path / ".agents" / "agents" / "data-engineer.md").exists()

    # Recreating without force must raise ResourceConflictError
    raised = False
    try:
        service.scaffold_single_subagent("data-engineer", force=False)
    except ResourceConflictError:
        raised = True
    assert raised is True

    # Scaffold single skill
    skill = service.scaffold_single_skill("test-skill")
    assert skill.name == "test-skill"
    assert (tmp_path / ".agents" / "skills" / "test-skill" / "SKILL.md").exists()


def test_security_service_audit(tmp_path: Path):
    """Test SecurityService audit and validation report output."""
    sec_service = SecurityService(default_target=tmp_path)
    
    # Clean workspace
    report = sec_service.audit()
    assert report.success is True
    assert report.has_violations is False

    # Prohibited file creation
    env_file = tmp_path / ".env"
    env_file.write_text("SECRET_KEY=12345", encoding="utf-8")

    dirty_report = sec_service.audit()
    assert dirty_report.success is False
    assert dirty_report.has_violations is True

    # Audit and abort must raise SecurityViolationError
    raised = False
    try:
        sec_service.audit_and_abort()
    except SecurityViolationError:
        raised = True
    assert raised is True


def test_memory_service_guard(tmp_path: Path):
    """Test MemoryService safeguards against uninitialized operations."""
    mem_service = MemoryService(memory_dir=tmp_path / "uninit_memory")
    assert mem_service.is_initialized() is False

    raised = False
    try:
        mem_service.harvest_from_workspace(tmp_path)
    except MemorySyncError:
        raised = True
    assert raised is True

