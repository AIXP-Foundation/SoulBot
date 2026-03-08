"""CommandExecutor — route and execute parsed commands."""

from __future__ import annotations

import asyncio
import logging
from typing import Any

from .parser import ParsedCommand

logger = logging.getLogger(__name__)


class CommandExecutor:
    """Route commands to registered service objects.

    Services are plain Python objects whose methods serve as actions.
    Both sync and async methods are supported.

    Usage::

        executor = CommandExecutor()
        executor.register_service("math", MathService())
        result = await executor.execute(ParsedCommand(
            service="math", action="add", params={"a": 1, "b": 2}, raw="..."
        ))
    """

    def __init__(self) -> None:
        self._services: dict[str, object] = {}

    def register_service(self, name: str, service: object) -> None:
        """Register a service object. Method names become actions."""
        self._services[name] = service

    def unregister_service(self, name: str) -> bool:
        """Remove a service. Returns True if found."""
        return self._services.pop(name, None) is not None

    @property
    def services(self) -> list[str]:
        """Return registered service names."""
        return list(self._services.keys())

    async def execute(
        self,
        cmd: ParsedCommand,
        context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Execute a single command.

        Returns:
            ``{"success": True, "data": ...}`` or
            ``{"success": False, "error": "..."}``
        """
        service = self._services.get(cmd.service)
        if service is None:
            return {"success": False, "error": f"Unknown service: {cmd.service}"}

        method = getattr(service, cmd.action, None)
        if method is None or not callable(method):
            return {
                "success": False,
                "error": f"Unknown action: {cmd.service}.{cmd.action}",
            }

        # Pop framework-level params before forwarding to service method
        params = dict(cmd.params)
        timeout = params.pop("timeout", None)

        try:
            if asyncio.iscoroutinefunction(method):
                coro = method(**params)
                if timeout:
                    result = await asyncio.wait_for(coro, timeout=timeout)
                else:
                    result = await coro
            else:
                result = method(**params)
            return {"success": True, "data": result}
        except asyncio.TimeoutError:
            logger.warning(
                "Command %s.%s timed out after %ss", cmd.service, cmd.action, timeout
            )
            return {"success": False, "error": f"Timed out after {timeout}s"}
        except Exception as exc:
            logger.warning(
                "Command %s.%s failed: %s", cmd.service, cmd.action, exc
            )
            return {"success": False, "error": str(exc)}

    async def execute_all(
        self,
        commands: list[ParsedCommand],
        context: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """Execute a batch of commands sequentially.

        Applies security rules:
        - Blocks nested scheduling (schedule commands from scheduled context).

        Returns:
            List of result dicts, one per command.
        """
        results: list[dict[str, Any]] = []
        for cmd in commands:
            # Security: block nested scheduling (unless explicitly allowed)
            if (
                context
                and context.get("type") == "scheduled"
                and cmd.service == "schedule"
                and not context.get("allow_nested_schedule", False)
            ):
                results.append({
                    "success": False,
                    "error": "Nested scheduling blocked",
                })
                continue
            # Heartbeat chain preservation: auto-inject origin_channel
            # so LLM doesn't need to remember to include it in SOULBOT_CMD
            if (
                context
                and context.get("origin_channel") == "heartbeat"
                and cmd.service == "schedule"
                and cmd.action == "add"
            ):
                cmd.params.setdefault("origin_channel", "heartbeat")
                cmd.params.setdefault("to_agent", context.get("to_agent", ""))

            result = await self.execute(cmd, context)
            results.append(result)
        return results
