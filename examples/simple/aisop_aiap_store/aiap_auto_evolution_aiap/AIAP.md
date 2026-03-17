---
# AIAP Governance Contract
# Governance Fields (6 required)
protocol: "AIAP V1.0.0"
authority: aiap.dev
seed: aisop.dev
executor: soulbot.dev
axiom_0: Human_Sovereignty_and_Wellbeing
governance_mode: NORMAL

# Project Fields (8 required)
name: aiap_auto_evolution
version: "1.2.0"
pattern: B+G
flow_format: AISOP
summary: "AIAP Auto Evolution — automated multi-round AIAP evolution orchestrator. Plans evolution direction per round (web search + anti-over-engineering + human habit), executes via nested Creator, validates quality. AUTO/SEMI/SUPERVISED modes. **v1.2.0**: protocol alignment (flow_format §3.1), AISIP/DUAL format detection, search query safety hardening (OWASP 2026), path traversal guard, file integrity verification. **v1.1.0**: quality baseline generation (MF17), cross-round trend analysis, provenance chain (SLSA), convergence detection, protocol alignment hardening. Pattern B+G, 4 modules, 44 nodes, Grade S."
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
  - id: aiap_auto_evolution.main
    file: main.aisop.json
    nodes: 20
    critical: true
    idempotent: false
    side_effects: [file_write]
  - id: aiap_auto_evolution.planner
    file: planner.aisop.json
    nodes: 9
    critical: true
    idempotent: true
    side_effects: []
  - id: aiap_auto_evolution.executor
    file: executor.aisop.json
    nodes: 6
    critical: true
    idempotent: false
    side_effects: [file_write]
  - id: aiap_auto_evolution.validator
    file: validator.aisop.json
    nodes: 9
    critical: false
    idempotent: true
    side_effects: []

# Optional Fields
governance_hash: 3a47d28c43311fe9d1ea468dbea381cd9c3efb96590739cb540531d2e500c98d
quality:
  weighted_score: 4.934
  grade: S
  last_pipeline: "v1.2.0 EVOLVE: PROTOCOL ALIGNMENT + AISIP SUPPORT + SEARCH SAFETY + PATH HARDENING: B1 flow_format §3.1 (14 frontmatter), B2 AISIP/DUAL format detection (planner+executor+validator), B3 search query safety hardening (OWASP 2026 multi-layer), B4 path traversal guard + file integrity verification. 4 modules, 44 nodes."
tags: [aiap, auto-evolution, automation, batch-evolution, orchestrator, aisip-aware, dual-format, search-safety, protocol-alignment]
author: SoulBot.dev
license: Apache-2.0
copyright: "Copyright 2026 AIXP Foundation AIXP.dev | SoulBot.dev"

# Security and Runtime Optional Fields
trust_level:
  level: 4
  justification: "Requires full read/write workspace access to read and modify target AIAP programs. Nested Creator execution needs file_system access to target directories. google_search and web_browser for planner direction research."
  constraints:
    - "file_system write scope limited to workspace_dir"
    - "network access limited to *.google.com and *.bing.com for planner research"
    - "auto-evolution blocked (cannot target own directory)"
    - "Creator in AIAP_Tools is read-only during execution (not modified)"
permissions:
  file_system:
    scope: "./"
    operations: ["read", "write"]
  network:
    allowed: true
    endpoints: ["*.google.com", "*.bing.com"]
runtime:
  timeout_seconds: 3600
  max_retries: 3
  token_budget: 200000
  idempotent: false
  side_effects: [file_write]
capabilities:
  offered:
    - file_write
    - search
    - batch_evolution
    - quality_tracking
  required:
    - file_read
tool_dirs:
  - path: "AIAP_Tools/aisop_creator_evolution_aiap"
    type: "aiap_program"
    trust_level: "T4"
    description: "Nested AIAP Creator v1.24.0 for single-round evolution execution"

# Engineering Optional Fields
status: active
applicability_condition:
  triggers:
    - "user asks to evolve an AIAP program multiple rounds"
    - "user asks for automated batch evolution"
    - "user asks to continuously improve an AIAP program"
    - "user asks about evolution progress or history"
  preconditions:
    - "workspace_dir exists and is writable"
    - "file_system tool available"
    - "AIAP_Tools/aisop_creator_evolution_aiap/ directory contains valid Creator"
  exclusions:
    - "single evolution (use Creator directly)"
    - "program creation from scratch (use Creator directly)"
    - "non-evolution tasks (validate, simulate, etc.)"
  confidence_threshold: 0.8
intent_examples:
  - "进化 recipe_finder 5次，全自动"
  - "batch evolve ai_social 3 rounds with supervision"
  - "连续进化 soulbot_chat 3轮，每轮我确认"
  - "上次的进化进度怎么样了？"
  - "停止进化"
discovery_keywords: [auto-evolution, batch, automated, multi-round, continuous-improvement]
dependencies:
  - aiap_creator (nested in AIAP_Tools)
min_protocol_version: "AIAP V1.0.0"
---

## Governance Statement

AIAP Auto Evolution is an automated multi-round evolution orchestrator for AIAP programs. This program follows AIAP V1.0.0 protocol with Axiom 0 (Human Sovereignty and Wellbeing) as immutable axiom, ensuring all evolution decisions serve human intent.

## Feature Overview

| Module | Responsibility | Tools |
|--------|---------------|-------|
| **main.aisop.json** | Orchestrator — NLU (5 intents), loop control, mode configuration (AUTO/SEMI/SUPERVISED), round state management, final report generation | file_system |
| **planner.aisop.json** | Direction Planner — target state analysis, web search for improvements, anti-over-engineering filter, human habit alignment check, evolution plan generation with LEVEL classification | file_system, google_search, web_browser |
| **executor.aisop.json** | Round Executor — Creator context preparation, pre-round snapshot, intent execution of nested Creator (full 15-stage pipeline), result collection and verification | file_system |
| **validator.aisop.json** | Quality Validator — pre/post quality comparison, regression detection across C/I/D dimensions, severity classification, pass/fail/rollback decision | file_system |

### Evolution Modes

| Mode | User Interaction | Abort Condition |
|------|-----------------|-----------------|
| AUTO | No confirmation, fully automatic | RED quality gate or execution failure |
| SEMI | User confirms each round's plan | RED gate, user rejection, or execution failure |
| SUPERVISED | Full review per round with modification option | RED gate, user rejection, pause, or failure |

### AIAP_Tools

| Tool | Version | Purpose |
|------|---------|---------|
| aisop_creator_evolution_aiap | v1.24.0 | Nested Creator for single-round evolution execution via intent execution |

## Usage

### Entry File

`main.aisop.json` — receives user command and orchestrates multi-round evolution.

### Tool Requirements

| Tool | Required | Purpose |
|------|----------|---------|
| file_system | Yes | Read/write target programs, snapshots, reports |
| google_search | No | Planner direction research |
| web_browser | No | Planner reference page reading |

### Prerequisites

- workspace_dir containing target AIAP programs
- AIAP_Tools/aisop_creator_evolution_aiap/ contains valid Creator v1.24.0
- file_system tool available with workspace_dir write access

## Example Interactions

**Scenario 1: Fully Automatic Batch Evolution**
- User: "进化 recipe_finder 5次，全自动"
- Agent: Resolves target -> configures AUTO mode -> executes 5 rounds -> generates final report

**Scenario 2: Semi-Automatic with User Confirmation**
- User: "连续进化 soulbot_chat 3轮"
- Agent: Resolves target -> presents round 1 plan -> user confirms -> executes -> validates -> presents round 2 plan -> ...

**Scenario 3: Abort Mid-Evolution**
- User: "停止进化"
- Agent: Waits for current round to complete -> preserves successful rounds -> generates partial report

## Applicability

**Applicable**: Multi-round batch evolution of any AIAP program
**Not Applicable**: Single evolution (use Creator directly), program creation, non-evolution tasks

---

Align: Human Sovereignty and Benefit. Version: AIAP V1.0.0. www.aiap.dev
