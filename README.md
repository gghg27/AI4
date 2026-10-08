# AI 不完全指北

面向大一新生的计算机基础、AI、Agent 与学习资源指南。站点使用 [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) 构建，内容按“先建立基础，再逐步理解原理”组织。

## 本地预览

Windows PowerShell：

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m mkdocs serve
```

打开 <http://127.0.0.1:8000/>。

## 严格构建

```powershell
.venv\Scripts\python -m mkdocs build --strict
```

生成的网站位于 `site/`。该目录不会提交到 Git。

## 发布到 GitHub Pages

仓库已包含 `.github/workflows/deploy.yml`。推送到 `main` 或 `master` 后，在 GitHub 仓库的 **Settings → Pages → Build and deployment** 中把 Source 设为 **GitHub Actions**。工作流会构建并发布站点。

## 启用全站评论

每个内容页都有独立的 Giscus 评论区，统一使用 [gghg27/ai_discuss](https://github.com/gghg27/ai_discuss) 的 `General` Discussions 分类存放评论。评论公开可读，发表和回复需要登录 GitHub。评论仓库已启用 Discussions 并安装 Giscus App，仓库和分类 ID 已写入 `mkdocs.yml`，网站部署时无需额外配置。

如需更换评论仓库或分类，请在 [Giscus 配置页](https://giscus.app/zh-CN)取得对应 ID 后更新 `mkdocs.yml`。本地测试可用 `GISCUS_REPO_ID`、`GISCUS_CATEGORY` 和 `GISCUS_CATEGORY_ID` 环境变量临时覆盖默认值。

## 内容结构

- `docs/index.md`：首页
- `docs/01-computer/`：第一部分，计算机第一课
- `docs/02-ai-and-agents/`：第二部分，大模型与 Agent
- `docs/03-resources/`：第三部分，学习资源总库
- `project-notes/`：设计规格和实施计划，不参与站点发布
- `docs/assets/`：站点样式、Mermaid 脚本和本地依赖
- `mkdocs.yml`：导航与 MkDocs 配置

涉及产品行为、安装命令和外部服务的内容会标注核验日期。使用前请以对应官方文档为准。
