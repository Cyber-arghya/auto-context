"""
services/scaffold_service.py — Service layer for workspace scaffolding and knowledge layout.
"""
from __future__ import annotations

import shutil
from pathlib import Path

from auto_context import config
from auto_context.config import AGENTS_SUBDIR, get_templates_dir
from auto_context.core.exceptions import ResourceConflictError
from auto_context.core.models import SkillDefinition, SubagentDefinition

DOCS_SUBDIRS = [
    "architecture",
    "development",
    "decisions",
]


class ScaffoldService:
    """Service orchestrating workspace scaffolding, documentation layouts, and agent personas."""

    def __init__(self, project_dir: Path | None = None):
        self.project_dir = (project_dir or Path.cwd()).resolve()

    def _render(self, template_path: Path, variables: dict[str, str]) -> str:
        content = template_path.read_text(encoding="utf-8")
        for key, val in variables.items():
            content = content.replace(f"{{{{{key}}}}}", val)
        return content

    def _write_file(self, dest: Path, content: str, force: bool = False, dry_run: bool = False) -> bool:
        if dest.exists() and not force:
            return False
        if not dry_run:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(content, encoding="utf-8")
        return True

    def scaffold_docs_layout(self, variables: dict[str, str], force: bool = False, dry_run: bool = False) -> list[Path]:
        """Scaffold standard docs/ knowledge layout and migrate legacy context."""
        docs_root = self.project_dir / "docs"
        templates_dir = get_templates_dir() / "docs"
        created: list[Path] = []

        for sub in DOCS_SUBDIRS:
            sub_path = docs_root / sub
            if not dry_run:
                sub_path.mkdir(parents=True, exist_ok=True)

        if templates_dir.exists():
            for tmpl in templates_dir.rglob("*.md"):
                rel_path = tmpl.relative_to(templates_dir)
                dest = docs_root / rel_path
                content = self._render(tmpl, variables)
                if self._write_file(dest, content, force=force, dry_run=dry_run):
                    created.append(dest)

        # Legacy migration: .agents/context/ -> docs/
        legacy_context = self.project_dir / AGENTS_SUBDIR / "context"
        if legacy_context.exists():
            legacy_mappings = [
                (legacy_context / "routes.md", docs_root / "architecture" / "api-design.md"),
                (legacy_context / "schema.md", docs_root / "architecture" / "database-schema.md"),
                (legacy_context / "gotchas.md", docs_root / "development" / "development-guide.md"),
            ]
            for src, dest in legacy_mappings:
                if src.exists() and not dest.exists() and not dry_run:
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src, dest)
                    created.append(dest)

        return created

    def scaffold_subagents(self, variables: dict[str, str], force: bool = False, dry_run: bool = False) -> list[Path]:
        """Scaffold default subagent persona files in .agents/agents/."""
        agents_dir = self.project_dir / AGENTS_SUBDIR / "agents"
        templates_dir = get_templates_dir() / "agents"
        created: list[Path] = []

        if not dry_run:
            agents_dir.mkdir(parents=True, exist_ok=True)

        if templates_dir.exists():
            for tmpl in templates_dir.glob("*.md"):
                dest = agents_dir / tmpl.name
                content = self._render(tmpl, variables)
                if self._write_file(dest, content, force=force, dry_run=dry_run):
                    created.append(dest)

        return created

    def scaffold_single_subagent(self, name: str, force: bool = False, dry_run: bool = False, global_: bool = False) -> SubagentDefinition:
        """Scaffold a single subagent persona."""
        clean_name = name.lower().replace(" ", "-").replace("_", "-").removesuffix(".md")
        role_title = clean_name.replace("-", " ").title()

        dest_dir = (
            config.GLOBAL_PLUGIN_DIR / "agents"
            if global_
            else self.project_dir / AGENTS_SUBDIR / "agents"
        )
        dest_file = dest_dir / f"{clean_name}.md"

        if dest_file.exists() and not force:
            raise ResourceConflictError(dest_file, resource_type="Subagent")

        tmpl = get_templates_dir() / "agent.template.md"
        if tmpl.exists():
            content = self._render(tmpl, {
                "AGENT_ROLE": role_title,
                "AGENT_NAME": clean_name,
                "PROJECT_NAME": self.project_dir.name,
            })
        else:
            content = (
                f"---\nname: {clean_name}\ndescription: Specialized {role_title} persona.\n---\n\n"
                f"# Persona: {role_title}\n\n## Objective\nSpecialized agent for {clean_name}.\n"
            )

        self._write_file(dest_file, content, force=force, dry_run=dry_run)
        if global_ and config.MEMORY_DIR.exists():
            mem_dest = config.MEMORY_DIR / "agents" / f"{clean_name}.md"
            self._write_file(mem_dest, content, force=force, dry_run=dry_run)

        return SubagentDefinition(name=clean_name, role=role_title, file_name=dest_file.name, path=dest_file, content=content)

    def scaffold_hooks(self, force: bool = False, dry_run: bool = False) -> list[Path]:
        """Scaffold cross-platform deterministic lifecycle hooks."""
        hooks_dir = self.project_dir / AGENTS_SUBDIR / "hooks"
        templates_dir = get_templates_dir() / "hooks"
        created: list[Path] = []

        if not dry_run:
            hooks_dir.mkdir(parents=True, exist_ok=True)

        if templates_dir.exists():
            for tmpl in templates_dir.iterdir():
                if tmpl.is_file():
                    dest = hooks_dir / tmpl.name
                    content = tmpl.read_text(encoding="utf-8")
                    if self._write_file(dest, content, force=force, dry_run=dry_run):
                        created.append(dest)

        return created

    def scaffold_instruction_harmonization(self, variables: dict[str, str], force: bool = False, dry_run: bool = False) -> list[Path]:
        """Scaffold harmonized GEMINI.md, AGENTS.md, and CLAUDE.md."""
        tmpl = get_templates_dir() / "AGENTS.template.md"
        created: list[Path] = []
        if not tmpl.exists():
            return created

        content = self._render(tmpl, variables)
        for target_name in ("GEMINI.md", "AGENTS.md", "CLAUDE.md"):
            dest = self.project_dir / target_name
            if self._write_file(dest, content, force=force, dry_run=dry_run):
                created.append(dest)

        return created

    def scaffold_single_skill(self, name: str, force: bool = False, dry_run: bool = False, global_: bool = False) -> SkillDefinition:
        """Scaffold a single operational skill directory."""
        clean_name = name.lower().replace(" ", "-").replace("_", "-")
        title = clean_name.replace("-", " ").title()

        dest_dir = (
            config.GLOBAL_PLUGIN_DIR / "skills" / clean_name
            if global_
            else self.project_dir / AGENTS_SUBDIR / "skills" / clean_name
        )
        dest_file = dest_dir / "SKILL.md"

        if dest_file.exists() and not force:
            raise ResourceConflictError(dest_file, resource_type="Skill")

        tmpl = get_templates_dir() / "skill.template.md"
        if tmpl.exists():
            content = self._render(tmpl, {"SKILL_NAME": clean_name, "SKILL_TITLE": title})
        else:
            content = f"---\nname: {clean_name}\ndescription: Runbook for {title}.\ntriggers: [\"{clean_name}\"]\n---\n\n# Skill: {title}\n"

        self._write_file(dest_file, content, force=force, dry_run=dry_run)
        if global_ and config.MEMORY_DIR.exists():
            mem_dest = config.MEMORY_DIR / "skills" / clean_name / "SKILL.md"
            self._write_file(mem_dest, content, force=force, dry_run=dry_run)

        return SkillDefinition(name=clean_name, path=dest_dir, triggers=[clean_name], content=content)

