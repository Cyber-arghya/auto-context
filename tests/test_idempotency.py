"""
Tests for Idempotency Proof: f(f(x)) = f(x).
Running scanner or context sync repeatedly produces the exact same deterministic output
without duplicating blocks or mutating user data.
"""
import hashlib
from pathlib import Path
from auto_context.commands import init_cmd, scan_cmd
from auto_context import scanner


def test_scan_idempotency_proof(tmp_path: Path):
    # Initialize basic project
    init_cmd.init(target=tmp_path)
    context_file = tmp_path / "context.md"
    assert context_file.exists()

    # Add custom user note outside anchored discovery zone
    user_note = "\n## My Custom Architecture Notes\n- Always use PostgreSQL read replicas.\n"
    with context_file.open("a", encoding="utf-8") as f:
        f.write(user_note)

    # First Scan
    scan_cmd.scan(target=tmp_path)
    first_run_content = context_file.read_text(encoding="utf-8")
    first_hash = hashlib.sha256(first_run_content.encode("utf-8")).hexdigest()

    # Second Scan
    scan_cmd.scan(target=tmp_path)
    second_run_content = context_file.read_text(encoding="utf-8")
    second_hash = hashlib.sha256(second_run_content.encode("utf-8")).hexdigest()

    # Third Scan
    scan_cmd.scan(target=tmp_path)
    third_run_content = context_file.read_text(encoding="utf-8")
    third_hash = hashlib.sha256(third_run_content.encode("utf-8")).hexdigest()

    # Mathematical Idempotency Proof: f(f(x)) == f(x)
    assert first_hash == second_hash == third_hash
    assert first_run_content == second_run_content == third_run_content

    # User content outside anchored block must remain 100% untouched
    assert "Always use PostgreSQL read replicas." in third_run_content
