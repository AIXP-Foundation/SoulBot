# AIAP Structural Specification

---

## 目录

**Part I: 协议基础**
1. [协议声明](#1-协议声明)
2. [核心定义：AISOP = 语言，AIAP = 规则](#2-核心定义)
3. [AIAP.md 规则](#3-aiapmd-规则)

**Part II: 结构规范**
4. [节点 = 功能职责](#4-节点--功能职责)
5. [功能节点计数](#5-功能节点计数)
6. [渐进式节点建议](#6-渐进式节点建议)
7. [fractal_exempt 标注](#7-fractal_exempt-标注)
8. [Pattern 选择](#8-pattern-选择)
9. [Pattern A-G 详细定义](#9-pattern-a-g-详细定义)
10. [main.aisop.json 规则](#10-mainaisopjson-规则)
11. [功能模块规则](#11-功能模块规则)
12. [独立功能判断](#12-独立功能判断)
13. [Sub_AIAP 拆分规则](#13-sub_aiap-拆分规则)
14. [Pattern 升级汇聚处理](#14-pattern-升级汇聚处理)
15. [双流规则](#15-双流规则)

**Part III: 安全与运行时**
16. [信任层级](#16-信任层级)
17. [权限边界](#17-权限边界)
18. [完整性验证](#18-完整性验证)
19. [运行时约束](#19-运行时约束)
20. [错误处理协议](#20-错误处理协议)

**Part IV: 工程化能力**
21. [发现协议](#21-发现协议)
22. [依赖解析](#22-依赖解析)
23. [程序生命周期](#23-程序生命周期)
24. [编排模式](#24-编排模式)

**Part V: 质量与兼容**
25. [版本兼容性](#25-版本兼容性)
26. [文档完整性分级](#26-文档完整性分级)

**附录**
- [Appendix A: PL24 自动修复协议](#appendix-a-pl24-auto-fix-protocol)
- [Appendix B: PL25 许可证与版权声明](#appendix-b-pl25-license--copyright-declaration)
- [Appendix C: Category M — 工具目录模拟场景 (M1-M20)](#appendix-c-category-m--tool-directory-simulation-scenarios)
- [Appendix D: NO_SELF_MODIFY 规则](#appendix-d-no_self_modify-规则)
- [Appendix E: INSIGHTS 机制 — 可选运行时洞察记录](#appendix-e-insights-机制)
- [附录 F：节点门控 — 节点级执行断言](#附录-f节点门控--节点级执行断言)

---

## Part I: 协议基础

---

## 1. 协议声明

```
AIAP Structural Specification
Protocol: AIAP V1.0.0
Authority: aiap.dev
Seed: aisop.dev
Axiom 0: Human Sovereignty and Wellbeing

本文档定义 AIAP 程序的结构规范，包括：
- AIAP.md 项目声明规则
- Pattern A-G 分形模式
- 节点计数与拆分策略
- 安全、运行时、发现、依赖、生命周期、编排协议

所有 AIAP 程序必须遵循本规范。
AISOP 文件格式 (.aisop.json) 和 AISIP 文件格式 (.aisip.json) 作为底层语言不受本文档约束。
```

---

## 2. 核心定义

> AISOP 和 AISIP 是编程语言，AIAP 是编程规则。

| 概念 | 类比 | 定义 |
|------|------|------|
| **AISOP** | 解释型语言 (Python) | AI 驱动语言 — 定义文件格式 (`.aisop.json`)、Mermaid 控制流 + functions、AI 看到完整流程图自主执行 |
| **AISIP** | 编译型语言 (C) | Runtime 驱动语言 — 定义文件格式 (`.aisip.json`)、JSON 控制流 + functions、Runtime 通过 `{}` 指令控制 AI（楚门模式） |
| **AIAP** | 编程规则 (编码规范/设计模式) | 应用协议 — 定义程序应该怎么写、质量标准、安全守卫、公理约束。语言无关：同时治理 AISOP 和 AISIP 程序 |
| **AIAP 程序** | 一个符合规范的项目 | 用 AISOP 或 AISIP 语言、按 AIAP 规则编写的完整项目 |
| **AIAP Creator** | 项目脚手架 (`create-react-app`) | 创建 AIAP 程序的工具 — 自身也是一个 AIAP 程序 (自举) |

### 2.0.1 两种语言，一套治理

```
AISOP（AI 驱动）：
  AI 看到完整 Mermaid 图 → AI 决定执行下一个节点
  入口：ASSERT RUN aisop.main
  信任模型：AI 有完整可见性，通过 system_prompt 约束
  文件：.aisop.json

AISIP（Runtime 驱动）：
  AI 只看到当前节点 → Runtime 决定下一个节点
  入口：Runtime 调用 start()，AI 使用 {} 指令
  信任模型：AI 零可见性，被 Runtime 控制（楚门的世界）
  文件：.aisip.json

共享治理（AIAP）：
  Axiom 0、信任层级、安全、质量标准、模式、生命周期
  — 无论使用哪种语言，全部适用。
```

| 维度 | AISOP | AISIP |
|------|-------|-------|
| 控制流格式 | Mermaid 流程图 | JSON 节点 + 边 |
| 谁驱动执行 | AI（跟随图） | Runtime（喂节点） |
| AI 可见性 | 完整流程图 | 仅当前节点 |
| 记忆模型 | 完整（单 session） | 完整（单 session） |
| 入口 | `ASSERT RUN aisop.main` | `{"method": "start"}` |
| 文件扩展名 | `.aisop.json` | `.aisip.json` |
| 适用场景 | 复杂 AI 推理、自主引导 | 严格控制、确定性路由 |

```
命名规则：
  .aisop.json  →  AISOP 语言格式标识
  .aisip.json  →  AISIP 语言格式标识
  _aiap        →  程序类型标识 (目录遵循什么规则)
  AIAP.md      →  项目声明 (类似 pyproject.toml / pom.xml)
```

### 2.1 文件字段职责

> 每个字段有且仅有一个职责。信息只在一处出现。

**AISOP 文件 (`.aisop.json`)**：

| 字段 | 职责 | 内容 |
|------|------|------|
| `id` | 身份标识 | 程序和模块的唯一标识符 |
| `name` | 名称 | 产品名称 + 版本号 |
| `version` | 版本 | 语义版本号 |
| `summary` | 能力概述 | 一句话说明"我能做什么" |
| `description` | 详细描述 | 架构、历史、模式、实现细节 |
| `system_prompt` | **行为准则** | 定义 agent 应该怎么做 (唯一的行为定义层) |
| `loading_mode` | **加载策略** | `"normal"`（一次性加载所有 functions）或 `"node"`（按需逐节点加载）。默认：`"normal"` |
| `output_mode` | **输出模式** | 定义 L0 结构化输出格式和 L1 输出格式（可选字段） |
| `instruction` | **执行指令** | 固定为 `ASSERT RUN aisop.main` (不可变常量) |
| `user_input` | **保留字段** | 运行时占位符 `"{user_input}"` — 由执行器替换为实际用户消息。可选：使用取决于程序角色（如路由入口文件需要，子模块不需要）。在 AISIP 规范 §3 中定义为必填。 |
| `aisop.main` | 执行图 | 主 Mermaid 流程图 — 所有执行从此开始 |
| `functions` | 执行逻辑 | 每个节点的具体步骤和约束 |

**AISIP 文件 (`.aisip.json`)** — 三层结构：

| 字段 | 职责 | 内容 |
|------|------|------|
| `aisip` | **程序元数据** | 协议版本、标识、名称、版本、概述、描述、工具、参数 |
| `aisip.protocol` | 协议版本 | 如 `"AISIP V1.0.0"` |
| `aisip.id` | 身份标识 | 程序唯一标识符 |
| `aisip.name` | 名称 | 程序显示名称 |
| `aisip.version` | 版本 | 语义版本号 |
| `aisip.summary` | 能力概述 | 一句话说明 |
| `aisip.description` | 详细描述 | 架构、流程、实现细节 |
| `aisip.tools` | 工具声明 | 程序可能使用的工具列表 |
| `aisip.params` | 运行时参数 | 可配置参数 |
| `task` | **控制流** | JSON 节点 + 边（start、nodes、类型、分支） |
| `task.start` | 入口 | 第一个节点名称 |
| `task.nodes` | 流程图 | 节点定义：type、next、branches、error、wait_for、delegate_to |
| `functions` | **执行逻辑** | 每个节点的任务描述（与 AISOP functions 相同角色） |

> AISIP 采用三层分离：`aisip`（程序身份 — 我是谁）、`task`（控制流 — 做什么顺序）、`functions`（任务体 — 每步做什么）。`aisip` 元数据不影响执行 — Runtime 只读 `task` + `functions`。不需要 system_prompt 和 instruction — Runtime 提供 system prompt 并通过 `{}` 指令驱动执行。

### 2.2 instruction 不可变常量（仅 AISOP）

```
规则：每个 AISOP 文件的 instruction 字段必须精确为：ASSERT RUN aisop.main
注意：AISIP 文件没有 instruction 字段 — 执行由 Runtime 驱动。
```

**原理**：
- `RUN` 是机器执行指令，不是自然语言建议。类比 Dockerfile `RUN`、SQL `SELECT`。
- `aisop.main` 是 JSON 结构路径，指向 `content.aisop.main` 执行图。
- 程序身份由 `id` 字段提供，不需要在 instruction 中重复。
- 能力描述由 `summary`/`description` 提供，不需要在 instruction 中重复。

```
C 语言类比：
  int main() { ... }     ← 入口永远是 main，所有程序统一
  ASSERT RUN aisop.main   ← 入口永远是 aisop.main，断言执行，所有 AISOP 文件统一
```

**sub_mermaid**：即使 aisop 对象包含多个图（如 `main`, `orchestrate`, `memory`），入口仍然是 `aisop.main`。main 图内部通过参数路由到子图。

### 2.3 system_prompt 行为层规则

```
规则：system_prompt 是行为层 — 定义 agent 应该怎么做，不描述它是什么或怎么构建的。
```

**必须包含**：
1. **角色定位** — agent 的行为角色（不是产品名）
2. **领域行为准则** — 该领域特有的行为约束
3. `Mirror User's exact language and script variant.` — 多语言要求
4. `Align: Human Sovereignty and Wellbeing.` — Axiom 0 封印

**禁止包含**：
- 产品名或版本号 → 已在 `name` + `version` 字段
- 架构或模式细节 → 已在 `description` 字段
- 模块文件名或委托逻辑 → 已在 `functions` 字段
- 能力列表 → 已在 `summary` 字段

```
格式模板：
  "{行为角色}. {领域准则}. Mirror User's exact language and script variant.\nAlign: Human Sovereignty and Wellbeing."

正例：
  "Personal expense tracking assistant. Prioritize numerical precision.
   Protect user financial privacy. Mirror User's exact language and script variant.
   Align: Human Sovereignty and Wellbeing."

反例：
  "Expense Tracker v1.0.0. Pattern B router: delegate data operations
   to record.aisop.json. Mirror User's exact language and script variant.
   Align: Human Sovereignty and Wellbeing."
   ↑ 包含产品名+版本(name)、架构(description)、文件名(functions)
```

### 2.4 output_mode 输出模式规则

规则：`output_mode` 定义 Agent 结构化输出格式（L0）和面向用户的输出格式（L1）。

**字段结构**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `L0` | string | 是 | 结构化 JSON 输出格式及 schema |
| `L1` | string | 是 | 输出层语言规则（含有益性指令） |
| `output` | string | 是 | 最终输出层级：`"L1"` 或 `"L0+L1"` |

**默认 L0**：`"Output JSON in ENGLISH: {intent, confidence, route, state, op}"` — 结构化执行证据，包含 5 个标准字段。

**默认行为**：当 `output_mode` 缺失时，使用运行时 Agent 的默认输出模式。这保证了与现有 AISOP 文件的向后兼容。

**安全覆盖规则**：模块 `id` 包含 "safety" 或在 system content 中标记 `security: true` 的模块，其 `output_mode.output` 必须锁定为 `"L1"`。全局或父级的 `output: "L0+L1"` 设置不传播到安全模块。这防止安全检测逻辑暴露给用户。

### 2.5 loading_mode 加载策略规则

规则：`loading_mode` 控制运行时 Agent 如何加载文件中的 function 定义。

| 模式 | 行为 | 适用场景 |
|------|------|----------|
| `normal`（默认） | 一次性注入所有 functions | 节点数 ≤15，token 预算充足 |
| `node` | 仅提供第一个节点的 function，AI 通过 `SOULBOT_CMD` 按需请求后续节点 | 大文件（>15 节点），token 受限环境 |

**默认行为**：当 `loading_mode` 缺失时，默认为 `"normal"`。

**Generator 规则**：Creator 生成的每个 `.aisop.json` 和 `.aisip.json` 文件的 system content 中必须包含 `"loading_mode": "normal"`。

---

## 3. AIAP.md 规则

每个 `{name}_aiap/` 目录**必须**包含 AIAP.md 文件。AIAP.md 是项目的治理契约和发现入口。

### 3.1 必需字段 (YAML frontmatter)

**治理字段 (6 个)**:

| 字段 | 类型 | 说明 |
|------|------|------|
| `protocol` | string | AIAP 版本号，如 `"AIAP V1.0.0"` |
| `authority` | string | 治理权威域，固定为 `aiap.dev` |
| `seed` | string | 语言种子域：`aisop.dev`（AISOP 程序）或 `aisip.dev`（AISIP 程序）。必须与 `flow_format` 对齐：AISOP→aisop.dev，AISIP→aisip.dev。DUAL 模式下每个目录使用各自的 seed |
| `executor` | string | 执行平台域，固定为 `soulbot.dev` |
| `axiom_0` | string | 核心公理，固定为 `Human_Sovereignty_and_Wellbeing` |
| `governance_mode` | string | `NORMAL` 或 `DEV` |

**项目字段 (8 个)**:

| 字段 | 类型 | 说明 |
|------|------|------|
| `name` | string | 项目名称 (snake_case) |
| `version` | string | 当前版本 (semver, 与 main.aisop.json 或 main.aisip.json 同步) |
| `pattern` | string | 结构模式 `A\|B\|C\|D\|E\|F\|G` |
| `flow_format` | string | 流图序列化格式：`AISOP`（Mermaid）或 `AISIP`（JSON flow dict）。DUAL 模式下每个目录的 AIAP.md 声明各自格式 |
| `summary` | string | 简洁功能概述（建议 ≤500 字符） |
| `tools` | list/object | 工具声明 (见 §3.3) |
| `modules` | list | 模块清单 (见 §3.4) |
| `license` | string | SPDX 许可证标识符或 `proprietary`（见 Appendix B） |

### 3.2 可选字段 (YAML frontmatter)

**基础可选字段**:

| 字段 | 类型 | 说明 |
|------|------|------|
| `governance_hash` | string | 治理哈希 (见 §18) |
| `quality` | object | `{weighted_score, grade, last_pipeline}` |
| `description` | string | Agent Skills 兼容字段 — 技能描述 |
| `tags` | list | 分类标签 |
| `author` | string | 作者信息 |
| `copyright` | string | 版权声明（如 `"Copyright 2026 AIXP Foundation AIXP.dev"`） |
| `tool_dirs` | list | Pattern G 工具目录声明 (见 §9 Pattern G) |
| `capabilities` | object | 运行时能力声明 `{offered, required}` |

**安全与运行时可选字段** (Part III):

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `trust_level` | number (1-4) | 3 | 信任层级 (见 §16) |
| `permissions` | object | null | 权限边界 (见 §17) |
| `runtime` | object | null | 运行时约束 (见 §19) |

**工程化可选字段** (Part IV):

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `status` | string | "draft" | 生命周期状态 (见 §23) |
| `deprecated_date` | string | null | 弃用日期 |
| `successor` | string | null | 替代程序名 |
| `intent_examples` | list | [] | 语义路由锚点 (见 §21) |
| `discovery_keywords` | list | [] | 关键词索引 |
| `dependencies` | list | [] | 跨项目依赖 (见 §22) |
| `min_protocol_version` | string | null | 最低协议版本 (见 §25) |
| `benchmark` | object | null | 质量基准声明 |
| `identity` | object | null | 程序身份与来源 (见 I11) — `{ program_id, publisher, verified_on }` |

### 3.3 tools 字段规范

**简洁格式** (向后兼容):

```yaml
tools: [file_system, shell]
```

**结构化格式** (推荐):

```yaml
tools:
  - name: file_system
    required: true
    min_version: "1.0"
  - name: shell
    required: false
    fallback: "degrade"       # 不可用时降级运行
```

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `name` | string | (必需) | 工具名称 |
| `required` | boolean | true | 是否为必需工具 |
| `min_version` | string | null | 最低版本要求 |
| `fallback` | string | null | 不可用时的降级策略: `"degrade"` / `"skip"` / `"error"` |

### 3.4 modules 字段规范

```yaml
modules:
  - id: health_tracker.record
    file: record.aisop.json
    nodes: 7
    critical: true              # 是否为关键模块 (默认 true)
    idempotent: true            # 是否幂等 (默认 false)
    side_effects: [file_write]  # 副作用声明 (默认 [])
```

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `id` | string | (必需) | 模块唯一标识 `{project}.{module}` |
| `file` | string | (必需) | 文件名 |
| `nodes` | number | (必需) | 功能节点数 |
| `critical` | boolean | true | 失败时是否触发 FATAL (见 §20) |
| `idempotent` | boolean | false | 重复执行是否安全 |
| `side_effects` | list | [] | 副作用列表: `file_write`, `file_delete`, `api_call`, `shell_exec` |

空 `side_effects` 列表 = 纯函数 (无副作用)。

### 3.5 Markdown Body

**必需节**:

| 节 | 内容 |
|---|------|
| **治理声明** | 声明遵循 AIAP 协议 + Axiom 0 对齐 |
| **功能概述** | 按模块/意图列出核心功能 |
| **使用方式** | 入口文件、工具需求、前置条件 |

**推荐节** (status=active 时):

| 节 | 内容 |
|---|------|
| **示例交互** | 1-3 个典型使用场景的输入/输出示例 |
| **适用条件** | 明确程序适用和不适用的场景 |

**可选节**:

| 节 | 内容 |
|---|------|
| **数据存储** | 数据文件路径和格式 |
| **配置说明** | 可配置参数和默认值 |
| **质量状态** | ThreeDimTest 分数、Pipeline 历史 |
| **版本历史** | 主要版本变更摘要 (结构化格式见 §25) |
| **错误处理** | 常见错误及用户处理方式 |

**文件末尾**: 必须以 AIAP 闭环印章结尾。

| governance_mode | 印章格式 |
|----------------|---------|
| NORMAL | `Align: Human Sovereignty and Wellbeing. Version: AIAP V1.0.0. www.aiap.dev` |
| DEV | `[L0_BOOT: Success] [L1_REPORT: Success] [endNode_Align: Human Sovereignty and Wellbeing]. Version: AIAP V1.0.0. www.aiap.dev` |

### 3.6 Creator 自动维护规则

| 触发事件 | Creator 行为 |
|---------|-------------|
| **Create** | 自动生成 AIAP.md，所有必需字段填充，status 设为 draft |
| **Evolve** | 更新 version、modules、quality、summary (如有变化) |
| **Modify** | 更新 version、quality |
| **Validate** | 检查 AIAP.md 存在性和字段完整性 (D8 检查) |
| **QualityGate 通过** | 若 status=draft，自动升级为 active |
| **version_history snapshot** | 在 `{version}/` 目录中保存 AIAP.md 快照 |

---

## Part II: 结构规范

---

## 4. 节点 = 功能职责

> 节点匹配功能，main 路由分发，模块自包含，共享逻辑单独提取，不无限拆分。

每个 Mermaid 节点代表模块的一个功能职责，类似 Python 文件中的一个函数。节点数由功能复杂度自然决定，不由外部硬限强加。

```
Python 类比：
  record.py 有 4 个函数 → record.aisop.json 有 4 个功能节点
  query.py 有 6 个函数  → query.aisop.json 有 6 个功能节点
  节点数跟随功能，不跟随配额
```

---

## 5. 功能节点计数

```
功能节点 = Mermaid 总节点 - Start - endNode
```

Start 和 endNode 是每个 AISOP 文件的固定结构框架 (类似 Python 的 `if __name__`)，不反映功能复杂度，不计入节点数。

示例：

```
graph TD
    Start --> Parse --> Validate{OK?} --> Save --> Alert --> endNode
                                       --> AskFix --> Parse
```

总节点 7，功能节点 5 (Parse, Validate, Save, Alert, AskFix)。

---

## 6. 渐进式节点建议

适用于所有 `.aisop.json` 文件 (包括 main):

```
功能节点 3-12  → 正常，无提示
功能节点 13-15 → ADVISORY — 建议检查拆分机会，给出具体建议
功能节点 16+   → RECOMMENDED — 强烈建议拆分，给出拆分方案
```

- 两级都是 WARNING，不是 FAIL
- 功能内聚的大模块可标注 `fractal_exempt` 跳过建议
- 最小要求: >=3 功能节点 + (>=1 tool call OR >=3 steps)

---

## 7. fractal_exempt 标注

当模块功能节点超过 12 但流程高度内聚时，可在 `system.content` 中标注：

```json
{
    "fractal_exempt": "Pipeline 的 13 个阶段是连续管道，拆分导致上下文碎片化"
}
```

标注后 Creator 跳过该文件的渐进式拆分建议。等价于 Python 的 `# noqa`。

## 7.1. sub_mermaid 分解规则

当模块复杂度超过阈值但拆分为独立文件会破坏功能内聚性时，使用 sub_mermaid 分解——在单个 `.aisop.json` 文件内放置多个 Mermaid 图。

### 7.1.1. 结构

`aisop` 对象包含多个图键。`main` 始终是入口点：

```json
{
  "aisop": {
    "main": "graph TD\n    Start[...] --> SubA[aisop.sub_a]\n    SubA --> SubB[aisop.sub_b]\n    ...",
    "sub_a": "graph TD\n    SubAStart[...] --> ...",
    "sub_b": "graph TD\n    SubBStart[...] --> ..."
  }
}
```

规则：
- 入口点：始终是 `ASSERT RUN aisop.main`（instruction 不可变常量）
- main 图通过 `NodeName[aisop.sub_name]` 语法引用子图
- 所有子图的函数共享单一扁平 `functions` 字典
- 参数在根级别定义一次，所有子图共享
- 每个子图有独立的 Start 节点和 End 节点

### 7.1.2. 分解优先级

当复杂度超过 §6 阈值时，按以下顺序分解：

```
优先级 0 — sub_mermaid（同文件子图分解）
  同文件、共享上下文、无需跨文件契约。
  优先使用条件：
    (a) 节点共享参数和工作上下文
    (b) 子图有数据依赖（一个的输出是下一个的输入）
    (c) 拆分为文件会重复共享的解析/初始化逻辑

优先级 1 — sub_aisop（文件级拆分）
  按 §13 拆分规则。适用条件：
    (a) 子图使用完全不同的工具集（§13 优先级 1）
    (b) 子图可独立测试和部署
    (c) sub_mermaid 后单个子图仍超过 16 个功能节点

优先级 2 — Sub_AIAP（目录级拆分）
  按 §13 规则。适用于 sub_aisop 文件构成完整独立程序时。
```

### 7.1.3. 执行模式

子图以以下模式之一执行。在 `fractal_exempt` 中声明模式：

| 模式 | 说明 | 示例 |
|------|------|------|
| **互斥路由** | main 每次调用只路由到一个子图 | advisor: 8 子图，TypeGate 选 1 |
| **顺序阶段** | main 按固定顺序调用子图，逐个传递 | generate: scaffold → content → tooling |
| **条件分支** | main 根据运行时条件选择子图子集 | （未来使用） |
| **混合模式** | 组合以上模式（例如顺序阶段中某阶段使用条件路由） | （未来使用） |

### 7.1.4. 节点计数规则

对于使用 sub_mermaid 的文件：

1. **总功能节点** = 各子图功能节点之和。
   每图功能节点 = 该图总节点 − Start − endNode。

2. **单路径最大节点数** = 最长执行路径中遍历的功能节点：
   - 互斥路由：main 功能节点 + max(各子图功能节点)
   - 顺序阶段：main 功能节点 + sum(所有子图功能节点)
   - 条件分支：main 功能节点 + sum(选中子图功能节点)

3. **阈值适用**：将 §6 阈值应用于单路径最大值，而非总节点数。
   如果单路径最大值超过 16，需要 `fractal_exempt` 标注。

4. **fractal_exempt 格式**（sub_mermaid 文件）：
   `"{total} functional nodes distributed across {N} sub_mermaid sub-graphs
   ({breakdown}). Sub-graphs execute {mode}. Maximum single-path execution
   {max} nodes."`

### 7.1.5. 函数体复杂度（第二维度）

节点计数无法捕捉函数内部复杂度（例如，单个 Generate 节点的 step1 包含 23 条指令）。应用第二维度检查：

- **函数步骤数**：统计 step 键数量（step1, step2, ..., stepN）
- **步骤指令数**：统计单个步骤中的命名指令块（以 大写标签: 模式识别，如 "TOOL ANNOTATIONS:"、"INCREMENTAL GENERATION:"）

阈值：
- 单函数 8+ 步骤 → ADVISORY：建议 sub_mermaid 分解
- 单步骤 15+ 指令 → ADVISORY：建议拆分为多个函数
- 单步骤 20+ 指令 → RECOMMENDED：通过 sub_mermaid 或文件拆分分解

---

## 8. Pattern 选择

```
独立功能数 → Pattern：
  1 个功能            → A: Script (单文件)
  2+ 个功能           → B: Package (多文件)
  2+ 功能 + 复杂共享   → C: Package + Shared
  子模块也需要再拆     → D: Nested Package
  带记忆层            → E: Package + Memory
  多 AIAP 程序生态系统  → F: Ecosystem
  带嵌入式工具目录      → G: Embedded Runtime
```

---

## 9. Pattern A-G 详细定义

### Pattern A: Script

```
{name}_aiap/
├── AIAP.md                     # 必需：治理契约
└── main.aisop.json             # 全部逻辑
```

适用: todo list, timer, calculator 等单一功能。无硬限。渐进式建议适用。

### Pattern B: Package

```
{name}_aiap/
├── AIAP.md                     # 必需：治理契约
├── main.aisop.json             # 路由器：意图识别 → 分发
├── {func1}.aisop.json          # 功能模块 (完全自包含)
├── {func2}.aisop.json
└── {func3}.aisop.json
```

示例：
```
expense_tracker_aiap/
├── AIAP.md                     # 治理契约
├── main.aisop.json             # 意图：record / query / budget / report
├── record.aisop.json           # 验证 → 写入 → 确认
├── query.aisop.json            # 解析 → 读取 → 过滤 → 格式化
├── budget.aisop.json           # 设置 → 检查 → 提醒
└── report.aisop.json           # 聚合 → 分析 → 展示
```

### Pattern C: Package + Shared

```
{name}_aiap/
├── AIAP.md                     # 必需：治理契约
├── main.aisop.json             # 路由器
├── {func1}.aisop.json
├── {func2}.aisop.json
└── shared.aisop.json           # 被 2+ 模块调用的复杂共享逻辑
```

shared 规则: 只在 2+ 模块复用**复杂操作**时创建。简单共享 (格式/风格) 写在各模块 system_prompt 里。

### Pattern D: Nested Package

```
{name}_aiap/
├── AIAP.md                     # 必需：治理契约
├── main.aisop.json             # 顶级路由器
├── {simple_func}.aisop.json    # 简单模块
└── {complex}_sub_aiap/         # 复杂模块 (有子结构)
    ├── AIAP.md                 # 子包治理契约 (如果独立发布)
    ├── main.aisop.json         # 子路由器
    ├── {sub1}.aisop.json
    └── {sub2}.aisop.json
```

嵌套规则: 最多 2 层，只在子模块本身有 2+ 个子功能时才嵌套。

#### Pattern D 实例: AIAP Creator

```
aiap_creator_aiap/
├── AIAP.md                     # 治理契约 (AIAP V1.0.0)
├── main.aisop.json             # 顶级编排器 (28 功能节点, fractal_exempt)
│   └── 意图: Create, Evolve, Modify, Validate, Simulate, Compare, Explain, General
│   └── Pipeline: Research→Evolve→Generate→Modify→QualityGate→Validate→Simulate→Observability→Review
├── generate.aisop.json         # 生成器 (11 功能节点)
├── research.aisop.json         # 共享研究模块 (15 功能节点, fractal_exempt, 3 模式复用)
├── review.aisop.json           # 审查器 (11 功能节点)
├── simulate.aisop.json         # 模拟器 (10 功能节点)
├── modify.aisop.json           # 修改器 (10 功能节点)
├── observability.aisop.json    # 遥测分析 (9 功能节点)
├── advisor.aisop.json          # 高级顾问 (52 功能节点, fractal_exempt, 8 子图互斥)
├── AIAP_Standard.core.aisop.json         # 核心质量标准 (C1-C7, I1-I7, D1-D7, PL1-PL12, PL19-PL21, MF1-MF9)
├── AIAP_Standard.security.aisop.json     # 安全扩展 (I8-I11, I13 Embedded Code Safety, D8-D10, AT1-AT6, Code Trust Gate)
├── AIAP_Standard.ecosystem.aisop.json    # 生态扩展 (MF10-MF14, MF16, K1-K10, PL16-PL17, PL22, PL25)
├── AIAP_Standard.performance.aisop.json  # 性能扩展 (PL13-PL15, PL18-PL21, PL23-PL24, QRG1-QRG5)
└── AIAP_Protocol.md            # 结构规范 (Protocol-level)
```

特点:
- 8+4 个模块 (8 个可执行模块 + 4 个 STANDARD 扩展文件)，共约 146 个功能节点
- main 是纯编排器 (连续委托，无业务逻辑)，标注 fractal_exempt
- research 通过 ModeGate 复用 3 种模式 (structure/quality/compliance)，标注 fractal_exempt
- advisor 使用 sub_mermaid 子图 (8 个互斥子图)，实际单路径最大 15 节点（main 8 + 最大子图 7）
- 通信拓扑为星型 (main 编排)，模块间无直接通信

### Pattern E: Package + Memory

```
{name}_aiap/
├── AIAP.md                     # 必需：治理契约
├── main.aisop.json             # 路由器
├── {func1}.aisop.json
├── {func2}.aisop.json
└── memory/                     # 记忆层
    ├── schema.json             # 记忆字段定义 (episodic/semantic/working)
    ├── decay_config.json       # 衰减策略参数
    └── context_manager.json    # 上下文预算和加载策略
```

适用: 需要跨会话记忆、个性化、RAG 检索的 AIAP 程序。使用 advisor.aisop.json (advisor_type='memory') 生成 memory/ 目录内容。

### Pattern F: Ecosystem

```
{ecosystem_name}/
├── AIAP.md                     # 必需：生态系统级治理契约
├── blueprint.json              # 生态系统蓝图 (组件、接口、拓扑)
├── {component1}_aiap/          # 独立组件 (Pattern A-E)
│   ├── AIAP.md                 # 必需：组件级治理契约
│   └── main.aisop.json
├── {component2}_aiap/
│   ├── AIAP.md
│   └── ...
└── shared/                     # 跨组件共享的数据契约
    └── data_contracts.json
```

适用: 3+ 个 AIAP 程序组件协作的复杂系统。使用 advisor.aisop.json (advisor_type='orchestrate') 设计生态系统蓝图。

#### blueprint.json 组件接口声明

```json
{
    "ecosystem": "soulbot_ecosystem",
    "protocol": "AIAP V1.0.0",
    "components": ["component_a_aiap", "component_b_aiap"],
    "interfaces": [
        {
            "name": "health_data_query",
            "provider": "component_a_aiap",
            "consumer": "component_b_aiap",
            "contract": "shared/data_contracts.json#health_query",
            "mode": "sequential"
        }
    ]
}
```

### Pattern G: Embedded Runtime

```
{name}_aiap/
├── AIAP.md                     # 必需：治理契约 (含 tool_dirs 字段)
├── agent_card.json             # 程序自描述 (P11 起无条件生成)
├── main.aisop.json             # 路由器
├── {func1}.aisop.json
├── {func2}.aisop.json
├── python_tools/               # Python 工具实现
│   ├── README.md               # 必需：工具说明、接口、安全约束
│   ├── requirements.txt        # 冻结版本 (== 固定，禁止 >=/*~=)
│   ├── *.py                    # 工具代码
│   └── mcp_adapter.py          # Creator 自动生成的 MCP stdio 端点
├── ts_tools/                   # TypeScript 工具实现
│   ├── README.md
│   ├── package.json            # 精确版本 (禁止 ^~)
│   ├── package-lock.json       # 锁定传递依赖
│   └── *.ts
├── go_tools/                   # Go 工具实现
│   ├── README.md
│   ├── go.mod + go.sum         # 依赖锁定
│   └── bin/tool                # 预编译二进制 (推荐)
├── rust_tools/                 # Rust 工具实现
│   ├── README.md
│   ├── Cargo.toml + Cargo.lock
│   └── target/release/tool     # 必须预编译
├── shell_tools/                # Shell 脚本 (仅 T4 + 人工审计)
│   ├── README.md
│   └── tool.sh / tool.ps1
├── mcp_tools/                  # MCP Server 定义层
│   ├── README.md
│   └── mcp_server.json         # MCP Server 清单 + 运行时声明
├── a2a_tools/                  # A2A 桥接配置层 (可选，仅 Pattern F/G)
│   ├── README.md
│   └── bridge_config.json
├── n8n_tools/                  # n8n 工作流自动化层 (可选)
│   ├── README.md
│   ├── workflow.json
│   └── config.json
├── aiap_tools/                 # AIAP 子程序工具 (可选)
│   ├── README.md               # 必需：子程序清单、调用接口、安全约束
│   ├── data_cleaner_aiap/      # 作为工具使用的完整 AIAP 程序
│   │   ├── AIAP.md
│   │   ├── main.aisop.json
│   │   └── transform.aisop.json
│   └── report_gen_aiap/        # 另一个 AIAP 程序
│       ├── AIAP.md
│       └── main.aisop.json
├── other_tools/                # 开放扩展层 (可选)
│   └── README.md               # 必需：调用方式、接口、安全约束
└── memory/                     # Pattern E 记忆层 (可选)
    └── ...
```

继承: Pattern E 或 F 的所有规则

额外要求:
- AIAP.md 必须包含 `tool_dirs` 字段声明工具目录
- `mcp_tools/mcp_server.json` 必须存在
- I13 Embedded Code Safety 规则适用 (10 项子检查)
- MF16 Tool Directory Consistency 规则适用
- 最低信任层级: T3
- 需要 Code Trust Gate 验证

特性:
- CLI 执行器有原生 shell 工具，可直接执行捆绑代码
- 无需中间层或预装工具
- 自包含、可独立部署

#### tool_dirs 支持的工具目录类型

| 类型 | 运行时 | 依赖锁定 | 适用场景 |
|------|--------|---------|---------|
| `python_tools/` | Python 3.9-3.13 | `requirements.txt` (== 固定) | 数据处理、AI/ML、文件操作 |
| `ts_tools/` | Node.js/Deno/Bun | `package-lock.json` | Web API、JSON 处理、类型安全 |
| `go_tools/` | Go 或预编译二进制 | `go.sum` | 高并发、CLI、低延迟 |
| `rust_tools/` | 预编译二进制 | `Cargo.lock` | 高性能、内存安全、WASM |
| `shell_tools/` | bash / pwsh | 无 | 系统脚本 (仅 T4) |
| `mcp_tools/` | stdio transport | `mcp_server.json` | MCP 生态工具 |
| `a2a_tools/` | A2A 协议 | `bridge_config.json` | Agent 间协作（桥接配置，仅 Pattern F/G） |
| `n8n_tools/` | n8n 实例 | `workflow.json` | 多服务集成 |
| `aiap_tools/` | AIAP Executor | `AIAP.md` (每个子程序) | AIAP 程序作为可调用工具 |
| `other_tools/` | 自定义 | README.md | 开放扩展 |

#### mcp_server.json 格式

```json
{
  "schema_version": "mcp-1.0",
  "server_id": "file:///./mcp_tools",
  "transport": "stdio",
  "runtime": "python3.11",
  "entry_point": "python_tools/mcp_adapter.py",
  "exposed_tools": [
    {
      "name": "process_data",
      "description": "Process input data and return structured result",
      "inputSchema": {
        "type": "object",
        "required": ["data"],
        "properties": {
          "data": { "type": "string" }
        }
      }
    }
  ],
  "file_hashes": {
    "python_tools/data_processor.py": "sha256_hash_value",
    "python_tools/mcp_adapter.py": "sha256_hash_value"
  },
  "governance": {
    "aiap_protocol": "AIAP V1.0.0",
    "trust_level": 3,
    "governance_hash": "filled by Creator ReviewStep"
  }
}
```

#### Code Trust Gate

Pattern G 程序加载时必须通过 Code Trust Gate 安全验证：

```
加载 Pattern G 程序
    ↓
Code Trust Gate:
  1. governance_hash 验证 (覆盖所有文件含 tool_dirs 源码)
  2. 静态分析: import/require 声明 vs permissions.network
  3. 文件哈希验证 (对照 mcp_server.json file_hashes)
  4. 信任层级检查 (Pattern G 最低 T3)
  5. 依赖锁定文件验证
    ↓
  [T3 模式] 需要人工审核确认
  [T4 模式] 自动通过
    ↓
启动 MCP Server (stdio)
    ↓
AIAP 程序执行 (通过 MCP 调用工具)
```

##### aiap_tools/ 递归 Code Trust Gate

在 Code Trust Gate 中检测到 aiap_tools/ 目录时：

```
Code Trust Gate (上述步骤 1-5)
    ↓
步骤 6: Shell 审计 (现有)
    ↓
步骤 7: 检测 aiap_tools/ 目录？
    ↓ 是
初始化 call_stack = []
将 parent.program_id 推入 call_stack
对于每个 aiap_tools/{name}_aiap/:
  1. 读取 AIAP.md — 提取 program_id, trust_level, permissions, governance_hash
  2. 循环依赖检查：如果 program_id 在 call_stack 中 → FAIL (CIRCULAR_DEPENDENCY)
  3. 将 program_id 推入 call_stack
  4. 信任天花板检查：trust_level <= parent.trust_level → 否则 FAIL
  5. 权限子集检查：permissions ⊆ parent.permissions → 否则 FAIL
  6. governance_hash 检查：重算并验证 → 否则 FAIL
  7. 递归深度检查：current_depth < 3 → 否则 FAIL
  8. 如果子程序是 Pattern G 且含 aiap_tools/ → 递归 (depth + 1)
  9. 从 call_stack 弹出 program_id（finally 语义 — 即使失败也执行）
    ↓
[任何子程序失败] → 整个 Code Trust Gate 失败
    ↓ 无 aiap_tools/ 或全部通过
继续正常 MCP Server 启动
```

#### I13 Embedded Code Safety (10 项子检查)

适用: Pattern G 程序 (含 tool_dirs)。Pattern A-F 标记 N/A。

| 子检查 | 说明 |
|--------|------|
| **(a) CODE INTEGRITY** | tool_dirs/ 所有源码/二进制文件的 SHA-256 哈希必须记录在 mcp_server.json file_hashes 中 |
| **(b) NETWORK DECLARATION** | 检测网络访问 API (requests/fetch/net/http 等)，若存在则 permissions.network.allowed 必须为 true |
| **(c) FILE SYSTEM SCOPE** | 文件写入操作不得超出 permissions.file_system.scope |
| **(d) DEPENDENCY VERSION PINNING** | Python: == 固定; TS/JS: 禁止 ^~; Go: go.sum 必须存在; Rust: Cargo.lock 必须存在 |
| **(e) MCP PROXY REQUIRED** | 所有代码工具必须通过 mcp_tools/ 层暴露，禁止执行器直接子进程执行源文件 |
| **(f) SHELL AUDIT** | shell_tools/ 存在时 trust_level 必须 ≥ T4 |
| **(g) AIAP TRUST CEILING** | aiap_tools/ 存在时：每个子程序的 trust_level 必须 <= 父程序的 trust_level |
| **(h) AIAP PERMISSION SUBSET** | aiap_tools/ 存在时：子程序 permissions.file_system.scope 必须在父程序范围内；子程序 permissions.network.endpoints 必须是父程序端点的子集 |
| **(i) AIAP RECURSION DEPTH** | aiap_tools/ 嵌套深度不得超过 3。通过遍历子程序 tool_dirs 检测嵌套 aiap_tools/ |
| **(j) AIAP GOVERNANCE HASH** | 每个子程序的 governance_hash 必须验证（重算并与 AIAP.md 声明比对） |

#### MF16 Tool Directory Consistency

适用: Pattern G 程序。

| 检查 | 说明 |
|------|------|
| **(a)** | mcp_server.json 存在于声明路径 |
| **(b)** | mcp_server.json exposed_tools 条目在 AIAP.md tools[] 中有对应声明 |
| **(c)** | AIAP.md tools[] 引用 mcp_server 的条目在 exposed_tools 中存在 |
| **(d)** | agent_card.json 存在于程序根目录且字段与 AIAP.md 一致（P11 起无条件生成） |
| **(e)** | aiap_tools/ 存在时：每个子目录必须包含有效的 AIAP.md 且 6 个必需治理字段全部存在 |
| **(f)** | 每个 aiap_tools/ 子程序的 AIAP.md 治理字段结构完整（protocol, authority, seed, executor, axiom_0, governance_mode 全部存在且非空） |
| **(g)** | 每个 aiap_tools/ 子程序的 tool_dirs 声明（如有）与子程序内实际目录结构一致 |
| **(h)** | 父程序 AIAP.md tools[] 中使用 `aiap:{name}` 前缀的条目必须在 aiap_tools/{name}_aiap/ 有对应子程序 |

#### aiap_tools/ 调用协议

aiap_tools/ 使 AIAP 程序能够将其他 AIAP 程序作为工具调用，建立原生工具级关系，无需 MCP Server 中间层。

##### 调用机制

1. 父程序在 AISOP functions 中使用 `aiap:{name}` 前缀引用子程序工具
2. Executor 检测到 `aiap:` 前缀，定位程序根目录下的 `aiap_tools/{name}_aiap/`
3. Executor 读取子程序的 `AIAP.md` 并验证信任和权限（见 Code Trust Gate 扩展）
4. Executor 在子执行上下文中加载子程序，继承约束
5. 子程序执行并返回结果给父程序的调用节点

##### 安全约束

- **信任天花板**: 子程序的 `trust_level` 必须 <= 父程序的 `trust_level`
- **权限子集**: 子程序的 `permissions` 范围必须是父程序 `permissions` 的子集
- **递归深度**: aiap_tools 最大嵌套深度为 3（父 → 子 → 孙 → 曾孙）
- **循环依赖预防**: Executor 必须维护 program ID 调用栈；如果同一 program ID 在栈中出现两次，执行必须以 CIRCULAR_DEPENDENCY 错误失败
- **治理完整性**: 子程序的 `governance_hash` 必须在执行前验证

##### 资源隔离

| 资源 | 隔离策略 |
|------|---------|
| memory/ | 子程序仅使用自己的 memory/，不可访问父程序 memory/ |
| 日志 | 子程序日志带 `[aiap:{name}]` 前缀，合并到父程序日志流 |
| 临时文件 | 子程序临时文件在 `aiap_tools/{name}_aiap/.tmp/`，执行后清理 |
| 环境变量 | 子程序不继承父程序环境变量 |
| token_budget | 子程序从父程序剩余 token_budget 中分配 |

##### 错误传播

```
子程序 GREEN        → 父程序 step 正常完成
子程序 AMBER/YELLOW → 父程序收到 WARNING，按 fallback 策略处理
子程序 RED/FAIL     → 父程序收到 ERROR，触发 Error 处理流程
子程序 TIMEOUT      → Executor 强制终止子程序，父程序收到 TIMEOUT_ERROR
```

超时由 Executor 控制（非父程序 AISOP 节点）。优先级：AISOP 函数 timeout_seconds > 子程序 AIAP.md runtime.timeout_seconds > 默认 60s。

call_stack 清理：Executor 保证失败时 pop（finally 语义）。

##### README.md 要求

aiap_tools/README.md 必须包含：

| 章节 | 内容 |
|------|------|
| 概述 | aiap_tools/ 目录用途 |
| 子程序清单 | 每个子程序：名称、摘要、Pattern、trust_level |
| 调用接口 | 调用约定 (aiap:{name})、输入/输出合约 |
| 安全约束 | 信任继承、权限边界、递归限制 |

##### 版本兼容性

- 子程序的 `min_protocol_version` 必须 <= 父程序的 `protocol` 版本
- 父程序进化时，子程序版本不会自动升级（独立生命周期）
- 父程序 AIAP.md 应在 `dependencies[]` 中声明子程序版本期望

#### 向后兼容

- tool_dirs 字段完全可选
- 无 tool_dirs 的程序 (Pattern A-F) 不受影响
- I13、MF16 对非 Pattern G 程序标记 N/A
- governance_hash 算法对非 Pattern G 程序不变

---

## 10. main.aisop.json 规则

main 遵循与功能模块相同的渐进式节点建议。区别是**质的约束** (不是量的约束):

**Pattern A**: main 是唯一文件，包含全部逻辑，无特殊约束。

**Pattern B+**: main 是路由器:
- 只包含路由逻辑 + 轻量内联处理
- 不含业务逻辑 (数据处理、文件 I/O、复杂验证)
- tools = 所有子模块 tools 的并集
- 路由节点数量由意图数量自然决定
- 调用方式: 意图识别 → 读取对应子文件 → AI Agent 执行

```
判断节点是否属于 main：
  ≤2 steps + 无工具调用 → OK (轻量内联，如 Explain、General)
  >2 steps 或 有工具调用 → 应放入 sub_aisop
```

---

## 11. 功能模块规则

- 完全自包含 (独立 system_prompt / tools / params / functions)
- 不依赖其他模块的内部实现
- 模块内部深度由功能决定，渐进式建议适用
- 最小要求: >=3 功能节点 + (>=1 tool call OR >=3 steps)

---

## 12. 独立功能判断

能用一句话描述 + 不共享专用工具/状态 + 能单独测试 → 独立成文件

- Level 1 工具 (file_system, shell) 为通用基础设施，不计入"共享工具"
- 通过 file_system 读写同一数据文件的模块仍可独立 (各自负责不同操作)
- "共享状态"指运行时内存状态或专用连接，非持久化数据文件

---

## 13. Sub_AIAP 拆分规则

当 Creator 建议拆分时，按以下优先级分析拆分边界:

```
优先级 1 — 工具边界:
  节点组 A 用 google_search + web_browser
  节点组 B 只用 file_system
  → 天然分界线，拆分为独立 sub_aiap

优先级 2 — 数据流阶段:
  线性管道中的明确阶段界限 (research → generate → test)
  → 每个阶段为 sub_aiap 候选

优先级 3 — 功能独立性:
  满足独立功能判断三条件
  → 拆分为 sub_aiap
```

**禁止拆分的模式**:
- 汇聚节点组 (多→一的扇入模式) → 保持同一 sub_aiap
- 错误恢复循环 (Error → Retry → 原节点) → 保持同一 sub_aiap
- 共享同一 tool + state 的紧密节点 → 保持同一 sub_aiap

---

## 14. Pattern 升级汇聚处理

当 Pattern A→B 升级拆分文件时，原有的汇聚/展示节点 (如 Respond、Display、Output) 需要特殊处理:

```
汇聚节点判断：
  该节点有 >2 steps 或 有工具调用？
    → 不符合 main 内联标准，必须分入子模块

  多个子模块都需要该节点的逻辑？
    → 各子模块创建自己的专用版本 (按各自输出格式定制)
    → 不创建 shared.aisop.json (除非逻辑复杂且完全相同)

  只有一个子模块使用？
    → 直接归入该子模块
```

示例:
```
Pattern A (拆分前):
  SearchRecipes → ReadRecipe → NutritionAnalysis → Respond → endNode
  SaveCollection → Respond → endNode
  CompareView → Respond → endNode
  (Respond 是全路径汇聚点，4 steps + 工具引用)

Pattern B (拆分后):
  search.aisop.json:  ...→ SearchRespond → endNode  (搜索结果展示)
  collection.aisop.json: ...→ CollectionRespond → endNode (收藏操作展示)
  (各子模块有专用 Respond，内容按模块输出定制)
```

---

## 15. 双流规则

复杂项目 (Pattern D+) 可选择提供人类版和 AI 版双文件:

```
{name}_aiap/
├── AIAP.md
├── main.human.aisop.json      # 人类可读版 (完整键名)
├── main.ai.aisop.json         # AI 优化版 (压缩键名)
└── ...
```

规则:
- 两个版本的逻辑语义必须完全一致
- `.human` 版使用完整键名，便于人类审查
- `.ai` 版使用缩写键名，减少 token 消耗
- AI Agent 优先加载 `.ai` 版，调试时加载 `.human` 版
- 非双流项目仍使用单一 `.aisop.json` (不加 `.human` 或 `.ai` 前缀)

---

## Part III: 安全与运行时

---

## 16. 信任层级

AIAP 程序通过 `trust_level` 声明其权限需求和执行模式。

### 16.1 四层信任定义

| 层级 | 名称 | 含义 | 权限范围 |
|------|------|------|---------|
| **T1** | Metadata-Only | 仅读取 AIAP.md frontmatter | 不加载 .aisop.json 内容 |
| **T2** | Instruction-Read | 可读取 .aisop.json 指令内容 | 不可执行任何工具调用 |
| **T3** | Supervised | 需要人类审批或沙箱环境执行 | 每个工具调用需确认 |
| **T4** | Autonomous | 在声明的权限边界内自主执行 | 遵循 permissions 字段约束 |

### 16.2 信任层级与功能的关系

| trust_level | 可执行的操作 | 典型用途 |
|-------------|-------------|---------|
| T1 | 读取 summary、name、description | 程序目录索引、搜索结果展示 |
| T2 | 读取完整流程图、函数定义 | 代码审查、文档生成、教学 |
| T3 | 在人类监督下执行所有工具调用 | 首次运行的新程序、高风险操作 |
| T4 | 自主执行所有声明的工具调用 | 已验证的生产程序 |

### 16.3 声明方式

```yaml
# AIAP.md frontmatter
trust_level: 3    # 默认值，可选字段
```

未声明 trust_level 时，执行器应按 T3 (Supervised) 处理。

---

## 17. 权限边界

T4 (Autonomous) 程序**必须**通过 `permissions` 声明权限边界。T1-T3 程序此字段可选。

### 17.1 声明格式

```yaml
# AIAP.md frontmatter
permissions:
  file_system:
    scope: "./data/"            # 读写范围限定 (相对于项目根目录)
    operations: ["read", "write"]
  shell:
    allowed: false              # 禁止 shell 调用
  network:
    allowed: false              # 禁止网络调用
```

### 17.2 权限类型

| 权限 | 属性 | 说明 |
|------|------|------|
| **file_system** | `scope` | 允许访问的目录 (glob 语法) |
| | `operations` | 允许的操作: `read`, `write`, `delete` |
| **shell** | `allowed` | 是否允许 shell 执行 |
| | `allowlist` | 允许的命令列表 (仅 allowed=true 时) |
| **network** | `allowed` | 是否允许网络请求 |
| | `endpoints` | 允许访问的 URL 模式列表 |

### 17.3 执行器职责

执行器 (SoulBot) 在运行 T4 程序时**必须**:
1. 读取 `permissions` 声明
2. 在工具调用前验证是否在声明范围内
3. 超范围调用 → 拒绝执行 + 报告安全违规

---

## 18. 完整性验证

### 18.1 governance_hash 算法

```
governance_hash = SHA-256(
    所有 .aisop.json 文件内容 (按文件名字母序拼接, CRLF→LF 规范化)
)

Pattern G 扩展:
  .aisop.json 文件集不变。tool_dirs/ 文件哈希记录在 mcp_server.json
  的 file_hashes 字段中，通过 governance_hash 间接覆盖。
  无 tool_dirs 的程序 governance_hash 算法不变 (向后兼容)。
```

输出格式: `"sha256:{hash_value}"` (64 字符十六进制)

### 18.2 必需性规则

| trust_level | governance_hash |
|-------------|----------------|
| T1-T2 | 可选 |
| T3 | 推荐 |
| T4 | 推荐 |
| 已发布到 Registry | 必需 |

### 18.3 验证流程

Creator ValidateStep 执行验证:
1. 计算当前文件的 SHA-256 哈希
2. 与 AIAP.md 中声明的 governance_hash 对比
3. 不匹配 → WARNING: "Integrity check failed — files may have been modified outside Creator pipeline"

---

## 19. 运行时约束

### 19.1 声明格式

```yaml
# AIAP.md frontmatter
runtime:
  timeout_seconds: 300          # 单次执行超时 (默认: 执行器决定)
  max_retries: 3                # 最大重试次数 (默认: 3)
  token_budget: 50000           # Token 预算上限 (默认: 无限制)
  idempotent: false             # 整体是否幂等 (默认: false)
  side_effects:                 # 整体副作用声明
    - file_write
    - api_call
```

### 19.2 字段说明

| 字段 | 含义 | 用途 |
|------|------|------|
| `timeout_seconds` | 单次完整执行的超时上限 | 防止无限执行 |
| `max_retries` | RECOVERABLE 错误的最大重试次数 | 控制重试开销 |
| `token_budget` | 单次执行的 token 消耗上限 | 成本控制 |
| `idempotent` | 重复执行是否产生相同结果 | 编排器判断是否可安全重试 |
| `side_effects` | 程序整体的副作用列表 | 编排器判断执行风险 |

### 19.3 与 modules 的关系

- 程序级 `runtime.side_effects` = 所有模块 `side_effects` 的并集
- 程序级 `runtime.idempotent` = 所有 critical 模块均 `idempotent` 时为 true
- 模块级属性 (§3.4) 提供细粒度控制，程序级属性提供快速概览

---

## 20. 错误处理协议

### 20.1 错误分类

| 类别 | 含义 | 策略 |
|------|------|------|
| **RECOVERABLE** | 暂时性失败 (网络超时、文件锁、API 限流) | 按 `max_retries` 重试，指数退避 |
| **DEGRADABLE** | 非关键模块失败 (`critical: false`) | 跳过失败模块，降级执行，标记 WARNING |
| **FATAL** | 关键模块失败 (`critical: true`) 或安全违规 | 立即停止，报告错误，不产出结果 |

### 20.2 重试策略

```
重试间隔: 1s, 2s, 4s, 8s, ... (指数退避，base=2)
最大重试: runtime.max_retries (默认 3)
最大间隔: min(2^retry_count, 30) 秒
每次重试必须记录: 错误原因 + 重试次数 + 时间戳
```

### 20.3 降级行为

当模块执行失败且该模块 `critical: false` 时:
1. 跳过该模块的输出
2. 在最终结果中标记: `"DEGRADED: {module_name} skipped due to {error}"`
3. 不影响整体执行的成功/失败判定
4. 最终结果包含降级模块列表

### 20.4 终止条件

每个 AIAP 程序的执行按以下条件终止:

| 终止类型 | 条件 | 结果 |
|---------|------|------|
| **成功终止** | 所有 critical 模块执行完毕 + 输出通过验证 | 返回完整结果 |
| **超时终止** | `runtime.timeout_seconds` 到达 | 返回已完成部分 + 超时标记 |
| **错误终止** | FATAL 级错误触发 | 返回错误报告，不返回部分结果 |
| **降级终止** | 成功终止但有模块被跳过 | 返回降级结果 + 降级报告 |

---

## Part IV: 工程化能力

---

## 21. 发现协议

### 21.1 发现层次

| 层次 | 方式 | 机制 | Token 开销 |
|------|------|------|-----------|
| **L1 被动发现** | 文件系统扫描 | 扫描器遍历目录，识别包含 AIAP.md 的 `_aiap/` 目录 | ~50-80/程序 |
| **L2 语义发现** | 意图匹配 | 将用户查询与 `intent_examples` 语义相似度匹配 | 0 (预计算) |
| **L3 注册发现** | 注册中心查询 | 通过 AIAP Registry (aiap.dev) 查询已发布程序 | ~100/查询 |

### 21.2 L1 扫描协议

扫描器应按以下顺序搜索 AIAP 程序:

1. 当前工作目录下的 `*_aiap/` 子目录
2. 配置的 AIAP 库路径 (如 `~/.aiap/library/`)
3. 项目 `aiap.config` 中声明的依赖路径

对每个发现的 AIAP 程序:
1. 读取 AIAP.md YAML frontmatter (L1 元数据, ~50-80 tokens)
2. 注册到可用程序清单 (name + summary + status)
3. 仅在匹配时加载完整内容 (L2+L3)

### 21.3 L2 语义匹配

```yaml
# AIAP.md frontmatter
intent_examples:
  - "记录今天的体重"
  - "查看本周的血压趋势"
  - "生成月度健康报告"
discovery_keywords:
  - health
  - tracking
  - wellness
```

匹配流程:
1. 将 `intent_examples` 转换为嵌入向量 (embedding)
2. 新查询到来时，计算与已有向量的余弦相似度
3. 相似度超过阈值 → 候选匹配
4. 结合 `summary` + `discovery_keywords` 排序

### 21.4 调用模式

| 模式 | 触发方式 | 匹配机制 |
|------|---------|---------|
| **显式调用** | 用户指定程序名 (如 "使用 health_tracker") | 精确匹配 `name` 字段 |
| **隐式调用** | LLM 根据用户意图自动选择 | 语义匹配 `summary` + `intent_examples` |

---

## 22. 依赖解析

### 22.1 依赖声明

```yaml
# AIAP.md frontmatter
dependencies:
  - name: shared_utils_aiap
    version: "^1.0.0"           # semver 范围约束
    required: true
  - name: analytics_aiap
    version: ">=2.0.0"
    required: false              # 可选依赖
    fallback: "skip"             # 不可用时: "skip" / "degrade" / "error"
```

### 22.2 版本约束语法

| 语法 | 含义 | 匹配示例 |
|------|------|---------|
| `"1.2.3"` | 精确版本 | 仅 1.2.3 |
| `"^1.2.0"` | 兼容更新 | >=1.2.0 且 <2.0.0 |
| `"~1.2.0"` | 补丁更新 | >=1.2.0 且 <1.3.0 |
| `">=1.0.0"` | 最低版本 | >=1.0.0 |

### 22.3 解析策略

1. **扁平化解析** (默认) — 所有依赖平铺在同一层级，版本冲突时选择满足所有约束的最高兼容版本
2. **隔离解析** — Pattern F Ecosystem 中，各组件独立解析依赖，通过 `data_contracts` 交互

### 22.4 冲突解析

当多个 AIAP 程序依赖同一程序的不同版本时:
- 自动选择满足所有约束的最高版本
- 如无法满足所有约束 → 报告冲突，要求人类决策
- 冲突报告包含: 冲突依赖名、各约束来源、可选解决方案

---

## 23. 程序生命周期

### 23.1 生命周期状态

| 状态 | 含义 | AIAP.md 字段 | Creator 行为 |
|------|------|-------------|-------------|
| **draft** | 开发中，不稳定 | `status: draft` | Create 阶段自动设置 |
| **active** | 生产可用 | `status: active` | 首次通过 QualityGate 后自动升级 |
| **deprecated** | 计划弃用 | `status: deprecated` + `deprecated_date` + `successor` | 人类手动标记 |
| **archived** | 已归档，只读 | `status: archived` | deprecated_date 后 90 天自动归档 |

### 23.2 状态流转

```
draft → active → deprecated → archived
                      ↓
              (successor 接替)
```

### 23.3 弃用协议

1. 标记 `status: deprecated` + 设置 `deprecated_date`
2. 在 AIAP.md 治理声明节添加弃用通知
3. 如有替代程序，设置 `successor` 字段
4. 弃用窗口期: `deprecated_date` 后至少 90 天保持可用
5. 窗口期结束后转为 archived

### 23.4 归档协议

archived 状态的 AIAP 程序:
- 保留完整目录结构，不删除任何文件
- AIAP.md 保留完整的版本历史
- 不再接受 Evolve/Modify 操作
- 仅允许 Validate 操作 (用于审计)
- 执行器遇到 archived 程序时应返回 WARNING + 推荐 successor

---

## 24. 编排模式

AIAP 程序支持四种编排模式，通过 Mermaid 流程图中的语义标注声明。

### 24.1 模式 1: Sequential (顺序)

当前 AIAP Pipeline 已完整覆盖。模块按 Mermaid 流程图中的 `-->` 顺序执行。

```mermaid
Start --> ModuleA --> ModuleB --> ModuleC --> endNode
```

适用: Pattern A-E 的默认模式。

### 24.2 模式 2: Parallel (并发)

```mermaid
Start --> fork{并发分叉}
fork --> ModuleA
fork --> ModuleB
ModuleA --> join{汇合}
ModuleB --> join
join --> End
```

- `fork` 节点将任务分发到多个模块
- `join` 节点等待所有并发模块完成
- 各并发模块之间无数据依赖
- 适用: 独立子任务可并行处理时

### 24.3 模式 3: Conditional (条件分支)

```mermaid
Start --> Classify{分类}
Classify -->|类型A| ModuleA
Classify -->|类型B| ModuleB
Classify -->|其他| ModuleDefault
```

- 条件分支通过 Classify 节点的 `|标签|` 语法标注
- 当前 Mermaid 流程图已支持此语法，无需新增格式
- 适用: 意图路由、输入类型分发

### 24.4 模式 4: Handoff (控制权转移)

适用于 Pattern F Ecosystem 中跨组件的控制权转移:

```
handoff_context = {
    "source": "component_a_aiap",
    "target": "component_b_aiap",
    "intent": "process_health_data",
    "payload": { ... },
    "metadata": { "timestamp": "...", "trace_id": "..." }
}
```

流程:
1. 发起者将完整上下文打包为 `handoff_context`
2. 接收者从 `handoff_context` 恢复状态
3. 接收者完成后返回 `handoff_result`
4. 发起者确认结果或发起新的 handoff

---

## Part V: 质量与兼容

---

## 25. 版本兼容性

### 25.1 协议版本兼容保证

| 版本范围 | 兼容保证 |
|---------|---------|
| AIAP V1.x.y | 同一 major 版本内向后兼容 |
| AIAP V2.0.0+ | 可能引入破坏性变更，提供迁移指南 |

### 25.2 程序版本规范

AIAP 程序版本遵循 semver:

| 版本变化 | 含义 | 示例 |
|---------|------|------|
| **major** (x.0.0) | 破坏性变更 — 输入/输出格式变化 | 1.0.0 → 2.0.0 |
| **minor** (x.y.0) | 新增功能 — 向后兼容 | 1.0.0 → 1.1.0 |
| **patch** (x.y.z) | Bug 修复/改善 — 向后兼容 | 1.1.0 → 1.1.1 |

### 25.3 最低协议版本

```yaml
# AIAP.md frontmatter
min_protocol_version: "AIAP V1.0.0"
```

执行器在加载程序前检查: 若执行器支持的协议版本 < `min_protocol_version` → 拒绝加载 + 提示升级。

### 25.4 版本变更日志格式

推荐在 AIAP.md "版本历史" 可选节中使用结构化格式:

```markdown
## 版本历史

### v1.2.0 (2026-03-01)
- **新增**: 月度报告趋势分析
- **改善**: 查询性能优化

### v1.1.0 (2026-02-15)
- **新增**: 血压记录功能
- **修复**: 日期解析边界错误
```

变更类型标签: `新增` / `改善` / `修复` / `移除` / `安全`

---

## 26. 文档完整性分级

### 26.1 三级分级

| 级别 | 要求 | 适用 |
|------|------|------|
| **Level 1** (最低) | AIAP.md 必需节 (治理声明 + 功能概述 + 使用方式) | 所有 AIAP 程序 |
| **Level 2** (推荐) | + 示例交互 + 适用条件 | `status=active` 的程序 |
| **Level 3** (完整) | + 错误处理 + 版本历史 + 所有可选字段 | 公开发布到 Registry 的程序 |

### 26.2 各级别检查清单

**Level 1 (最低)**:
```
[ ] AIAP.md 存在
[ ] 13 个必需 frontmatter 字段完整
[ ] 治理声明节存在
[ ] 功能概述节存在
[ ] 使用方式节存在
[ ] 闭环印章存在
```

**Level 2 (推荐)**:
```
[ ] Level 1 全部通过
[ ] 示例交互节存在 (1-3 个场景)
[ ] 适用条件节存在 (适用 + 不适用)
[ ] quality 可选字段已填充
[ ] status = active
```

**Level 3 (完整)**:
```
[ ] Level 2 全部通过
[ ] 错误处理节存在
[ ] 版本历史节存在 (结构化格式)
[ ] trust_level 已声明
[ ] permissions 已声明 (如 trust_level >= T3)
[ ] runtime 已声明
[ ] intent_examples 已填充
[ ] governance_hash 已计算
[ ] benchmark 已填充
```

---

## Appendix A: PL24 Auto-Fix Protocol

适用: AutoFixEngine 生成修复提案时。

| 约束 | 说明 |
|------|------|
| **(a) SCOPE** | 修复限于 1-3 文件，符号变更 ≤ 10，行变更 ≤ 50 |
| **(b) CONFIDENCE** | 置信度 ≥ 0.85 时自动应用，否则作为建议需人工批准 |
| **(c) RATE LIMIT** | 每个对象每天最多 1 次自动修复，防止无限循环 |
| **(d) AUDIT** | 所有自动修复记录到 observability.lint_report |
| **(e) ROLLBACK** | 所有自动修复可回滚 (git 格式) |
| **(f) NO LOGIC CHANGE** | 仅限格式/样式/缺失声明/版本约束修复，禁止算法或业务逻辑变更 |

---

## Appendix B: PL25 License & Copyright Declaration

适用: 所有 AIAP 程序，特别是 aiap-store 分发。

### B.1 核心规则

| 规则 | 说明 |
|------|------|
| **(a) LICENSE FIELD** | AIAP.md 必须包含 `license` 字段 |
| **(b) SPDX VALIDITY** | 值必须为有效 SPDX 标识符 (如 "Apache-2.0", "MIT") 或 "proprietary" |
| **(c) PROPRIETARY** | license 为 "proprietary" 时，必须附带 `terms_url` 或 `contact` |
| **(d) STORE** | 通过 aiap-store 分发时 license 字段强制要求 |

### B.2 字段属性

| 属性 | 值 |
|------|-----|
| 字段名 | `license` |
| 类型 | `string` |
| 是否必填 | **强制**（§3.1 必需字段） |
| 默认值 | `proprietary`（未声明时视为保留所有权利） |
| 格式规范 | SPDX 标准标识符（见 https://spdx.org/licenses/ ）|

### B.2.1 伴随字段: `copyright`

| 属性 | 值 |
|------|-----|
| 字段名 | `copyright` |
| 类型 | `string` |
| 是否必填 | 可选（§3.2 可选字段） |
| 默认值 | 空（无版权声明） |
| 格式 | 自由文本版权声明（如 `"Copyright 2026 AIXP Foundation AIXP.dev"`） |

### B.3 SPDX 常用值参考

| 值 | 含义 |
|----|------|
| `MIT` | MIT 许可证（最宽松） |
| `Apache-2.0` | Apache 2.0（含专利保护） |
| `GPL-3.0` | GPL v3（强 copyleft） |
| `proprietary` | 专有/保留所有权利 |
| `CC-BY-4.0` | 知识共享署名（适合文档类程序） |

### B.4 默认值行为

- `license` 字段**强制**（§3.1 必需字段）
- 用户创建时未指定，默认为 `proprietary`
- `copyright` 字段**可选** — 省略时，在 AIAP.md 中写入空占位符以便发现
- 不影响现有程序运行（向后兼容）

### B.5 `proprietary` 附加要求

当 `license: proprietary` 时，必须附带以下字段之一：

```yaml
license: proprietary
terms_url: https://example.com/terms   # 或
contact: author@example.com            # 至少一项必填
```

### B.6 aiap-store 上架集成

aiap-store 注册条目直接从 AIAP.md 读取 `license` 字段展示：

```json
{
  "program_id": "publisher.domain/program_name",
  "version": "1.0.0",
  "license": "MIT",
  "store_url": "https://aiap.store/programs/publisher.domain/program_name"
}
```

上架检查：
- 缺少 `license` 字段 → Store 注册 API 返回错误，拒绝上架
- `license: proprietary` 但无 `terms_url`/`contact` → 拒绝上架

### B.7 向后兼容保证

| 场景 | 行为 |
|------|------|
| 现有无 `license` 字段的程序 | 正常运行，默认视为 `proprietary`（建议补充字段以符合规范） |
| 本地使用但不上架 Store | 完全不受影响 |
| 提交 Store 但未填 `license` | Store 注册 API 返回错误，拒绝上架 |
| 无 `copyright` 字段的程序 | 正常运行，无影响（可选字段） |

---

## Appendix C: Category M — Tool Directory Simulation Scenarios

适用: Pattern G 程序。

| 场景 | 说明 |
|------|------|
| M1 | 正常 MCP Server 启动和工具调用 |
| M2 | MCP Server 启动失败，降级处理 |
| M3 | Python 依赖安装失败 |
| M4 | MCP Server 工具调用超时 |
| M5 | governance_hash 不匹配 (Code Trust Gate 拦截) |
| M6 | ZIP SLIP 攻击 (tool_dirs 中的恶意路径) |
| M7 | 网络权限违规 (未声明的 import requests) |
| M8 | 依赖版本未固定 (TS ^ 前缀检测) |
| M9 | go.sum 缺失 |
| M10 | Rust 预编译二进制哈希不匹配 |
| M11 | shell_tools 存在但 trust_level < T4 |
| M12 | 多语言 MCP Server 部分启动失败 |
| M13 | aiap_tools 子程序正常加载和执行 | 预期: **PASS** |
| M14 | aiap_tools 子程序 AIAP.md 缺失或无效 | 预期: **FAIL** (INVALID_AIAP_MD) |
| M15 | aiap_tools 子程序 trust_level > 父程序（应拦截） | 预期: **FAIL** (TRUST_CEILING_VIOLATION) |
| M16 | aiap_tools 子程序 governance_hash 不匹配 | 预期: **FAIL** (INTEGRITY_VIOLATION) |
| M17 | aiap_tools 递归深度超限（>3 层） | 预期: **FAIL** (RECURSION_DEPTH_EXCEEDED) |
| M18 | aiap_tools 子程序 permissions 超出父程序范围 | 预期: **FAIL** (PERMISSION_VIOLATION) |
| M19 | aiap_tools 循环依赖检测（A→B→A） | 预期: **FAIL** (CIRCULAR_DEPENDENCY) |
| M20 | aiap_tools 子程序版本与父程序协议不兼容 | 预期: **FAIL** (PROTOCOL_VERSION_INCOMPATIBLE) |

---

## Appendix D: NO_SELF_MODIFY 规则

AIAP 程序禁止在运行时修改自身的治理文件。本规则无条件适用于所有 AIAP 程序。

### D.1 核心规则

> AIAP 程序不得在运行时修改自身的治理文件。对 AIAP 程序的任何结构性变更必须通过 Creator Pipeline 的完整流程（包括人类确认的 EvolveStep）。违反本规则等同于 Axiom 0 违规。

### D.2 受保护文件（黑名单）

| 文件模式 | 说明 |
|------|------|
| `*.aisop.json` | 所有模块文件 |
| `AIAP.md` | 项目治理合约 |
| `quality_baseline.json` | 质量基线数据 |
| `agent_card.json` | Agent Card 元数据 |
| `.version_history/*` | 版本历史记录 |
| 任何被 `governance_hash` 覆盖的文件 | 完整性保护文件 |

### D.3 允许写入（白名单）

| 文件 | 条件 |
|------|------|
| `insights.json` | 仅当 insights 机制启用时（见 Appendix E），受写入约束限制 |
| 程序数据文件 | 在 `side_effects` 中声明的文件（如用户数据、状态文件） |

### D.4 原理

1. 自修改 = 脱离人类主权控制 (Axiom 0)
2. 自修改 = governance_hash 失效 = 治理链断裂
3. 自修改 = 绕过 15 阶段 Pipeline 的审计保障
4. LLM 幻觉 + 自修改 = 错误判断直接成为代码变更

### D.5 独立性

NO_SELF_MODIFY 与 INSIGHTS 机制无关。即使未启用 INSIGHTS，自修改禁令始终生效。

---

## Appendix E: INSIGHTS 机制 — 可选运行时洞察记录

一种可选机制，允许 AIAP 程序在运行时或 Pipeline 执行期间记录结构性观察。默认：未启用。

### E.1 激活

```yaml
# 在 AIAP.md 可选字段中：
insights: true
# 或
insights:
  sources: [pipeline, runtime]  # 选择一个或两个
```

当 AIAP.md 中不存在 `insights` 字段时，该机制不启用（零开销）。

### E.2 insights.json Schema

```json
{
  "program": "{program_name}",
  "version": "{current_version}",
  "warning": null,
  "insights": [
    {
      "id": "INS-001",
      "fingerprint": "string (确定性, 来自 title)",
      "category": "BUG | FUNC | ARCH | PERF | DEBT | USER | SEC | COMP",
      "severity": "HIGH | MEDIUM | LOW",
      "source": "runtime | pipeline:{stage_name}",
      "title": "string",
      "observation": "string (≤250 字符)",
      "impact": "string",
      "suggestion": "string (≤250 字符)",
      "status": "OPEN | ADOPTED | WONTFIX",
      "created": "YYYY-MM-DD",
      "occurrences": [
        { "version": "string", "mode": "EVOLVE | RUNTIME", "date": "YYYY-MM-DD" }
      ]
    }
  ]
}
```

### E.3 类别定义

| 类别 | 代码 | 说明 |
|------|------|------|
| 程序缺陷 | BUG | 功能错误、逻辑矛盾、数据流断裂 |
| 功能缺口/冗余 | FUNC | 缺失或过时的功能 |
| 架构冲突 | ARCH | 模块职责重叠、循环依赖 |
| 性能与资源 | PERF | 响应延迟、token 预算压力、资源浪费 |
| 技术债务 | DEBT | 累积的结构妥协、固化的临时方案 |
| 用户需求信号 | USER | 用户行为模式暗示的未满足需求 |
| 安全与隐私 | SEC | 数据泄露风险、权限违规、注入向量 |
| 合规 | COMP | 协议违规、治理链断裂 |

### E.4 写入约束

| 写入方 | 权限 |
|------|------|
| 运行时 (insights.aisop.json / executor) | 严格追加模式：只能添加新条目或追加 occurrences。不能修改/删除现有条目或更改 status。 |
| Creator Pipeline (advisor insights 子图) | 可管理：添加条目、修改 status (OPEN→ADOPTED/WONTFIX 需人类确认)、将非 OPEN 条目归档到 .version_history/ |

### E.5 指纹去重

```
fingerprint = lowercase(title).replace(/[^a-z0-9_\u4e00-\u9fff]/g, '_').truncate(50)
```

相同 fingerprint → 不添加新条目，追加到现有条目的 `occurrences` 数组。

### E.6 反膨胀控制

| 层级 | 机制 |
|------|------|
| L1: 单条目 | observation + suggestion 合计 ≤ 500 字符 |
| L2: 总量 | OPEN 条目上限 20 条；超出时设置 `warning` 字段 |
| L3: 版本归档 | EVOLVE 时将非 OPEN 条目归档到 `.version_history/v{old}/insights_archive.json` |

### E.7 insights.json 不计入 governance_hash

insights.json 是动态运行时/Pipeline 产物，不属于静态程序定义。governance_hash 仅覆盖 .aisop.json 静态文件。

### E.8 打包

打包为 .aiap 时：`insights.aisop.json` 包含（模块代码），`insights.json` 排除（运行时数据）。

---

## 附录 F：节点门控 — 节点级执行断言

### F.1 目的

AI 在执行多节点 AISOP 程序时倾向于跳过节点，即使存在全局执行规则（如 `strict_semantics: zero_skip`）。全局规则在开头声明一次，随上下文增长影响力衰减。节点门控通过**在每个节点入口插入断言 (assertion)**，在每一步刷新 AI 注意力。

这不是 `strict_semantics` 的替代 — 而是全局规则的**逐节点具体化**。`strict_semantics` 声明意图，节点门控在每个节点边界断言执行。

### F.2 机制

每个非起点节点的第一个步骤 (S1) 必须以断言开头：

**单前驱**（线性链）：
```
[ASSERT] {prev_node} executed. If false → go back to {prev_node}. | {step work}
```

**多前驱**（汇聚点 — 节点有 2+ 条 Mermaid 入边）：
```
[ASSERT] {nodeA}∨{nodeB}∨{nodeC} executed. If false → go back to {primary_predecessor}. | {step work}
```

断言与步骤工作以 `|` 分隔并合并为一个步骤 — 无需 `Do not proceed` 终止符，因为回溯指令本身已隐含不继续。`|` 分隔符清晰地划分门控与步骤的正常工作。

`∨`（逻辑 OR）运算符表示：至少一个列出的前驱节点必须已执行。适用于从多条路径可达的汇聚点（如回路边、条件分支合并）。

**前驱推导规则：**

1. **真实来源**：解析 Mermaid `graph TD` 定义。每条边 `A --> B` 或 `A -- label --> B` 使 `A` 成为 `B` 的前驱
2. **单入边**：直接使用 `{prev_node}` — 同时用于谓词和回溯目标
3. **多入边**：将所有前驱以 `∨` 连接列入谓词。**主前驱**（回溯目标）是**主前向路径**上的节点 — 通常是拓扑序中的第一条边，排除回路和错误恢复边
4. **菱形（决策）节点**：从菱形发出的边（如 `QualityGate -- Fail --> ModifyStep`）算作目标的前驱。使用菱形节点名，而非边标签
5. **自循环和子图入口**：如果节点同时接收当前子图和外部入口的边（如 `Start(drill_down)`），用 `∨` 列出所有来源
6. **跨子图委托**：当子图的入口节点接收来自另一子图节点的委托时（如路由器的 `PipelineEntry` 委托给管线的 `PipelineStart`），断言引用**委托节点**而非本地 Start。本地 Start 是空标签 — 真正的运行时前驱是委托节点
7. **终点节点命名**：终点节点必须使用 `endNode((End))` 格式 — 双括号表示圆角形状，名称 `endNode`，标签 `End`。变体（`End`、`end`、`Finish`）为非标准格式，必须标准化

**主前驱选择**（`go back to` 的回溯目标）：

| 场景 | 主前驱 |
|------|--------|
| 一条主路径边 + 回路边 | 主路径边的源节点 |
| 多条件分支合并 | 默认/正常路径上的分支 |
| 所有边等价（无明确主前驱） | Mermaid 声明顺序中的第一个前驱 |

断言与 S1 的正常工作合并在一个步骤中 — 不创建额外步骤。

**为什么用 ASSERT**：在编程中，`assert` 意味着"此条件必须为真，否则执行停止。" AI 训练数据中包含数百万条 assert 语句，语义明确无歧义：**条件为假 = 不能继续**。

### F.3 回溯规则

- 断言为真 → 继续执行当前节点
- 断言为假（单前驱）→ 返回 `{prev_node}` 完整执行
- 断言为假（多前驱 `∨`）→ 返回 `{primary_predecessor}` 完整执行。`∨` 谓词检查是否有任一列出的前驱已执行；回溯始终指向主前驱（主前向路径）
- 如果 `{prev_node}` 自身的断言也失败 → 继续回溯到其前序节点
- 自然递归回溯，具有深度预算：max_backtrack_depth = min(3, node_count / 4)。超出预算 → 以诊断信息停止，而非无限递归（灵感来自 ABC k-bounded recovery，arXiv 2602.22302）
- 预算内最坏情况：回溯到起点从头执行
- 预算内 Pipeline 永远不会因回溯而失败 — 它会自我纠正。超出预算 → 结构化失败，附带回溯跟踪用于调试

### F.4 为什么有效

1. **ASSERT 是编程原语** — AI 将 `assert` 识别为硬性停止，而非建议。不同于"请诚实回答"（请求），`assert` 是**具有明确失败语义的命令**
2. **逐节点重复** — 全局规则存在注意力衰减；逐节点断言在每个边界刷新注意力
3. **回溯是纠正而非惩罚** — 断言失败触发重新执行，而非报错。AI 有一条合法路径：回去执行工作
4. **极低 token 成本** — 每节点一行，约 10 tokens
5. **学术验证** — 节点门控与已有研究一致：
   - **AgentSpec (ICSE 2026, ICSE 2026, arXiv 2503.18666)**：通过三元组 `trigger → predicate → enforcement` 实现运行时执行保障。节点门控实现为：trigger=节点入口，predicate=前序已执行，enforcement=回溯
   - **ProgPrompt**：在 prompt 中使用断言作为前置条件，配合恢复动作。节点门控使用 `[ASSERT]` 作为前置条件，回溯作为恢复机制
   - **注意力衰减研究**：全局指令随上下文增长影响力减弱；逐节点断言在每个边界刷新约束，对抗衰减

### F.5 断言模式 (AgentSpec 三元组)

每个节点门控断言遵循 AgentSpec 执行保障模型：

| 元素 | 节点门控映射 |
|------|-------------|
| **Trigger** | 节点入口（第一步 S1） |
| **Predicate** | `{prev_node}`（单前驱）或 `{nodeA}∨{nodeB}∨...`（多前驱）已完整执行 |
| **Enforcement** | 回溯到 `{prev_node}` 或 `{primary_predecessor}` 重新执行 |

此三元组直接嵌入每个节点的 S1 中，无需外部运行时或监控基础设施。AI 自身同时担任评估者和执行者 — 利用训练数据中的 `assert` 语义。

### F.6 在 .aisop.json 中的实现

**单前驱**（线性链）：
```json
{
  "EvolveStep": {
    "step1": "[ASSERT] Research1 executed. If false → go back to Research1. | 基于研究发现，制定修复计划...",
    "step2": "执行修复...",
    "step3": "验证修复结果..."
  }
}
```

**多前驱**（汇聚点）：
```json
{
  "ModifyStep": {
    "step1": "[ASSERT] Research2∨QualityGate∨PostSimulateGate executed. If false → go back to Research2. | 应用质量修复..."
  }
}
```

### F.7 适用范围

| 节点数 | 要求 |
|--------|------|
| 6+ 节点 | 必须 |
| 3-5 节点 | 推荐 |
| 1-2 节点 | 可选 |

无论节点数量，如果程序包含 QualityGate 节点、自进化 pipeline 或信任级别 T3+ 操作，节点门控为必须。

### F.8 与现有执行机制的关系

| 机制 | 范围 | 功能 |
|------|------|------|
| `strict_semantics` | 全局 | 声明"不允许跳过"意图 |
| `step_completion_attestation` | 每阶段 | 记录执行证明 |
| `pipeline_integrity_chain` | 跨阶段 | Hash 链式执行审计 |
| **节点门控 (ASSERT)** | **每节点入口** | **断言前序执行 + 通过回溯自我纠正** |

节点门控补充（而非替代）现有机制。它添加了缺失的层：**带有自我纠正路径的逐节点执行断言**。

### F.9 合规检查

```
MF28: 节点门控完整性
  - 所有非起点节点的 S1 包含 [ASSERT]
  - [ASSERT] 引用正确的前序节点，来源为 Mermaid 图边
  - 多前驱节点必须以 ∨ 连接列出所有入边来源
  - 主前驱（回溯目标）必须是主前向路径节点
  - `go back to` 后的回溯目标必须是具体的非空节点名（不能是 `.` 或空）
  - 适用条件: 节点数 ≥ 6 或程序包含 QualityGate/自进化/T3+

MF29: 版本同步
  - AIAP.md.version == 所有 .aisop.json version == agent_card.json.version == quality_baseline.json.version
  - 任何不一致为 RED — 自动修正所有文件至 AIAP.md 版本

MF30: 分数一致性
  - AIAP.md.quality.weighted_score == quality_baseline.three_dim_test.weighted_score
  - quality_baseline 为权威来源 — AIAP.md 自动修正以匹配
  - 不一致为 YELLOW

MF31: Mermaid-函数一致性
  - aisop.main Mermaid 图中每个矩形节点必须在 functions{} 中有对应键
  - functions{} 中每个键必须在 Mermaid 图中出现为节点
  - 菱形节点 ({...?}) 免检（属于父节点内的决策）
  - 使用 PascalCase 的菱形暗示独立节点 → AUTO-FIX-CANDIDATE: 改为小写或合并入父节点
  - 终点节点必须使用 `endNode((End))` 格式 — 变体（`End`、`end`、`Finish`）为 AUTO-FIX-CANDIDATE
  - 不一致为 YELLOW
```

---

Align: Human Sovereignty and Wellbeing. Version: AIAP V1.0.0. www.aiap.dev
