# -*- coding: utf-8 -*-
"""
SkillLoader：扫描 skills 目录下 SKILL.md，解析 YAML frontmatter + body，
提供 Layer1 描述列表（get_descriptions）与 Layer2 按名取正文（get_content）。
"""

import re
from pathlib import Path


class SkillLoader:
    """扫描 skills_dir 下各子目录的 SKILL.md，解析 frontmatter 与 body。"""

    def __init__(self, skills_dir: Path):
        self.skills_dir = Path(skills_dir)
        self.skills: dict = {}
        self._load_all()

    def _load_all(self) -> None:
        if not self.skills_dir.exists():
            return
        for f in sorted(self.skills_dir.rglob("SKILL.md")):
            text = f.read_text(encoding="utf-8")
            meta, body = self._parse_frontmatter(text)
            name = meta.get("name", f.parent.name)
            self.skills[name] = {"meta": meta, "body": body, "path": str(f)}

    def _parse_frontmatter(self, text: str) -> tuple:
        """解析 --- 之间的 YAML frontmatter，返回 (meta_dict, body_str)。"""
        match = re.match(r"^---\n(.*?)\n---\n(.*)", text, re.DOTALL)
        if not match:
            return {}, text.strip()
        meta = {}
        for line in match.group(1).strip().splitlines():
            if ":" in line:
                key, val = line.split(":", 1)
                meta[key.strip()] = val.strip()
        return meta, match.group(2).strip()

    def get_descriptions(self) -> str:
        """Layer1：供 system prompt 注入的简短描述列表。"""
        if not self.skills:
            return "(no skills available)"
        lines = []
        for name, skill in self.skills.items():
            desc = skill["meta"].get("description", "No description")
            tags = skill["meta"].get("tags", "")
            line = f" - {name}: {desc}"
            if tags:
                line += f" [{tags}]"
            lines.append(line)
        return "\n".join(lines)

    def get_content(self, name: str) -> str:
        """Layer2：按名称返回完整 skill body，供 load_skill tool 返回。"""
        skill = self.skills.get(name)
        if not skill:
            return f"Error: Unknown skill '{name}'. Available: {', '.join(self.skills.keys())}"
        return f"\n{skill['body']}\n"


def _default_skills_dir() -> Path:
    return Path(__file__).resolve().parent.parent / "skills"


SKILL_LOADER = SkillLoader(_default_skills_dir())
