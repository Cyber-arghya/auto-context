"""
services/registry_service.py — Service layer for rule domain registry and collision checks.
"""
from __future__ import annotations

import json
import logging
import re
from datetime import date
from pathlib import Path
from typing import Any

from auto_context import config
from auto_context.config import AGENTS_SUBDIR, get_templates_dir

logger = logging.getLogger(__name__)

STOP_WORDS: set[str] = {
    "about", "above", "after", "again", "against", "all", "also", "and", "any",
    "are", "because", "been", "before", "being", "below", "between", "both",
    "but", "cannot", "could", "did", "does", "doing", "down", "during", "each",
    "few", "for", "from", "further", "had", "has", "have", "having", "here",
    "how", "into", "itself", "just", "make", "more", "most", "must", "myself",
    "no", "nor", "not", "off", "once", "only", "other", "ought", "our", "ours",
    "out", "over", "own", "same", "should", "some", "such", "than", "that",
    "the", "their", "theirs", "them", "then", "there", "these", "they", "this",
    "those", "through", "too", "under", "until", "very", "was", "were", "what",
    "when", "where", "which", "while", "who", "whom", "why", "will", "with",
    "would", "your", "yours", "rule", "rules", "guideline", "guidelines",
}


class RegistryService:
    """Service handling rule domain indexing, duplicate detection, and file registration."""

    def __init__(self, target_dir: Path | None = None, global_: bool = False):
        self.global_ = global_
        self.target_dir = (target_dir or Path.cwd()).resolve()
        if self.global_:
            self.rules_dir = config.GLOBAL_PLUGIN_DIR / "rules"
        else:
            self.rules_dir = self.target_dir / AGENTS_SUBDIR / "rules"
        self.registry_file = self.rules_dir / "registry.json"

    def load_registry(self) -> dict[str, Any]:
        """Load registry from disk, falling back to bundled template or empty default."""
        if self.registry_file.exists():
            try:
                return json.loads(self.registry_file.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError) as exc:
                logger.debug("Failed to read registry from %s: %s", self.registry_file, exc)
        tmpl = get_templates_dir() / "rules" / "registry.json"
        if tmpl.exists():
            try:
                return json.loads(tmpl.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError) as exc:
                logger.debug("Failed to read template registry from %s: %s", tmpl, exc)
        return {"version": "1.0.0", "domains": {}}

    def find_duplicate(self, text_or_title: str) -> tuple[str, str, str] | None:
        """Check if guideline or title collides with existing rules in registry."""
        registry = self.load_registry()
        clean_query = re.sub(r"[^a-zA-Z0-9\s]", "", text_or_title).lower().strip()
        query_words = set(w for w in clean_query.split() if len(w) > 3 and w not in STOP_WORDS)

        for d_key, domain in registry.get("domains", {}).items():
            d_file = domain.get("file", f"{d_key}.md")
            for r in domain.get("rules", []):
                r_title = r.get("title", "")
                r_id = r.get("id", "")
                clean_title = re.sub(r"[^a-zA-Z0-9\s]", "", r_title).lower().strip()

                if clean_query == clean_title or (len(clean_query) > 6 and clean_query in clean_title) or (len(clean_title) > 6 and clean_title in clean_query):
                    return d_key, r_title, d_file
                if r_id and r_id in clean_query.replace(" ", "-"):
                    return d_key, r_title, d_file

                r_keywords = set()
                for k in r.get("keywords", []):
                    for word in re.sub(r"[^a-zA-Z0-9\s]", "", k).lower().split():
                        if len(word) > 3 and word not in STOP_WORDS:
                            r_keywords.add(word)

                if query_words and len(query_words.intersection(r_keywords)) >= 3:
                    return d_key, r_title, d_file

        return None

    def register_rule(self, domain_key: str, rule_title: str, file_name: str, target_file: Path | None = None) -> None:
        """Register a new or updated rule entry into registry.json."""
        dest_reg = target_file or self.registry_file
        registry = self.load_registry()
        if "domains" not in registry:
            registry["domains"] = {}

        if domain_key not in registry["domains"]:
            registry["domains"][domain_key] = {
                "file": file_name,
                "name": domain_key.replace("-", " ").title(),
                "description": f"Domain rules for {domain_key}",
                "rules": [],
            }

        clean_first_line = rule_title.strip().splitlines()[0].strip("* ").strip()
        slug = re.sub(r"[^a-zA-Z0-9\s-]", "", clean_first_line).strip().lower().replace(" ", "-")
        clean_words = [w for w in re.sub(r"[^a-zA-Z0-9\s]", "", clean_first_line).lower().split() if len(w) > 3 and w not in STOP_WORDS]

        existing_ids = [r.get("id") for r in registry["domains"][domain_key].get("rules", [])]
        if slug not in existing_ids:
            registry["domains"][domain_key]["rules"].append({
                "id": slug,
                "title": clean_first_line,
                "keywords": clean_words,
            })
            registry["last_updated"] = date.today().isoformat()
            dest_reg.parent.mkdir(parents=True, exist_ok=True)
            dest_reg.write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    def append_guideline(self, dest_file: Path, text_to_append: str) -> None:
        """Append a formatted guideline to an existing rule Markdown file."""
        content = dest_file.read_text(encoding="utf-8") if dest_file.exists() else ""
        existing_nums = [int(m) for m in re.findall(r"(?m)^(\d+)\.\s+\*", content)]
        next_num = (max(existing_nums) + 1) if existing_nums else 1

        clean_guideline = text_to_append.strip()
        if not re.match(r"^\d+\.\s+", clean_guideline):
            if not clean_guideline.startswith("**"):
                lines = clean_guideline.splitlines()
                title = lines[0]
                rest = lines[1:] if len(lines) > 1 else []
                entry = f"{next_num}. **{title}**\n"
                for r in rest:
                    entry += f"   {r}\n"
            else:
                entry = f"{next_num}. {clean_guideline}\n"
        else:
            entry = f"{clean_guideline}\n"

        if not content.endswith("\n") and content:
            content += "\n"
        content += entry
        dest_file.write_text(content, encoding="utf-8")

