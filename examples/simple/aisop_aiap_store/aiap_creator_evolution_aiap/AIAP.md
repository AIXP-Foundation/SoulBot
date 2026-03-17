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
name: aiap_creator
version: "1.2.0"
pattern: D+G
flow_format: "AISOP"
summary: "AIAP Creator — reference implementation for creating, evolving, validating, simulating, and managing AIAP programs via a 15-stage pipeline. 14 modules, 207 nodes, 643 scenarios (A-Z, AA). Features: ThreeDimTest (MF1-MF38), EVOLVE CAP with adaptive complexity, governance integrity sync, quality history archival, stage cache chain verification, AISOP/AISIP/DUAL support, format conversion, protocol alignment (MCP/A2A). Pattern D+G, Grade S."
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
    nodes: 32
    critical: true
    idempotent: false
    side_effects: [file_write]
  - id: aiap_creator.generate
    file: generate.aisop.json
    nodes: 29
    critical: true
    idempotent: false
    side_effects: [file_write]
  - id: aiap_creator.research
    file: research.aisop.json
    nodes: 17
    critical: false
    idempotent: true
    side_effects: []
  - id: aiap_creator.modify
    file: modify.aisop.json
    nodes: 11
    critical: true
    idempotent: false
    side_effects: [file_write]
  - id: aiap_creator.review
    file: review.aisop.json
    nodes: 13
    critical: true
    idempotent: false
    side_effects: [file_write]
  - id: aiap_creator.simulate
    file: simulate.aisop.json
    nodes: 13
    critical: false
    idempotent: true
    side_effects: []
  - id: aiap_creator.observability
    file: observability.aisop.json
    nodes: 11
    critical: false
    idempotent: true
    side_effects: []
  - id: aiap_creator.convert
    file: convert.aisop.json
    nodes: 18
    critical: true
    idempotent: false
    side_effects: [file_write]
  - id: aiap_creator.advisor
    file: advisor.aisop.json
    nodes: 63
    critical: false
    idempotent: false
    side_effects: [file_write]
  - id: aiap.standard.core
    file: AIAP_Standard.core.aisop.json
    nodes: 0
    critical: true
    idempotent: true
    side_effects: []
  - id: aiap.standard.security
    file: AIAP_Standard.security.aisop.json
    nodes: 0
    critical: true
    idempotent: true
    side_effects: []
  - id: aiap.standard.performance
    file: AIAP_Standard.performance.aisop.json
    nodes: 0
    critical: false
    idempotent: true
    side_effects: []
  - id: aiap.standard.ecosystem
    file: AIAP_Standard.ecosystem.aisop.json
    nodes: 0
    critical: false
    idempotent: true
    side_effects: []
  - id: aiap.standard.runtime_extensions
    file: AIAP_Standard.runtime_extensions.aisop.json
    nodes: 0
    critical: true
    idempotent: true
    side_effects: []

# Optional Fields
governance_hash: 667dc9319358a71373c5e39a3eca8e539565cd86dd2a63cd59615ad71c98396a
quality:
  weighted_score: 4.899
  grade: S
  last_pipeline: "v1.2.0"
tags: [aiap, creator, pipeline, governance, meta, execution, strict_mode, density_metrics, strict_semantics, self_evolution, dsm, token_efficiency, evolution_fitness, attestation, insights, quality, threedimscore]
author: SoulBot.dev
license: Apache-2.0
copyright: "Copyright 2026 AIXP Foundation AIXP.dev | SoulBot.dev"

# Security and Runtime Optional Fields
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

# Engineering Optional Fields
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
  - "Create a personal expense tracker AIAP program"
  - "Evolve health_tracker from v1.1 to v1.2"
  - "Modify the search module of recipe_finder"
  - "Validate the code quality of expense_tracker"
  - "Simulate the execution paths of travel_planner"
  - "Search for any health-related AIAP programs"
  - "Deprecate old_tracker program"
  - "Export recipe_finder as SKILL.md"
  - "Import a SKILL.md file as an AIAP program"
  - "Map health_tracker tools to MCP protocol"
  - "Search remote registry for health-related AIAP programs"
  - "Package health_tracker as a .aiap file"
  - "Unpack and verify recipe_finder_v1.0.0.aiap"
  - "Add a Dashboard UI component to health_tracker"
discovery_keywords: [aiap, creator, aisop, pipeline, evolve, generate, validate, simulate, skill, discover, deprecate, export, import, mcp, registry, adapter, package, pack, capability, ui, dashboard, agent_card, migration, auto_fix, a2a, license, store, safety_card, insights, self_observation, execution_config, strict_mode, density_metrics, strict_semantics, self_evolution, dsm, token_efficiency, attestation, fitness, quality, governance, threedimscore, pattern_g, pattern_d]
dependencies:
  - file: AIAP_Protocol.md
    required: true
    description: "AIAP protocol specification used by ReadTemplate and research modules"
min_protocol_version: "AIAP V1.0.0"
identity:
  program_id: "aiap.dev/aiap_creator"
  publisher: "AIXP Foundation AIXP.dev | SoulBot.dev"
  verified_on: "2026-03-13"
benchmark:
  threedimscore: 4.899
  grade: "S"
  simulation_coverage: "A(16)+B(13)+C(10)+D(10)+E(13)+F(8)+G(10)+H(14)+J(4)+K(7)+L(2)+M(22)+N(5)+O(6)+P(10)+Q(12)+R(376)+S(14)+T(13)+U(4)+V(10)+W(6)+X(15)+Y(11)+Z(16)+AA(16) = 643 scenarios"
  total_nodes: 207
  pass_rate: "643/643 (100%) — 0 RED, 10 YELLOW_accepted"
---

## Governance Declaration

AIAP Creator is the reference implementation and bootstrapping tool for the AIAP protocol.
This program follows the AIAP V1.0.0 protocol, with Axiom 0 (Human Sovereignty and Wellbeing)
as its immutable axiom, ensuring all outputs align with human sovereignty and benefit through
the three-domain governance chain (aisop.dev -> aiap.dev -> soulbot.dev).

AIAP Creator is itself an AIAP program (bootstrapping property) — it creates AIAP programs
while also following all AIAP rules itself.

## Feature Overview

AIAP Creator manages the complete lifecycle of AIAP programs through a 15-stage pipeline (with automatic ProtocolAlign):

| Intent | Description | Pipeline |
|--------|-------------|----------|
| **Create** | Create a new AIAP program | Research -> Evolve -> Generate -> Modify -> QualityGate -> Validate -> Simulate -> PostSimulateGate -> Observability -> Review |
| **Evolve** | Evolve an existing AIAP program | Same as Create (with incremental diff analysis) |
| **Modify** | Modify a specific module | Research(quality) -> Modify -> Generate -> Validate -> [Simulate] -> [PostSimulateGate] -> Review |
| **Validate** | Validate code quality | ThreeDimTest 33+ checks (C1-C7, I1-I13, D1-D10) |
| **Simulate** | Simulate execution paths | Path tracing + scenario coverage (Categories A-X) |
| **Compare** | Compare two versions | Side-by-side diff display |
| **Discover** | Search existing programs | Workspace scan + federated registry query + semantic matching + related recommendations |
| **Deprecate** | Deprecate/archive a program | State transition + migration guide generation |
| **Export** | Export as SKILL.md | AIAP->SKILL.md field mapping + governance metadata preservation |
| **Import** | Import from SKILL.md | SKILL.md->AIAP skeleton generation + governance defaults |
| **Explain** | Explain AIAP concepts | Inline knowledge response |
| **Package** | Pack/unpack a program | advisor package sub-graph (pack -> .aiap / unpack -> verify) |
| **Convert** | Convert AISOP↔AISIP format | Standalone bidirectional conversion (auto-direction, §4 topology transform, manifest) |

### Module Architecture (Pattern D+G)

- **main.aisop.json** — Top-level orchestrator (32 nodes, fractal_exempt)
- **protocol_config.json** — Protocol metadata config (execution, density metrics, strict semantics, self-evolution verification, DSM, token efficiency, volume monitor)
- **generate.aisop.json** — Generator (29 nodes, sub_mermaid architecture, MF1-MF38 cross-module audits)
- **research.aisop.json** — Shared research module (17 nodes, fractal_exempt, 3-mode reuse)
- **modify.aisop.json** — Modifier (11 nodes)
- **review.aisop.json** — Reviewer (13 nodes, +AutoFixEngine)
- **simulate.aisop.json** — Simulator (13 nodes, +YellowRemediationGuide, +ContractCheck)
- **observability.aisop.json** — Telemetry analysis (11 nodes)
- **advisor.aisop.json** — Advanced advisor (63 nodes, fractal_exempt, 9 sub-graphs)
- **convert.aisop.json** — Format converter (18 nodes, AISOP↔AISIP bidirectional)
- **AIAP_Standard.core.aisop.json** — Core quality standard
- **AIAP_Standard.security.aisop.json** — Security extension
- **AIAP_Standard.ecosystem.aisop.json** — Ecosystem extension
- **AIAP_Standard.performance.aisop.json** — Performance extension

## Usage

### Entry File

`main.aisop.json` — AI Agent loads this file to start AIAP Creator.

### Tool Requirements

| Tool | Required | Purpose |
|------|----------|---------|
| file_system | Yes | Read/write AISOP files |
| google_search | No | Search best practices during research stages |
| web_browser | No | Deep web research |

### Prerequisites

- AIAP_Standard.core.aisop.json (and extension files) and AIAP_Protocol.md accessible in target directory
- AI Agent supports the file_system tool

## Example Interactions

**Scenario 1: Create a New Program**
- User: "Create a personal expense tracker AIAP program"
- Agent: Executes full Pipeline -> generates expense_tracker_aiap/ directory with AIAP.md + main + modules

**Scenario 2: Evolve an Existing Program**
- User: "Evolve health_tracker from v1.1 to v1.2 with monthly report functionality"
- Agent: Analyzes existing structure -> proposes LEVEL_A/B changes -> user confirms -> generates new version

**Scenario 3: Validate Quality**
- User: "Validate the code quality of recipe_finder"
- Agent: Runs ThreeDimTest -> outputs three-dimensional scores + traffic light classification

## Applicability

**Applicable**: Creating, evolving, modifying, validating, simulating, discovering, and deprecating AIAP programs; SKILL.md bidirectional conversion; MCP tool mapping; federated registry discovery (with MCP/A2A endpoint discovery); AIAP packaging/unpackaging (with tool_dirs directory and Code Trust Gate); UI component declaration generation; Pattern G embedded tool directory (tool_dirs) validation and auto-generation; Pattern E/F->G migration guidance; auto-fix proposal generation and application; YELLOW persistence tracking and remediation guide; automated quality verification (lint_report); MCP 2025 alignment (Tasks primitive, Elicitation, Extensions, AAIF governance); A2A v0.3 alignment (gRPC transport, signed Agent Cards, Linux Foundation governance); Safety Card generation (risk_level, data_handling, limitations in agent_card.json); NIST AI Agent Standards Initiative reference
**Not applicable**: Direct execution of AIAP programs (that is the SoulBot executor's responsibility); non-AISOP format projects

---

Align: Human Sovereignty and Wellbeing. Version: AIAP V1.0.0. www.aiap.dev
