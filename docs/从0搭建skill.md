**Skill 是一个给 Agent 使用的“能力包”**。它把某类任务的操作方法、规则、模板、脚本、参考资料封装起来，让 Agent 在遇到类似任务时，不需要每次重新理解规则，而是直接调用这套能力。

当前主流 Agent Skill 的基本形态通常是：
```
my-skill/
├── SKILL.md
├── scripts/
├── references/
├── assets/
└── examples/
```

其中 SKILL.md 是核心。
Claude Code 文档说，每个 Skill 都需要一个 SKILL.md，里面包含 YAML frontmatter 和 Markdown 指令；
OpenAI Codex 的 Skill 文档也采用类似结构：一个 Skill 是包含 SKILL.md 的目录，可选带 scripts、references、assets 等文件，这些文件的具体意思，往下看：

# 一个skill的组成
## 第一部分：skill.md

SKILL.md 通常包含两部分：

```
---
name: my-skill
description: 这个 skill 做什么，什么时候应该使用
---

# Instructions

这里写具体执行步骤。
```

Claude Code 文档里说明，`description` 会帮助模型判断什么时候自动加载这个 Skill；目录名也会成为直接调用时使用的 skill 名称。

### metadata / frontmatter
就是 SKILL.md 顶部的 YAML 区域。
常见字段：
```
---
name: code-review
description: Review code changes for bugs, security issues, style problems, and missing tests.
---
```
在 Claude Code 里，description 是推荐字段，因为模型会用它决定是否应用该 Skill；在 Codex 里，description 同样影响隐式触发，所以应该写得清楚、范围明确、关键词靠前。

### Instructions
这是 Skill 真正的“工作流程”，在这里介绍你的skill的具体步骤。

比如一个代码审查 Skill 可以这样写：
```
# Code Review Skill

When reviewing code, follow this order:

1. Identify the changed files.
2. Check for correctness bugs.
3. Check error handling.
4. Check security risks.
5. Check performance risks.
6. Check whether tests are needed.
7. Return findings in this format:

## Summary
One short paragraph.

## Issues
- Severity:
- Location:
- Problem:
- Suggested fix:

## Missing tests
List tests that should be added.
```

## 第二部分：scripts

如果 Skill 需要实际执行操作，可以放脚本。
```
my-skill/
├── SKILL.md
└── scripts/
    ├── run_tests.py
    └── collect_diff.sh
```
比如可以在workflow中添加：
```
Before reviewing, run:

```bash
python scripts/run_tests.py
```


## 第三部分：references  
  
放长文档、规范、说明书。  
  
```text  
my-skill/  
├── SKILL.md  
└── references/  
	├── api-style-guide.md  
	├── database-rules.md  
	└── security-checklist.md
```
这样 SKILL.md 不需要写得很长，只要告诉 Agent：
```
For detailed API naming rules, read `references/api-style-guide.md`.
```
这叫渐进式加载：先让 Agent 看到简短描述，需要时再读取完整说明。Codex 文档也说明 Skills 会先暴露 name、description 和路径，只有当模型决定使用某个 Skill 时，才读取完整 SKILL.md。

## 第四部分：assets

放模板、样例文件、配置文件。
```
my-skill/
├── SKILL.md
└── assets/
    ├── report-template.md
    ├── presentation-template.pptx
    └── config.example.json
```
## 第五部分：examples
放输入输出示例。
```
my-skill/
├── SKILL.md
└── examples/
    ├── good-output.md
    └── bad-output.md
```
示例很重要，因为很多 Skill 写不好不是因为规则少，而是因为**没有明确告诉 Agent 最终结果应该长什么样**。

# skill的分层披露（渐进式加载）
参见[大模型应用开发技术篇(二) - 为你的 Agent 集成 Skill 系统 - 开发调优 - LINUX DO](https://linux.do/t/topic/1974585)
[Learn Claude Code skill系统](https://learn.shareai.run/zh/s05/)


# skill如何接入agent的
skill如何接入agent，对应上一节的渐进式加载，

一个可接入 Agent 的 Skill 最好长这样：
```
skills/
└── code-review/
    ├── SKILL.md
    ├── manifest.yaml
    ├── tools.py
    ├── schema.py
    ├── examples/
    └── references/
```
其中
```
SKILL.md：给 Agent 看的说明书
manifest.yaml：给系统看的注册信息
tools.py：真正执行任务的代码，可选
schema.py：输入输出格式约束，可选
examples/：示例，可选
references/：长文档或规范，可选
```

## 发现👀
### skill Registry 注册表
可以将skill写入system prompt，也可以通过注册表。
也就是系统启动时扫描所有 Skill 文件夹，读取它们的元信息。
例如：
```
skills/
├── code-review/
│   ├── SKILL.md
│   └── manifest.yaml
├── report-writer/
│   ├── SKILL.md
│   └── manifest.yaml
└── data-cleaner/
    ├── SKILL.md
    ├── manifest.yaml
    └── tools.py
```
每个manifest可以这样写：
```
name: data-cleaner
description: Clean CSV datasets by handling missing values, duplicates, column names, and type conversion.
entrypoint: tools.clean_dataset
has_tools: true
version: 0.1.0
```

当agent启动时：
- 扫描 skills/ 目录  
- 读取所有 manifest.yaml  
- 建立 Skill 列表

最后形成一个注册表：
```json
{
  "code-review": {
    "description": "Review source code for correctness, security, maintainability, and missing tests.",
    "path": "skills/code-review",
    "has_tools": false
  },
  "data-cleaner": {
    "description": "Clean CSV datasets by handling missing values, duplicates, column names, and type conversion.",
    "path": "skills/data-cleaner",
    "has_tools": true,
    "entrypoint": "tools.clean_dataset"
  }
}
```


### agent自动选择
当用户输入命令，可以现在skill registry做筛选后，再由agent决定调用哪一个

选择逻辑有以下几种：
- 关键词匹配
- LLM 判断，把可用 Skill 的名字和 description 给模型，让模型选择
- 向量检索，把每个 Skill 的 description 做 embedding，用户请求也做 embedding，然后找最相似的 Skill。

## 加载🥱

当skill被选中后，系统读取它的 SKILL.md。

如果 Skill 只有说明，没有代码，怎么执行？这种叫 **Prompt-only Skill**。它不调用脚本，只是改变 Agent 的行为。
流程是：
```
用户请求
 ↓
Agent 选择 Skill
 ↓
加载 SKILL.md
 ↓
Agent 按 SKILL.md 的流程回答
```

如果有代码，则会根据用户需求调用
流程：
```
用户：帮我清洗这个 CSV 文件
 ↓
Agent 选择 data-cleaner Skill
 ↓
加载 SKILL.md
 ↓
根据用户请求生成工具参数
 ↓
调用 tools.clean_dataset(...)
 ↓
拿到 JSON 结果
 ↓
Agent 解释结果
```

### Workflow Skill



## 一个成熟的skill调用流程
```
1. 用户输入任务
2. Orchestrator 解析任务意图
3. Skill Selector 从 Registry 选择候选 Skill
4. Skill Loader 读取 SKILL.md
5. Agent 判断是否需要更多用户信息
6. Agent 生成结构化参数
7. Schema Validator 校验参数
8. Sandbox Runner 创建隔离工作区
9. Tool Executor 执行 Skill 代码
10. Artifact Manager 保存产物
11. Logger 记录执行日志
12. Agent 读取 Skill 输出
13. Agent 生成最终回复
```





















