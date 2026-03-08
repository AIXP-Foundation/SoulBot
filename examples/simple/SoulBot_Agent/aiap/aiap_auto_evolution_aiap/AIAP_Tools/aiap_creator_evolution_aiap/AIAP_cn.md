---
# AIAP Governance Contract
# 治理字段 (6 个必需)
protocol: "AIAP V1.0.0"
authority: aiap.dev
seed: aisop.dev
executor: soulbot.dev
axiom_0: Human_Sovereignty_and_Benefit
governance_mode: NORMAL

# 项目字段 (7 个必需)
name: aiap_creator
version: "1.1.0"
pattern: D+G
summary: "AIAP Creator — reference implementation for creating, evolving, validating, simulating, and managing AIAP programs via a 15-stage pipeline. 13 modules, 171 nodes, 301 scenarios (A-X). Features: ThreeDimTest (MF1-MF27), PL28 self-observation with PostExecution convergence, INSIGHTS lifecycle management, EVOLVE CAP, dry-run preview, AutoFixEngine, CREATE mode enhancements. Pattern D+G, Grade S/4.899."
tools:
  - name: file_system
    required: true
    annotations:
      read_only: false
      destructive: false
      idempotent: false
      open_world: false
  - name: google_search
    required: false
    fallback: "degrade"
    annotations:
      read_only: true
      destructive: false
      idempotent: true
      open_world: true
  - name: web_browser
    required: false
    fallback: "degrade"
    annotations:
      read_only: true
      destructive: false
      idempotent: true
      open_world: true
modules:
  - id: aiap_creator.main
    file: main.aisop.json
    nodes: 28
    critical: true
    idempotent: false
    side_effects: [file_write]
  - id: aiap_creator.generate
    file: generate.aisop.json
    nodes: 21
    critical: true
    idempotent: false
    side_effects: [file_write]
  - id: aiap_creator.research
    file: research.aisop.json
    nodes: 15
    critical: false
    idempotent: true
    side_effects: []
  - id: aiap_creator.modify
    file: modify.aisop.json
    nodes: 9
    critical: true
    idempotent: false
    side_effects: [file_write]
  - id: aiap_creator.review
    file: review.aisop.json
    nodes: 11
    critical: true
    idempotent: false
    side_effects: [file_write]
  - id: aiap_creator.simulate
    file: simulate.aisop.json
    nodes: 10
    critical: false
    idempotent: true
    side_effects: []
  - id: aiap_creator.observability
    file: observability.aisop.json
    nodes: 9
    critical: false
    idempotent: true
    side_effects: []
  - id: aiap_creator.advisor
    file: advisor.aisop.json
    nodes: 60
    critical: false
    idempotent: false
    side_effects: [file_write]
  - id: aiap_creator.standard_core
    file: AIAP_Standard.core.aisop.json
    nodes: 0
    critical: true
    idempotent: true
    side_effects: []
  - id: aiap_creator.standard_security
    file: AIAP_Standard.security.aisop.json
    nodes: 0
    critical: true
    idempotent: true
    side_effects: []
  - id: aiap_creator.standard_ecosystem
    file: AIAP_Standard.ecosystem.aisop.json
    nodes: 0
    critical: false
    idempotent: true
    side_effects: []
  - id: aiap_creator.standard_performance
    file: AIAP_Standard.performance.aisop.json
    nodes: 0
    critical: false
    idempotent: true
    side_effects: []

# 基础可选字段
governance_hash: e8bec69cfa786acc95b4906e05a583c8f8d747ec9829b88eb28bdff559b83085
quality:
  weighted_score: 4.899
  grade: S
  last_pipeline: "v1.1.0 AIAP Creator — 15-stage pipeline with PL28 parallel self-observation, PostExecution convergence node, INSIGHTS mechanism, 13 modules, 171 nodes, 301 scenarios"
tags: [aiap, creator, pipeline, governance, meta]
author: SoulBot.dev
license: Apache-2.0
copyright: "Copyright 2026 AIXP Foundation AIXP.dev | SoulBot.dev"

# 安全与运行时可选字段
trust_level:
  level: 4
  justification: "AIAP Creator requires full read/write access to workspace for creating, evolving, and modifying AIAP programs. Network access needed for research stages (google_search, web_browser)."
  constraints:
    - "file_system write scope limited to workspace_dir"
    - "network access limited to *.google.com and *.bing.com"
permissions:
  file_system:
    scope: "./"
    operations: ["read", "write"]
  network:
    allowed: true
    endpoints: ["*.google.com", "*.bing.com"]
runtime:
  timeout_seconds: 600
  max_retries: 3
  token_budget: 100000
  idempotent: false
  side_effects: [file_write]
capabilities:
  offered:
    - file_write
    - search
    - state_persistence
    - code_generation
  required:
    - file_read
ui:
  components:
    - type: dashboard
      title: "Pipeline Progress"
      data_source: pipeline_metadata
      refresh: "on_event"
    - type: form
      title: "Configuration"
      fields:
        - { name: quality_threshold, type: select, options: [strict, standard, relaxed], default: standard }
        - { name: research_mode, type: select, options: [structure, quality, compliance] }
    - type: visualization
      title: "Quality Trend"
      chart_type: line
      data_source: quality_baseline
  rendering: "mcp_apps_v1"

# 工程化可选字段
status: active
applicability_condition:
  triggers:
    - "user asks to create a new AIAP program"
    - "user asks to evolve an existing AIAP program"
    - "user asks to validate or simulate an AIAP program"
    - "user asks to modify a specific AIAP module"
    - "file with .aisop.json extension detected in workspace"
    - "user asks to discover or search for existing AIAP programs"
    - "user asks to deprecate or archive an AIAP program"
    - "user asks to export an AIAP program to SKILL.md format"
    - "user asks to import a SKILL.md file as an AIAP program"
    - "user asks to map AIAP tools to MCP protocol"
    - "user asks to discover programs from a remote registry"
    - "user asks to pack or package an AIAP program"
    - "user asks to unpack or verify a .aiap archive"
    - "user asks about UI components or dashboard for an AIAP program"
  preconditions:
    - "AIAP_Standard.core.aisop.json and extension files accessible in workspace"
    - "AIAP_Protocol.md accessible in workspace"
    - "workspace_dir writable"
  exclusions:
    - "input is not related to AIAP/AISOP format"
    - "user requests direct execution of an AIAP program (SoulBot executor responsibility)"
    - "target project uses non-AISOP format"
  confidence_threshold: 0.8
intent_examples:
  - "创建一个健康追踪 AIAP 程序"
  - "将 health_tracker 从 v1.1 进化到 v1.2"
  - "修改 recipe_finder 的搜索模块"
  - "验证 expense_tracker 的代码质量"
  - "模拟 travel_planner 的执行路径"
  - "查找有没有健康相关的 AIAP 程序"
  - "弃用 old_tracker 程序"
  - "将 recipe_finder 导出为 SKILL.md"
  - "从 SKILL.md 导入一个技能作为 AIAP 程序"
  - "将 health_tracker 的工具映射到 MCP 协议"
  - "从远程注册表搜索健康相关的 AIAP 程序"
  - "将 health_tracker 打包为 .aiap 文件"
  - "解包并验证 recipe_finder_v1.0.0.aiap"
  - "为 health_tracker 添加 Dashboard UI 组件"
discovery_keywords: [aiap, creator, aisop, pipeline, evolve, generate, validate, simulate, skill, discover, deprecate, export, import, mcp, registry, adapter, package, pack, sampling, capability, ui, dashboard, form, visualization, tool_dirs, pattern_g, embedded_runtime, code_trust, mcp_server, agent_card, migration, auto_fix, remediation, yellow_persistence, lint_report, automated_verification, endpoint, a2a, license, spdx, store, safety_card, nist, grpc, elicitation, aaif, signed_agent_card, insights, no_self_modify, self_observation, pl28, no_cross_write, insights_lifecycle]
dependencies:
  - file: AIAP_Protocol.md
    required: true
    description: "AIAP protocol specification used by ReadTemplate and research modules"
min_protocol_version: "AIAP V1.0.0"
identity:
  program_id: "aiap.dev/aiap_creator"
  publisher: "AIXP Foundation AIXP.dev | SoulBot.dev"
  verified_on: "2026-03-08"
benchmark:
  threedimscore: 4.899
  grade: "S"
  simulation_coverage: "A(16)+B(13)+C(10)+D(10)+E(13)+F(8)+G(10)+H(14)+J(4)+K(7)+L(2)+M(22)+N(5)+O(6)+P(10)+Q(12)+R(59)+S(11)+T(13)+U(4)+V(10) = 280 scenarios"
  total_nodes: 163
  pass_rate: "280/280 (100%) — 0 RED, 10 YELLOW_accepted"
---

## 治理声明

AIAP Creator 是 AIAP 协议的参考实现和自举工具。本程序遵循 AIAP V1.0.0 协议，
以 Axiom 0 (Human Sovereignty and Benefit) 为不可变公理，通过三域治理链
(aisop.dev → aiap.dev → soulbot.dev) 确保所有产出对齐人类主权与福祉。

AIAP Creator 自身是一个 AIAP 程序 (自举属性)——它创建 AIAP 程序，同时自身也遵循
所有 AIAP 规则。

## 功能概述

AIAP Creator 通过 15 阶段 Pipeline（含自动 ProtocolAlign）管理 AIAP 程序的完整生命周期：

| 意图 | 说明 | Pipeline |
|------|------|----------|
| **Create** | 创建新的 AIAP 程序 | Research → Evolve → Generate → Modify → QualityGate → Validate → Simulate → PostSimulateGate → Observability → Review |
| **Evolve** | 进化现有 AIAP 程序 | 同 Create (带增量差异分析) |
| **Modify** | 修改特定模块 | Research(quality) → Modify → Generate → Validate → [Simulate] → [PostSimulateGate] → Review |
| **Validate** | 验证代码质量 | ThreeDimTest 33+ 项检查 (C1-C7, I1-I13, D1-D10) |
| **Simulate** | 模拟执行路径 | 路径追踪 + 场景覆盖 (Categories A-X) |
| **Compare** | 对比两个版本 | 并排差异展示 |
| **Discover** | 搜索现有程序 | 工作区扫描 + 联邦注册表查询 + 语义匹配 + 关联推荐 |
| **Deprecate** | 弃用/归档程序 | 状态转换 + 迁移指南生成 |
| **Export** | 导出为 SKILL.md | AIAP→SKILL.md 字段映射 + 治理元数据保留 |
| **Import** | 从 SKILL.md 导入 | SKILL.md→AIAP 骨架生成 + 治理默认值填充 |
| **Explain** | 解释 AIAP 概念 | 内联知识回答 |
| **Package** | 打包/解包程序 | advisor package 子图 (pack → .aiap / unpack → verify) |

### 模块架构 (Pattern D+G)

- **main.aisop.json** — 顶级编排器 (28 节点, fractal_exempt, **主动分解建议**)
- **generate.aisop.json** — 生成器 (21 功能节点, sub_mermaid 架构: main 12 + 3 子图, **智能描述更新, MF14-MF27 跨模块审计, 参数名漂移检测 (CR1), 节点计数精确检查 (CR2), 绕过路径检测 (CR4), MF24 协议文档一致性, MF25 工具集成完整性, MF26 枚举注册表一致性, MF27 新模块依赖对称性, 分数轨迹根因分析**)
- **research.aisop.json** — 共享研究模块 (15 节点, fractal_exempt, 3 模式复用, **结构化 research_finding 输出, 自动 LEVEL 分类器, 维度校准完整性 (RES-1), 显式 CREATE/EVOLVE 模式路由, vision extraction NLP guidance**)
- **modify.aisop.json** — 修改器 (9 节点)
- **review.aisop.json** — 审查器 (11 节点, +AutoFixEngine, **数据路径 schema 验证 (VAL-1), 分数轨迹增量展示, 回滚安全增强, QRG2 累积漂移检测, 测试边界澄清**)
- **simulate.aisop.json** — 模拟器 (10 节点, +YellowRemediationGuide, +YellowFixProposalGenerator, **Category R 变更驱动场景, Category S 多机制交互, Category T 异步委托竞态检测, 枚举值锚定 (CR3)**)
- **observability.aisop.json** — 遥测分析 (9 节点, Token/Error/Dimension/RootCause/QRG 分析)
- **advisor.aisop.json** — 高级顾问 (60 节点, fractal_exempt, 9 子图: main 路由 + 8 互斥子图 orchestrate/memory/protocol/skill_export/skill_import/mcp_adapter/package/insights lifecycle)
- **AIAP_Standard.core.aisop.json** — 核心质量标准 (C1-C7, I1-I7, I12-I13, D1-D7, PL1-PL12, PL19-PL21, MF1-MF9, MF15-MF27 + extension_registry + tool_annotations + json_schema + interop.mcp_tool_mapping + tool_dirs_spec + data_contracts + cascade_on_reject + **MF24 协议文档一致性, MF25 工具集成完整性, MF26 枚举注册表一致性, MF27 新模块依赖对称性**)
- **AIAP_Standard.security.aisop.json** — 安全扩展 (I8-I11, I13 Embedded Code Safety, D8-D10, AT1-AT6 威胁分类, Code Trust Gate with ZIP SLIP extension + P14 Safety Card 要求)
- **AIAP_Standard.ecosystem.aisop.json** — 生态扩展 (MF10-MF14, MF16, MF19, K1-K10, PL16-PL17 动态 TTL, PL22 Registry Integration, packaging_specification + tool_dirs_packaging, registry_endpoint_extension, tool_dirs extension, ui_rendering_rules, yellow_persistence_tracking, Categories F-M + P12 MCP 2025 对齐 + P13 A2A v0.3 对齐 + **MF14 多跳链验证, MF19 数据生命周期审计**)
- **AIAP_Standard.performance.aisop.json** — 性能扩展 (PL13-PL15, PL18-PL21, PL23 Sampling Protocol, PL24 Auto-Fix Protocol, PL26 Pre-Evolution Snapshot, PL28 Self-Observation Verification, QRG1-QRG5, E.injection)

## 使用方式

### 入口文件

`main.aisop.json` — AI Agent 加载此文件启动 AIAP Creator。

### 工具需求

| 工具 | 必需 | 用途 |
|------|------|------|
| file_system | 是 | 读写 AISOP 文件 |
| google_search | 否 | 研究阶段搜索最佳实践 |
| web_browser | 否 | 深度网页研究 |

### 前置条件

- 目标目录中包含 AIAP_Standard.core.aisop.json (及扩展文件) 和 AIAP_Protocol.md
- AI Agent 支持 file_system 工具

## 示例交互

**场景 1: 创建新程序**
- 用户: "创建一个个人支出追踪器 AIAP 程序"
- Agent: 执行完整 Pipeline → 生成 expense_tracker_aiap/ 目录含 AIAP.md + main + 模块

**场景 2: 进化现有程序**
- 用户: "将 health_tracker 从 v1.1 进化到 v1.2，添加月度报告功能"
- Agent: 分析现有结构 → 提议 LEVEL_A/B 变更 → 用户确认 → 生成新版本

**场景 3: 验证质量**
- 用户: "验证 recipe_finder 的代码质量"
- Agent: 运行 ThreeDimTest → 输出三维成绩 + 流量分级

## 适用条件

**适用**: 创建、进化、修改、验证、模拟、搜索、弃用 AIAP 程序；SKILL.md 双向转换；MCP 工具映射；联邦注册表发现 (含 MCP/A2A 端点发现)；AIAP 打包/解包 (含 tool_dirs 目录和 Code Trust Gate)；UI 组件声明生成；Pattern G 嵌入式工具目录 (tool_dirs) 验证与自动生成；Pattern E/F→G 迁移指导；自动修复提案生成与应用；YELLOW 持久化追踪与修复指南；自动化质量验证 (lint_report)
**不适用**: 直接执行 AIAP 程序 (那是 SoulBot 执行器的职责)、非 AISOP 格式的项目

---

Align: Human Sovereignty and Benefit. Version: AIAP V1.0.0. www.aiap.dev
