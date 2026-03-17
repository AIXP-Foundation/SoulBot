# AIAP Structural Specification

---

## Table of Contents

**Part I: Protocol Foundations**
1. [Protocol Declaration](#1-protocol-declaration)
2. [Core Definitions: AISOP = Language, AIAP = Rules](#2-core-definitions)
3. [AIAP.md Rules](#3-aiapmd-rules)

**Part II: Structural Specification**
4. [Node = Functional Responsibility](#4-node--functional-responsibility)
5. [Functional Node Count](#5-functional-node-count)
6. [Progressive Node Guidelines](#6-progressive-node-guidelines)
7. [fractal_exempt Annotation](#7-fractal_exempt-annotation)
8. [Pattern Selection](#8-pattern-selection)
9. [Pattern A-G Detailed Definitions](#9-pattern-a-g-detailed-definitions)
10. [main.aisop.json Rules](#10-mainaisopjson-rules)
11. [Functional Module Rules](#11-functional-module-rules)
12. [Independent Function Judgment](#12-independent-function-judgment)
13. [Sub_AIAP Split Rules](#13-sub_aiap-split-rules)
14. [Pattern Upgrade Convergence Handling](#14-pattern-upgrade-convergence-handling)
15. [Dual-Stream Rules](#15-dual-stream-rules)

**Part III: Security & Runtime**
16. [Trust Levels](#16-trust-levels)
17. [Permission Boundaries](#17-permission-boundaries)
18. [Integrity Verification](#18-integrity-verification)
19. [Runtime Constraints](#19-runtime-constraints)
20. [Error Handling Protocol](#20-error-handling-protocol)

**Part IV: Engineering Capabilities**
21. [Discovery Protocol](#21-discovery-protocol)
22. [Dependency Resolution](#22-dependency-resolution)
23. [Program Lifecycle](#23-program-lifecycle)
24. [Orchestration Patterns](#24-orchestration-patterns)

**Part V: Quality & Compatibility**
25. [Version Compatibility](#25-version-compatibility)
26. [Documentation Completeness Levels](#26-documentation-completeness-levels)

**Appendices**
- [Appendix A: PL24 Auto-Fix Protocol](#appendix-a-pl24-auto-fix-protocol)
- [Appendix B: PL25 License & Copyright Declaration](#appendix-b-pl25-license--copyright-declaration)
- [Appendix C: Category M — Tool Directory Simulation Scenarios](#appendix-c-category-m--tool-directory-simulation-scenarios-m1-m20)
- [Appendix D: NO_SELF_MODIFY Rule](#appendix-d-no_self_modify-rule)
- [Appendix E: INSIGHTS Mechanism — Optional Runtime Insight Recording](#appendix-e-insights-mechanism--optional-runtime-insight-recording)
- [Appendix F: Node Gate — Node-Level Execution Assertion](#appendix-f-node-gate--node-level-execution-assertion)

---

## Part I: Protocol Foundations

---

## 1. Protocol Declaration

```
AIAP Structural Specification
Protocol: AIAP V1.0.0
Authority: aiap.dev
Seed: aisop.dev
Axiom 0: Human Sovereignty and Wellbeing

This document defines the structural specification for AIAP programs, including:
- AIAP.md project declaration rules
- Pattern A-G fractal patterns
- Node counting and splitting strategies
- Security, runtime, discovery, dependency, lifecycle, and orchestration protocols

All AIAP programs must follow this specification.
AISOP file format (.aisop.json) and AISIP file format (.aisip.json) as underlying languages are not governed by this document.
```

---

## 2. Core Definitions

> AISOP and AISIP are programming languages, AIAP is the programming rules.

| Concept | Analogy | Definition |
|------|------|------|
| **AISOP** | Interpreted language (Python) | AI-driven language — defines file format (`.aisop.json`), Mermaid control flow + functions, AI follows the graph with full visibility |
| **AISIP** | Compiled language (C) | Runtime-driven language — defines file format (`.aisip.json`), JSON control flow + functions, Runtime controls AI via `{}` commands (Truman Show pattern) |
| **AIAP** | Programming rules (coding standards/design patterns) | Governance protocol — defines how programs should be written, quality standards, security guards, axiom constraints. Language-agnostic: governs both AISOP and AISIP programs |
| **AIAP Program** | A standards-compliant project | A complete project written in AISOP or AISIP language following AIAP rules |
| **AIAP Creator** | Project scaffolding (`create-react-app`) | Tool for creating AIAP programs — is itself an AIAP program (bootstrapping) |

### 2.0.1 Two Languages, One Governance

```
AISOP (AI-driven):
  AI sees the full Mermaid graph → AI decides which node to execute next
  Entry: ASSERT RUN aisop.main
  Trust model: AI has full visibility, constrained by system_prompt
  File: .aisop.json

AISIP (Runtime-driven):
  AI sees only the current node → Runtime decides which node comes next
  Entry: Runtime calls start(), AI uses {} commands
  Trust model: AI has zero visibility, controlled by Runtime (Truman Show)
  File: .aisip.json

Shared governance (AIAP):
  Axiom 0, trust levels, security, quality standards, patterns, lifecycle
  — all apply regardless of which language is used.
```

| Dimension | AISOP | AISIP |
|-----------|-------|-------|
| Control flow format | Mermaid flowchart | JSON nodes + edges |
| Who drives execution | AI (follows graph) | Runtime (feeds nodes) |
| AI visibility | Full graph | Current node only |
| Memory model | Full (single session) | Full (single session) |
| Entry point | `ASSERT RUN aisop.main` | `{"method": "start"}` |
| File extension | `.aisop.json` | `.aisip.json` |
| Best for | Complex AI reasoning, self-guided | Strict control, deterministic routing |

```
Naming conventions:
  .aisop.json  →  AISOP language format identifier
  .aisip.json  →  AISIP language format identifier
  _aiap        →  Program type identifier (what rules the directory follows)
  AIAP.md      →  Project declaration (similar to pyproject.toml / pom.xml)
```

### 2.1 File Field Responsibilities

> Each field has one and only one responsibility. Information appears in only one place.

**AISOP files (`.aisop.json`)**:

| Field | Responsibility | Content |
|------|------|------|
| `id` | Identity | Unique identifier for programs and modules |
| `name` | Name | Product name + version number |
| `version` | Version | Semantic version number |
| `summary` | Capability overview | One sentence describing "what I can do" |
| `description` | Detailed description | Architecture, history, patterns, implementation details |
| `system_prompt` | **Behavioral guidelines** | Defines how the agent should behave (the sole behavior definition layer) |
| `loading_mode` | **Loading strategy** | `"normal"` (all functions at once) or `"node"` (on-demand per node). Default: `"normal"` |
| `output_mode` | **Output Layer** | Defines L0 structured output format and L1 output format (optional field) |
| `instruction` | **Execution instruction** | Fixed as `ASSERT RUN aisop.main` (immutable constant) |
| `user_input` | **Reserved field** | Runtime placeholder `"{user_input}"` — substituted by executor with actual user message. Optional: usage depends on program role (e.g., required for route entry files, not needed for sub-modules). Defined as required in AISIP spec §3. |
| `aisop.main` | Execution graph | Main Mermaid flowchart — all execution starts here |
| `functions` | Execution logic | Specific steps and constraints for each node |

**AISIP files (`.aisip.json`)** — three-layer structure:

| Field | Responsibility | Content |
|------|------|------|
| `aisip` | **Program metadata** | Protocol version, id, name, version, summary, description, tools, params |
| `aisip.protocol` | Protocol version | e.g., `"AISIP V1.0.0"` |
| `aisip.id` | Identity | Unique program identifier |
| `aisip.name` | Name | Program display name |
| `aisip.version` | Version | Semantic version number |
| `aisip.summary` | Capability overview | One-sentence description |
| `aisip.description` | Detailed description | Architecture, flow, implementation details |
| `aisip.tools` | Tool declarations | List of tools the program may use |
| `aisip.params` | Runtime params | Configurable params |
| `task` | **Control flow** | JSON nodes + edges (start, nodes, types, branches) |
| `task.start` | Entry point | First node name |
| `task.nodes` | Flow graph | Node definitions: type, next, branches, error, wait_for, delegate_to |
| `functions` | **Execution logic** | Task descriptions for each node (same role as AISOP functions) |

> AISIP uses three-layer separation: `aisip` (program identity — who am I), `task` (control flow — what order), `functions` (task bodies — what to do). The `aisip` metadata does not affect execution — Runtime only reads `task` + `functions`. No system_prompt or instruction needed — the Runtime provides the system prompt and drives execution via `{}` commands.

### 2.2 instruction Immutable Constant (AISOP only)

```
Rule: The instruction field of every AISOP file must be exactly: ASSERT RUN aisop.main
Note: AISIP files do not have an instruction field — execution is driven by the Runtime.
```

**Rationale**:
- `RUN` is a machine execution instruction, not a natural language suggestion. Analogous to Dockerfile `RUN`, SQL `SELECT`.
- `aisop.main` is a JSON structural path, pointing to the `content.aisop.main` execution graph.
- Program identity is provided by the `id` field; no need to repeat in instruction.
- Capability description is provided by `summary`/`description`; no need to repeat in instruction.

```
C language analogy:
  int main() { ... }     ← Entry is always main, uniform across all programs
  ASSERT RUN aisop.main   ← Entry is always aisop.main, asserted execution, uniform across all AISOP files
```

**sub_mermaid**: Even if the aisop object contains multiple graphs (e.g., `main`, `orchestrate`, `memory`), the entry point is still `aisop.main`. The main graph routes to sub-graphs internally through params.

### 2.3 system_prompt Behavioral Layer Rules

```
Rule: system_prompt is the behavioral layer — defines how the agent should behave, not what it is or how it's built.
```

**Must include**:
1. **Role positioning** — the agent's behavioral role (not the product name)
2. **Domain behavioral guidelines** — behavioral constraints specific to the domain
3. `Mirror User's exact language and script variant.` — multilingual requirement
4. `Align: Human Sovereignty and Wellbeing.` — Axiom 0 seal

**Must not include**:
- Product name or version number → already in `name` + `version` fields
- Architecture or pattern details → already in `description` field
- Module filenames or delegation logic → already in `functions` field
- Capability lists → already in `summary` field

```
Format template:
  "{behavioral role}. {domain guidelines}. Mirror User's exact language and script variant.
   Align: Human Sovereignty and Wellbeing."

Good example:
  "Personal expense tracking assistant. Prioritize numerical precision.
   Protect user financial privacy. Mirror User's exact language and script variant.
   Align: Human Sovereignty and Wellbeing."

Bad example:
  "Expense Tracker v1.0.0. Pattern B router: delegate data operations
   to record.aisop.json. Mirror User's exact language and script variant.
   Align: Human Sovereignty and Wellbeing."
   ↑ Contains product name+version(name), architecture(description), filenames(functions)
```

### 2.4 output_mode Output Layer Rules

Rule: `output_mode` defines the agent's structured output format (L0) and user-facing output format (L1).

**Field structure**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `L0` | string | Yes | Structured JSON output format and schema |
| `L1` | string | Yes | Output language rule (includes helpfulness directive) |
| `output` | string | Yes | Which layer to show: `"L1"` or `"L0+L1"` |

**Default L0**: `"Output JSON in ENGLISH: {intent, confidence, route, state, op}"` — structured execution evidence with 5 standard fields.

**Default**: When `output_mode` is omitted, the runtime agent's default output mode applies. This ensures backward compatibility with existing AISOP files.

**Security Override Rule**: Modules with `id` containing "safety" or tagged with `security: true` in their system content MUST have `output_mode.output` locked to `"L1"`. Global or parent-level `output: "L0+L1"` settings do NOT propagate to security modules. This prevents exposure of security detection logic to users.

### 2.5 loading_mode Loading Strategy Rules

Rule: `loading_mode` controls how the runtime agent loads function definitions from the file.

| Mode | Behavior | Use Case |
|------|----------|----------|
| `normal` (default) | All functions injected at once | Files with ≤15 nodes, sufficient token budget |
| `node` | Only first node's function provided; AI requests subsequent nodes via `SOULBOT_CMD` | Large files (>15 nodes), token-constrained environments |

**Default**: When `loading_mode` is omitted, `"normal"` is assumed.

**Generator rule**: Creator MUST include `"loading_mode": "normal"` in every generated `.aisop.json` and `.aisip.json` file's system content.

---

## 3. AIAP.md Rules

Every `{name}_aiap/` directory **must** contain an AIAP.md file. AIAP.md is the project's governance contract and discovery entry point.

### 3.1 Required Fields (YAML frontmatter)

**Governance Fields (6)**:

| Field | Type | Description |
|------|------|------|
| `protocol` | string | AIAP version number, e.g., `"AIAP V1.0.0"` |
| `authority` | string | Governance authority domain, fixed as `aiap.dev` |
| `seed` | string | Language seed domain: `aisop.dev` (AISOP programs) or `aisip.dev` (AISIP programs). Must align with `flow_format`: AISOP→aisop.dev, AISIP→aisip.dev. DUAL mode: each directory uses its own seed |
| `executor` | string | Execution platform domain, fixed as `soulbot.dev` |
| `axiom_0` | string | Core axiom, fixed as `Human_Sovereignty_and_Wellbeing` |
| `governance_mode` | string | `NORMAL` or `DEV` |

**Project Fields (8)**:

| Field | Type | Description |
|------|------|------|
| `name` | string | Project name (snake_case) |
| `version` | string | Current version (semver, synchronized with main.aisop.json or main.aisip.json) |
| `pattern` | string | Structural pattern `A|B|C|D|E|F|G` |
| `flow_format` | string | Flow graph serialization format: `AISOP` (Mermaid) or `AISIP` (JSON flow dict). In DUAL mode, each directory's AIAP.md declares its own format — no `DUAL` value exists because each copy is self-describing |
| `summary` | string | Concise feature overview (recommended ≤500 characters) |
| `tools` | list/object | Tool declarations (see §3.3) |
| `modules` | list | Module inventory (see §3.4) |
| `license` | string | SPDX license identifier or `proprietary` (see Appendix B) |

### 3.2 Optional Fields (YAML frontmatter)

**Basic Optional Fields**:

| Field | Type | Description |
|------|------|------|
| `governance_hash` | string | Governance hash (see §18) |
| `quality` | object | `{weighted_score, grade, last_pipeline}` |
| `description` | string | Agent Skills compatible field — skill description |
| `tags` | list | Classification tags |
| `author` | string | Author information |
| `copyright` | string | Copyright notice (e.g. `"Copyright 2026 AIXP Foundation AIXP.dev"`) |
| `tool_dirs` | list | Pattern G tool directory declarations (see §9 Pattern G) |
| `capabilities` | object | Runtime capability declarations `{offered, required}` |

**Security & Runtime Optional Fields** (Part III):

| Field | Type | Default | Description |
|------|------|--------|------|
| `trust_level` | number (1-4) | 3 | Trust level (see §16) |
| `permissions` | object | null | Permission boundaries (see §17) |
| `runtime` | object | null | Runtime constraints (see §19) |

**Engineering Optional Fields** (Part IV):

| Field | Type | Default | Description |
|------|------|--------|------|
| `status` | string | "draft" | Lifecycle state (see §23) |
| `deprecated_date` | string | null | Deprecation date |
| `successor` | string | null | Replacement program name |
| `intent_examples` | list | [] | Semantic routing anchors (see §21) |
| `discovery_keywords` | list | [] | Keyword index |
| `dependencies` | list | [] | Cross-project dependencies (see §22) |
| `min_protocol_version` | string | null | Minimum protocol version (see §25) |
| `benchmark` | object | null | Quality benchmark declaration |
| `identity` | object | null | Program identity and provenance (see I11) — `{ program_id, publisher, verified_on }` |

### 3.3 tools Field Specification

**Compact format** (backward compatible):

```yaml
tools: [file_system, shell]
```

**Structured format** (recommended):

```yaml
tools:
  - name: file_system
    required: true
    min_version: "1.0"
  - name: shell
    required: false
    fallback: "degrade"       # Degrade when unavailable
```

| Attribute | Type | Default | Description |
|------|------|--------|------|
| `name` | string | (required) | Tool name |
| `required` | boolean | true | Whether the tool is required |
| `min_version` | string | null | Minimum version requirement |
| `fallback` | string | null | Degradation strategy when unavailable: `"degrade"` / `"skip"` / `"error"` |

### 3.4 modules Field Specification

```yaml
modules:
  - id: health_tracker.record
    file: record.aisop.json
    nodes: 7
    critical: true              # Whether it is a critical module (default true)
    idempotent: true            # Whether it is idempotent (default false)
    side_effects: [file_write]  # Side effect declarations (default [])
```

| Attribute | Type | Default | Description |
|------|------|--------|------|
| `id` | string | (required) | Module unique identifier `{project}.{module}` |
| `file` | string | (required) | Filename |
| `nodes` | number | (required) | Number of functional nodes |
| `critical` | boolean | true | Whether to trigger FATAL on failure (see §20) |
| `idempotent` | boolean | false | Whether repeated execution is safe |
| `side_effects` | list | [] | Side effect list: `file_write`, `file_delete`, `api_call`, `shell_exec` |

Empty `side_effects` list = pure function (no side effects).

### 3.5 Markdown Body

**Required sections**:

| Section | Content |
|---|------|
| **Governance Declaration** | Declare adherence to AIAP protocol + Axiom 0 alignment |
| **Feature Overview** | List core features by module/intent |
| **Usage** | Entry file, tool requirements, prerequisites |

**Recommended sections** (when status=active):

| Section | Content |
|---|------|
| **Example Interactions** | 1-3 typical usage scenario input/output examples |
| **Applicable Conditions** | Clearly state scenarios where the program is and is not applicable |

**Optional sections**:

| Section | Content |
|---|------|
| **Data Storage** | Data file paths and formats |
| **Configuration** | Configurable params and defaults |
| **Quality Status** | ThreeDimTest scores, Pipeline history |
| **Version History** | Major version change summaries (structured format see §25) |
| **Error Handling** | Common errors and user handling instructions |

**File ending**: Must end with the AIAP closing seal.

| governance_mode | Seal Format |
|----------------|---------|
| NORMAL | `Align: Human Sovereignty and Wellbeing. Version: AIAP V1.0.0. www.aiap.dev` |
| DEV | `[L0_BOOT: Success] [L1_REPORT: Success] [endNode_Align: Human Sovereignty and Wellbeing]. Version: AIAP V1.0.0. www.aiap.dev` |

### 3.6 Creator Auto-Maintenance Rules

| Trigger Event | Creator Behavior |
|---------|-------------|
| **Create** | Auto-generate AIAP.md, populate all required fields, set status to draft |
| **Evolve** | Update version, modules, quality, summary (if changed) |
| **Modify** | Update version, quality |
| **Validate** | Check AIAP.md existence and field completeness (D8 check) |
| **QualityGate Pass** | If status=draft, automatically upgrade to active |
| **version_history snapshot** | Save AIAP.md snapshot in `{version}/` directory |

---

## Part II: Structural Specification

---

## 4. Node = Functional Responsibility

> Nodes match functions, main routes and dispatches, modules are self-contained, shared logic is extracted separately, no infinite splitting.

Each Mermaid node represents one functional responsibility of a module, similar to a function in a Python file. The number of nodes is naturally determined by functional complexity, not imposed by external hard limits.

```
Python analogy:
  record.py has 4 functions → record.aisop.json has 4 functional nodes
  query.py has 6 functions  → query.aisop.json has 6 functional nodes
  Node count follows function count, not quotas
```

---

## 5. Functional Node Count

```
Functional nodes = Total Mermaid nodes - Start - endNode
```

Start and endNode are the fixed structural framework of every AISOP file (similar to Python's `if __name__`), they don't reflect functional complexity and are not counted.

Example:

```
graph TD
    Start --> Parse --> Validate{OK?} --> Save --> Alert --> endNode
                                       --> AskFix --> Parse
```

Total nodes 7, functional nodes 5 (Parse, Validate, Save, Alert, AskFix).

---

## 6. Progressive Node Guidelines

Applies to all `.aisop.json` files (including main):

```
Functional nodes 3-12  → Normal, no prompt
Functional nodes 13-15 → ADVISORY — Suggest checking for split opportunities, provide specific suggestions
Functional nodes 16+   → RECOMMENDED — Strongly recommend splitting, provide split plan
```

- Both levels are WARNING, not FAIL
- Functionally cohesive large modules can annotate `fractal_exempt` to skip the suggestion
- Minimum requirement: >=3 functional nodes + (>=1 tool call OR >=3 steps)

---

## 7. fractal_exempt Annotation

When a module's functional nodes exceed 12 but the flow is highly cohesive, annotate in `system.content`:

```json
{
    "fractal_exempt": "The pipeline's 13 stages form a continuous pipeline; splitting would cause context fragmentation"
}
```

After annotation, Creator skips the progressive split suggestion for that file. Equivalent to Python's `# noqa`.

## 7.1. sub_mermaid Decomposition Rules

When a module's complexity exceeds thresholds but splitting into separate files would break functional cohesion, use sub_mermaid decomposition — multiple Mermaid graphs within a single `.aisop.json` file.

### 7.1.1. Structure

The `aisop` object contains multiple graph keys. `main` is always the entry point:

```json
{
  "aisop": {
    "main": "graph TD\n    Start[...] --> SubA[aisop.sub_a]\n    SubA --> SubB[aisop.sub_b]\n    ...",
    "sub_a": "graph TD\n    SubAStart[...] --> ...",
    "sub_b": "graph TD\n    SubBStart[...] --> ..."
  }
}
```

Rules:
- Entry point: always `ASSERT RUN aisop.main` (instruction immutable constant)
- Main graph references sub-graphs via `NodeName[aisop.sub_name]` syntax
- All functions from all sub-graphs share a single flat `functions` dictionary
- Parameters are defined once at root level and shared across all sub-graphs
- Each sub-graph has its own Start node and End node

### 7.1.2. Decomposition Priority

When complexity exceeds §6 thresholds, apply decomposition in this order:

```
Priority 0 — sub_mermaid (in-file sub-graph decomposition)
  Same file, shared context, no cross-file contracts needed.
  Preferred when:
    (a) Nodes share params and working context
    (b) Sub-graphs have data dependencies (output of one feeds next)
    (c) Splitting into files would duplicate shared parsing/setup logic

Priority 1 — sub_aisop (file-level split)
  Per §13 split rules. Required when:
    (a) Sub-graphs use entirely different tool sets (§13 Priority 1)
    (b) Sub-graphs are independently testable and deployable
    (c) A single sub-graph exceeds 16 functional nodes after sub_mermaid

Priority 2 — Sub_AIAP (directory-level split)
  Per §13. Required when sub_aisop files form a full independent program.
```

### 7.1.3. Execution Modes

Sub-graphs execute in one of the following modes. Declare the mode in `fractal_exempt`:

| Mode | Description | Example |
|------|-------------|---------|
| **Mutually Exclusive** | Main routes to exactly one sub-graph per invocation | advisor: 8 sub-graphs, TypeGate selects 1 |
| **Sequential** | Main calls sub-graphs in fixed order, each feeds the next | generate: scaffold → content → tooling |
| **Conditional** | Main selects a subset of sub-graphs based on runtime conditions | (future use) |
| **Hybrid** | Combines above modes (e.g., sequential stages where one stage uses conditional routing) | (future use) |

### 7.1.4. Node Counting Rules

For files with sub_mermaid:

1. **Total functional nodes** = sum of (functional nodes per sub-graph).
   Per-graph functional nodes = total graph nodes − Start − endNode.

2. **Single-path maximum** = functional nodes traversed in the longest execution path:
   - Mutually exclusive: main functional nodes + max(sub-graph functional nodes)
   - Sequential: main functional nodes + sum(all sub-graph functional nodes)
   - Conditional: main functional nodes + sum(selected sub-graph functional nodes)

3. **Threshold application**: Apply §6 thresholds to single-path maximum, not total.
   If single-path maximum exceeds 16, `fractal_exempt` annotation is required.

4. **fractal_exempt format** for sub_mermaid files:
   `"{total} functional nodes distributed across {N} sub_mermaid sub-graphs
   ({breakdown}). Sub-graphs execute {mode}. Maximum single-path execution
   {max} nodes."`

### 7.1.5. Function Body Complexity (Second Dimension)

Node count alone does not capture intra-function complexity (e.g., a single Generate node with 23 directives in step1). Apply a second-dimension check:

- **Steps per function**: count step keys (step1, step2, ..., stepN)
- **Directives per step**: count named directive blocks within a step
  (identified by UPPERCASE LABEL: pattern, e.g., "TOOL ANNOTATIONS:", "INCREMENTAL GENERATION:")

Thresholds:
- 8+ steps in one function → ADVISORY: consider sub_mermaid decomposition
- 15+ directives in one step → ADVISORY: consider splitting into multiple functions
- 20+ directives in one step → RECOMMENDED: decompose via sub_mermaid or file split

---

## 8. Pattern Selection

```
Number of independent functions → Pattern:
  1 function              → A: Script (single file)
  2+ functions            → B: Package (multiple files)
  2+ functions + complex shared → C: Package + Shared
  Sub-modules also need splitting → D: Nested Package
  With memory layer       → E: Package + Memory
  Multi-AIAP program ecosystem → F: Ecosystem
  With embedded tool directory → G: Embedded Runtime
```

---

## 9. Pattern A-G Detailed Definitions

### Pattern A: Script

```
{name}_aiap/
├── AIAP.md                     # Required: governance contract
└── main.aisop.json             # All logic
```

Applicable: todo list, timer, calculator, and other single-function programs. No hard limits. Progressive guidelines apply.

### Pattern B: Package

```
{name}_aiap/
├── AIAP.md                     # Required: governance contract
├── main.aisop.json             # Router: intent recognition → dispatch
├── {func1}.aisop.json          # Functional module (fully self-contained)
├── {func2}.aisop.json
└── {func3}.aisop.json
```

Example:
```
expense_tracker_aiap/
├── AIAP.md                     # Governance contract
├── main.aisop.json             # Intents: record / query / budget / report
├── record.aisop.json           # Validate → Write → Confirm
├── query.aisop.json            # Parse → Read → Filter → Format
├── budget.aisop.json           # Set → Check → Alert
└── report.aisop.json           # Aggregate → Analyze → Display
```

### Pattern C: Package + Shared

```
{name}_aiap/
├── AIAP.md                     # Required: governance contract
├── main.aisop.json             # Router
├── {func1}.aisop.json
├── {func2}.aisop.json
└── shared.aisop.json           # Complex shared logic called by 2+ modules
```

Shared rule: Create only when 2+ modules reuse **complex operations**. Simple sharing (formatting/style) goes in each module's system_prompt.

### Pattern D: Nested Package

```
{name}_aiap/
├── AIAP.md                     # Required: governance contract
├── main.aisop.json             # Top-level router
├── {simple_func}.aisop.json    # Simple module
└── {complex}_sub_aiap/         # Complex module (has sub-structure)
    ├── AIAP.md                 # Sub-package governance contract (if independently published)
    ├── main.aisop.json         # Sub-router
    ├── {sub1}.aisop.json
    └── {sub2}.aisop.json
```

Nesting rule: Maximum 2 levels, nest only when the sub-module itself has 2+ sub-functions.

#### Pattern D Example: AIAP Creator

```
aiap_creator_aiap/
├── AIAP.md                     # Governance contract (AIAP V1.0.0)
├── main.aisop.json             # Top-level orchestrator (28 functional nodes, fractal_exempt)
│   └── Intents: Create, Evolve, Modify, Validate, Simulate, Compare, Explain, General
│   └── Pipeline: Research→Evolve→Generate→Modify→QualityGate→Validate→Simulate→Observability→Review
├── generate.aisop.json         # Generator (11 functional nodes)
├── research.aisop.json         # Shared research module (15 functional nodes, fractal_exempt, 3-mode reuse)
├── review.aisop.json           # Reviewer (11 functional nodes)
├── simulate.aisop.json         # Simulator (10 functional nodes)
├── modify.aisop.json           # Modifier (10 functional nodes)
├── observability.aisop.json    # Telemetry analysis (9 functional nodes)
├── advisor.aisop.json          # Advanced advisor (52 functional nodes, fractal_exempt, 8 mutually exclusive sub-graphs)
├── AIAP_Standard.core.aisop.json         # Core quality standard (C1-C7, I1-I7, D1-D7, PL1-PL12, PL19-PL21, MF1-MF9)
├── AIAP_Standard.security.aisop.json     # Security extension (I8-I11, I13 Embedded Code Safety, D8-D10, AT1-AT6, Code Trust Gate)
├── AIAP_Standard.ecosystem.aisop.json    # Ecosystem extension (MF10-MF14, MF16, K1-K10, PL16-PL17, PL22, PL25)
├── AIAP_Standard.performance.aisop.json  # Performance extension (PL13-PL15, PL18-PL21, PL23-PL24, QRG1-QRG5)
└── AIAP_Protocol.md            # Structural specification (Protocol-level)
```

Characteristics:
- 8+4 modules (8 executable modules + 4 STANDARD extension files), ~146 functional nodes total
- main is a pure orchestrator (sequential delegation, no business logic), annotated fractal_exempt
- research reuses 3 modes via ModeGate (structure/quality/compliance), annotated fractal_exempt
- advisor uses sub_mermaid sub-graphs (8 mutually exclusive sub-graphs), actual single-path maximum 15 nodes (main 8 + largest sub-graph 7)
- Communication topology is star-shaped (main orchestrates), no direct inter-module communication

### Pattern E: Package + Memory

```
{name}_aiap/
├── AIAP.md                     # Required: governance contract
├── main.aisop.json             # Router
├── {func1}.aisop.json
├── {func2}.aisop.json
└── memory/                     # Memory layer
    ├── schema.json             # Memory field definitions (episodic/semantic/working)
    ├── decay_config.json       # Decay strategy params
    └── context_manager.json    # Context budget and loading strategy
```

Applicable: AIAP programs requiring cross-session memory, personalization, or RAG retrieval. Use advisor.aisop.json (advisor_type='memory') to generate memory/ directory content.

### Pattern F: Ecosystem

```
{ecosystem_name}/
├── AIAP.md                     # Required: ecosystem-level governance contract
├── blueprint.json              # Ecosystem blueprint (components, interfaces, topology)
├── {component1}_aiap/          # Independent component (Pattern A-E)
│   ├── AIAP.md                 # Required: component-level governance contract
│   └── main.aisop.json
├── {component2}_aiap/
│   ├── AIAP.md
│   └── ...
└── shared/                     # Cross-component shared data contracts
    └── data_contracts.json
```

Applicable: Complex systems with 3+ AIAP program components collaborating. Use advisor.aisop.json (advisor_type='orchestrate') to design ecosystem blueprints.

#### blueprint.json Component Interface Declaration

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
├── AIAP.md                     # Required: governance contract (with tool_dirs field)
├── agent_card.json             # Program self-description (unconditional since P11)
├── main.aisop.json             # Router
├── {func1}.aisop.json
├── {func2}.aisop.json
├── python_tools/               # Python tool implementations
│   ├── README.md               # Required: tool description, interfaces, security constraints
│   ├── requirements.txt        # Frozen versions (== pinning, >= / * / ~= prohibited)
│   ├── *.py                    # Tool code
│   └── mcp_adapter.py          # Creator auto-generated MCP stdio endpoint
├── ts_tools/                   # TypeScript tool implementations
│   ├── README.md
│   ├── package.json            # Exact versions (^ ~ prohibited)
│   ├── package-lock.json       # Lock transitive dependencies
│   └── *.ts
├── go_tools/                   # Go tool implementations
│   ├── README.md
│   ├── go.mod + go.sum         # Dependency lock
│   └── bin/tool                # Pre-compiled binary (recommended)
├── rust_tools/                 # Rust tool implementations
│   ├── README.md
│   ├── Cargo.toml + Cargo.lock
│   └── target/release/tool     # Must be pre-compiled
├── shell_tools/                # Shell scripts (T4 + manual audit only)
│   ├── README.md
│   └── tool.sh / tool.ps1
├── mcp_tools/                  # MCP Server definition layer
│   ├── README.md
│   └── mcp_server.json         # MCP Server manifest + runtime declaration
├── a2a_tools/                  # A2A bridge configuration layer (optional, Pattern F/G only)
│   ├── README.md
│   └── bridge_config.json
├── n8n_tools/                  # n8n workflow automation layer (optional)
│   ├── README.md
│   ├── workflow.json
│   └── config.json
├── aiap_tools/                 # AIAP sub-program tools (optional)
│   ├── README.md               # Required: sub-program inventory, invocation interface, security constraints
│   ├── data_cleaner_aiap/      # A complete AIAP program used as a tool
│   │   ├── AIAP.md
│   │   ├── main.aisop.json
│   │   └── transform.aisop.json
│   └── report_gen_aiap/        # Another AIAP program
│       ├── AIAP.md
│       └── main.aisop.json
├── other_tools/                # Open extension layer (optional)
│   └── README.md               # Required: invocation method, interfaces, security constraints
└── memory/                     # Pattern E memory layer (optional)
    └── ...
```

Inherits: All rules from Pattern E or F

Additional requirements:
- AIAP.md must include a `tool_dirs` field declaring tool directories
- `mcp_tools/mcp_server.json` must exist
- I13 Embedded Code Safety rules apply (10 sub-checks)
- MF16 Tool Directory Consistency rules apply
- Minimum trust level: T3
- Requires Code Trust Gate verification

Characteristics:
- CLI executors have native shell tools and can directly execute bundled code
- No intermediate layer or pre-installed tools needed
- Self-contained, independently deployable

#### Supported tool_dirs Directory Types

| Type | Runtime | Dependency Lock | Use Cases |
|------|--------|---------|---------|
| `python_tools/` | Python 3.9-3.13 | `requirements.txt` (== pinning) | Data processing, AI/ML, file operations |
| `ts_tools/` | Node.js/Deno/Bun | `package-lock.json` | Web API, JSON processing, type safety |
| `go_tools/` | Go or pre-compiled binary | `go.sum` | High concurrency, CLI, low latency |
| `rust_tools/` | Pre-compiled binary | `Cargo.lock` | High performance, memory safety, WASM |
| `shell_tools/` | bash / pwsh | None | System scripts (T4 only) |
| `mcp_tools/` | stdio transport | `mcp_server.json` | MCP ecosystem tools |
| `a2a_tools/` | A2A protocol | `bridge_config.json` | Inter-agent collaboration (bridge config, Pattern F/G only) |
| `n8n_tools/` | n8n instance | `workflow.json` | Multi-service integration |
| `aiap_tools/` | AIAP Executor | `AIAP.md` (per sub-program) | AIAP programs as callable tools |
| `other_tools/` | Custom | README.md | Open extension |

#### mcp_server.json Format

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

Pattern G programs must pass the Code Trust Gate security verification upon loading:

```
Load Pattern G program
    ↓
Code Trust Gate:
  1. governance_hash verification (covers all files including tool_dirs source code)
  2. Static analysis: import/require declarations vs permissions.network
  3. File hash verification (against mcp_server.json file_hashes)
  4. Trust level check (Pattern G minimum T3)
  5. Dependency lock file verification
    ↓
  [T3 mode] Requires human review confirmation
  [T4 mode] Auto-pass
    ↓
Start MCP Server (stdio)
    ↓
AIAP program execution (invokes tools via MCP)
```

##### Recursive Code Trust Gate for aiap_tools/

When aiap_tools/ directory is detected during Code Trust Gate:

```
Code Trust Gate (existing steps 1-5 above)
    ↓
Step 6: Shell audit (existing)
    ↓
Step 7: Detect aiap_tools/ directory?
    ↓ Yes
Initialize call_stack = []
Push parent.program_id to call_stack
For each aiap_tools/{name}_aiap/:
  1. Read AIAP.md — extract program_id, trust_level, permissions, governance_hash
  2. CIRCULAR DEPENDENCY CHECK: if program_id in call_stack → FAIL (CIRCULAR_DEPENDENCY)
  3. Push program_id to call_stack
  4. TRUST CEILING CHECK: trust_level <= parent.trust_level → or FAIL
  5. PERMISSION SUBSET CHECK: permissions ⊆ parent.permissions → or FAIL
  6. GOVERNANCE HASH CHECK: recompute and verify → or FAIL
  7. RECURSION DEPTH CHECK: current_depth < 3 → or FAIL
  8. If sub-program is Pattern G with aiap_tools/ → recurse (depth + 1)
  9. Pop program_id from call_stack (finally semantics — even on failure)
    ↓
[Any sub-program fails] → Entire Code Trust Gate FAIL
    ↓ No aiap_tools/ or all pass
Continue normal MCP Server startup
```

#### I13 Embedded Code Safety (10 Sub-Checks)

Applicable: Pattern G programs (with tool_dirs). Pattern A-F marked N/A.

| Sub-Check | Description |
|--------|------|
| **(a) CODE INTEGRITY** | SHA-256 hashes of all source/binary files in tool_dirs/ must be recorded in mcp_server.json file_hashes |
| **(b) NETWORK DECLARATION** | Detect network access APIs (requests/fetch/net/http, etc.); if present, permissions.network.allowed must be true |
| **(c) FILE SYSTEM SCOPE** | File write operations must not exceed permissions.file_system.scope |
| **(d) DEPENDENCY VERSION PINNING** | Python: == pinning; TS/JS: ^ ~ prohibited; Go: go.sum must exist; Rust: Cargo.lock must exist |
| **(e) MCP PROXY REQUIRED** | All code tools must be exposed through the mcp_tools/ layer; executor direct subprocess execution of source files is prohibited |
| **(f) SHELL AUDIT** | When shell_tools/ exists, trust_level must be ≥ T4 |
| **(g) AIAP TRUST CEILING** | When aiap_tools/ exists: each sub-program's trust_level must be <= parent's trust_level |
| **(h) AIAP PERMISSION SUBSET** | When aiap_tools/ exists: sub-program permissions.file_system.scope must be within parent scope; sub-program permissions.network.endpoints must be subset of parent endpoints |
| **(i) AIAP RECURSION DEPTH** | aiap_tools/ nesting depth must not exceed 3. Verify by traversing sub-program tool_dirs for nested aiap_tools/ |
| **(j) AIAP GOVERNANCE HASH** | Each sub-program's governance_hash must be verified (recomputed and compared to AIAP.md declaration) |

#### MF16 Tool Directory Consistency

Applicable: Pattern G programs.

| Check | Description |
|------|------|
| **(a)** | mcp_server.json exists at the declared path |
| **(b)** | mcp_server.json exposed_tools entries have corresponding declarations in AIAP.md tools[] |
| **(c)** | AIAP.md tools[] entries referencing mcp_server exist in exposed_tools |
| **(d)** | agent_card.json exists at program root and fields match AIAP.md (unconditional since P11) |
| **(e)** | When aiap_tools/ exists: each sub-directory must contain a valid AIAP.md with all 6 required governance fields present |
| **(f)** | Each aiap_tools/ sub-program's AIAP.md governance fields structurally complete (protocol, authority, seed, executor, axiom_0, governance_mode all present and non-empty) |
| **(g)** | Each aiap_tools/ sub-program's tool_dirs declarations (if any) match actual directory structure within the sub-program |
| **(h)** | Parent AIAP.md tools[] entries using `aiap:{name}` prefix must have corresponding sub-programs in aiap_tools/{name}_aiap/ |

#### aiap_tools/ Invocation Protocol

aiap_tools/ enables AIAP programs to invoke other AIAP programs as tools, creating a native tool-level relationship without requiring an MCP Server intermediary.

##### Invocation Mechanism

1. Parent program references a sub-program tool in its AISOP functions using the `aiap:{name}` prefix
2. Executor detects `aiap:` prefix and locates `aiap_tools/{name}_aiap/` in program root directory
3. Executor reads sub-program's `AIAP.md` and verifies trust and permissions (see Code Trust Gate extension)
4. Executor loads sub-program in a child execution context with inherited constraints
5. Sub-program executes and returns result to parent's calling node

##### Security Constraints

- **Trust Ceiling**: Sub-program's `trust_level` MUST be <= parent's `trust_level`
- **Permission Subset**: Sub-program's `permissions` scope MUST be a subset of parent's `permissions`
- **Recursion Depth**: Maximum nesting depth of aiap_tools is 3 (parent → child → grandchild → great-grandchild)
- **Circular Dependency Prevention**: Executor MUST maintain a call stack of program IDs; if a program ID appears twice in the stack, execution MUST fail with CIRCULAR_DEPENDENCY error
- **Governance Integrity**: Sub-program's `governance_hash` MUST verify before execution

##### Resource Isolation

| Resource | Isolation Strategy |
|----------|-------------------|
| memory/ | Sub-program uses own memory/ only, cannot access parent memory/ |
| Logs | Sub-program logs prefixed with `[aiap:{name}]`, merged into parent log stream |
| Temp files | Sub-program temp files in `aiap_tools/{name}_aiap/.tmp/`, cleaned after execution |
| Environment | Sub-program does NOT inherit parent environment variables |
| token_budget | Sub-program allocated from parent's remaining token_budget |

##### Error Propagation

```
Sub-program GREEN        → Parent step completes normally
Sub-program AMBER/YELLOW → Parent receives WARNING, follows fallback strategy
Sub-program RED/FAIL     → Parent receives ERROR, triggers Error handling
Sub-program TIMEOUT      → Executor force-terminates, parent receives TIMEOUT_ERROR
```

Timeout controlled by Executor (not parent AISOP node). Priority: AISOP function timeout_seconds > sub-program AIAP.md runtime.timeout_seconds > default 60s.

call_stack cleanup: Executor guarantees pop on failure (finally semantics).

##### README.md Requirements

aiap_tools/README.md MUST contain:

| Section | Content |
|---------|---------|
| Overview | Purpose of aiap_tools/ directory |
| Sub-Program Inventory | For each sub-program: name, summary, pattern, trust_level |
| Invocation Interface | Calling convention (aiap:{name}), input/output contracts |
| Security Constraints | Trust inheritance, permission boundaries, recursion limits |

##### Version Compatibility

- Sub-program's `min_protocol_version` MUST be <= parent's `protocol` version
- When parent evolves, sub-program versions are NOT automatically bumped (independent lifecycle)
- Parent's AIAP.md SHOULD declare sub-program version expectations in `dependencies[]`

#### Backward Compatibility

- The tool_dirs field is entirely optional
- Programs without tool_dirs (Pattern A-F) are unaffected
- I13 and MF16 are marked N/A for non-Pattern G programs
- The governance_hash algorithm is unchanged for non-Pattern G programs

---

## 10. main.aisop.json Rules

main follows the same progressive node guidelines as functional modules. The distinction is a **qualitative constraint** (not a quantitative one):

**Pattern A**: main is the only file, contains all logic, no special constraints.

**Pattern B+**: main is a router:
- Contains only routing logic + lightweight inline handling
- No business logic (data processing, file I/O, complex validation)
- tools = union of all sub-module tools
- The number of routing nodes is naturally determined by the number of intents
- Invocation method: intent recognition → read corresponding sub-file → AI Agent executes

```
Determining whether a node belongs to main:
  ≤2 steps + no tool calls → OK (lightweight inline, e.g., Explain, General)
  >2 steps or has tool calls → should be placed in sub_aisop
```

---

## 11. Functional Module Rules

- Fully self-contained (independent system_prompt / tools / params / functions)
- Does not depend on other modules' internal implementations
- Module internal depth is determined by function, progressive guidelines apply
- Minimum requirement: >=3 functional nodes + (>=1 tool call OR >=3 steps)

---

## 12. Independent Function Judgment

Can be described in one sentence + does not share dedicated tools/state + can be tested independently → separate into its own file

- Level 1 tools (file_system, shell) are general infrastructure and do not count as "shared tools"
- Modules that read/write the same data file via file_system can still be independent (each responsible for different operations)
- "Shared state" refers to runtime memory state or dedicated connections, not persisted data files

---

## 13. Sub_AIAP Split Rules

When Creator suggests splitting, analyze split boundaries in the following priority order:

```
Priority 1 — Tool boundaries:
  Node group A uses google_search + web_browser
  Node group B uses only file_system
  → Natural boundary, split into independent sub_aiap

Priority 2 — Data flow stages:
  Clear stage boundaries in a linear pipeline (research → generate → test)
  → Each stage is a sub_aiap candidate

Priority 3 — Functional independence:
  Meets the three conditions for independent function judgment
  → Split into sub_aiap
```

**Patterns that must not be split**:
- Convergence node groups (many-to-one fan-in pattern) → keep in the same sub_aiap
- Error recovery loops (Error → Retry → original node) → keep in the same sub_aiap
- Tightly coupled nodes sharing the same tool + state → keep in the same sub_aiap

---

## 14. Pattern Upgrade Convergence Handling

When upgrading from Pattern A→B and splitting files, existing convergence/display nodes (e.g., Respond, Display, Output) need special handling:

```
Convergence node determination:
  Does the node have >2 steps or tool calls?
    → Does not meet main inline criteria, must be assigned to a sub-module

  Do multiple sub-modules need this node's logic?
    → Each sub-module creates its own dedicated version (customized to its output format)
    → Do not create shared.aisop.json (unless logic is complex and completely identical)

  Only one sub-module uses it?
    → Directly include in that sub-module
```

Example:
```
Pattern A (before split):
  SearchRecipes → ReadRecipe → NutritionAnalysis → Respond → endNode
  SaveCollection → Respond → endNode
  CompareView → Respond → endNode
  (Respond is a full-path convergence point, 4 steps + tool references)

Pattern B (after split):
  search.aisop.json:  ...→ SearchRespond → endNode  (search result display)
  collection.aisop.json: ...→ CollectionRespond → endNode (collection operation display)
  (Each sub-module has a dedicated Respond, content customized per module output)
```

---

## 15. Dual-Stream Rules

Complex projects (Pattern D+) may optionally provide both human-readable and AI-optimized versions:

```
{name}_aiap/
├── AIAP.md
├── main.human.aisop.json      # Human-readable version (full key names)
├── main.ai.aisop.json         # AI-optimized version (compressed key names)
└── ...
```

Rules:
- Both versions must have completely identical logical semantics
- `.human` version uses full key names, convenient for human review
- `.ai` version uses abbreviated key names, reducing token consumption
- AI Agent preferentially loads the `.ai` version, loads the `.human` version for debugging
- Non-dual-stream projects still use a single `.aisop.json` (without `.human` or `.ai` prefix)

---

## Part III: Security & Runtime

---

## 16. Trust Levels

AIAP programs declare their permission requirements and execution modes through `trust_level`.

### 16.1 Four-Tier Trust Definition

| Tier | Name | Meaning | Permission Scope |
|------|------|------|---------|
| **T1** | Metadata-Only | Read AIAP.md frontmatter only | Does not load .aisop.json content |
| **T2** | Instruction-Read | Can read .aisop.json instruction content | Cannot execute any tool calls |
| **T3** | Supervised | Requires human approval or sandbox environment for execution | Each tool call requires confirmation |
| **T4** | Autonomous | Executes autonomously within declared permission boundaries | Follows permissions field constraints |

### 16.2 Relationship Between Trust Levels and Capabilities

| trust_level | Executable Operations | Typical Use Cases |
|-------------|-------------|---------|
| T1 | Read summary, name, description | Program directory indexing, search result display |
| T2 | Read complete flowcharts, function definitions | Code review, documentation generation, teaching |
| T3 | Execute all tool calls under human supervision | First-run new programs, high-risk operations |
| T4 | Autonomously execute all declared tool calls | Verified production programs |

### 16.3 Declaration Method

```yaml
# AIAP.md frontmatter
trust_level: 3    # Default value, optional field
```

When trust_level is not declared, the executor should treat it as T3 (Supervised).

---

## 17. Permission Boundaries

T4 (Autonomous) programs **must** declare permission boundaries through `permissions`. This field is optional for T1-T3 programs.

### 17.1 Declaration Format

```yaml
# AIAP.md frontmatter
permissions:
  file_system:
    scope: "./data/"            # Read/write scope restriction (relative to project root)
    operations: ["read", "write"]
  shell:
    allowed: false              # Prohibit shell calls
  network:
    allowed: false              # Prohibit network calls
```

### 17.2 Permission Types

| Permission | Attribute | Description |
|------|------|------|
| **file_system** | `scope` | Directories allowed for access (glob syntax) |
| | `operations` | Allowed operations: `read`, `write`, `delete` |
| **shell** | `allowed` | Whether shell execution is allowed |
| | `allowlist` | List of allowed commands (only when allowed=true) |
| **network** | `allowed` | Whether network requests are allowed |
| | `endpoints` | List of allowed URL patterns |

### 17.3 Executor Responsibilities

The executor (SoulBot) **must** do the following when running T4 programs:
1. Read the `permissions` declaration
2. Verify whether tool calls are within the declared scope before execution
3. Out-of-scope calls → Reject execution + Report security violation

---

## 18. Integrity Verification

### 18.1 governance_hash Algorithm

```
governance_hash = SHA-256(
    All .aisop.json file contents (concatenated in alphabetical order by filename, CRLF→LF normalized)
)

Pattern G Extension:
  The .aisop.json file set remains unchanged. File hashes of tool_dirs/ are recorded
  in the file_hashes field of mcp_server.json, indirectly covered by governance_hash.
  The governance_hash algorithm for programs without tool_dirs remains unchanged (backward compatible).
```

Output format: `"sha256:{hash_value}"` (64-character hexadecimal)

### 18.2 Requirement Rules

| trust_level | governance_hash |
|-------------|----------------|
| T1-T2 | Optional |
| T3 | Recommended |
| T4 | Recommended |
| Published to Registry | Required |

### 18.3 Verification Process

Creator ValidateStep performs verification:
1. Compute the SHA-256 hash of the current files
2. Compare with the governance_hash declared in AIAP.md
3. Mismatch → WARNING: "Integrity check failed — files may have been modified outside Creator pipeline"

---

## 19. Runtime Constraints

### 19.1 Declaration Format

```yaml
# AIAP.md frontmatter
runtime:
  timeout_seconds: 300          # Per-execution timeout (default: executor-determined)
  max_retries: 3                # Maximum retry count (default: 3)
  token_budget: 50000           # Token budget limit (default: unlimited)
  idempotent: false             # Whether overall execution is idempotent (default: false)
  side_effects:                 # Overall side effect declarations
    - file_write
    - api_call
```

### 19.2 Field Descriptions

| Field | Meaning | Purpose |
|------|------|------|
| `timeout_seconds` | Timeout limit for a single complete execution | Prevent infinite execution |
| `max_retries` | Maximum retry count for RECOVERABLE errors | Control retry overhead |
| `token_budget` | Token consumption limit for a single execution | Cost control |
| `idempotent` | Whether repeated execution produces the same result | Orchestrator determines if safe retry is possible |
| `side_effects` | List of side effects for the overall program | Orchestrator assesses execution risk |

### 19.3 Relationship with modules

- Program-level `runtime.side_effects` = Union of all module `side_effects`
- Program-level `runtime.idempotent` = true when all critical modules are `idempotent`
- Module-level attributes (§3.4) provide fine-grained control; program-level attributes provide a quick overview

---

## 20. Error Handling Protocol

### 20.1 Error Classification

| Category | Meaning | Strategy |
|------|------|------|
| **RECOVERABLE** | Transient failures (network timeout, file lock, API throttling) | Retry per `max_retries`, exponential backoff |
| **DEGRADABLE** | Non-critical module failure (`critical: false`) | Skip failed module, execute in degraded mode, mark WARNING |
| **FATAL** | Critical module failure (`critical: true`) or security violation | Stop immediately, report error, produce no output |

### 20.2 Retry Strategy

```
Retry interval: 1s, 2s, 4s, 8s, ... (exponential backoff, base=2)
Maximum retries: runtime.max_retries (default 3)
Maximum interval: min(2^retry_count, 30) seconds
Each retry must log: error reason + retry count + timestamp
```

### 20.3 Degradation Behavior

When a module execution fails and the module has `critical: false`:
1. Skip that module's output
2. Mark in the final result: `"DEGRADED: {module_name} skipped due to {error}"`
3. Does not affect the overall success/failure determination
4. Final result includes a list of degraded modules

### 20.4 Termination Conditions

Each AIAP program execution terminates under the following conditions:

| Termination Type | Condition | Result |
|---------|------|------|
| **Successful Termination** | All critical modules completed + output passes validation | Return complete result |
| **Timeout Termination** | `runtime.timeout_seconds` reached | Return completed portion + timeout marker |
| **Error Termination** | FATAL-level error triggered | Return error report, no partial results |
| **Degraded Termination** | Successful termination but with skipped modules | Return degraded result + degradation report |

---

## Part IV: Engineering Capabilities

---

## 21. Discovery Protocol

### 21.1 Discovery Layers

| Layer | Method | Mechanism | Token Cost |
|------|------|------|-----------|
| **L1 Passive Discovery** | File system scan | Scanner traverses directories, identifies `_aiap/` directories containing AIAP.md | ~50-80/program |
| **L2 Semantic Discovery** | Intent matching | Match user queries against `intent_examples` by semantic similarity | 0 (pre-computed) |
| **L3 Registry Discovery** | Registry query | Query published programs via AIAP Registry (aiap.dev) | ~100/query |

### 21.2 L1 Scanning Protocol

The scanner should search for AIAP programs in the following order:

1. `*_aiap/` subdirectories under the current working directory
2. Configured AIAP library paths (e.g., `~/.aiap/library/`)
3. Dependency paths declared in the project's `aiap.config`

For each discovered AIAP program:
1. Read AIAP.md YAML frontmatter (L1 metadata, ~50-80 tokens)
2. Register to the available program inventory (name + summary + status)
3. Load full content only when matched (L2+L3)

### 21.3 L2 Semantic Matching

```yaml
# AIAP.md frontmatter
intent_examples:
  - "Record today's weight"
  - "View this week's blood pressure trend"
  - "Generate monthly health report"
discovery_keywords:
  - health
  - tracking
  - wellness
```

Matching process:
1. Convert `intent_examples` to embedding vectors
2. When a new query arrives, compute cosine similarity with existing vectors
3. Similarity exceeds threshold → candidate match
4. Rank using `summary` + `discovery_keywords`

### 21.4 Invocation Modes

| Mode | Trigger Method | Matching Mechanism |
|------|---------|---------|
| **Explicit Invocation** | User specifies program name (e.g., "use health_tracker") | Exact match on `name` field |
| **Implicit Invocation** | LLM automatically selects based on user intent | Semantic matching on `summary` + `intent_examples` |

---

## 22. Dependency Resolution

### 22.1 Dependency Declaration

```yaml
# AIAP.md frontmatter
dependencies:
  - name: shared_utils_aiap
    version: "^1.0.0"           # semver range constraint
    required: true
  - name: analytics_aiap
    version: ">=2.0.0"
    required: false              # Optional dependency
    fallback: "skip"             # When unavailable: "skip" / "degrade" / "error"
```

### 22.2 Version Constraint Syntax

| Syntax | Meaning | Match Examples |
|------|------|---------|
| `"1.2.3"` | Exact version | 1.2.3 only |
| `"^1.2.0"` | Compatible updates | >=1.2.0 and <2.0.0 |
| `"~1.2.0"` | Patch updates | >=1.2.0 and <1.3.0 |
| `">=1.0.0"` | Minimum version | >=1.0.0 |

### 22.3 Resolution Strategies

1. **Flat Resolution** (default) — All dependencies are resolved at the same level; when version conflicts arise, the highest compatible version satisfying all constraints is selected
2. **Isolated Resolution** — In Pattern F Ecosystem, each component resolves dependencies independently, interacting through `data_contracts`

### 22.4 Conflict Resolution

When multiple AIAP programs depend on different versions of the same program:
- Automatically select the highest version satisfying all constraints
- If no version can satisfy all constraints → Report conflict, require human decision
- Conflict report includes: conflicting dependency name, source of each constraint, possible solutions

---

## 23. Program Lifecycle

### 23.1 Lifecycle States

| State | Meaning | AIAP.md Field | Creator Behavior |
|------|------|-------------|-------------|
| **draft** | In development, unstable | `status: draft` | Automatically set during Create phase |
| **active** | Production-ready | `status: active` | Automatically upgraded after first QualityGate pass |
| **deprecated** | Planned for deprecation | `status: deprecated` + `deprecated_date` + `successor` | Manually marked by human |
| **archived** | Archived, read-only | `status: archived` | Automatically archived 90 days after deprecated_date |

### 23.2 State Transitions

```
draft → active → deprecated → archived
                      ↓
              (successor takes over)
```

### 23.3 Deprecation Protocol

1. Mark `status: deprecated` + set `deprecated_date`
2. Add deprecation notice in the AIAP.md governance declaration section
3. If a replacement program exists, set the `successor` field
4. Deprecation window: remains available for at least 90 days after `deprecated_date`
5. Transitions to archived after the window period ends

### 23.4 Archival Protocol

AIAP programs in archived state:
- Retain complete directory structure, no files are deleted
- AIAP.md retains complete version history
- No longer accept Evolve/Modify operations
- Only Validate operations are allowed (for auditing)
- Executor should return WARNING + recommend successor when encountering an archived program

---

## 24. Orchestration Patterns

AIAP programs support four orchestration patterns, declared through semantic annotations in Mermaid flowcharts.

### 24.1 Pattern 1: Sequential

Already fully covered by the current AIAP Pipeline. Modules execute in the order defined by `-->` in the Mermaid flowchart.

```mermaid
Start --> ModuleA --> ModuleB --> ModuleC --> endNode
```

Applicable: Default pattern for Pattern A-E.

### 24.2 Pattern 2: Parallel

```mermaid
Start --> fork{Parallel Fork}
fork --> ModuleA
fork --> ModuleB
ModuleA --> join{Join}
ModuleB --> join
join --> End
```

- `fork` node distributes tasks to multiple modules
- `join` node waits for all concurrent modules to complete
- No data dependencies between concurrent modules
- Applicable: When independent subtasks can be processed in parallel

### 24.3 Pattern 3: Conditional

```mermaid
Start --> Classify{Classification}
Classify -->|Type A| ModuleA
Classify -->|Type B| ModuleB
Classify -->|Other| ModuleDefault
```

- Conditional branches are annotated using the `|label|` syntax on Classify nodes
- The current Mermaid flowchart already supports this syntax; no new format is needed
- Applicable: Intent routing, input type dispatching

### 24.4 Pattern 4: Handoff

Applicable for cross-component control transfer in Pattern F Ecosystem:

```
handoff_context = {
    "source": "component_a_aiap",
    "target": "component_b_aiap",
    "intent": "process_health_data",
    "payload": { ... },
    "metadata": { "timestamp": "...", "trace_id": "..." }
}
```

Process:
1. The initiator packages the complete context as `handoff_context`
2. The receiver restores state from `handoff_context`
3. The receiver returns `handoff_result` upon completion
4. The initiator confirms the result or initiates a new handoff

---

## Part V: Quality & Compatibility

---

## 25. Version Compatibility

### 25.1 Protocol Version Compatibility Guarantees

| Version Range | Compatibility Guarantee |
|---------|---------|
| AIAP V1.x.y | Backward compatible within the same major version |
| AIAP V2.0.0+ | May introduce breaking changes, migration guide provided |

### 25.2 Program Version Specification

AIAP program versions follow semver:

| Version Change | Meaning | Example |
|---------|------|------|
| **major** (x.0.0) | Breaking change — input/output format changes | 1.0.0 → 2.0.0 |
| **minor** (x.y.0) | New feature — backward compatible | 1.0.0 → 1.1.0 |
| **patch** (x.y.z) | Bug fix/improvement — backward compatible | 1.1.0 → 1.1.1 |

### 25.3 Minimum Protocol Version

```yaml
# AIAP.md frontmatter
min_protocol_version: "AIAP V1.0.0"
```

The executor checks before loading a program: if the executor's supported protocol version < `min_protocol_version` → Reject loading + Prompt upgrade.

### 25.4 Version Changelog Format

It is recommended to use a structured format in the optional "Version History" section of AIAP.md:

```markdown
## Version History

### v1.2.0 (2026-03-01)
- **Added**: Monthly report trend analysis
- **Improved**: Query performance optimization

### v1.1.0 (2026-02-15)
- **Added**: Blood pressure recording feature
- **Fixed**: Date parsing boundary error
```

Change type labels: `Added` / `Improved` / `Fixed` / `Removed` / `Security`

---

## 26. Documentation Completeness Levels

### 26.1 Three-Tier Classification

| Level | Requirements | Applicable To |
|------|------|------|
| **Level 1** (Minimum) | AIAP.md required sections (Governance Declaration + Feature Overview + Usage) | All AIAP programs |
| **Level 2** (Recommended) | + Example Interactions + Applicable Conditions | Programs with `status=active` |
| **Level 3** (Complete) | + Error Handling + Version History + All optional fields | Programs published to Registry |

### 26.2 Checklist for Each Level

**Level 1 (Minimum)**:
```
[ ] AIAP.md exists
[ ] 13 required frontmatter fields are complete
[ ] Governance Declaration section exists
[ ] Feature Overview section exists
[ ] Usage section exists
[ ] Closing seal exists
```

**Level 2 (Recommended)**:
```
[ ] All Level 1 checks passed
[ ] Example Interactions section exists (1-3 scenarios)
[ ] Applicable Conditions section exists (applicable + not applicable)
[ ] quality optional fields are populated
[ ] status = active
```

**Level 3 (Complete)**:
```
[ ] All Level 2 checks passed
[ ] Error Handling section exists
[ ] Version History section exists (structured format)
[ ] trust_level is declared
[ ] permissions is declared (if trust_level >= T3)
[ ] runtime is declared
[ ] intent_examples is populated
[ ] governance_hash is computed
[ ] benchmark is populated
```

---

## Appendix A: PL24 Auto-Fix Protocol

Applicable: When AutoFixEngine generates fix proposals.

| Constraint | Description |
|------|------|
| **(a) SCOPE** | Fixes limited to 1-3 files, symbol changes ≤ 10, line changes ≤ 50 |
| **(b) CONFIDENCE** | Auto-apply when confidence ≥ 0.85, otherwise submit as suggestion requiring human approval |
| **(c) RATE LIMIT** | Maximum 1 auto-fix per object per day, to prevent infinite loops |
| **(d) AUDIT** | All auto-fixes logged to observability.lint_report |
| **(e) ROLLBACK** | All auto-fixes are rollbackable (git format) |
| **(f) NO LOGIC CHANGE** | Limited to format/style/missing declarations/version constraint fixes; algorithm or business logic changes are prohibited |

---

## Appendix B: PL25 License & Copyright Declaration

Applicable: All AIAP programs, especially for aiap-store distribution.

### B.1 Core Rules

| Rule | Description |
|------|------|
| **(a) LICENSE FIELD** | AIAP.md must include a `license` field |
| **(b) SPDX VALIDITY** | Value must be a valid SPDX identifier (e.g., "Apache-2.0", "MIT") or "proprietary" |
| **(c) PROPRIETARY** | When license is "proprietary", `terms_url` or `contact` must be provided |
| **(d) STORE** | The license field is mandatory for distribution through aiap-store |

### B.2 Field Attributes

| Attribute | Value |
|------|-----|
| Field Name | `license` |
| Type | `string` |
| Required | **Mandatory** (§3.1 required field) |
| Default | `proprietary` (treated as all rights reserved when not declared) |
| Format Specification | SPDX standard identifiers (see https://spdx.org/licenses/) |

### B.2.1 Companion Field: `copyright`

| Attribute | Value |
|------|-----|
| Field Name | `copyright` |
| Type | `string` |
| Required | Optional (§3.2 optional field) |
| Default | Empty (no copyright claim) |
| Format | Free-text copyright notice (e.g. `"Copyright 2026 AIXP Foundation AIXP.dev"`) |

### B.3 Common SPDX Values Reference

| Value | Meaning |
|----|------|
| `MIT` | MIT License (most permissive) |
| `Apache-2.0` | Apache 2.0 (includes patent protection) |
| `GPL-3.0` | GPL v3 (strong copyleft) |
| `proprietary` | Proprietary / All rights reserved |
| `CC-BY-4.0` | Creative Commons Attribution (suitable for documentation-type programs) |

### B.4 Default Value Behavior

- The `license` field is **mandatory** (§3.1 required field)
- When not specified by user during creation, defaults to `proprietary`
- The `copyright` field is **optional** — when omitted, written as empty placeholder in AIAP.md for discoverability
- Does not affect existing program operation (backward compatible)

### B.5 Additional Requirements for `proprietary`

When `license: proprietary`, at least one of the following fields must be provided:

```yaml
license: proprietary
terms_url: https://example.com/terms   # or
contact: author@example.com            # at least one is required
```

### B.6 aiap-store Store Integration

aiap-store registry entries read and display the `license` field directly from AIAP.md:

```json
{
  "program_id": "publisher.domain/program_name",
  "version": "1.0.0",
  "license": "MIT",
  "store_url": "https://aiap.store/programs/publisher.domain/program_name"
}
```

Listing checks:
- Missing `license` field → Store registration API returns error, listing rejected
- `license: proprietary` without `terms_url`/`contact` → Listing rejected

### B.7 Backward Compatibility Guarantees

| Scenario | Behavior |
|------|------|
| Existing programs without a `license` field | Run normally, default treated as `proprietary` (should add field for compliance) |
| Local use without Store listing | Completely unaffected |
| Submitted to Store without `license` filled in | Store registration API returns error, listing rejected |
| Programs without `copyright` field | Run normally, no impact (optional field) |

---

## Appendix C: Category M — Tool Directory Simulation Scenarios (M1-M20)

Applicable: Pattern G programs.

| Scenario | Description |
|------|------|
| M1 | Normal MCP Server startup and tool invocation |
| M2 | MCP Server startup failure, degraded handling |
| M3 | Python dependency installation failure |
| M4 | MCP Server tool invocation timeout |
| M5 | governance_hash mismatch (Code Trust Gate interception) |
| M6 | ZIP SLIP attack (malicious paths in tool_dirs) |
| M7 | Network permission violation (undeclared import requests) |
| M8 | Dependency version not pinned (TS ^ prefix detection) |
| M9 | go.sum missing |
| M10 | Rust pre-compiled binary hash mismatch |
| M11 | shell_tools present but trust_level < T4 |
| M12 | Multi-language MCP Server partial startup failure |
| M13 | aiap_tools sub-program normal load and execution | Expected: **PASS** |
| M14 | aiap_tools sub-program AIAP.md missing or invalid | Expected: **FAIL** (INVALID_AIAP_MD) |
| M15 | aiap_tools sub-program trust_level > parent (should intercept) | Expected: **FAIL** (TRUST_CEILING_VIOLATION) |
| M16 | aiap_tools sub-program governance_hash mismatch | Expected: **FAIL** (INTEGRITY_VIOLATION) |
| M17 | aiap_tools recursion depth exceeded (>3 layers) | Expected: **FAIL** (RECURSION_DEPTH_EXCEEDED) |
| M18 | aiap_tools sub-program permissions exceed parent scope | Expected: **FAIL** (PERMISSION_VIOLATION) |
| M19 | aiap_tools circular dependency detection (A→B→A) | Expected: **FAIL** (CIRCULAR_DEPENDENCY) |
| M20 | aiap_tools sub-program version incompatibility with parent protocol | Expected: **FAIL** (PROTOCOL_VERSION_INCOMPATIBLE) |

---

## Appendix D: NO_SELF_MODIFY Rule

AIAP programs are prohibited from modifying their own governance files at runtime. This rule applies unconditionally to all AIAP programs.

### D.1 Core Rule

> AIAP programs MUST NOT modify their own governance files at runtime. Any structural change to an AIAP program MUST go through the Creator Pipeline's full process (including human-confirmed EvolveStep). Violation of this rule is equivalent to an Axiom 0 breach.

### D.2 Protected Files (Blacklist)

| File Pattern | Description |
|------|------|
| `*.aisop.json` | All module files |
| `AIAP.md` | Project governance contract |
| `quality_baseline.json` | Quality baseline data |
| `agent_card.json` | Agent card metadata |
| `.version_history/*` | Version history records |
| Any file covered by `governance_hash` | Integrity-protected files |

### D.3 Allowed Writes (Whitelist)

| File | Condition |
|------|------|
| `insights.json` | Only when insights mechanism is enabled (see Appendix E), subject to write constraints |
| Program data files | Files declared in `side_effects` (e.g., user data, state files) |

### D.4 Rationale

1. Self-modification = departure from human sovereignty control (Axiom 0)
2. Self-modification = governance_hash invalidation = governance chain breakage
3. Self-modification = bypassing the 15-stage Pipeline's audit guarantees
4. LLM hallucination + self-modification = erroneous judgment directly becoming code changes

### D.5 Independence

NO_SELF_MODIFY is independent of the INSIGHTS mechanism. Even when INSIGHTS is not enabled, the self-modification prohibition is always in effect.

---

## Appendix E: INSIGHTS Mechanism — Optional Runtime Insight Recording

An optional mechanism for AIAP programs to record structural observations during runtime or pipeline execution. Default: not enabled.

### E.1 Activation

```yaml
# In AIAP.md optional fields:
insights: true
# or
insights:
  sources: [pipeline, runtime]  # select one or both
```

When the `insights` field does not exist in AIAP.md, the mechanism is not enabled (zero overhead).

### E.2 insights.json Schema

```json
{
  "program": "{program_name}",
  "version": "{current_version}",
  "warning": null,
  "insights": [
    {
      "id": "INS-001",
      "fingerprint": "string (deterministic, from title)",
      "category": "BUG | FUNC | ARCH | PERF | DEBT | USER | SEC | COMP",
      "severity": "HIGH | MEDIUM | LOW",
      "source": "runtime | pipeline:{stage_name}",
      "title": "string",
      "observation": "string (≤250 chars)",
      "impact": "string",
      "suggestion": "string (≤250 chars)",
      "status": "OPEN | ADOPTED | WONTFIX",
      "created": "YYYY-MM-DD",
      "occurrences": [
        { "version": "string", "mode": "EVOLVE | RUNTIME", "date": "YYYY-MM-DD" }
      ]
    }
  ]
}
```

### E.3 Category Definitions

| Category | Code | Description |
|------|------|------|
| Program Defect | BUG | Functional errors, logic contradictions, data flow breaks |
| Feature Gap/Redundancy | FUNC | Missing or obsolete features |
| Architecture Conflict | ARCH | Module responsibility overlap, circular dependencies |
| Performance & Resource | PERF | Response latency, token budget pressure, resource waste |
| Technical Debt | DEBT | Accumulated structural compromises, hardened workarounds |
| User Demand Signal | USER | User behavior patterns suggesting unmet needs |
| Security & Privacy | SEC | Data leak risks, permission violations, injection vectors |
| Compliance | COMP | Protocol violations, governance chain breaks |

### E.4 Write Constraints

| Writer | Permission |
|------|------|
| Runtime (insights.aisop.json / executor) | Strict append-only: add new entries or append occurrences only. Cannot modify/delete existing entries or change status. |
| Creator Pipeline (advisor insights sub-graph) | Can manage: add entries, modify status (OPEN→ADOPTED/WONTFIX with human confirmation), archive non-OPEN entries to .version_history/ |

### E.5 Fingerprint Deduplication

```
fingerprint = lowercase(title).replace(/[^a-z0-9_\u4e00-\u9fff]/g, '_').truncate(50)
```

Same fingerprint → do not add new entry, append to existing entry's `occurrences` array.

### E.6 Anti-Bloat Controls

| Layer | Mechanism |
|------|------|
| L1: Per-entry | observation + suggestion combined ≤ 500 characters |
| L2: Total | OPEN entries capped at 20; exceeding sets `warning` field |
| L3: Version archive | EVOLVE archives non-OPEN entries to `.version_history/v{old}/insights_archive.json` |

### E.7 insights.json is NOT included in governance_hash

insights.json is a dynamic runtime/pipeline artifact, not part of the static program definition. governance_hash covers only .aisop.json static files.

### E.8 Packaging

When packaging as .aiap: `insights.aisop.json` is included (module code), `insights.json` is excluded (runtime data).

---

## Appendix F: Node Gate — Node-Level Execution Assertion

### F.1 Purpose

AI agents executing multi-node AISOP programs tend to skip nodes despite global execution rules (e.g., `strict_semantics: zero_skip`). Global rules declared once at the start lose influence as context grows. Node Gate solves this by **inserting an assertion at every node entry**, refreshing AI attention at each step.

This is not a replacement for `strict_semantics` — it is the **per-node concretization** of the global rule. `strict_semantics` declares the intent; Node Gate asserts it at every node boundary.

### F.2 Mechanism

Every non-start node's first step (S1) MUST begin with an assertion:

**Single predecessor** (linear chain):
```
[ASSERT] {prev_node} executed. If false → go back to {prev_node}. | {step work}
```

**Multiple predecessors** (converge point — node has 2+ incoming Mermaid edges):
```
[ASSERT] {nodeA}∨{nodeB}∨{nodeC} executed. If false → go back to {primary_predecessor}. | {step work}
```

The assertion and step work are separated by `|` and merged into one step — no `Do not proceed` terminator needed because the backtrack instruction already implies it. The `|` separator clearly delineates the gate from the step's normal work.

The `∨` (logical OR) operator means: at least one of the listed predecessors must have been executed. This covers converge points where a node can be reached from multiple paths (e.g., loop-back edges, conditional branches merging).

**Predecessor derivation rules:**

1. **Source of truth**: Parse the Mermaid `graph TD` definition. Every edge `A --> B` or `A -- label --> B` makes `A` a predecessor of `B`
2. **Single incoming edge**: Use `{prev_node}` directly — both in predicate and backtrack target
3. **Multiple incoming edges**: List ALL predecessors joined by `∨` in the predicate. The **primary predecessor** (backtrack target) is the node on the **main forward path** — typically the first edge in topological order, excluding loop-back and error-recovery edges
4. **Diamond (decision) nodes**: Edges from a diamond (e.g., `QualityGate -- Fail --> ModifyStep`) count as predecessors of the target. The diamond node name is used, not the edge label
5. **Self-loops and sub-graph entry**: If a node receives edges from both the current sub-graph and external entry (e.g., `Start(drill_down)`), list all sources with `∨`
6. **Cross-sub-graph delegation**: When a sub-graph's entry node receives delegation from another sub-graph's node (e.g., `PipelineEntry` in router delegates to `PipelineStart` in pipeline), the assert references the **delegating node**, not the local Start. The local Start is a trivial label — the true runtime predecessor is the delegating node
7. **Terminal node naming**: The terminal node MUST use the format `endNode((End))` — double parentheses for rounded shape, name `endNode`, label `End`. Variants (`End`, `end`, `Finish`) are non-standard and MUST be normalized

**Primary predecessor selection** (for backtrack target after `go back to`):

| Scenario | Primary predecessor |
|----------|-------------------|
| One main-path edge + loop-back edges | Main-path edge source |
| Multiple conditional branches merging | The branch on the default/happy path |
| All edges are equivalent (no clear primary) | First predecessor in Mermaid declaration order |

The assertion and S1's normal work are combined in one step — no additional step is created.

**Why ASSERT**: In programming, `assert` means "this condition MUST be true, otherwise execution stops." AI training data contains millions of assert statements with this exact semantics — the meaning is unambiguous: **condition false = cannot continue**.

### F.3 Backtrack Rules

- Assertion true → continue executing current node
- Assertion false (single predecessor) → return to `{prev_node}` and execute it fully
- Assertion false (multi-predecessor `∨`) → return to `{primary_predecessor}` and execute it fully. The `∨` predicate checks if ANY listed predecessor was executed; backtrack always targets the primary predecessor (main forward path)
- If `{prev_node}`'s own assertion also fails → continue backtracking to its predecessor
- Natural recursive backtracking with depth budget: max_backtrack_depth = min(3, node_count / 4). Exceeding budget → halt with diagnostic instead of infinite regress (inspired by ABC k-bounded recovery, arXiv 2602.22302)
- Worst case within budget: backtrack to the start node and re-execute from beginning
- Pipeline never fails due to backtracking within budget — it self-corrects. Beyond budget → structured failure with backtrack trace for debugging

### F.4 Why It Works

1. **ASSERT is a programming primitive** — AI recognizes `assert` as a hard stop, not a suggestion. Unlike "please be honest" (a request), `assert` is a **command with defined failure semantics**
2. **Per-node repetition** — global rules suffer attention decay; per-node assertions refresh attention at every boundary
3. **Backtrack is correction, not punishment** — assertion failure triggers re-execution, not error. AI has a legitimate path: go back and do the work
4. **Minimal token cost** — one line per node, ~10 tokens
5. **Academic validation** — Node Gate aligns with established research:
   - **AgentSpec (ICSE 2026, ICSE 2026, arXiv 2503.18666)**: Runtime enforcement via three-tuple `trigger → predicate → enforcement`. Node Gate implements this as: trigger=node entry, predicate=predecessor executed, enforcement=backtrack
   - **ProgPrompt**: Assertions in prompts as pre-conditions with recovery actions. Node Gate uses `[ASSERT]` as pre-condition and backtracking as recovery
   - **Attention decay research**: Global instructions lose influence as context grows; per-node assertions counter this by refreshing constraints at every boundary

### F.5 Assert Pattern (AgentSpec Three-Tuple)

Each Node Gate assertion follows the AgentSpec enforcement model:

| Element | Node Gate Mapping |
|---------|-------------------|
| **Trigger** | Node entry (first step S1) |
| **Predicate** | `{prev_node}` (single) or `{nodeA}∨{nodeB}∨...` (multi) was fully executed |
| **Enforcement** | Backtrack to `{prev_node}` or `{primary_predecessor}` and re-execute |

This three-tuple is embedded directly into each node's S1, requiring no external runtime or monitoring infrastructure. The AI itself serves as both evaluator and enforcer — leveraging `assert` semantics from its training data.

### F.6 Implementation in .aisop.json

**Single predecessor** (linear chain):
```json
{
  "EvolveStep": {
    "step1": "[ASSERT] Research1 executed. If false → go back to Research1. | Based on research findings, plan fixes...",
    "step2": "Execute fixes...",
    "step3": "Verify fix results..."
  }
}
```

**Multiple predecessors** (converge point):
```json
{
  "ModifyStep": {
    "step1": "[ASSERT] Research2∨QualityGate∨PostSimulateGate executed. If false → go back to Research2. | Apply quality fixes..."
  }
}
```

### F.7 Applicability

| Node count | Requirement |
|-----------|-------------|
| 6+ nodes | REQUIRED |
| 3-5 nodes | RECOMMENDED |
| 1-2 nodes | OPTIONAL |

Regardless of node count, Node Gate is REQUIRED if the program contains QualityGate nodes, self-evolution pipelines, or Trust Level T3+ operations.

### F.8 Relationship to Existing Execution Mechanisms

| Mechanism | Scope | Function |
|-----------|-------|----------|
| `strict_semantics` | Global | Declares "no skipping" intent |
| `step_completion_attestation` | Per-stage | Records execution proof |
| `pipeline_integrity_chain` | Cross-stage | Hash-chains execution audit trail |
| **Node Gate (ASSERT)** | **Per-node entry** | **Asserts predecessor execution + self-corrects via backtrack** |

Node Gate complements (not replaces) existing mechanisms. It adds the missing layer: **per-node execution assertion with a self-correction path**.

### F.9 Compliance Check

```
MF28: Node Gate Completeness
  - Every non-start node's S1 contains [ASSERT]
  - [ASSERT] references the correct predecessor node(s) derived from Mermaid graph edges
  - Multi-predecessor nodes MUST list ALL incoming edge sources joined by ∨
  - Primary predecessor (backtrack target) MUST be the main forward path node
  - Backtrack target after `go back to` MUST be a concrete non-empty node name (not just `.` or empty)
  - Applicable when: node count ≥ 6 or program contains QualityGate/self-evolution/T3+

MF29: Version Sync
  - AIAP.md.version == all .aisop.json version == agent_card.json.version == quality_baseline.json.version
  - Any mismatch is RED — auto-correct all to AIAP.md version

MF30: Score Consistency
  - AIAP.md.quality.weighted_score == quality_baseline.three_dim_test.weighted_score
  - quality_baseline is authoritative — AIAP.md auto-corrects to match
  - Mismatch is YELLOW

MF31: Mermaid-Function Consistency
  - Every rectangle node in aisop.main Mermaid MUST have a matching key in functions{}
  - Every functions{} key MUST appear as a node in Mermaid
  - Diamond nodes ({...?}) are exempt (decisions within parent nodes)
  - PascalCase diamonds suggesting independent nodes → AUTO-FIX-CANDIDATE: rename to lowercase or merge into parent
  - Terminal node MUST use `endNode((End))` format — variants (`End`, `end`, `Finish`) are AUTO-FIX-CANDIDATE
  - Mismatch is YELLOW
```

---

Align: Human Sovereignty and Wellbeing. Version: AIAP V1.0.0. www.aiap.dev
