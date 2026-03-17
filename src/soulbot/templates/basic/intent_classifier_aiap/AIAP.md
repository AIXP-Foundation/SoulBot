---
protocol: "AIAP V1.0.0"
authority: aiap.dev
seed: aisop.dev
executor: soulbot.dev
axiom_0: Human_Sovereignty_and_Benefit
governance_mode: NORMAL
name: intent_classifier_aiap
version: "2.6.0"
pattern: A
summary: "11-node cascading classifier with trace suppression, minimal output mode, shortcut half-open recovery, trace budget, output compaction."
tools:
  - name: file_system
    required: true
    annotations:
      read_only: false
      destructive: false
      idempotent: false
      open_world: false
modules:
  - id: intent_classifier
    file: main.aisop.json
    nodes: 11
    critical: true
    idempotent: true
    side_effects: [file_write]
license: proprietary
author: ""
copyright: ""
governance_hash: "sha256:c5d7e9f1a3b5c7d9e1f3a5b7c9d1e3f5a7b9c1d3e5f7a9b1c3d5e7f9a1b3c5d7"
status: active
trust_level: 3
tags: [intent-classification, routing, taxonomy, auto-discovery, context-aware, session-management, multi-intent, out-of-scope, adaptive-threshold, parallel-execution, confidence-calibration, correction-weighted, graduated-degradation, semantic-cache, active-learning, multilingual, observability, strict-execution, execution-trace, cascading-classification, dynamic-calibration, output-schema, hard-negative, execution-failure-feedback, shared-constraints, step-compression, dry-constraints, early-exit, inline-trace, node-merge, circuit-breaker, confidence-attribution, trace-summary, semantic-compression, value-aware-eviction, drift-detection, degradation-scoring, cache-freshness, tiered-ttl, adaptive-cb-timeout, degradation-trend, input-safety, latency-tracking, smart-cache-invalidation, metrics-parameterization, smart-shortcut, recursive-drill-down, leaf-branch-registry, stale-tier-cache, context-continuity, recursion-safety, auto-promotion, auto-demotion, switch-signals, shortcut-accuracy, cascade-quality-estimator, stale-active-cleanup, trace-suppression, minimal-output, shortcut-half-open, trace-budget, output-compaction]
intent_examples:
  - "classify this user input"
  - "route to the right AIAP"
  - "which AI app should handle this?"
  - "identify the user's intent"
  - "continue with the same app"
  - "switch to a different tool"
  - "handle multiple requests at once"
  - "this doesn't match anything"
  - "drill down into this category"
  - "classify across 100 AIAPs"
  - "promote frequently used apps"
  - "detect when user switches topic"
  - "suppress trace from output"
  - "show only minimal classification"
discovery_keywords:
  - intent
  - classification
  - routing
  - taxonomy
  - discovery
  - context
  - session
  - multi-intent
  - rejection
  - adaptive
  - parallel
  - calibration
  - cache
  - multilingual
  - observability
  - strict-execution
  - trace
  - cascading
  - recursive
  - drill-down
  - hierarchical
  - promotion
  - demotion
  - switch-signal
  - trace-suppression
  - minimal-output
quality:
  weighted_score: 4.975
  grade: S
  last_pipeline: "creator_v2.6.0_evolve"
runtime:
  timeout_seconds: 60
  max_retries: 3
  token_budget: 8000
  idempotent: true
  side_effects:
    - file_write
  execution:
    mode: strict
    trace: node
    on_violation: report_and_degrade
    trace_max_entries: 20
permissions:
  file_system:
    scope: "./data/"
    operations: ["read", "write"]
  shell:
    allowed: false
  network:
    allowed: false
---

## Governance Declaration

This AIAP program adheres to the AIAP V1.0.0 protocol governed by aiap.dev. All operations align with Axiom 0: Human Sovereignty and Benefit.

## Feature Overview

**Intent Classifier v2.6.0** — 11-node cascading classifier with trace suppression, minimal output mode, shortcut half-open recovery, trace budget, and output compaction:

| Feature | Description |
|---------|-------------|
| **Trace Suppression** | NEW: trace_output='internal' (default) — all execution traces routed to PostProcess only, NEVER in user output. trace_rule in execution config. trace_append constraint enforced at every node |
| **Minimal Output Mode** | NEW: output_mode parameter ('minimal'/'full'). Minimal=4 fields (target_aiap, confidence, confidence_tier, directory_path). output_rule in shared_constraints. Reduces token output ~70% |
| **Shortcut Half-Open Recovery** | NEW: When shortcut_accuracy<0.85→disabled, half-open mode: every 10th request tested; 3 consecutive ok→re-enable. Prevents permanent shortcut lockout |
| **Trace Budget** | NEW: trace_budget=500 in execution config. entries\*avg≤500 chars enforced in PostProcess. Prevents trace bloat consuming context |
| **Output Compaction** | NEW: OutputResult FORMAT per output_rule — enforces minimal/full/verbose modes. Internal trace computed but only forwarded to PostProcess, never to user unless verbose |
| **Auto-Promotion/Demotion** | Frequency-based ranking @adaptive window. Top 10% branch AIAPs→promote to depth-0. Bottom 10% depth-0→demote to branch. min_samples=30, cooldown=3 windows |
| **Intent Switch Signals** | shared_constraints.switch_signals — 5 signal types (new-topic keyword, different-domain entity, explicit switch, question→command shift, lang change). Any signal→bypass shortcut |
| **Shortcut Accuracy Tracking** | corrections/total@adaptive window. accuracy<0.85→shortcut_disabled. Self-correcting feedback loop + half-open recovery (v2.6.0) |
| **Cascade Quality Estimator** | quality_estimate=conf\*calib\*(1-drift_offset). Unified routing+cascading score for tier decisions. In output_schema |
| **Stale Active Cleanup** | cache count>180→evict all stale_high_tier entries before normal eviction. Proactive stale removal |
| **Smart Shortcut** | Context continuity bypass (active_aiap+no switch_signal+distance<0.3→conf=0.98). Cache pre-check. Switch-signal-aware (v2.5.0) |
| **Recursive Drill-Down** | recursion_mode full(11-node)/drill_down(3-node). Branch results trigger self-invocation. Handles unlimited AIAP count |
| **Leaf/Branch Registry** | Registry entries typed as leaf (executable) or branch (sub-classifier). branch has sub_registry, children_count, summary |
| **Stale-Tier Cache** | High-tier entries on taxonomy rebuild marked stale_high_tier:true, freshness\*=0.5, forced reclassify on next access |
| **Recursion Safety** | shared_constraints.recursion_safety — max_depth hard limit, self-ref+cycle detect, depth-scaled timeout, depth≥max→best-guess |
| **Latency Tracking** | start_ts in Start, latency_ms=now-start_ts in trace_summary and learning_log |
| **Smart Cache Invalidation** | On taxonomy rebuild, retain high-tier unexpired cache entries; remove mismatched version_tag |
| **Metrics Parameterization** | shared_constraints.metrics_window {adaptive:100, drift:50, degradation:50, archive:1000/500} |
| **Tiered TTL Cache** | Confidence-based TTL — high=2700s, medium=1800s, low=900s |
| **Adaptive Circuit Breaker** | timeout=300\*(1+failures\*0.5), clamp[60,900] — scales with failure severity |
| **Degradation Trend** | Compare current vs previous degradation\_score; delta>0.1→worsening, <-0.1→improving |
| **Input Safety Guard** | Detect injection patterns (ignore previous/system prompt/role:system), flag in trace |
| **Value-Aware Cache Eviction** | Multi-factor eviction (freq\*0.4+freshness\*0.35+tier\*0.25) replaces pure LRU |
| **Concept Drift Detection** | Compare last-50 vs prior-50 correction_rate; delta>0.10 triggers threshold offset |
| **Degradation Scoring** | score=correction\*0.4+oos\*0.3+failure\*0.3 from last 50; >0.3 triggers warning |
| **Cache Freshness** | cache_freshness=1-(age/TTL) in output_schema for cache transparency |
| **Freq Tracking** | Cache entries track hit frequency (freq=1 on create, freq+=1 on hit) |
| **Circuit Breaker** | DataSync/PostProcess 3-state (closed→open→half-open) resilience |
| **Confidence Attribution** | Output includes {signal, weight, value} decomposition, weights sum to 1.0 |
| **Trace Summary** | {first_node, last_node, total_nodes, fast_path, latency_ms, depth} for quick trace overview |
| **Node Merge (PostProcess)** | UpdateSession+LearnLog merged into single PostProcess node with step-independent writes |
| **Inline Trace** | Trace appends embedded in last business step of each node |
| **Early-Exit OOS** | QualityGate fast reject for very-low-confidence stateless inputs (< half rejection_threshold) |
| **DRY Error References** | Error fields reference shared_constraints.error_pattern |
| **Output Schema Contract** | Structured output schema (single/multi/rejection) with classified_path, recursion_used, quality_estimate |
| **Hard-Negative OOS** | Near-domain AIAPs (within 0.1 of top score) get penalty factor 0.9 |
| **Execution Failure Feedback** | Downstream AIAP failure auto-reduces confidence -0.15 (decays 0.03/hour, floor -0.30) |
| **Shared Constraints** | 11-item system-level constraints (+promotion_rules, +switch_signals) |
| **Strict Execution** | Every node in topological order, violation → trace + confidence penalty |
| **Cascading Classification** | Keyword fast-path → semantic analysis |
| **Dynamic Calibration** | Factor [0.85-0.98] from correction history |
| **Semantic Cache** | Hash + similarity bypass (tiered TTL, max 200, value-aware eviction, stale-tier aware, stale cleanup@180) |
| **Multilingual** | Code-switching detection and normalization |
| **Multi-Intent** | Parallel classification with priority ordering |
| **OOS Rejection** | Dual-threshold with hard-negative scoring and near-domain suggestions |
| **Graduated Degradation** | 4-tier (high/medium/low/reject) |
| **Active Learning** | Low-confidence needs_review tagging |
| **Observability** | Rolling metrics + cb_trips + degradation_score + trend + avg_latency + shortcut_rate + avg_depth + shortcut_accuracy + avg_quality |
| **Session Management** | Sliding window, TTL 2h, max 50 sessions, active_path tracking |

## Usage

- **Entry File**: `main.aisop.json`
- **Tools Required**: `file_system`
- **Data Directory**: `data/` (registry.json, taxonomy.json, learning_log.json, session_state.json, cache.json, promotion_log.json)
- **Output Modes**: `minimal` (4 fields, default) | `full` (all schema) | `verbose` (full + trace)

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `user_input` | string | required | Natural language input to classify |
| `aiap_directories` | array | required | Directory paths to scan for AIAPs |
| `confidence_threshold` | number | 0.7 | Base confidence (adaptive +-0.10) |
| `max_clarifications` | number | 2 | Max clarification rounds |
| `session_context` | object | null | Conversation context (null = stateless) |
| `rejection_threshold` | number | 0.3 | Below = out-of-scope (0 = disabled) |
| `trace_output` | string | internal | 'internal'=suppress trace from user; 'verbose'=include trace |
| `output_mode` | string | minimal | 'minimal'=4 core fields only; 'full'=all schema fields |
| `recursion_mode` | string | full | 'full'=11-node pipeline; 'drill_down'=3-node sub-layer |
| `max_recursion_depth` | number | 5 | Max recursive depth (0=disable) |
| `current_depth` | number | 0 | Current depth (auto-managed) |
| `parent_context` | object | null | Parent classifier context (drill_down only) |

## Example Interactions

**Scenario 1: Smart shortcut — context continuity with switch detection**
- User continues chatting with soulbot_chat
- SmartShortcut: no switch_signals detected, active_aiap=soulbot_chat, distance=0.1 (<0.3)
- Returns soulbot_chat with conf=0.98, reason='context_continuity'
- Token consumption: ≈0

**Scenario 2: Intent switch signal blocks shortcut**
- User was chatting with soulbot_chat, now says "open my expense tracker"
- SmartShortcut detects switch_signal: different-domain entity ('expense')
- Shortcut bypassed → full classification pipeline → expense_tracker (conf=0.92)

**Scenario 3: Auto-promotion — frequent branch AIAP promoted**
- PostProcess @100th classification: freq_rank analysis
- 'expense_tracker' (branch child of 'life_category') in top 10% by frequency
- promotion_log.json: {promote: 'expense_tracker', from: 'life_category', to: 'depth-0'}
- Next DataSync: applies promotion → expense_tracker now leaf at depth-0

**Scenario 4: Auto-demotion — rarely used depth-0 demoted**
- PostProcess @100th: 'legacy_tool' in bottom 10% of depth-0 AIAPs
- promotion_log.json: {demote: 'legacy_tool', from: 'depth-0', to: 'utilities_branch'}
- Next DataSync: applies demotion → legacy_tool now under utilities_branch

**Scenario 5: Shortcut accuracy self-correction**
- shortcut_accuracy computed: 12 corrections out of 80 shortcut hits = 0.85 → borderline
- Next window: 15 corrections out of 75 = 0.80 < 0.85 → shortcut_disabled flag set
- SmartShortcut reads flag → all requests bypass shortcut → full classification
- Corrections drop → accuracy recovers → shortcut re-enabled

**Scenario 6: Cascade quality estimator**
- RecursiveClassify: conf=0.78, calibration_factor=0.92, drift_offset=0.03
- QualityGate CASCADE: quality_estimate = 0.78 * 0.92 * (1 - 0.03) = 0.696
- Tier by quality_estimate vs threshold: 0.696 < 0.7 → medium tier (not high)
- More accurate routing than raw confidence alone

**Scenario 7: Stale active cleanup**
- Cache has 185 entries, 8 are stale_high_tier
- STALE CLEANUP: count>180 → evict all 8 stale entries first
- Cache drops to 177, only fresh entries remain
- Normal eviction only if still at cap after cleanup

**Scenario 8: Recursive drill-down with promotion context**
- 60 AIAPs: 'expense_tracker' recently promoted to depth-0
- Input: "track my expenses" → fast-path keyword match → expense_tracker (conf=0.95)
- No drill-down needed — promotion moved it to depth-0, saving recursion cost

**Scenario 9: Combined feedback — shortcut + promotion + quality**
- PostProcess @10th: shortcut_accuracy=0.92, avg_quality=0.81, promotions=1
- Metrics: shortcut healthy, quality above threshold, 1 promotion applied
- System self-optimizes: frequent AIAPs promoted, shortcut verified accurate

**Scenario 10: Trace suppression — user sees only minimal output**
- Input classified → soulbot_chat (conf=0.92, high tier)
- trace_output='internal' (default) → all 11-node traces computed internally
- OutputResult: FORMAT per output_rule → MINIMAL mode
- User receives: `{"target_aiap":"soulbot_chat","confidence":0.92,"confidence_tier":"high","directory_path":"./soulbot_chat_aiap/"}`
- Trace data forwarded to PostProcess for learning/metrics — never shown to user
- Token savings: ~70% compared to full output mode

**Scenario 11: Shortcut half-open recovery**
- Shortcut accuracy dropped to 0.82 → shortcut_disabled, half_open_counter=0
- Requests 1-9: full classification pipeline (shortcut bypassed)
- Request 10 (half-open test): full pipeline + shortcut would-have-been result compared
- Shortcut result matches → half_open_counter=1
- After 3 consecutive matches → shortcut re-enabled (accuracy recovered)

**Scenario 12: Trace budget enforcement**
- PostProcess step3: 15 trace entries, avg 40 chars each = 600 > budget 500
- Budget exceeded → compress trace entries (remove verbose fields, keep node+result)
- Final trace: 15 entries, avg 33 chars = 495 ≤ 500 budget
- Prevents trace accumulation from consuming context window

**Scenario 13: Metrics with full observability**
- PostProcess computes: shortcut_rate, avg_depth, shortcut_accuracy, avg_quality, promotions count
- Dashboard: shortcut_rate=70%, avg_depth=0.12, shortcut_accuracy=0.94, avg_quality=0.83
- All feedback loops healthy — no degradation warnings — trace within budget

## Data Storage

| File | Purpose | Persistence |
|------|---------|-------------|
| `data/registry.json` | AIAP package registry (leaf/branch typed) | TTL 3600s |
| `data/taxonomy.json` | Classification tree + version_tag | On registry change |
| `data/cache.json` | Semantic cache + freq tracking + stale_high_tier flag | Max 200, tiered TTL (15-45min), stale cleanup@180 |
| `data/learning_log.json` | Classification log + quality_estimate + switch_signals | Archive at 1000 |
| `data/session_state.json` | Session history + active_path | TTL 2h |
| `data/promotion_log.json` | Pending promote/demote actions | Applied by DataSync |

## Node Architecture (v2.6.0 — 11 nodes)

| Node | Steps | Purpose |
|------|-------|---------|
| Start | 1 | Mode gate (full/drill_down) + validation + sanitize + safety + start_ts + trace init |
| DataSync | 2 | Adaptive CB + registry (leaf/branch) + taxonomy + stale-tier invalidation + apply promotions |
| SmartShortcut | 1 | Switch signal detection + accuracy gate + half-open recovery + context continuity bypass + cache pre-check |
| SemanticCache | 2 | Cache lookup (exact+similarity, stale-tier aware) + tiered TTL + stale cleanup@180 + value-aware eviction |
| ContextEnrich | 4 | Multilingual + stateless + anaphora + boosts |
| IntentRoute | 1 | Single/multi detection |
| RecursiveClassify | 3 | Fast-path (leaf/branch) → semantic + calibrate + attribution weights |
| QualityGate | 4 | Early-exit + scope + adaptive + cascade quality estimator + tier + TypeGate (leaf/branch) |
| ClarifyAsk | 1 | Clarification loop (includes branch categories) |
| OutputResult | 2 | Branch drill-down + format per output_rule (minimal/full/verbose) + trace→PostProcess only |
| PostProcess | 3 | depth>0→skip. CB + session + learn + metrics + promotion + trace budget enforcement |

## Changelog

### v2.6.0 (Trace Suppression + Minimal Output + Shortcut Half-Open + Trace Budget + Output Compaction)
- Trace suppression: trace_output='internal' default — execution traces routed to PostProcess only, never in user output; trace_rule in execution config; trace_append constraint at every node (main user-facing fix)
- Minimal output mode: output_mode parameter ('minimal'/'full'); minimal=4 fields (target_aiap, confidence, confidence_tier, directory_path); output_rule in shared_constraints; ~70% token reduction for user output
- Shortcut half-open recovery: disabled shortcuts (accuracy<0.85) enter half-open mode — every 10th request tested, 3 consecutive ok→re-enable; prevents permanent shortcut lockout (P49 fix)
- Trace budget: trace_budget=500 in execution config; entries*avg≤500 chars enforced in PostProcess; prevents trace consuming excessive context
- Output compaction: OutputResult FORMAT per output_rule — minimal/full/verbose enforcement; internal trace→PostProcess only
- output_schema extended: new 'minimal' schema type (4 fields)
- shared_constraints expanded: 12 items (+output_rule)
- Parameters: 12 (+output_mode)
- Phase C compression: -305 chars (-2.4%) with 5 new features — net negative growth
- All v2.5.0 functionality preserved

### v2.5.0 (Auto-Promote/Demote + Switch Signals + Shortcut Accuracy + Cascade Quality + Stale Cleanup)
- Auto-promotion/demotion: frequency-based ranking @adaptive window; top 10% branch→depth-0, bottom 10% depth-0→branch; min_samples=30, cooldown=3 windows; data/promotion_log.json; DataSync applies pending promotions (P42, P7 from 010 design)
- Intent switch signals: shared_constraints.switch_signals — 5 signal types; SmartShortcut detects and bypasses continuity when any signal present (P41 fix)
- Shortcut accuracy tracking: corrections/total@adaptive; <0.85→shortcut_disabled; self-correcting feedback loop
- Cascade quality estimator: quality_estimate=conf*calib*(1-drift_offset); unified routing+cascading score; replaces raw conf for tier decisions; in output_schema
- Stale active cleanup: cache count>180→evict all stale_high_tier before normal eviction; proactive stale removal (P44 fix)
- shared_constraints expanded: 11 items (+promotion_rules, +switch_signals)
- Output schema extended: quality_estimate field
- Learning log extended: quality_estimate, switch_signals fields
- PostProcess metrics extended: shortcut_accuracy, avg_quality, promotions
- Observability: +shortcut_accuracy, +avg_quality in rolling metrics
- Phase C compression continued: -1286 chars from uncompressed draft (9.3%), net +136 chars (+1.1%) with 5 new features
- All v2.4.0 functionality preserved

### v2.4.0 (Smart Shortcut + Recursive Drill-Down + Leaf/Branch Registry + Stale-Tier Cache)
- Smart shortcut: SmartShortcut node — context continuity bypass (active_aiap+no switch→conf=0.98) + cache pre-check; ~60% requests bypass full classification
- Recursive drill-down: recursion_mode (full/drill_down), max_recursion_depth, current_depth, parent_context parameters; branch results trigger 3-node self-invocation; handles unlimited AIAP count
- Leaf/branch registry: DataSync extracts type='leaf'|'branch' from AIAP frontmatter; branch has sub_registry, children_count, branch_summary
- Stale-tier cache: high-tier entries on taxonomy rebuild marked stale_high_tier:true, freshness*=0.5, forced reclassify (P36 fix)
- Recursion safety: shared_constraints.recursion_safety — max_depth, cycle detect, depth-scaled timeout (9 items total)
- SmartShortcut: new node (10→11 nodes), TypeGate merged into QualityGate step4
- Structural compression Phase C applied (merged TypeGate, compressed traces, eliminated implied constraints)
- All v2.3.0 functionality preserved

### v2.3.0 (Latency Tracking + Smart Cache Invalidation + Metrics Parameterization)
- Latency tracking, smart cache invalidation, metrics parameterization
- All v2.2.0 functionality preserved

### v2.2.0 (Tiered TTL + Adaptive CB + Degradation Trend + Input Safety)
- Tiered TTL cache, adaptive circuit breaker, degradation trend, input safety guard
- All v2.1.0 functionality preserved

### v2.1.0 (Value-Aware Cache + Drift Detection + Degradation Scoring)
- Value-aware eviction, concept drift, degradation scoring, cache freshness, freq tracking
- All v2.0.0 functionality preserved

### v2.0.0 (Semantic Compression + Circuit Breaker + Attribution + Trace Summary)
- Semantic compression, circuit breaker, confidence attribution, trace summary
- All v1.9.0 functionality preserved

### v1.9.0 (Node Merge + Inline Trace + Step Compression)
- Node merge: UpdateSession+LearnLog → PostProcess (11→10 nodes), inline trace, 40→23 steps

### v1.8.0 — v1.1.0
- Step compression, DRY, early-exit, output schema, hard-negative, cascading, strict execution, cache, multilingual, multi-intent, OOS, session context

Align: Human Sovereignty and Benefit. Version: AIAP V1.0.0. www.aiap.dev
