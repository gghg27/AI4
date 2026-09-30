# New Content Structure Realignment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 让 MkDocs 导航、总览页、内部链接和页面标题完整匹配用户重新整理后的三个内容目录，并恢复无警告的严格构建。

**Architecture:** 以三个部分的 `index.md` roadmap 和设计规格中的路径映射为唯一信息架构来源。使用一个纯 Python 结构验证脚本检查导航路径、页面标题、双链和旧链接，再使用现有 Playwright 脚本验证最终浏览器导航与响应式布局。

**Tech Stack:** MkDocs 1.6.1、Material for MkDocs 9.6.20、Python 3.11、Markdown、Playwright

**Spec:** `project-notes/specs/2026-10-01-content-structure-realignment-design.md`

## Global Constraints

- 保留现有中文文件名，不重新命名文件。
- 不引入自动导航插件或新的运行时依赖。
- 不扩写作者观点；空白页只增加一级标题和“本页内容待补充”说明。
- 已有零散内容只增加标题和修复链接，不调整原文顺序。
- 保留现有 CS 自学指南式布局、蓝色配色、暗色模式和响应式行为。
- `Markdown语法详细教程.md` 不做内容重写，只处理会阻止严格构建的示例链接。
- 最终 `mkdocs build --clean --strict` 必须无警告通过。

---

## File Map

- `mkdocs.yml`：新文件结构的导航顺序和显示名称。
- `tests/verify_content_structure.py`：不启动浏览器即可运行的导航、标题和内部链接结构测试。
- `tests/verify_site.py`：真实浏览器中的导航、页面、暗色模式和响应式验收。
- `docs/01-computer/*.md`：第一部分总览、页面标题、占位说明和内部链接。
- `docs/02-ai-and-agents/*.md`：第二部分总览、页面标题、占位说明和内部链接。
- `docs/03-resources/*.md`：第三部分总览、页面标题和格式错误的外部链接。
- `docs/index.md`：第三张入口卡片名称与新第三部分标题对齐。

### Task 1: 建立新内容结构的失败测试

**Files:**
- Create: `tests/verify_content_structure.py`
- Modify: `tests/verify_site.py`
- Test: `tests/verify_content_structure.py`
- Test: `tests/verify_site.py`

**Interfaces:**
- Consumes: `mkdocs.yml` 的 `nav` 配置和 `docs/` 下的 Markdown 文件。
- Produces: 结构契约 `EXPECTED_NAV_PATHS`、`EXPECTED_TITLES`、`STALE_REFERENCES`，供后续任务验证。

- [x] **Step 1: 创建结构验证脚本**

写入以下脚本：

```python
from pathlib import Path

from mkdocs.config import load_config


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

EXPECTED_NAV_PATHS = [
    "index.md",
    "introduction.md",
    "01-computer/index.md",
    "01-computer/计算机基础扫盲.md",
    "01-computer/电子笔记.md",
    "01-computer/与ai交互的文档格式.md",
    "01-computer/Markdown语法详细教程.md",
    "01-computer/科学上网.md",
    "01-computer/cs自学指南.md",
    "01-computer/技术论坛与电子书资源.md",
    "01-computer/工程化技能.md",
    "02-ai-and-agents/index.md",
    "02-ai-and-agents/底层原理.md",
    "02-ai-and-agents/应用层.md",
    "03-resources/index.md",
    "03-resources/魔法.md",
    "03-resources/学习资源类.md",
    "03-resources/大模型agent.md",
    "03-resources/软件开发.md",
    "03-resources/算法训练.md",
    "about.md",
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


def flatten_nav(items: list[object]) -> list[str]:
    paths: list[str] = []
    for item in items:
        if isinstance(item, str):
            paths.append(item)
        elif isinstance(item, dict):
            for value in item.values():
                if isinstance(value, str):
                    paths.append(value)
                else:
                    paths.extend(flatten_nav(value))
    return paths


config = load_config(config_file=ROOT / "mkdocs.yml")
actual_nav_paths = flatten_nav(config["nav"])
assert actual_nav_paths == EXPECTED_NAV_PATHS, actual_nav_paths

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
```

- [x] **Step 2: 先把浏览器测试切换到新导航和新页面**

在桌面端左侧导航断言中增加：

```python
    assert primary_sidebar.get_by_text("计算机基础扫盲", exact=True).is_visible()
    assert primary_sidebar.get_by_text("底层原理", exact=True).is_visible()
    assert primary_sidebar.get_by_text("链接合集", exact=True).is_visible()
```

将旧 `llm-basics` 页面访问和 Mermaid 检查替换为：

```python
    page.goto(
        f"{BASE_URL}02-ai-and-agents/底层原理/",
        wait_until="domcontentloaded",
    )
    assert page.locator("h1").first.inner_text() == "底层原理"

    page.goto(
        f"{BASE_URL}01-computer/Markdown语法详细教程/",
        wait_until="domcontentloaded",
    )
    page.locator(".mermaid svg").first.wait_for(state="visible")
    assert page.locator(".mermaid svg").count() > 0
```

- [x] **Step 3: 运行结构脚本并确认导航仍指向旧结构**

Run: `.venv\Scripts\python.exe tests\verify_content_structure.py`

Expected: FAIL at `actual_nav_paths == EXPECTED_NAV_PATHS`，输出仍包含 `file-system-and-terminal.md` 等旧路径。

- [x] **Step 4: 运行浏览器测试并确认左侧导航不含新页面**

Run:

```powershell
python C:\Users\zj\.codex\skills\webapp-testing\scripts\with_server.py `
  --server ".venv\Scripts\python.exe -m mkdocs serve --dev-addr 127.0.0.1:8000" `
  --port 8000 -- python tests\verify_site.py
```

Expected: FAIL at“计算机基础扫盲”“底层原理”或“链接合集”的左侧导航断言。

- [x] **Step 5: 提交失败测试**

```powershell
git add -- tests/verify_content_structure.py tests/verify_site.py
git commit -m "test: define new content structure"
```

### Task 2: 重建 MkDocs 导航并规范页面入口

**Files:**
- Modify: `mkdocs.yml`
- Modify: `docs/01-computer/计算机基础扫盲.md`
- Modify: `docs/01-computer/电子笔记.md`
- Modify: `docs/01-computer/与ai交互的文档格式.md`
- Modify: `docs/01-computer/科学上网.md`
- Modify: `docs/01-computer/cs自学指南.md`
- Modify: `docs/01-computer/技术论坛与电子书资源.md`
- Modify: `docs/01-computer/工程化技能.md`
- Modify: `docs/02-ai-and-agents/底层原理.md`
- Modify: `docs/02-ai-and-agents/应用层.md`
- Modify: `docs/03-resources/魔法.md`
- Modify: `docs/03-resources/学习资源类.md`
- Modify: `docs/03-resources/大模型agent.md`
- Modify: `docs/03-resources/软件开发.md`
- Modify: `docs/03-resources/算法训练.md`
- Test: `tests/verify_content_structure.py`

**Interfaces:**
- Consumes: Task 1 的 `EXPECTED_NAV_PATHS` 和 `EXPECTED_TITLES`。
- Produces: 所有新页面均可从 MkDocs 导航到达，并以一致一级标题开头。

- [x] **Step 1: 用新路径映射替换 `mkdocs.yml` 的 `nav`**

将 `nav` 完整替换为：

```yaml
nav:
  - 首页: index.md
  - 引言: introduction.md
  - 学习地图:
      - 第一部分：计算机第一课:
          - 总览: 01-computer/index.md
          - 计算机基础扫盲: 01-computer/计算机基础扫盲.md
          - 电子笔记: 01-computer/电子笔记.md
          - 与 AI 交互的文档格式:
              - 总览: 01-computer/与ai交互的文档格式.md
              - Markdown 语法详细教程: 01-computer/Markdown语法详细教程.md
          - 科学上网: 01-computer/科学上网.md
          - CS 自学指南: 01-computer/cs自学指南.md
          - 技术论坛与电子书资源: 01-computer/技术论坛与电子书资源.md
          - 工程化技能: 01-computer/工程化技能.md
      - 第二部分：大模型与 Agent:
          - 总览: 02-ai-and-agents/index.md
          - 底层原理: 02-ai-and-agents/底层原理.md
          - 应用层: 02-ai-and-agents/应用层.md
      - 第三部分：链接合集:
          - 总览: 03-resources/index.md
          - 魔法: 03-resources/魔法.md
          - 学习资源类: 03-resources/学习资源类.md
          - 大模型与 Agent: 03-resources/大模型agent.md
          - 软件开发: 03-resources/软件开发.md
          - 算法训练: 03-resources/算法训练.md
  - 关于: about.md
```

- [x] **Step 2: 为七个空白页面加入最小页面骨架**

每个文件使用各自标题，正文统一为：

```markdown
# 对应页面标题

> 本页内容待补充。
```

适用文件：`计算机基础扫盲.md`、`电子笔记.md`、`科学上网.md`、`cs自学指南.md`、`技术论坛与电子书资源.md`、`底层原理.md`、`应用层.md`。

- [x] **Step 3: 为七个已有内容页面补一级标题**

分别在文件最前面增加：

```markdown
# 与 AI 交互的文档格式
# 工程化技能
# 魔法
# 学习资源类
# 大模型与 Agent
# 软件开发
# 算法训练
```

每个标题只加入对应文件，并在标题后保留一个空行；原有正文顺序不变。

- [x] **Step 4: 运行结构测试并确认只剩链接类失败**

Run: `.venv\Scripts\python.exe tests\verify_content_structure.py`

Expected: 导航和标题断言 PASS；测试继续因 `[[` 或旧文件名出现在总览页而 FAIL。

- [x] **Step 5: 提交导航和页面入口**

```powershell
git add -- mkdocs.yml docs/01-computer docs/02-ai-and-agents docs/03-resources
git commit -m "refactor: align navigation with content structure"
```

### Task 3: 对齐总览页并修复链接

**Files:**
- Modify: `docs/index.md`
- Modify: `docs/01-computer/index.md`
- Modify: `docs/01-computer/与ai交互的文档格式.md`
- Modify: `docs/01-computer/Markdown语法详细教程.md`
- Modify: `docs/02-ai-and-agents/index.md`
- Modify: `docs/03-resources/index.md`
- Modify: `docs/03-resources/大模型agent.md`
- Modify: `docs/03-resources/软件开发.md`
- Test: `tests/verify_content_structure.py`

**Interfaces:**
- Consumes: Task 2 的最终导航路径和页面标题。
- Produces: 总览页与导航互相一致，站内不再含 Obsidian 双链或旧页面引用。

- [x] **Step 1: 把第一部分 roadmap 改为可点击链接**

将列表替换为：

```markdown
## Roadmap

- [计算机基础扫盲](计算机基础扫盲.md)
- [电子笔记](电子笔记.md)
- [与 AI 交互的文档格式](与ai交互的文档格式.md)
- [科学上网](科学上网.md)
- [CS 自学指南](cs自学指南.md)
- [技术论坛与电子书资源](技术论坛与电子书资源.md)
- [工程化技能](工程化技能.md)
```

- [x] **Step 2: 修复第一部分的教程链接**

把仓库绝对双链改为：

```markdown
[Markdown 语法详细教程](Markdown语法详细教程.md)
```

- [x] **Step 3: 对齐第二部分总览**

将 roadmap 和下一步替换为：

```markdown
## Roadmap

- [底层原理](底层原理.md)
- [应用层](应用层.md)
```

```markdown
进入[底层原理](底层原理.md)。
```

- [x] **Step 4: 对齐第三部分总览**

将标题、资源地图和下一步替换为：

```markdown
# 第三部分：链接合集

## 资源地图

- [魔法](魔法.md)
- [学习资源类](学习资源类.md)
- [大模型与 Agent](大模型agent.md)
- [软件开发](软件开发.md)
- [算法训练](算法训练.md)
```

保留目标说明与“使用规则”段落，将末行改为：

```markdown
下一步可从[魔法](魔法.md)开始。
```

- [x] **Step 5: 对齐首页第三张卡片名称**

在 `docs/index.md` 中只将第三张卡片的：

```html
<strong>学习资源总库</strong>
```

改为：

```html
<strong>链接合集</strong>
```

- [x] **Step 6: 修复资源页中缺失左方括号的外链**

将资源页中的链接统一为以下有效 Markdown：

```markdown
[御舆 — 解码 Agent Harness · Claude Code 架构深度剖析](https://lintsinghua.github.io/)
[Learn Claude Code](https://learn.shareai.run/zh/)
[AgentGuide - AI Agent 开发学习指南](https://adongwanai.github.io/AgentGuide/)
[Hello-Agents](https://datawhalechina.github.io/hello-agents/#/)
[前端基础教程 - 搞七捻三 - LINUX DO](https://linux.do/t/topic/489164/13)
```

- [x] **Step 7: 把会触发缺失资源警告的演示图片改为代码示例**

在 `Markdown语法详细教程.md` 的实验报告模板中，将活动图片链接：

```markdown
![实验结果](assets/result.png)
```

改为行内代码展示：

```markdown
`![实验结果](assets/result.png)`
```

- [x] **Step 8: 运行结构测试**

Run: `.venv\Scripts\python.exe tests\verify_content_structure.py`

Expected: 输出 `Content structure verification passed: navigation, titles, and links.`。

- [x] **Step 9: 运行严格构建**

Run: `.venv\Scripts\python.exe -m mkdocs build --clean --strict`

Expected: exit code 0，且无 WARNING。

- [x] **Step 10: 提交总览与链接修复**

```powershell
git add -- docs tests/verify_content_structure.py
git commit -m "fix: repair guide navigation links"
```

### Task 4: 更新浏览器验收并验证布局无回归

**Files:**
- Modify: `tests/verify_site.py`
- Modify: `task_plan.md`
- Test: `tests/verify_site.py`
- Test: `tests/verify_content_structure.py`

**Interfaces:**
- Consumes: Task 1 已经写入的新导航断言，以及 Tasks 2–3 的新导航和页面 URL。
- Produces: 覆盖新内容结构、Mermaid、暗色、平板和手机行为的最终验收证据。

- [x] **Step 1: 运行浏览器测试验证新结构与布局**

Run:

```powershell
python C:\Users\zj\.codex\skills\webapp-testing\scripts\with_server.py `
  --server ".venv\Scripts\python.exe -m mkdocs serve --dev-addr 127.0.0.1:8000" `
  --port 8000 -- python tests\verify_site.py
```

Expected: 输出 `Site verification passed: desktop, dark mode, tablet, and mobile.`，控制台错误列表为空。

- [x] **Step 2: 执行全部最终验证**

Run: `.venv\Scripts\python.exe tests\verify_content_structure.py`

Expected: PASS。

Run: `.venv\Scripts\python.exe -m mkdocs build --clean --strict`

Expected: PASS，无 WARNING。

Run: `git diff --check`

Expected: 无空白错误。

- [x] **Step 3: 更新任务记录**

在 `task_plan.md` 增加 2026-10-01 小节，记录：新导航完成、页面标题规范化、链接修复、严格构建通过、桌面/平板/手机测试通过。

- [x] **Step 4: 提交最终验收更新**

```powershell
git add -- tests/verify_site.py task_plan.md
git commit -m "test: verify rebuilt content navigation"
```
