# SoulBot

**基于 AISOP 协议和 AIAP 包系统的 AI Agent 框架**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-Apache%202.0-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-1266%20passed-brightgreen.svg)](#测试)

[English](README.md) | 中文文档

---

## SoulBot 是什么？

SoulBot 是一个基于 Python 的 AI Agent 框架，通过 CLI 子进程（ACP 协议）连接 LLM —— **无需 API Key**。它引入了独特的架构：Agent 行为由 **AISOP 蓝图**（`.aisop.json`）定义，通过 **AIAP 包**（`*_aiap`）扩展能力，使 AI Agent 的行为变得确定性、可复现、可版本控制。

### 核心特性

- **免 API Key** — 通过 Claude Code / Gemini CLI / OpenCode CLI 子进程接入 LLM
- **多模型切换** — Claude、Gemini、OpenCode（Kimi 等），`.env` 一行切换
- **AISOP 驱动** — Agent 行为由 `.aisop.json` 蓝图定义，mermaid 流程图作为确定性执行路径
- **AIAP 包系统** — 热插拔功能包（`*_aiap`），即插即用扩展 Agent 能力
- **Agent 组合** — 单 Agent、多 Agent 路由、Sequential / Parallel / Loop 工作流
- **工具系统** — Python 函数自动包装为 LLM 可调用工具
- **多通道接入** — 终端 CLI、Web Dev UI、Telegram Bot
- **流式输出** — SSE 打字机效果（Web + Telegram）

---

## 快速开始

### 前置条件

- Python 3.11+
- 至少安装一个 LLM CLI 工具：

| 工具 | 安装命令 | 登录 |
|------|----------|------|
| Claude Code | `npm install -g @anthropic-ai/claude-code` | `claude login` |
| Gemini CLI | `npm install -g @google/gemini-cli` | `gemini login` |
| OpenCode | `npm install -g opencode` | 免费模型，无需登录 |

### 安装

```bash
git clone https://github.com/AIXP-Foundation/SoulBot.git
cd SoulBot
pip install -e .
```

### 运行

```bash
# Web Dev UI（浏览器打开 http://127.0.0.1:8000）
soulbot web --agents-dir examples/simple

# 终端交互模式
soulbot run examples/simple/SoulBot_Agent

# Telegram Bot
soulbot telegram examples/simple/SoulBot_Agent
```

### 创建你自己的 Agent

```bash
soulbot create my_agent
```

生成以下文件：

```
my_agent/
├── agent.py          # Agent 定义（AISOP Runtime）
├── main.aisop.json   # AISOP 蓝图（意图路由）
├── .env              # 配置（模型选择等）
└── aiap/             # AIAP 功能包目录
    └── README.md
```

编辑 `.env` 选择 LLM 后端，然后运行：

```bash
soulbot run my_agent
```

---

## 架构

### AISOP + AIAP

SoulBot 引入了两个核心概念：

| 概念 | 说明 |
|------|------|
| **AISOP V1.0.0** | AI Standard Operating Procedure — 基于 JSON 的蓝图协议，通过 mermaid 流程图定义 Agent 行为 |
| **AIAP 包** | AI Application Package — 热插拔功能模块（`*_aiap/`），每个包含 `main.aisop.json` 入口 |

**核心理念**：mermaid 流程图是确定性执行路径（类似电路图），prompt 提供上下文和约束（类似元器件参数）。这种分离使 Agent 行为可复现、可版本控制。

```
用户消息
    ↓
agent.py → _dynamic_instruction()
    ├── _SYSTEM_PROMPT（WHO — 运行时身份）
    ├── main.aisop.json（WHAT — 路由规则）
    └── [Available AIAP packages]（可用能力）
    ↓
LLM 按 mermaid 流程执行：
    NLU[匹配意图] → Run[加载并执行 *_aiap/main.aisop.json]
    ↓
AIAP 包内的 mermaid 流程执行领域逻辑
    ↓
返回结果给用户
```

### 治理域

AIAP 采用三方联邦信任模型：

- **aisop.dev**（种子层）：定义不可变的格式结构。
- **aiap.dev**（权威层）：定义可演进的治理规则。
- **soulbot.dev**（执行层）：物理执行 AISOP 代码的参考运行时引擎。

### 系统架构

```
用户入口
├── CLI Terminal     →  soulbot run <agent_dir>
├── Web Dev UI       →  soulbot web --agents-dir <dir>
├── API Server       →  soulbot api-server --agents-dir <dir>
└── Telegram Bot     →  soulbot telegram <agent_dir>
         ↓
Runner
├── Agent 树执行    →  LlmAgent / SequentialAgent / ParallelAgent / LoopAgent
├── AISOP 引擎     →  main.aisop.json → mermaid 流程 → AIAP 包路由
├── 工具调用        →  FunctionTool / AgentTool / TransferToAgentTool
├── CMD 系统       →  嵌入式命令（定时任务等）
├── Session 管理    →  InMemory / SQLite + State delta
├── EventBus        →  发布/订阅 + 过滤 + 优先级
└── 流式输出        →  partial Event → SSE / Telegram 打字机效果
         ↓
模型层
├── ModelRegistry    →  正则匹配模型名 → 适配器选择
└── ACPLlm           →  CLI 子进程 JSON-RPC
     ├── ClaudeACPClient    (claude-acp/*)
     ├── GeminiACPClient    (gemini-acp/*)
     ├── OpenCodeACPClient  (opencode-acp/*)
     └── OpenClawClient     (openclaw/*)
```

---

## Agent 开发

### 最简 Agent

```python
from soulbot.agents import LlmAgent

root_agent = LlmAgent(
    name="my_agent",
    model="claude-acp/sonnet",
    instruction="你是一个友好的助手。",
)
```

### 带工具的 Agent

```python
from soulbot.agents import LlmAgent

def get_weather(city: str) -> dict:
    """获取城市天气。"""
    return {"city": city, "temp": 25, "condition": "sunny"}

root_agent = LlmAgent(
    name="weather_agent",
    model="claude-acp/sonnet",
    instruction="你可以查询任何城市的天气。",
    tools=[get_weather],
)
```

函数自动包装为 LLM 工具：函数名 → 工具名，docstring → 描述，type hints → JSON Schema。

### 多 Agent 路由

```python
from soulbot.agents import LlmAgent

billing = LlmAgent(name="billing", model="claude-acp/sonnet",
                    description="处理账单问题",
                    instruction="你是账单专员。")

tech = LlmAgent(name="tech", model="claude-acp/sonnet",
                description="处理技术问题",
                instruction="你是技术支持。")

root_agent = LlmAgent(
    name="router",
    model="claude-acp/sonnet",
    instruction="根据用户问题转移到合适的专员。",
    sub_agents=[billing, tech],
)
```

### 工作流 Agent

```python
from soulbot.agents import LlmAgent, SequentialAgent, ParallelAgent, LoopAgent

# 顺序执行
root_agent = SequentialAgent(name="pipeline", sub_agents=[analyzer, responder])

# 并行执行
root_agent = ParallelAgent(name="parallel", sub_agents=[search, summarize])

# 循环执行
root_agent = LoopAgent(name="refiner", sub_agents=[draft, review], max_iterations=3)
```

---

## 配置

### .env 参考

```env
# LLM 后端（四选一设为 true）
CLAUDE_CLI=true
GEMINI_CLI=false
OPENCODE_CLI=false
OPENCLAW_CLI=false

# 模型名
CLAUDE_MODEL=claude-acp/sonnet
GEMINI_MODEL=gemini-acp/gemini-2.5-flash
OPENCODE_MODEL=opencode-acp/opencode/kimi-k2.5-free

# 行为控制
WORKSPACE_DIR=aiap            # AIAP 包目录
ENABLE_FALLBACK=false         # 失败自动切换备用模型
AUTO_APPROVE_PERMISSIONS=true # 自动批准 CLI 权限请求
SHOW_THOUGHTS=false           # 显示 AI 思考过程

# Telegram（可选）
TELEGRAM_BOT_TOKEN=
```

### 模型名格式

| 格式 | 说明 |
|------|------|
| `claude-acp/sonnet` | Claude Sonnet |
| `claude-acp/opus` | Claude Opus |
| `gemini-acp/gemini-2.5-flash` | Gemini Flash |
| `opencode-acp/opencode/kimi-k2.5-free` | OpenCode 免费 Kimi |
| `opencode-acp/anthropic/claude-sonnet-4-5` | OpenCode 转接 Claude |
| `openclaw/default` | OpenClaw 默认模型 |

---

## CLI 命令

| 命令 | 说明 |
|------|------|
| `soulbot run <agent_path>` | 终端交互模式 |
| `soulbot web --agents-dir <dir>` | Web Dev UI + API Server |
| `soulbot api-server --agents-dir <dir>` | 仅 API Server（无 UI） |
| `soulbot telegram <agent_path>` | Telegram Bot |
| `soulbot create <name>` | 创建 Agent 项目脚手架 |

未安装时也可以用 `python -m soulbot` 替代 `soulbot`。

---

## Web Dev UI

```bash
soulbot web --agents-dir examples/simple
# 浏览器打开 http://127.0.0.1:8000
```

功能：Markdown 实时渲染、SSE 流式输出、Agent 切换、Session 管理、暗色主题。

### API 端点

| 路由 | 方法 | 说明 |
|------|------|------|
| `/health` | GET | 健康检查 |
| `/list-apps` | GET | 列出所有 Agent |
| `/apps/{name}` | GET | Agent 详情 |
| `/run` | POST | 同步执行 |
| `/run_sse` | POST | SSE 流式执行 |

---

## Telegram Bot

1. 从 [@BotFather](https://t.me/BotFather) 获取 Bot Token
2. 在 `.env` 中添加 `TELEGRAM_BOT_TOKEN=你的Token`
3. 运行：`soulbot telegram examples/simple/SoulBot_Agent`

或 Web + Telegram 同时运行：`soulbot web --agents-dir examples/simple`

Bot 命令：`/start`、`/clear`、`/history`

特性：流式输出、Markdown 渲染、长消息自动分割、多 Agent 路由（InlineKeyboard 切换）。

---

## 定时任务

AI 自驱动定时调度系统 — AI 在回复中嵌入 `<!--SOULBOT_CMD:-->` 指令自动创建定时任务。

- 三种触发器：Once（一次性）/ Interval（间隔）/ Cron（定时）
- 跨 Agent 调度：Agent A 创建任务让 Agent B 执行
- AISOP payload：定时任务携带完整 AISOP V1.0.0 蓝图
- 持久化恢复：重启后自动恢复活跃任务

---

## 项目结构

```
SoulBot/
├── src/soulbot/              # 框架源码
│   ├── agents/               # Agent 系统 (LlmAgent, Sequential, Parallel, Loop)
│   ├── tools/                # 工具系统 (FunctionTool, AgentTool)
│   ├── models/               # 模型层 (ACPLlm, ModelRegistry)
│   ├── acp/                  # ACP 协议 (Claude/Gemini/OpenCode 客户端)
│   ├── runners/              # Runner (驱动 Agent 执行)
│   ├── sessions/             # Session (InMemory / SQLite)
│   ├── server/               # Web/API Server (FastAPI + SSE)
│   ├── connect/              # 通道连接器 (Telegram)
│   ├── commands/             # CMD 命令系统 (嵌入式命令)
│   ├── scheduler/            # 定时任务
│   ├── templates/            # Agent 脚手架模板
│   └── cli.py                # CLI 入口
├── examples/simple/          # 示例 Agent
│   └── SoulBot_Agent/        # 主 Agent（含 AIAP 包）
├── tests/                    # 1266 单元测试
├── docs/                     # 文档
└── pyproject.toml            # 项目配置
```

---

## 测试

```bash
# 全部单元测试
python -m pytest tests/ -q

# 指定模块
python -m pytest tests/test_agents/ -q

# E2E 测试（需要真实 CLI 登录）
python -m pytest tests/e2e/ -m live -q
```

---

## 安装选项

```bash
# 开发模式
pip install -e ".[dev]"

# 含 Telegram 支持
pip install -e ".[telegram]"

# 含 SQLite Session
pip install -e ".[sqlite]"

# 全部安装
pip install -e ".[dev,telegram,sqlite]"

# 从 GitHub 安装
pip install git+https://github.com/AIXP-Foundation/SoulBot.git

# 一键运行（uv）
uvx --from git+https://github.com/AIXP-Foundation/SoulBot.git soulbot web --agents-dir .
```

详细的安装与发布说明见 [INSTALL.md](INSTALL.md)。

---

## 文档

| 文档 | 说明 |
|------|------|
| [GUIDE.md](GUIDE.md) | 完整使用指南 |
| [INSTALL.md](INSTALL.md) | 安装、打包与发布 |
| [docs/guide/01-function-call-guide.md](docs/guide/01-function-call-guide.md) | Function Call 开发指南 |
| [docs/guide/02-soulbot-cmd-guide.md](docs/guide/02-soulbot-cmd-guide.md) | SoulBot CMD 开发指南 |

---

## 许可证

本项目基于 Apache License 2.0 许可证开源 — 详见 [LICENSE](LICENSE) 文件。

```
Copyright 2026 AIXP Foundation AIXP.dev | SoulBot.dev

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```
