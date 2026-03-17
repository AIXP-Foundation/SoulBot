---
protocol: "AIAP V1.0.0"
authority: aiap.dev
seed: aisop.dev
executor: soulbot.dev
axiom_0: Human_Sovereignty_and_Benefit
governance_mode: NORMAL
name: intent_classifier_aiap
version: "3.1.0"
pattern: A
summary: "11-node cascading classifier with assertion execution, node gate, and context-aware fast routing. Session pattern prediction, domain affinity, temporal matching bypass full classification. k-bounded backtrack (depth 2). Cold-start, CJK labels, privacy scope, domain hints, configurable trace history."
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
governance_hash: "sha256:d6e8f0a2b4c6d8e0f2a4b6c8d0e2f4a6b8c0d2e4f6a8b0c2d4e6f8a0b2c4d6e8"
status: active
trust_level: 3
tags: [intent-classification, routing, cascading, taxonomy, multi-intent, semantic-cache, recursive-drill-down, context-aware, multilingual, observability, circuit-breaker, auto-promotion, cold-start-discovery, assertion-execution, node-gate, trace-privacy, signal-decision-routing, adaptive-threshold, graduated-degradation, drift-detection, candidate-pruning, cjk-label, domain-hints, minimal-output, configurable-trace-history]
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
  - "debug with trace history"
  - "persist promotions across restart"
  - "classify multiple intents with minimal output"
  - "filter trace for privacy"
  - "ensure new AIAPs get discovered"
  - "classify CJK language inputs"
  - "configure trace history buffer size"
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
  - signal-decision
  - trace-history
  - trace-privacy
  - compact-label
  - candidate-pruning
  - cold-start
  - cjk-label
  - domain-hint
  - configurable-history
quality:
  weighted_score: 4.970
  grade: S
  last_pipeline: "creator_v3.7.0_evolve — CONTEXT FAST ROUTING + PROTOCOL HARDENING: SmartShortcut enhanced with 3 context signals (session pattern, domain affinity, temporal match). Mermaid cleaned (removed phantom nodes TypeGate/PostGate/ReturnParent). ASSERT backtrack targets fixed. k-bounded backtrack depth=2 added. v3.1.0."
runtime:
  timeout_seconds: 60
  max_retries: 3
  token_budget: 8000
  idempotent: true
  side_effects:
    - file_write
  execution:
    mode: assert
    trace: node
    on_violation: report_and_degrade
    trace_max: 20
    max_backtrack_depth: 2
    backtrack_exceeded: halt_with_diagnostic
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

**Intent Classifier v3.0.0** — 11-node cascading classifier with assertion execution, node gate, cold-start discovery, CJK labels, privacy scope, domain hints, and configurable trace history:

| Feature | Description |
|---------|-------------|
| **Assertion Execution (ASSERT RUN)** | NEW: instruction field uses `ASSERT RUN aisop.main` — assertion semantics enforce pipeline execution as programming invariant, not suggestion |
| **Node Gate** | NEW: All 10 non-start nodes have `[ASSERT] {prev_node} executed` gate at S1 opening. Natural recursive backtracking on failure. Per Protocol Appendix F (MF28 compliant) |
| **Cold-Start Discovery Guarantee** | RecursiveClassify PRUNE reserves ≥1 slot for new AIAPs (reg<24h ∨ freq<10). Prevents pruning from permanently excluding newly registered AIAPs (P62 fix) |
| **CJK Compact Label Rules** | NEW: DataSync compact_label rule extended — en≤3 words, CJK≤6 chars. Proper multilingual label normalization for keyword signal matching (P61 fix) |
| **Trace Privacy Scope Clarification** | NEW: trace_privacy scope explicitly defined — "history only; verbose unfiltered". Verbose output exempt from privacy filtering (P64 fix) |
| **Signal Weight Domain Hints** | NEW: DataSync scans optional signal_bias field from AIAP registry. RecursiveClassify applies +0.1 to biased signal weight. Per-domain signal tuning (P56 partial fix) |
| **Configurable Trace History Size** | NEW: trace_history_size parameter [1,20] default 5. PostProcess ring buffer uses configurable size instead of hardcoded 5 (P60 fix) |
| **Multi-Intent Minimal Output** | output_schema.multi_minimal — multi-intent results in compact array [{target,conf,tier,path}]+count. output_rule updated. Consistent minimal format for multi-intent (P52 fix) |
| **Trace Privacy Filter** | shared_constraints.trace_privacy — allow-list filter for trace_history.json. Only node,result,tier,latency_ms retained; scores,context,hash dropped. PII sanitization at source (P57 fix) |
| **Signal Scope Constraint** | RecursiveClassify drill_down constraint — signals scoped to parent.sub_programs only. Prevents cross-branch signal matching in recursive mode (P59 fix) |
| **Candidate Pruning** | RecursiveClassify PRUNE — top-k(≤7) candidates by signal scores before detailed scoring. Reduces computation for large registries (P58 fix) |
| **Compact Labels** | DataSync extracts compact_label from AIAP name during scan. Used in keyword signal matching for faster, more precise matching |
| **Trace History Ring Buffer** | PostProcess writes last 5 complete traces to data/trace_history.json (FIFO). Privacy-filtered per trace_privacy. Enables retrospective debugging |
| **Promotion Persistence** | promotion_log entries marked applied:true after DataSync applies. Confirmed promotions survive registry rescan |
| **Trace Overflow Compression** | execution.trace_overflow — budget exceeded→keep node+result, drop verbose fields |
| **Signal-Decision Routing** | RecursiveClassify multi-signal scoring — keyword(w0.4)+semantic(w0.4)+context(w0.2). Combined weighted decision with compact_label support |
| **Promotion Safety Guards** | promotion_rules Safety — branch≥1 child, no circular, affinity≥0.5 |
| **Trace Suppression** | trace_output='internal' (default) — all execution traces routed to PostProcess only, NEVER in user output |
| **Minimal Output Mode** | output_mode parameter ('minimal'/'full'). Minimal=4 fields. ~70% token reduction |
| **Shortcut Half-Open Recovery** | shortcut_accuracy<0.85→disabled, half-open: every 10th tested; 3 ok→re-enable |
| **Trace Budget** | trace_budget=500 in execution. entries\*avg≤500 chars. Overflow→compress per trace_overflow |
| **Output Compaction** | OutputResult FORMAT per output_rule — minimal/multi_minimal/full/verbose |
| **Auto-Promotion/Demotion** | Frequency-based ranking @adaptive window. Top 10%→promote, Bottom 10%→demote. min_samples=30, cooldown=3 |
| **Intent Switch Signals** | shared_constraints.switch_signals — 5 signal types. Any signal→bypass shortcut |
| **Shortcut Accuracy Tracking** | corrections/total@adaptive window. accuracy<0.85→shortcut_disabled. Self-correcting feedback loop + half-open |
| **Cascade Quality Estimator** | quality_estimate=conf\*calib\*(1-drift_offset). Abbreviated as qe. Unified routing score |
| **Stale Active Cleanup** | cache count>180→evict all stale_high_tier entries before normal eviction |
| **Smart Shortcut** | Context continuity bypass (active_aiap+no switch_signal+distance<0.3→conf=0.98). Cache pre-check |
| **Recursive Drill-Down** | recursion_mode full(11-node)/drill_down(3-node). Branch results trigger self-invocation |
| **Leaf/Branch Registry** | Registry entries typed as leaf (executable) or branch (sub-classifier). branch has sub_registry, children_count |
| **Stale-Tier Cache** | High-tier entries on taxonomy rebuild marked stale_high_tier:true, freshness\*=0.5 |
| **Recursion Safety** | shared_constraints.recursion_safety — max_depth hard limit, cycle detect, depth-scaled timeout |
| **Latency Tracking** | start_ts in Start, latency_ms in trace_summary and learning_log |
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
| **Output Schema Contract** | Structured output schema (single/multi/multi_minimal/rejection) with qe, classified_path |
| **Hard-Negative OOS** | Near-domain AIAPs (within 0.1 of top score) get penalty factor 0.9 |
| **Execution Failure Feedback** | Downstream AIAP failure auto-reduces confidence -0.15 (decays 0.03/hour, floor -0.30) |
| **Shared Constraints** | 13-item system-level constraints (+trace_privacy) |
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
- **Output Modes**: `minimal` (4 fields, default) | `multi_minimal` (array+count) | `full` (all schema) | `verbose` (full + trace)

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
| `trace_history_size` | number | 5 | Ring buffer size for trace history [1,20] |

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
- QualityGate CASCADE: qe = 0.78 * 0.92 * (1 - 0.03) = 0.696
- Tier by qe vs threshold: 0.696 < 0.7 → medium tier (not high)
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

**Scenario 13: Trace history — retrospective debugging**
- User reports intermittent misclassification but can't reproduce
- Admin reads data/trace_history.json — contains last 5 complete traces
- Trace #3 shows: signal_scores={keyword:0.3,semantic:0.45,context:0.1}, qe=0.62
- Root cause: semantic signal was ambiguous, keyword signal below threshold
- Fix applied without needing to reproduce in verbose mode

**Scenario 14: Promotion persistence across rescan**
- expense_tracker promoted to depth-0, promotion_log: {applied:true}
- Registry goes stale (>3600s) → DataSync triggers full rescan
- After rescan: promotion_log entries with applied:true re-applied to new registry
- expense_tracker remains at depth-0 — promotion survives rebuild

**Scenario 15: Signal-decision routing with compact labels**
- Input: "open my expense tracker"
- Signal scores: keyword=0.85 (matched compact_label "expense tracker"), semantic=0.78, context=0.10
- Combined: 0.85*0.4 + 0.78*0.4 + 0.10*0.2 = 0.672 → normalized to 0.92
- Gap to second best > 0.2 → signal_match, conf=0.95, skip semantic
- Compact label matching faster than full name comparison

**Scenario 16: Promotion safety guard**
- PostProcess: freq_rank suggests promoting 'sub_tool' from 'utilities_branch'
- Safety check: utilities_branch has only 1 child (sub_tool)
- branch≥1 child violated post-promote → promotion blocked
- Prevents creating empty branch with no children

**Scenario 17: Metrics with full observability**
- PostProcess computes: shortcut_rate, avg_depth, shortcut_accuracy, avg_quality, promotions count
- Dashboard: shortcut_rate=70%, avg_depth=0.12, shortcut_accuracy=0.94, avg_quality=0.83
- Trace history: 5 entries, budget compliant — trace overflow compression not triggered
- All feedback loops healthy — no degradation warnings

**Scenario 18: Multi-intent minimal output**
- User: "translate this document and summarize it"
- IntentRoute: compound detected, split into 2 intents
- Parallel classification: translator(0.91,high), summarizer(0.88,high)
- output_mode='minimal' → multi_minimal format:
- `{"intent_mode":"multi","results":[{"target":"translator","conf":0.91,"tier":"high","path":"./translator_aiap/"},{"target":"summarizer","conf":0.88,"tier":"high","path":"./summarizer_aiap/"}],"count":2}`
- Compact array format vs full multi schema — ~60% fewer tokens

**Scenario 19: Trace privacy filter**
- PostProcess writes trace to trace_history.json
- Per trace_privacy: allow-list applied — only node, result, tier, latency_ms retained
- Raw signal_scores, context data, input hash all dropped
- Trace history safe for external review without PII exposure risk

**Scenario 20: Candidate pruning for large registry**
- Registry has 120 leaf AIAPs
- RecursiveClassify PRUNE: top-k(≤7) by signal scores → 7 candidates selected
- Only these 7 scored in detail (semantic + calibrate)
- 94% reduction in scoring computation vs scoring all 120
- Accuracy maintained: top signals already capture best candidates

**Scenario 21: Cold-start discovery — new AIAP gets classified**
- New AIAP "budget_planner" registered 2 hours ago, only 3 classifications so far
- Input: "help me plan my budget"
- RecursiveClassify PRUNE: top-7 by signals, budget_planner's signal score is low (0.35)
- Cold-start guarantee: ≥1 slot reserved for new AIAPs (reg<24h ∨ freq<10)
- budget_planner included in top-7 despite low signal → scored in detail → matched (conf=0.82)
- Without cold-start slot, budget_planner would have been pruned at position 9

**Scenario 22: CJK compact label matching**
- Registry contains AIAP "費用追蹤器應用" (Expense Tracker App in Traditional Chinese)
- DataSync: compact_label rule CJK≤6c → compact_label = "費用追蹤" (4 chars, within limit)
- Input: "幫我追蹤費用" → keyword signal matches compact_label "費用追蹤" (0.88)
- Combined signal → expense_tracker (conf=0.93)
- CJK label normalization enables cross-language matching without tokenization

**Scenario 23: Domain hint biases signal weights**
- AIAP "code_reviewer" has signal_bias: "keyword" in registry
- Input: "review this code" → keyword signal normally w0.4, with domain hint → w0.5
- signal_bias→+0.1 to keyword weight, other weights renormalized (sum=1 + hint)
- Code_reviewer gets stronger keyword match → conf=0.94 (vs 0.89 without hint)
- Domain-specific AIAPs can self-declare their strongest signal channel

## Data Storage

| File | Purpose | Persistence |
|------|---------|-------------|
| `data/registry.json` | AIAP package registry (leaf/branch typed, compact_label, signal_bias) | TTL 3600s |
| `data/taxonomy.json` | Classification tree + version_tag | On registry change |
| `data/cache.json` | Semantic cache + freq tracking + stale_high_tier flag | Max 200, tiered TTL (15-45min), stale cleanup@180 |
| `data/learning_log.json` | Classification log + qe + switch_signals + domain_hint_used | Archive at 1000 |
| `data/session_state.json` | Session history + active_path | TTL 2h |
| `data/promotion_log.json` | Pending promote/demote actions (applied:true persisted) | Applied by DataSync |
| `data/trace_history.json` | Ring buffer of last N traces (privacy-filtered, N=trace_history_size) | FIFO, max configurable [1,20] |

## Node Architecture (v3.0.0 — 11 nodes, 10 with [ASSERT] gate)

| Node | Steps | Purpose |
|------|-------|---------|
| Start | 1 | Mode gate (full/drill_down) + validation + sanitize + safety + start_ts + trace init |
| DataSync | 2 | CB + registry (leaf/branch, compact_label en≤3w/CJK≤6c, signal_bias) + taxonomy + stale-tier + promotions (persist+safety) |
| SmartShortcut | 1 | Switch signal detection + accuracy gate + half-open recovery + context continuity + cache pre-check |
| SemanticCache | 2 | Cache lookup (exact+similarity, stale-tier aware) + tiered TTL + stale cleanup@180 + value-aware eviction |
| ContextEnrich | 4 | Multilingual + stateless + anaphora + boosts |
| IntentRoute | 1 | Single/multi detection |
| RecursiveClassify | 3 | Signal-decision routing (keyword+compact_label+semantic+context) + domain hint → candidate prune (cold-start slot) → semantic + calibrate |
| QualityGate | 4 | Early-exit + scope + adaptive + cascade qe + tier + TypeGate |
| ClarifyAsk | 1 | Clarification loop (includes branch categories) |
| OutputResult | 2 | Branch drill-down + format per output_rule (minimal/multi_minimal/full/verbose) + trace→PostProcess only |
| PostProcess | 3 | depth>0→skip. CB + session + learn (domain_hint_used) + metrics + promo(+safety) + trace overflow + trace history ring (configurable size, privacy-scoped) |

## Changelog

### v3.1.0 (Context Fast Routing + Protocol Hardening — Creator v3.7.0)
- B1: Context-aware fast routing — SmartShortcut enhanced with 3 context signals: session pattern (3+ consecutive same-domain→predict, conf 0.93), domain affinity (>40% frequency + keyword match, conf 0.90), temporal match (similar hash within 24h, conf 0.92). Bypasses SemanticCache→ContextEnrich→IntentRoute→RecursiveClassify chain
- C1: Mermaid cleanup — removed phantom nodes (TypeGate merged into QualityGate, PostGate/ReturnParent merged into OutputResult/PostProcess, End→endNode). SmartShortcut edge label `continuity`→`fast` (covers all fast paths)
- C2: ASSERT backtrack targets fixed — RecursiveClassify `go back.`→`go back to IntentRoute.`, OutputResult `go back.`→`go back to QualityGate.` per Protocol F.2
- C3: k-bounded backtrack — execution.max_backtrack_depth=2 (min(3, 11/4)=2), backtrack_exceeded=halt_with_diagnostic per Protocol F.3 ABC-inspired
- C4: agent_card.json generator updated v3.3.0→v3.7.0

### v3.0.0 (Assertion Execution + Node Gate — Protocol v3.3.0 Alignment)
- Assertion execution: instruction `RUN aisop.main` → `ASSERT RUN aisop.main`; assertion semantics enforce execution as programming invariant
- Execution mode: `strict` → `assert` per AIAP Protocol v3.3.0
- Node Gate: all 10 non-start nodes have `[ASSERT] {prev_node} executed. If false → go back.` at S1 opening; MF28 compliant
- Multi-predecessor gates: RecursiveClassify (IntentRoute∨Start∨ClarifyAsk), OutputResult (QualityGate∨SmartShortcut∨SemanticCache) list all valid predecessors
- Tags compressed: 75→25 items (removed internal implementation details, kept user-facing terms)
- agent_card.json synced v2.3.0→v3.0.0 (was 6 versions behind)
- quality_baseline.json synced v2.3.0→v3.0.0
- quality score aligned: AIAP.md 4.990→4.970 (matched quality_baseline actual weighted_score)
- All v2.9.0 functionality preserved

### v2.9.0 (Cold-Start Discovery + CJK Labels + Privacy Scope + Domain Hints + Configurable History)
- Cold-start discovery guarantee: RecursiveClassify PRUNE reserves ≥1 slot for new AIAPs (reg<24h ∨ freq<10); prevents pruning from excluding newly registered AIAPs (P62 fix)
- CJK compact label rules: DataSync compact_label extended — en≤3 words, CJK≤6 chars; proper multilingual label normalization (P61 fix)
- Trace privacy scope clarification: trace_privacy scope explicitly defined — "history only; verbose unfiltered"; verbose output exempt from privacy filtering (P64 fix)
- Signal weight domain hints: DataSync scans optional signal_bias from registry; RecursiveClassify applies +0.1 to biased signal weight; per-domain signal tuning (P56 partial fix)
- Configurable trace history size: trace_history_size parameter [1,20] default 5; PostProcess ring buffer uses configurable size (P60 fix)
- domain_hint_used field added to learning_log
- shared_constraints: 13 items (trace_privacy scope expanded)
- Parameters: 13 (+trace_history_size)
- Phase C compression: -69 chars (-0.55%) with 5 new features — net negative growth
- All v2.8.0 functionality preserved

### v2.8.0 (Multi-Intent Minimal + Trace Privacy + Signal Scope + Candidate Pruning + Compact Labels)
- Multi-intent minimal output: output_schema.multi_minimal — compact array [{target,conf,tier,path}]+count; output_rule updated for multi_minimal; consistent minimal format for multi-intent scenarios (P52 fix)
- Trace privacy filter: shared_constraints.trace_privacy — allow-list filter (node,result,tier,latency_ms); drops scores,context,hash from trace_history.json; PII sanitization at source; inspired by OpenTelemetry redaction best practices (P57 fix)
- Signal scope constraint: RecursiveClassify drill_down constraint — signals scoped to parent.sub_programs only; prevents cross-branch signal matching in recursive mode (P59 fix)
- Candidate pruning: RecursiveClassify PRUNE — top-k(≤7) by signal scores before detailed scoring; reduces computation for large registries; inspired by REIC hierarchical classification architecture
- Compact labels: DataSync extracts compact_label(≤3 words) from AIAP name; used in keyword signal matching; faster, more precise matching
- quality_estimate abbreviated to qe throughout (compression)
- shared_constraints: 13 items (+trace_privacy)
- Phase C compression: +126 chars (+1.0%) with 5 new features
- All v2.7.0 functionality preserved

### v2.7.0 (Trace History + Promotion Persistence + Trace Compression + Signal-Decision + Promotion Safety)
- Trace history ring buffer: PostProcess writes last 5 traces to data/trace_history.json (FIFO); enables retrospective debugging without verbose mode (P55 fix)
- Promotion persistence: promotion_log entries marked applied:true; confirmed promotions survive registry rescan; prevents promotion loss on rebuild (P46 fix)
- Trace overflow compression: execution.trace_overflow — budget exceeded→keep node+result, drop verbose fields; defined compression strategy (P51 fix)
- Signal-decision routing: RecursiveClassify multi-signal — keyword(w0.4)+semantic(w0.4)+context(w0.2); weighted combined score replaces single-path; inspired by vLLM Signal-Decision Architecture
- Promotion safety guards: promotion_rules Safety — branch≥1 child, no circular, affinity≥0.5; prevents orphan branches and circular promote/demote (S28/P46 fix)
- Learning log extended: signal_scores field
- Phase C compression: +120 chars (+1.0%) with 5 new features
- All v2.6.0 functionality preserved

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
