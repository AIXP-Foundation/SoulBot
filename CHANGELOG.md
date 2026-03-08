# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-03-03

### Added

- **Agent System** — LlmAgent, SequentialAgent, ParallelAgent, LoopAgent with composable workflows
- **ACP Protocol** — CLI subprocess communication with Claude Code, Gemini CLI, OpenCode, OpenClaw
- **AISOP Runtime** — Execute `.aisop.json` blueprints with mermaid flowcharts as deterministic execution paths
- **AIAP Package System** — Hot-pluggable capability packages (`*_aiap/`) with dynamic discovery and loading
- **Tool System** — Python functions auto-wrapped as LLM-callable tools via type hint introspection
- **Multi-Model Switching** — Claude, Gemini, OpenCode (Kimi, etc.) — switch with one line in `.env`
- **Web Dev UI** — FastAPI-based development interface with Markdown rendering and SSE streaming
- **API Server** — RESTful API with `/run` (sync) and `/run_sse` (streaming) endpoints
- **Telegram Bot** — Full-featured bot with streaming output, Markdown rendering, and multi-agent routing
- **Session Management** — InMemory and SQLite session backends with state delta tracking
- **EventBus** — Pub/sub event system with filtering and priority support
- **Scheduling** — AI-driven task scheduling with Once / Interval / Cron triggers and cross-agent dispatch
- **CLI** — `soulbot run`, `soulbot web`, `soulbot telegram`, `soulbot create` commands
- **Model Registry** — Regex-based model name matching with adapter auto-selection
- **1266 unit tests** covering agents, tools, models, ACP, sessions, server, and scheduling

[1.0.0]: https://github.com/AIXP-Foundation/SoulBot/releases/tag/v1.0.0
