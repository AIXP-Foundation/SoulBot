"""CLI entry point for SoulBot.

After ``pip install -e .``, the ``soulbot`` command is available globally::

    soulbot run <agent_dir>            # Interactive terminal chat
    soulbot web --agents-dir .         # Dev UI + API server
    soulbot api-server --agents-dir .  # API server only (no UI)
    soulbot telegram <agent_dir>       # Run Telegram bot for an agent
    soulbot create <name>              # Scaffold a new agent project

Or run without installing::

    python -m soulbot <command>
"""

from __future__ import annotations

import asyncio
import logging
import sys
from pathlib import Path

import click

logger = logging.getLogger(__name__)

from .server.config import load_dotenv


@click.group()
def main():
    """SoulBot — AI Agent Framework CLI."""
    pass


# ---------------------------------------------------------------------------
# soulbotrun
# ---------------------------------------------------------------------------


@main.command()
@click.argument("agent_path")
def run(agent_path: str):
    """Run an agent interactively in the terminal.

    AGENT_PATH can be:
    - A directory containing agent.py (or __init__.py with root_agent)
    - A path like agents_dir/agent_name
    """
    agent_dir = Path(agent_path).resolve()

    # Load per-agent .env first (override=True), then cwd/.env as fallback
    load_dotenv(str(agent_dir))

    # Determine agents_dir and agent_name
    if (agent_dir / "agent.py").exists() or (agent_dir / "__init__.py").exists():
        agents_dir = agent_dir.parent
        agent_name = agent_dir.name
    elif agent_dir.is_file() and agent_dir.suffix == ".py":
        agents_dir = agent_dir.parent
        agent_name = agent_dir.stem
    else:
        click.echo(f"Error: Cannot find agent at '{agent_path}'", err=True)
        sys.exit(1)

    # Load shared .env from agents_dir (agent-level already loaded above)
    load_dotenv(str(agents_dir))

    from .server.agent_loader import AgentLoader
    from .runners import Runner
    from .sessions import DatabaseSessionService
    from .sessions.constants import resolve_cli_name, resolve_db_path

    cli_name = resolve_cli_name()
    db_path = resolve_db_path(str(agents_dir))

    try:
        loader = AgentLoader(agents_dir)
        agent = loader.load_agent(agent_name)
    except (FileNotFoundError, AttributeError, TypeError) as e:
        click.echo(f"Error loading agent: {e}", err=True)
        sys.exit(1)

    click.echo(f"Agent: {agent.name}")
    click.echo(f"Description: {agent.description or '(none)'}")
    click.echo("Type 'quit' or 'exit' to stop.\n")

    svc = DatabaseSessionService(db_path)
    history_service = _build_history_service(str(agents_dir))
    _setup_provider_session_store()
    _inject_history_tool(agent, history_service)
    runner = Runner(
        agent=agent, app_name=cli_name, session_service=svc,
        history_service=history_service,
    )

    async def chat_loop():
        import uuid
        from datetime import datetime
        from .sessions.constants import DEFAULT_USER_ID

        user_id = DEFAULT_USER_ID

        # Auto-resume: current agent's most recent session (Doc 11)
        sessions = await svc.list_sessions(cli_name, user_id, agent_name=agent.name)

        if sessions:
            last = sessions[0]  # ORDER BY last_update_time DESC
            dt = datetime.fromtimestamp(last.last_update_time).strftime("%m-%d %H:%M")
            title_display = last.title or last.id[:8]
            agent_info = f" ({last.last_agent})" if last.last_agent else ""
            click.echo(f"Resuming: [{dt}] {title_display}{agent_info}")
            session_id = last.id
        else:
            session_id = str(uuid.uuid4())
            click.echo("Starting new session.")
            # Offer to import history (Doc 22 Step 7)
            try:
                count = await history_service.count(user_id, agent.name)
                if count > 0:
                    answer = input(
                        f"Found {count} messages with {agent.name}. "
                        "Import recent history? [y/N]: "
                    )
                    if answer.strip().lower() == "y":
                        from .history import import_history_to_session
                        session = await svc.create_session(
                            cli_name, user_id, agent_name=agent.name,
                            session_id=session_id,
                        )
                        imported = await import_history_to_session(
                            history_service, svc, session,
                            user_id, agent.name,
                        )
                        click.echo(f"Imported {imported} messages.")
            except (EOFError, KeyboardInterrupt):
                pass

        while True:
            try:
                user_input = input("You: ")
            except (EOFError, KeyboardInterrupt):
                click.echo("\nBye!")
                break

            if user_input.strip().lower() in ("quit", "exit"):
                click.echo("Bye!")
                break

            if not user_input.strip():
                continue

            try:
                async for event in runner.run(
                    user_id=user_id,
                    session_id=session_id,
                    message=user_input,
                ):
                    if event.partial:
                        continue
                    if event.content and event.content.parts:
                        for part in event.content.parts:
                            if part.text:
                                click.echo(f"[{event.author}]: {part.text}")
                            if part.function_call:
                                click.echo(
                                    f"[{event.author}]: calling {part.function_call.name}"
                                    f"({part.function_call.args})"
                                )
                            if part.function_response:
                                click.echo(
                                    f"[{event.author}]: {part.function_response.name} "
                                    f"→ {part.function_response.response}"
                                )
            except Exception as e:
                click.echo(f"Error: {e}", err=True)

    asyncio.run(chat_loop())


# ---------------------------------------------------------------------------
# Frontend auto-build
# ---------------------------------------------------------------------------


def _auto_build_frontend() -> None:
    """Check if frontend source changed, auto-rebuild + start watcher."""
    import subprocess
    from .server.api_server import STATIC_DIR

    frontend_dir = STATIC_DIR.parent.parent.parent.parent / "frontend"
    if not (frontend_dir / "package.json").is_file():
        return

    src_dir = frontend_dir / "src"
    if not src_dir.is_dir():
        return

    # Compare newest source mtime vs newest build mtime
    src_exts = {".vue", ".ts", ".js", ".css", ".html"}
    src_newest = 0.0
    for f in src_dir.rglob("*"):
        if f.is_file() and f.suffix in src_exts:
            src_newest = max(src_newest, f.stat().st_mtime)

    build_newest = 0.0
    if STATIC_DIR.is_dir():
        for f in STATIC_DIR.rglob("*"):
            if f.is_file():
                build_newest = max(build_newest, f.stat().st_mtime)

    needs_build = src_newest > build_newest or build_newest == 0.0

    if needs_build:
        click.echo("Frontend source changed, auto-rebuilding...")
        try:
            subprocess.run(
                "npm run build",
                cwd=str(frontend_dir),
                shell=True,
                check=True,
            )
            click.echo("Frontend rebuild complete.")
        except subprocess.CalledProcessError as e:
            click.echo(f"Warning: Frontend build failed (exit {e.returncode})", err=True)
        except FileNotFoundError:
            click.echo("Warning: npm not found, skipping frontend build", err=True)

    # Start vite build --watch in background for live reload
    try:
        import atexit
        proc = subprocess.Popen(
            "npx vite build --watch",
            cwd=str(frontend_dir),
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        atexit.register(lambda: proc.terminate())
    except FileNotFoundError:
        pass


# ---------------------------------------------------------------------------
# soulbotweb
# ---------------------------------------------------------------------------


@main.command()
@click.option("--agents-dir", required=True, help="Directory containing agent modules")
@click.option("--host", default="127.0.0.1", help="Bind host")
@click.option("--port", default=8000, type=int, help="Bind port")
@click.option("--telegram/--no-telegram", default=None,
              help="Enable/disable Telegram bot (auto-detected from TELEGRAM_BOT_TOKEN)")
def web(agents_dir: str, host: str, port: int, telegram: bool | None):
    """Start the dev web UI with API server."""
    import os
    load_dotenv(agents_dir)

    import uvicorn
    from .server.api_server import create_app
    from .sessions import DatabaseSessionService
    from .sessions.constants import resolve_cli_name, resolve_db_path

    cli_name = resolve_cli_name()
    db_path = resolve_db_path(agents_dir)

    web_svc = DatabaseSessionService(db_path)
    web_history = _build_history_service(agents_dir)
    _setup_provider_session_store()

    # Schedule service — set by Telegram pipeline when available
    sched_svc = None
    active_hb_store = None

    # Auto-start Telegram bot(s)
    # Scan agents, group by TELEGRAM_BOT_TOKEN, start one bridge per token.
    # Agents without a token fall into the root token (from agents_dir/.env).
    if telegram is not False:
        try:
            from .connect.telegram import TelegramBridge
            from .server.agent_loader import AgentLoader
            from .runners import Runner
            from .sessions import DatabaseSessionService

            loader = AgentLoader(agents_dir)
            root_token = loader._root_env.get("TELEGRAM_BOT_TOKEN", "").strip()
            token_groups = _scan_telegram_tokens(loader, root_token)

            enable_tg = telegram if telegram is not None else bool(token_groups)

            if enable_tg and token_groups:
                for token, agent_names in token_groups.items():
                    svc = DatabaseSessionService(db_path)
                    agents = []
                    for name in agent_names:
                        try:
                            agent = loader.load_agent(name)
                            agents.append(agent)
                        except (AttributeError, TypeError, FileNotFoundError):
                            continue
                    if not agents:
                        continue

                    # Wire up schedule pipeline (Doc 17.6)
                    agents_dict = {a.name: a for a in agents}
                    bus, cmd_executor, cron, _svc, hb_store = _build_schedule_pipeline(
                        agents=agents_dict, session_service=svc,
                        agents_dir=agents_dir, cli_name=cli_name,
                    )
                    sched_svc = _svc  # capture for web API
                    active_hb_store = hb_store

                    tg_history = _build_history_service(agents_dir)

                    for a in agents:
                        _inject_history_tool(a, tg_history)

                    if len(agents) == 1:
                        # Single agent → direct binding
                        agent = agents[0]
                        runner = Runner(
                            agent=agent, app_name=cli_name,
                            session_service=svc,
                            bus=bus, cmd_executor=cmd_executor,
                            history_service=tg_history,
                        )
                        bridge = TelegramBridge(
                            runner=runner, bot_token=token,
                            session_service=svc, bus=bus,
                            on_startup=[cron.start],
                            history_service=tg_history,
                        )
                        bridge.start_in_thread()
                        click.echo(f"Telegram Bot started for agent: {agent.name}")
                    else:
                        # Multi-agent → routing mode
                        runners = {}
                        for agent in agents:
                            runners[agent.name] = Runner(
                                agent=agent, app_name=cli_name,
                                session_service=svc,
                                bus=bus, cmd_executor=cmd_executor,
                                history_service=tg_history,
                            )
                        first_name = agents[0].name
                        bridge = TelegramBridge(
                            runner=runners[first_name],
                            bot_token=token,
                            session_service=svc,
                            runners=runners,
                            default_agent=first_name,
                            bus=bus,
                            on_startup=[cron.start],
                            history_service=tg_history,
                        )
                        bridge.start_in_thread()
                        names = ", ".join(runners.keys())
                        click.echo(
                            f"Telegram Bot started (multi-agent): {names}"
                        )
            elif telegram is True:
                click.echo(
                    "Warning: --telegram enabled but no TELEGRAM_BOT_TOKEN found",
                    err=True,
                )
        except ImportError:
            if telegram is True:
                click.echo(
                    "Warning: python-telegram-bot not installed. "
                    "Install with: pip install 'python-telegram-bot>=20.0'",
                    err=True,
                )
        except Exception as e:
            click.echo(f"Warning: Failed to start Telegram bot: {e}", err=True)

    # Create heartbeat store for web API (fallback if no Telegram pipeline)
    if active_hb_store is None:
        from .scheduler.heartbeat_store import HeartbeatStore as _HBStore
        _data_dir = Path(agents_dir) / "data" if agents_dir else Path(".")
        _data_dir.mkdir(exist_ok=True)
        active_hb_store = _HBStore(str(_data_dir / "heartbeat.db"))

    app = create_app(
        agents_dir=agents_dir, dev_ui=True,
        session_service=web_svc,
        schedule_service=sched_svc,
        heartbeat_store=active_hb_store,
        cli_name=cli_name,
    )

    # Auto-build frontend if source changed + start watcher
    _auto_build_frontend()

    click.echo(f"Starting SoulBot Dev UI at http://{host}:{port}")
    click.echo(f"Agents directory: {Path(agents_dir).resolve()}")
    uvicorn.run(app, host=host, port=port)


# ---------------------------------------------------------------------------
# soulbotapi_server
# ---------------------------------------------------------------------------


@main.command()
@click.option("--agents-dir", required=True, help="Directory containing agent modules")
@click.option("--host", default="127.0.0.1", help="Bind host")
@click.option("--port", default=8000, type=int, help="Bind port")
def api_server(agents_dir: str, host: str, port: int):
    """Start the API server (no dev UI)."""
    load_dotenv(agents_dir)

    import uvicorn
    from .server.api_server import create_app
    from .sessions.constants import resolve_cli_name

    cli_name = resolve_cli_name()
    app = create_app(agents_dir=agents_dir, dev_ui=False, cli_name=cli_name)
    click.echo(f"Starting SoulBot API Server at http://{host}:{port}")
    uvicorn.run(app, host=host, port=port)


# ---------------------------------------------------------------------------
# soulbot telegram
# ---------------------------------------------------------------------------


@main.command()
@click.argument("agent_path")
def telegram(agent_path: str):
    """Run a Telegram bot for an agent (Long Polling).

    AGENT_PATH is a directory containing agent.py and .env with TELEGRAM_BOT_TOKEN.
    """
    import os

    agent_dir = Path(agent_path).resolve()
    load_dotenv(str(agent_dir))

    bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    if not bot_token:
        click.echo(
            "Error: TELEGRAM_BOT_TOKEN not set. "
            "Add it to your agent's .env file.",
            err=True,
        )
        sys.exit(1)

    # Determine agents_dir and agent_name
    if (agent_dir / "agent.py").exists() or (agent_dir / "__init__.py").exists():
        agents_dir = agent_dir.parent
        agent_name = agent_dir.name
    else:
        click.echo(f"Error: Cannot find agent at '{agent_path}'", err=True)
        sys.exit(1)

    # Load shared .env from agents_dir (agent-level already loaded above)
    load_dotenv(str(agents_dir))

    try:
        from .connect.telegram import TelegramBridge
    except ImportError:
        click.echo(
            "Error: python-telegram-bot is required. "
            "Install with: pip install 'python-telegram-bot>=20.0'",
            err=True,
        )
        sys.exit(1)

    from .server.agent_loader import AgentLoader
    from .runners import Runner
    from .sessions import DatabaseSessionService
    from .sessions.constants import resolve_cli_name, resolve_db_path

    cli_name = resolve_cli_name()
    db_path = resolve_db_path(str(agents_dir))

    try:
        loader = AgentLoader(agents_dir)
        agent = loader.load_agent(agent_name)
    except (FileNotFoundError, AttributeError, TypeError) as e:
        click.echo(f"Error loading agent: {e}", err=True)
        sys.exit(1)

    # Enable logging so users can see activity
    import logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    click.echo(f"Agent: {agent.name}")
    click.echo(f"Model: {agent.model or 'default'}")
    click.echo(f"Starting Telegram Bot (Long Polling)...")

    svc = DatabaseSessionService(db_path)
    tg_history = _build_history_service(str(agents_dir))
    _setup_provider_session_store()
    _inject_history_tool(agent, tg_history)

    # Wire up schedule pipeline (Doc 17.6)
    bus, cmd_executor, cron, sched_svc, hb_store = _build_schedule_pipeline(
        agents={agent.name: agent}, session_service=svc,
        agents_dir=str(agents_dir), cli_name=cli_name,
    )

    runner = Runner(
        agent=agent, app_name=cli_name, session_service=svc,
        bus=bus, cmd_executor=cmd_executor,
        history_service=tg_history,
    )
    bridge = TelegramBridge(
        runner=runner, bot_token=bot_token, session_service=svc,
        bus=bus, on_startup=[cron.start],
        history_service=tg_history,
    )

    # Build and run polling (blocks until Ctrl+C)
    bridge.build_application()
    try:
        from telegram import Update
        bridge.app.run_polling(allowed_updates=Update.ALL_TYPES)
    except KeyboardInterrupt:
        click.echo("\nTelegram Bot stopped.")


# ---------------------------------------------------------------------------
# soulbot create
# ---------------------------------------------------------------------------


@main.command()
@click.argument("name")
@click.option("--template", "-t", default="basic",
              type=click.Choice(["basic"]),
              help="Agent template: basic (AIAP intent router)")
@click.option("--output-dir", default=".", help="Where to create the agent directory")
def create(name: str, template: str, output_dir: str):
    """Scaffold a new agent project from template."""
    from soulbot.templates import scaffold_agent

    try:
        target = scaffold_agent(name, template, Path(output_dir))
    except ValueError as exc:
        click.echo(f"Error: {exc}", err=True)
        sys.exit(1)
    except FileExistsError as exc:
        click.echo(f"Error: {exc}", err=True)
        sys.exit(1)
    except Exception as exc:
        click.echo(f"Error creating agent: {exc}", err=True)
        sys.exit(1)

    click.echo(f"Created agent project: {target} (template: {template})")
    click.echo(f"\nRun it with: python -m soulbot run {target}")


# ---------------------------------------------------------------------------
# History service + provider session store factory (Doc 22)
# ---------------------------------------------------------------------------


def _build_history_service(agents_dir: str | None = None):
    """Create a SqliteChatHistoryService in agents_dir/data/.

    Returns a :class:`SqliteChatHistoryService` instance.
    """
    from pathlib import Path
    from .history import SqliteChatHistoryService

    if agents_dir:
        data_dir = Path(agents_dir) / "data"
        data_dir.mkdir(exist_ok=True)
        db_path = str(data_dir / "soulbot_history.db")
    else:
        db_path = "soulbot_history.db"
    return SqliteChatHistoryService(db_path)


def _inject_history_tool(agent, history_service) -> None:
    """Add search_history tool to *agent* (Doc 22 Step 8).

    Skips agents without a ``tools`` attribute (e.g. SequentialAgent).
    """
    if not hasattr(agent, "tools"):
        return
    from .tools.function_tool import FunctionTool
    from .tools.history_tool import create_history_tool

    fn = create_history_tool(history_service, default_agent=agent.name)
    agent.tools.append(FunctionTool(fn))


def _setup_provider_session_store() -> None:
    """Create and inject ProviderSessionStore into ACPLlm for session reuse."""
    from .conversation import ProviderSessionStore
    from .models.acp_llm import ACPLlm

    prov_store = ProviderSessionStore()
    ACPLlm.set_provider_session_store(prov_store)


# ---------------------------------------------------------------------------
# Schedule pipeline wiring (Doc 17.6)
# ---------------------------------------------------------------------------


def _build_schedule_pipeline(
    agents: dict,
    session_service: "object",
    agents_dir: str | None = None,
    cli_name: str | None = None,
) -> tuple:
    """Create EventBus + CronScheduler + CommandExecutor + ScheduleService + HeartbeatStore.

    Args:
        agents_dir: Base directory for schedule store file.
        cli_name: CLI name to use as app_name in Runners.

    Returns ``(bus, cmd_executor, cron, schedule_service, heartbeat_store)``
    ready to inject into Runner and TelegramBridge.
    """
    from .bus.event_bus import EventBus
    from .commands.executor import CommandExecutor
    from .scheduler.cron import CronScheduler
    from .scheduler.heartbeat_store import HeartbeatStore
    from .scheduler.schedule_service import ScheduleService
    from .scheduler.sqlite_store import SqliteScheduleStore
    from .sessions.constants import DEFAULT_USER_ID

    bus = EventBus()
    cron = CronScheduler(bus=bus)
    cmd_executor = CommandExecutor()

    # Resolve schedule store path — SQLite in data/ directory (Doc 23)
    if agents_dir:
        data_dir = Path(agents_dir) / "data"
        data_dir.mkdir(exist_ok=True)
        sched_db_path = str(data_dir / "soulbot_schedules.db")
        # Old JSON path for migration
        old_json = str(Path(agents_dir).resolve() / ".soulbot_schedules.json")
    else:
        sched_db_path = "soulbot_schedules.db"
        old_json = ".soulbot_schedules.json"

    sched_store = SqliteScheduleStore(sched_db_path, migrate_json=old_json)

    # Heartbeat store — independent SQLite for heartbeat execution history
    hb_db_path = str(Path(sched_db_path).parent / "heartbeat.db") if agents_dir else "heartbeat.db"
    heartbeat_store = HeartbeatStore(hb_db_path)

    # runner_factory: (agent_name, message, context) -> AsyncGenerator[Event]
    # Lazily captures runners dict; runners must be created before first cron fire.
    _runners: dict = {}

    async def runner_factory(agent_name, message, context):
        from .runners import Runner

        runner = _runners.get(agent_name)
        if not runner:
            agent = agents.get(agent_name)
            if not agent:
                return
            runner = Runner(
                agent=agent,
                app_name=cli_name or agent.name,
                session_service=session_service,
                bus=bus,
                cmd_executor=cmd_executor,
            )
            _runners[agent_name] = runner

        from .agents.invocation_context import RunConfig

        async for event in runner.run(
            user_id=DEFAULT_USER_ID,
            session_id=f"sched_{agent_name}",
            message=message,
            run_config=RunConfig(context=context or {}),
        ):
            yield event

    schedule_service = ScheduleService(
        cron=cron, bus=bus, runner_factory=runner_factory,
        store=sched_store,
        heartbeat_store=heartbeat_store,
    )
    cmd_executor.register_service("schedule", schedule_service)

    # Restore persisted tasks (cron.start deferred to on_startup)
    restored = schedule_service.restore()
    if restored:
        click.echo(f"Restored {restored} scheduled tasks")

    # Register heartbeat seeds for agents with heartbeat config
    from .scheduler.heartbeat import register_heartbeats

    hb_count, catch_up_ids = register_heartbeats(agents, schedule_service)
    if hb_count:
        click.echo(f"Registered {hb_count} heartbeat seeds")

    # Wrap cron.start + catch-up into a single startup coroutine
    _original_cron_start = cron.start

    if catch_up_ids:
        click.echo(f"Heartbeat catch-up: {len(catch_up_ids)} missed seed(s) will fire on startup")

        async def _cron_start_with_catch_up():
            await _original_cron_start()
            for eid in catch_up_ids:
                logger.info("Firing heartbeat catch-up: %s", eid)
                await schedule_service.fire_now(entry_id=eid)

        cron.start = _cron_start_with_catch_up  # type: ignore[assignment]

    return bus, cmd_executor, cron, schedule_service, heartbeat_store


# ---------------------------------------------------------------------------
# Telegram token scanning
# ---------------------------------------------------------------------------


def _scan_telegram_tokens(
    loader, root_token: str = "",
) -> dict[str, list[str]]:
    """Scan all agents and group by TELEGRAM_BOT_TOKEN.

    Reads tokens directly from the AgentLoader env cache — no agent
    modules are loaded and no ``os.environ`` manipulation is needed.

    Args:
        loader: An AgentLoader instance (provides ``get_agent_env``).
        root_token: The root-level shared bot token.

    Rules:
        - Agent env has its own token (different from root) → grouped by that token
        - Agent env has no token or same as root → falls into root_token group
        - If no root_token and agent has no token → agent is skipped

    Returns:
        ``{token: [agent_name, ...]}``
    """
    token_groups: dict[str, list[str]] = {}
    no_token_names: list[str] = []

    for name in loader.list_agents():
        env = loader.get_agent_env(name)
        agent_token = env.get("TELEGRAM_BOT_TOKEN", "").strip()

        if agent_token and agent_token != root_token:
            # Agent has its own independent token
            token_groups.setdefault(agent_token, []).append(name)
        else:
            # No token, or same as root → shared bot candidate
            no_token_names.append(name)

    # Agents without their own token go into root_token group
    if root_token and no_token_names:
        token_groups.setdefault(root_token, []).extend(no_token_names)

    return token_groups
