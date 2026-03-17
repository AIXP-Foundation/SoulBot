"""Runner — drives agent execution and manages the session lifecycle."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, AsyncGenerator, Optional

from ..agents.base_agent import BaseAgent
from ..agents.invocation_context import InvocationContext, RunConfig
from ..events.event import Content, Event, Part
from ..sessions.base_session_service import BaseSessionService

if TYPE_CHECKING:
    from ..bus.event_bus import EventBus
    from ..commands.executor import CommandExecutor
    from ..history.base_history_service import BaseChatHistoryService

logger = logging.getLogger(__name__)


class Runner:
    """Runs an agent in the context of a session.

    Usage::

        runner = Runner(
            agent=my_agent,
            app_name="my_app",
            session_service=InMemorySessionService(),
        )

        async for event in runner.run(user_id="u1", session_id="s1", message="Hello"):
            print(event)
    """

    def __init__(
        self,
        *,
        agent: BaseAgent,
        app_name: str,
        session_service: BaseSessionService,
        bus: Optional[EventBus] = None,
        cmd_executor: Optional[CommandExecutor] = None,
        history_service: Optional[BaseChatHistoryService] = None,
    ) -> None:
        self.agent = agent
        self.app_name = app_name  # semantic: cli_name (Doc 21)
        self.agent_name = agent.name  # agent soft-classification key (Doc 21)
        self.session_service = session_service
        self.bus = bus
        self._cmd_executor = cmd_executor
        self._history_service = history_service

    async def run(
        self,
        *,
        user_id: str,
        session_id: str,
        message: str,
        run_config: Optional[RunConfig] = None,
    ) -> AsyncGenerator[Event, None]:
        """Run the agent with a user message and yield events.

        Steps:
        1. Get or create the session.
        2. Append the user message as an event.
        3. Record user message to history (Doc 22).
        4. Create an InvocationContext.
        5. Execute the agent and yield events (appending each to the session).
        6. Record assistant response to history (Doc 22).
        """
        # 1. Get or create session
        session = await self.session_service.get_session(
            self.app_name, user_id, session_id
        )
        if session is None:
            # Auto-generate title from first message (Doc 20)
            title = message[:30].strip()
            if len(message) > 30:
                title += "..."
            session = await self.session_service.create_session(
                self.app_name, user_id, agent_name=self.agent_name,
                session_id=session_id, title=title,
            )
        else:
            # Update last_agent if changed (Doc 21 — agent soft classification)
            if session.last_agent != self.agent_name:
                await self.session_service.update_last_agent(
                    self.app_name, user_id, session_id, self.agent_name
                )
                session.last_agent = self.agent_name

        # 1.5 User message length guard — suggest file-based workflow
        max_msg_len = run_config.max_message_length if run_config else None
        if max_msg_len and len(message) > max_msg_len:
            yield Event(
                author="system",
                content=Content(
                    role="model",
                    parts=[Part(text=(
                        f"消息长度 {len(message)} 字符超过建议上限 {max_msg_len}。\n"
                        "建议：将内容保存为文件，然后告诉我文件路径，我会读取后回复。"
                    ))],
                ),
            )
            return

        # 2. Create and append user event
        user_event = Event(
            author="user",
            content=Content(role="user", parts=[Part(text=message)]),
        )
        await self.session_service.append_event(session, user_event)

        # Publish session event
        if self.bus:
            from ..bus.events import BusEvent, SESSION_UPDATED

            await self.bus.publish(BusEvent(
                type=SESSION_UPDATED,
                data={"session_id": session_id, "user_id": user_id},
                source="runner",
            ))

        # 3. Record user message to chat history (Doc 22)
        if self._history_service:
            try:
                await self._history_service.add_message(
                    user_id, self.agent_name, session_id, "user", message,
                )
            except Exception as exc:
                logger.warning("History write failed (user): %s", exc)

        # 4. Create InvocationContext
        ctx = InvocationContext(
            session=session,
            agent=self.agent,
            session_service=self.session_service,
            run_config=run_config or RunConfig(),
            bus=self.bus,
            cmd_executor=self._cmd_executor,
        )

        # 5. Execute agent and yield events
        async for event in self.agent.run_async(ctx):
            event.invocation_id = ctx.invocation_id

            # CMD processing moved to LlmAgent layer (Doc 26)

            # Don't persist partial (streaming) events to session history
            if not event.partial:
                await self.session_service.append_event(session, event)

            # Publish agent response event
            if self.bus and event.is_final_response():
                from ..bus.events import BusEvent, AGENT_RESPONSE

                text = ""
                if event.content:
                    text = " ".join(
                        p.text for p in event.content.parts if p.text
                    )
                await self.bus.publish(BusEvent(
                    type=AGENT_RESPONSE,
                    data={
                        "agent": event.author,
                        "text": text,
                        "session_id": session_id,
                    },
                    source="runner",
                ))

            # 6. Record assistant response to chat history (Doc 22)
            #    Split L1 (human text) / L2 (audit JSON) before saving
            if self._history_service and event.is_final_response():
                final_text = ""
                if event.content:
                    final_text = " ".join(
                        p.text for p in event.content.parts if p.text
                    )
                if final_text:
                    try:
                        from ..l2_splitter import split_l2
                        split = split_l2(final_text)
                        await self._history_service.add_message(
                            user_id, self.agent_name, session_id,
                            "assistant", split.l1, l2_json=split.l2_json,
                        )
                    except Exception as exc:
                        logger.warning("History write failed (assistant): %s", exc)

            yield event
