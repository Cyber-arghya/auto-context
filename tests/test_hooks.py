"""
Tests for deterministic lifecycle hooks (.agents/hooks/ format and validate scripts).
"""
from pathlib import Path
from auto_context.commands import init_cmd


def test_init_scaffolds_lifecycle_hooks(tmp_path: Path):
    init_cmd.init(target=tmp_path)
    hooks_dir = tmp_path / ".agents" / "hooks"
    assert hooks_dir.is_dir()

    expected_hooks = ["format.sh", "format.ps1", "validate.sh", "validate.ps1"]
    for hook_name in expected_hooks:
        hook_file = hooks_dir / hook_name
        assert hook_file.is_file(), f"Expected hook {hook_name} to exist"
        content = hook_file.read_text(encoding="utf-8")
        assert tmp_path.name in content


def test_hooks_preservation_and_force(tmp_path: Path):
    init_cmd.init(target=tmp_path)
    custom_format = tmp_path / ".agents" / "hooks" / "format.sh"
    custom_format.write_text("#!/bin/bash\necho 'custom format'", encoding="utf-8")

    # Second init without force preserves user modifications
    init_cmd.init(target=tmp_path)
    assert custom_format.read_text(encoding="utf-8") == "#!/bin/bash\necho 'custom format'"

    # Init with force overwrites
    init_cmd.init(target=tmp_path, force=True)
    assert custom_format.read_text(encoding="utf-8") != "#!/bin/bash\necho 'custom format'"
    assert tmp_path.name in custom_format.read_text(encoding="utf-8")
