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
