"""
Tests for Idempotency Proof: f(f(x)) = f(x).
Running init-context repeatedly produces the exact same deterministic output
without duplicating blocks or mutating user data.
"""
import hashlib
from pathlib import Path
from auto_context.commands import init_cmd


def test_init_idempotency_proof(tmp_path: Path):
    # First init
    init_cmd.init(target=tmp_path)
    context_file = tmp_path / ".agents" / "context.md"
    assert context_file.exists()

    first_run_content = context_file.read_text(encoding="utf-8")
    first_hash = hashlib.sha256(first_run_content.encode("utf-8")).hexdigest()

    # Second init
    init_cmd.init(target=tmp_path)
    second_run_content = context_file.read_text(encoding="utf-8")
    second_hash = hashlib.sha256(second_run_content.encode("utf-8")).hexdigest()

    # Third init
    init_cmd.init(target=tmp_path)
    third_run_content = context_file.read_text(encoding="utf-8")
    third_hash = hashlib.sha256(third_run_content.encode("utf-8")).hexdigest()

    # Mathematical Idempotency Proof: f(f(x)) == f(x)
    assert first_hash == second_hash == third_hash
    assert first_run_content == second_run_content == third_run_content


def test_docs_scaffolding_fresh(tmp_path: Path):
    init_cmd.init(target=tmp_path)
    docs_dir = tmp_path / "docs"
    assert (docs_dir / "architecture" / "system-design.md").is_file()
    assert (docs_dir / "architecture" / "database-schema.md").is_file()
    assert (docs_dir / "architecture" / "api-design.md").is_file()
    assert (docs_dir / "development" / "development-guide.md").is_file()
    assert (docs_dir / "decisions" / "ADR-001.md").is_file()

    content = (docs_dir / "architecture" / "system-design.md").read_text(encoding="utf-8")
    assert tmp_path.name in content


def test_docs_legacy_migration(tmp_path: Path):
    legacy_ctx = tmp_path / ".agents" / "context"
    legacy_ctx.mkdir(parents=True)
    (legacy_ctx / "routes.md").write_text("# My Legacy Routes", encoding="utf-8")
    (legacy_ctx / "schema.md").write_text("# My Legacy Schema", encoding="utf-8")
    (legacy_ctx / "gotchas.md").write_text("# My Legacy Gotchas", encoding="utf-8")

    init_cmd.init(target=tmp_path)

    docs_dir = tmp_path / "docs"
    assert (docs_dir / "architecture" / "api-design.md").read_text(encoding="utf-8") == "# My Legacy Routes"
    assert (docs_dir / "architecture" / "database-schema.md").read_text(encoding="utf-8") == "# My Legacy Schema"
    assert (docs_dir / "development" / "development-guide.md").read_text(encoding="utf-8") == "# My Legacy Gotchas"


def test_triple_instruction_harmonization(tmp_path: Path):
    init_cmd.init(target=tmp_path)
    gemini_file = tmp_path / "GEMINI.md"
    agents_file = tmp_path / "AGENTS.md"
    claude_file = tmp_path / "CLAUDE.md"

    assert gemini_file.is_file(), "GEMINI.md must be generated"
    assert agents_file.is_file(), "AGENTS.md must be generated"
    assert claude_file.is_file(), "CLAUDE.md must be generated"

    gemini_content = gemini_file.read_text(encoding="utf-8")
    agents_content = agents_file.read_text(encoding="utf-8")
    claude_content = claude_file.read_text(encoding="utf-8")

    # Triple files must be completely harmonized and identical
    assert gemini_content == agents_content == claude_content
    assert tmp_path.name in gemini_content
    assert "docs/architecture/system-design.md" in gemini_content
    assert ".agents/hooks/validate" in gemini_content


def test_promote_recursive_skill_tree(tmp_path: Path):
    from unittest.mock import patch
    from auto_context import config

    fake_global = tmp_path / "fake_global"
    fake_memory = tmp_path / "fake_memory"
    fake_global.mkdir(parents=True)
    fake_memory.mkdir(parents=True)

    local_skill_dir = tmp_path / config.AGENTS_SUBDIR / "skills" / "k8s-ops"
    res_dir = local_skill_dir / "resources"
    res_dir.mkdir(parents=True)
    (local_skill_dir / "SKILL.md").write_text("# K8s Ops", encoding="utf-8")
    (res_dir / "pod.yaml").write_text("apiVersion: v1\nkind: Pod", encoding="utf-8")

    with patch.object(config, "GLOBAL_PLUGIN_DIR", fake_global), patch.object(config, "MEMORY_DIR", fake_memory):
        init_cmd.promote("k8s-ops", target=tmp_path)

        assert (fake_global / "skills" / "k8s-ops" / "SKILL.md").is_file()
        assert (fake_global / "skills" / "k8s-ops" / "resources" / "pod.yaml").is_file()
        assert (fake_memory / "skills" / "k8s-ops" / "resources" / "pod.yaml").is_file()



