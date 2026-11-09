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

