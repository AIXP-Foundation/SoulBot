# AIAP_Tools

## Purpose

This directory contains nested AIAP programs used as tools by `aiap_auto_evolution`. Programs here are invoked via **intent execution** — the runtime reads their AISOP files and executes them node-by-node, not as API calls.

## Contents

| Directory | Program | Version | Purpose |
|-----------|---------|---------|---------|
| `aisop_creator_evolution_aiap/` | AIAP Creator | v1.24.0 | Single-round AIAP evolution engine (full 15-stage pipeline) |

## Interface

### aisop_creator_evolution_aiap

- **Invocation**: Intent execution via `executor.aisop.json` IntentExecute node
- **Input**: Natural language evolution instruction (classified by Creator's NLU as "Evolve" intent)
- **Output**: Evolved target program files + quality metrics (ThreeDimTest scores, simulation results)
- **Parameters**: `workspace_dir` (string, required), `quality_threshold` (string, default: "standard")
- **Entry file**: `main.aisop.json`

## Security Constraints

- **Read-only during execution**: AIAP_Tools programs must NOT be modified by the host program during execution.
- **Trust level**: T4 (full workspace read/write — same as host program).
- **Isolation**: Creator operates on the target program directory, not on itself or the host program.
- **Self-evolution guard**: Host program blocks any attempt to target AIAP_Tools subdirectories for evolution.

## Maintenance

- When upgrading Creator, replace the entire `aisop_creator_evolution_aiap/` directory with the new version.
- Verify Creator version compatibility with host program's `executor.aisop.json` PrepareContext step.
