# CS 自学指南式布局重构 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将现有 Material for MkDocs 站点重构为顶部单工具栏、左侧完整学习导航、中间正文、右侧文章目录的文档布局，同时保留当前配色、暗色模式和移动端体验。

**Architecture:** 继续使用 Material for MkDocs 的原生 HTML 与交互，只通过主题 feature 配置改变导航骨架，并在现有 `extra.css` 中覆盖尺寸、间距和视觉层级。自动化验证直接检查最终浏览器布局和现有交互，不引入自定义模板或 JavaScript。

**Tech Stack:** MkDocs 1.6.1、Material for MkDocs 9.6.20、CSS、Python、Playwright

**Spec:** `project-notes/specs/2026-09-30-cs-guide-layout-refactor-design.md`

## Global Constraints

- 保留现有深蓝、浅蓝和亮蓝配色，以及明暗模式。
- 不更换 Material for MkDocs，不覆盖完整主题模板。
- 不新增 JavaScript，不改写正文内容。
- 桌面端使用左侧学习导航、中间正文和右侧文章目录。
- 手机端侧栏不常驻，左侧导航通过顶部菜单按钮打开。
- 所有断点下不得产生页面级横向滚动。
- 搜索、代码复制、Mermaid、暗色模式和现有主要页面链接不得回归。

---

## File Map

- `mkdocs.yml`：站点导航 feature 和栏目层级的唯一配置来源。
- `docs/assets/stylesheets/extra.css`：站点颜色、三栏布局、导航、正文组件和响应式规则。
- `tests/verify_site.py`：真实浏览器中的桌面、深色、文章页和移动端验收测试。
- `artifacts/home-desktop.png`、`artifacts/home-dark.png`、`artifacts/home-mobile.png`：测试运行时更新的视觉复核截图，不作为生产源文件。

### Task 1: 建立左侧主导航骨架

**Files:**
- Modify: `tests/verify_site.py`
- Modify: `mkdocs.yml`

**Interfaces:**
- Consumes: Material for MkDocs 的 `.md-header`、`.md-tabs`、`.md-sidebar--primary` 和 `.md-nav` DOM 结构。
- Produces: 无顶部标签栏、桌面端主导航可见且包含全部一级入口的页面骨架。

- [x] **Step 1: 在桌面测试中写入失败的导航骨架断言**

在 `verify_desktop` 首页加载完成后加入以下断言：

```python
    assert page.locator(".md-tabs").count() == 0

    primary_sidebar = page.locator(".md-sidebar--primary")
    assert primary_sidebar.is_visible()
    assert primary_sidebar.get_by_role("link", name="首页", exact=True).is_visible()
    assert primary_sidebar.get_by_role("link", name="引言", exact=True).is_visible()
    assert primary_sidebar.get_by_text("第一部分：计算机第一课", exact=True).is_visible()
    assert primary_sidebar.get_by_text("第二部分：大模型与 Agent", exact=True).is_visible()
    assert primary_sidebar.get_by_text("第三部分：学习资源总库", exact=True).is_visible()
    assert primary_sidebar.get_by_role("link", name="关于", exact=True).is_visible()
```

- [x] **Step 2: 运行浏览器验证并确认因顶部标签仍存在或左栏入口缺失而失败**

Run: `.venv\Scripts\python tests\verify_site.py`

Expected: FAIL at `.md-tabs` or primary sidebar assertions because `navigation.tabs` still moves the main navigation into the header.

- [x] **Step 3: 用最小配置切换为单栏顶部 + 左侧完整导航**

在 `mkdocs.yml` 的 `theme.features` 中删除：

```yaml
    - navigation.tabs
```

并添加：

```yaml
    - navigation.expand
```

保留 `navigation.instant`、`navigation.tracking`、`navigation.sections`、`navigation.top`、`toc.follow`、搜索和代码功能。

- [x] **Step 4: 运行严格构建和浏览器验证**

Run: `.venv\Scripts\python -m mkdocs build --strict`

Expected: PASS，且不出现导航或链接警告。

Run: `.venv\Scripts\python tests\verify_site.py`

Expected: 新增导航骨架断言 PASS；若旧的截图样式断言失败，只记录为 Task 2 的预期失败，不回退配置。

- [x] **Step 5: 提交导航骨架**

```powershell
git add -- mkdocs.yml tests/verify_site.py
git commit -m "refactor: move guide navigation to sidebar"
```

### Task 2: 实现桌面三栏阅读布局与紧凑首页

**Files:**
- Modify: `tests/verify_site.py`
- Modify: `docs/assets/stylesheets/extra.css`

**Interfaces:**
- Consumes: Task 1 生成的 `.md-sidebar--primary` 左栏和 Material 原生 `.md-sidebar--secondary` 文章目录。
- Produces: 桌面端从左到右排列的主导航、正文、文章目录，以及视觉重量更轻的首页入口卡片。

- [x] **Step 1: 写入失败的桌面几何和首页卡片断言**

在 `verify_desktop` 中取得元素边界并加入：

```python
    primary_box = page.locator(".md-sidebar--primary").bounding_box()
    content_box = page.locator(".md-content").bounding_box()
    secondary_box = page.locator(".md-sidebar--secondary").bounding_box()
    assert primary_box is not None
    assert content_box is not None
    assert secondary_box is not None
    assert primary_box["x"] < content_box["x"] < secondary_box["x"]
    assert content_box["width"] >= 640

    route_card = page.locator(".route-card").first
    assert route_card.evaluate("el => parseFloat(getComputedStyle(el).minHeight)") <= 160
```

将旧的页头背景色断言保留，用于证明现有配色未改变。

- [x] **Step 2: 运行验证并确认几何或卡片高度断言失败**

Run: `.venv\Scripts\python tests\verify_site.py`

Expected: FAIL because the current `.md-grid`/`.md-content__inner` sizing and `.route-card` minimum height do not meet the new layout contract.

- [x] **Step 3: 在现有 CSS 变量基础上实现三栏尺寸**

在 `extra.css` 中调整现有规则，不复制主题完整样式：

```css
.md-grid {
  max-width: 90rem;
}

.md-main__inner {
  margin-top: 1rem;
}

.md-sidebar--primary {
  width: 13.5rem;
}

.md-sidebar--secondary {
  width: 11rem;
}

.md-content__inner {
  max-width: 48rem;
  margin-inline: 0 auto;
}
```

为左栏增加清晰的层级、当前项和滚动条样式：

```css
.md-sidebar--primary .md-sidebar__scrollwrap {
  scrollbar-width: thin;
  scrollbar-color: var(--guide-border) transparent;
}

.md-sidebar--primary .md-nav__title {
  color: var(--guide-navy);
  font-weight: 700;
}

.md-sidebar--primary .md-nav__link {
  line-height: 1.45;
}

.md-sidebar--primary .md-nav__link--active {
  color: var(--guide-link);
  font-weight: 700;
}
```

保持顶栏现有颜色，只压缩工具栏的视觉高度和阴影；不要创建第二层导航。

- [x] **Step 4: 降低首页卡片视觉重量**

修改现有 `.route-card` 和 hover 规则：

```css
.route-card {
  min-height: 9.5rem;
  padding: 0.9rem;
  box-shadow: none;
}

.route-card:hover {
  box-shadow: 0 5px 16px rgba(23, 105, 224, 0.08);
  transform: translateY(-1px);
}
```

在 `prefers-reduced-motion` 规则下继续禁用该位移过渡。

- [x] **Step 5: 为暗色模式补齐侧栏文字与边界颜色**

在现有 slate 主题块中让侧栏标题、链接和滚动条使用 `--guide-ink`、`--guide-muted`、`--guide-border`，不得引入新的紫色或灰黑配色体系。

- [x] **Step 6: 运行严格构建和桌面验证**

Run: `.venv\Scripts\python -m mkdocs build --strict`

Expected: PASS.

Run: `.venv\Scripts\python tests\verify_site.py`

Expected: 桌面首页、暗色模式、文章页 Mermaid 验证均 PASS，控制台错误列表为空。

- [x] **Step 7: 提交桌面布局**

```powershell
git add -- docs/assets/stylesheets/extra.css tests/verify_site.py
git commit -m "style: add three-column reading layout"
```

### Task 3: 完成响应式导航与最终视觉验证

**Files:**
- Modify: `tests/verify_site.py`
- Modify: `docs/assets/stylesheets/extra.css`
- Modify: `task_plan.md`

**Interfaces:**
- Consumes: Task 2 的桌面三栏布局和 Material 原生抽屉开关 `#__drawer`。
- Produces: 中等屏幕隐藏右侧目录、手机端使用导航抽屉、所有视口无横向溢出的最终站点。

- [ ] **Step 1: 扩展失败的中等屏幕和移动端断言**

新增 `verify_tablet`：

```python
def verify_tablet(browser) -> None:
    page = browser.new_page(viewport={"width": 960, "height": 900})
    page.emulate_media(color_scheme="light")
    page.goto(BASE_URL, wait_until="domcontentloaded")
    page.locator(".route-card").first.wait_for(state="visible")

    assert page.locator(".md-sidebar--primary").is_visible()
    assert not page.locator(".md-sidebar--secondary").is_visible()
    assert_no_horizontal_overflow(page, 960)
    page.close()
```

在 `verify_mobile` 中补充：

```python
    assert not page.locator(".md-sidebar--primary").is_visible()
    assert not page.locator(".md-sidebar--secondary").is_visible()
```

并在主流程中于 `verify_desktop(chromium)` 和 `verify_mobile(chromium)` 之间调用 `verify_tablet(chromium)`。

- [ ] **Step 2: 运行验证并确认断点行为尚未满足测试**

Run: `.venv\Scripts\python tests\verify_site.py`

Expected: FAIL at 960px 的侧栏可见性或水平溢出断言。

- [ ] **Step 3: 收敛响应式规则**

在现有 `@media screen and (max-width: 60rem)` 中保留首页卡片单列，并确保主题在该宽度隐藏右侧目录但保留左侧导航。不要用 `display: none` 覆盖 Material 的抽屉状态。

在现有 `@media screen and (max-width: 44rem)` 中：

```css
.md-content__inner {
  max-width: none;
  margin-inline: auto;
}

.route-card {
  min-height: 8.5rem;
}
```

依赖主题自带的 drawer CSS 隐藏常驻侧栏，以保证菜单按钮仍能打开相同导航内容。

- [ ] **Step 4: 运行完整验证并检查截图**

Run: `.venv\Scripts\python -m mkdocs build --strict`

Expected: PASS，无警告。

Run: `.venv\Scripts\python tests\verify_site.py`

Expected: 输出 `Site verification passed: desktop, dark mode, tablet, and mobile.`，并更新三张截图。

逐一检查：

- `artifacts/home-desktop.png`：顶部只有一层工具栏，左栏完整，正文与右侧目录不重叠。
- `artifacts/home-dark.png`：侧栏、正文和卡片在深色模式下均清晰可读。
- `artifacts/home-mobile.png`：正文无裁切，菜单抽屉能显示完整导航。

- [ ] **Step 5: 更新测试完成文案与任务记录**

将测试脚本末尾输出改为：

```python
print("Site verification passed: desktop, dark mode, tablet, and mobile.")
```

在 `task_plan.md` 的 2026-09-30 小节勾选实施、严格构建、自动化验证和视觉复核，并将 `Current Status` 改为完成。

- [ ] **Step 6: 最终提交**

```powershell
git add -- docs/assets/stylesheets/extra.css tests/verify_site.py task_plan.md artifacts/home-desktop.png artifacts/home-dark.png artifacts/home-mobile.png
git commit -m "test: verify responsive guide layout"
```

### Task 4: 完成前的独立验证

**Files:**
- Verify only: `mkdocs.yml`
- Verify only: `docs/assets/stylesheets/extra.css`
- Verify only: `tests/verify_site.py`

**Interfaces:**
- Consumes: Tasks 1–3 的全部实现。
- Produces: 可交付的验证证据，不再新增行为。

- [ ] **Step 1: 从干净进程执行严格构建**

Run: `.venv\Scripts\python -m mkdocs build --clean --strict`

Expected: exit code 0，无 WARNING 或 ERROR。

- [ ] **Step 2: 启动本地站点并执行浏览器验收**

Run: `.venv\Scripts\python -m mkdocs serve`

在另一终端运行：

Run: `.venv\Scripts\python tests\verify_site.py`

Expected: exit code 0，浏览器控制台错误为空。

- [ ] **Step 3: 检查改动范围**

Run: `git diff --check`

Expected: 无尾随空格或空白错误。

Run: `git status --short`

Expected: 只包含本计划列出的站点配置、样式、测试、任务记录和截图文件改动；不得包含 `site/`、缓存或临时文件。

- [ ] **Step 4: 记录最终验证结果**

在交付说明中列出严格构建、桌面/平板/手机浏览器验证、暗色模式、Mermaid 和视觉截图检查的实际结果；任何未能运行的验证必须明确说明原因。
