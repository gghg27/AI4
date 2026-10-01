from pathlib import Path

from mkdocs.config import load_config


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

EXPECTED_NAV = [
    {"首页": "index.md"},
    {"引言": "introduction.md"},
    {
        "学习地图": [
            {
                "第一部分：计算机第一课": [
                    {"总览": "01-computer/index.md"},
                    {"计算机基础扫盲": "01-computer/计算机基础扫盲.md"},
                    {"电子笔记": "01-computer/电子笔记.md"},
                    {
                        "与 AI 交互的文档格式": [
                            {"总览": "01-computer/与ai交互的文档格式.md"},
                            {"Markdown 语法详细教程": "01-computer/Markdown语法详细教程.md"},
                        ]
                    },
                    {"科学上网": "01-computer/科学上网.md"},
                    {"CS 自学指南": "01-computer/cs自学指南.md"},
                    {"技术论坛与电子书资源": "01-computer/技术论坛与电子书资源.md"},
                    {"工程化技能": "01-computer/工程化技能.md"},
                ]
            },
            {
                "第二部分：大模型与 Agent": [
                    {"总览": "02-ai-and-agents/index.md"},
                    {"底层原理": "02-ai-and-agents/底层原理.md"},
                    {"应用层": "02-ai-and-agents/应用层.md"},
                ]
            },
            {
                "第三部分：链接合集": [
                    {"总览": "03-resources/index.md"},
                    {"魔法": "03-resources/魔法.md"},
                    {"学习资源类": "03-resources/学习资源类.md"},
                    {"大模型与 Agent": "03-resources/大模型agent.md"},
                    {"软件开发": "03-resources/软件开发.md"},
                    {"算法训练": "03-resources/算法训练.md"},
                ]
            },
        ]
    },
    {"关于": "about.md"},
]

EXPECTED_TITLES = {
    "01-computer/计算机基础扫盲.md": "计算机基础扫盲",
    "01-computer/电子笔记.md": "电子笔记",
    "01-computer/与ai交互的文档格式.md": "与 AI 交互的文档格式",
    "01-computer/科学上网.md": "科学上网",
    "01-computer/cs自学指南.md": "CS 自学指南",
    "01-computer/技术论坛与电子书资源.md": "技术论坛与电子书资源",
    "01-computer/工程化技能.md": "工程化技能",
    "02-ai-and-agents/底层原理.md": "底层原理",
    "02-ai-and-agents/应用层.md": "应用层",
    "03-resources/魔法.md": "魔法",
    "03-resources/学习资源类.md": "学习资源类",
    "03-resources/大模型agent.md": "大模型与 Agent",
    "03-resources/软件开发.md": "软件开发",
    "03-resources/算法训练.md": "算法训练",
}

STALE_REFERENCES = {
    "file-system-and-terminal.md",
    "git-and-environment.md",
    "essential-tools.md",
    "llm-basics.md",
    "practical-llm-use.md",
    "agent-basics.md",
    "ai-application-roadmap.md",
    "build-an-agent.md",
    "computer-foundations.md",
    "llm-and-agent-resources.md",
    "coding-and-projects.md",
    "communities-and-forums.md",
    "resource-selection.md",
}


def nav_paths(items: list[dict[str, object]]) -> list[str]:
    paths: list[str] = []
    for item in items:
        for value in item.values():
            if isinstance(value, str):
                paths.append(value)
            else:
                paths.extend(nav_paths(value))
    return paths


config = load_config(config_file=str(ROOT / "mkdocs.yml"))
assert config["nav"] == EXPECTED_NAV, config["nav"]
expected_nav_paths = nav_paths(EXPECTED_NAV)
assert len(expected_nav_paths) == 21
for relative_path in expected_nav_paths:
    assert (DOCS / relative_path).is_file(), relative_path

for relative_path, title in EXPECTED_TITLES.items():
    text = (DOCS / relative_path).read_text(encoding="utf-8")
    first_content_line = next(line for line in text.splitlines() if line.strip())
    assert first_content_line == f"# {title}", (relative_path, first_content_line)

all_markdown = "\n".join(
    path.read_text(encoding="utf-8") for path in DOCS.rglob("*.md")
)
assert "[[" not in all_markdown
for stale_reference in STALE_REFERENCES:
    assert stale_reference not in all_markdown, stale_reference

print("Content structure verification passed: navigation, titles, and links.")
