"""ACP LLM adapter — connect to LLMs via CLI subprocess with connection pooling.

Uses the ACP (Agent Communication Protocol) JSON-RPC over stdio to communicate
with CLI tools (Claude Code, Gemini CLI, OpenCode, Cursor).  This allows using
subscription credentials without needing a separate API key.

Prerequisites (Claude):
    npm install -g @anthropic-ai/claude-code
    claude login

Usage::

    from soulbot.agents import LlmAgent
    agent = LlmAgent(name="my_agent", model="claude-acp/sonnet")
    agent = LlmAgent(name="my_agent", model="gemini-acp/pro")
"""

from __future__ import annotations

import asyncio
import json
import logging
from typing import Any, AsyncGenerator, ClassVar, Optional

from ..acp.config import ACPConfig, FALLBACK_MAP, resolve_client_class, resolve_provider
from ..acp.pool import ACPConnectionPool
from .base_llm import BaseLlm
from .llm_request import LlmRequest, LlmResponse

logger = logging.getLogger(__name__)

# Auth error keywords → re-login commands per provider
_AUTH_KEYWORDS = ("authentication required", "unauthorized", "not authenticated", "auth", "expired")
_RELOGIN_COMMANDS = {
    "claude": "claude login",
    "gemini": "gemini auth",
    "opencode": "opencode auth login",
    "openclaw": "openclaw login",
    "cursor": "cursor login",
}


def _enrich_auth_error(error_msg: str, model: str) -> str:
    """Append a re-login hint if the error looks like an auth failure."""
    lower = error_msg.lower()
    if not any(kw in lower for kw in _AUTH_KEYWORDS):
        return error_msg
    # Determine provider from model string (e.g. "claude-acp/sonnet" → "claude")
    provider = model.split("-")[0] if model else "claude"
    cmd = _RELOGIN_COMMANDS.get(provider, "claude login")
    return f"{error_msg}  [Hint: authentication may have expired. Run `{cmd}` to re-authenticate]"


def _extract_function_call(text: str) -> dict | None:
    """Extract a ``{"function_call": ...}`` JSON object from *text*.

    Uses a find-then-parse strategy: locate ``"function_call"`` in the text,
    walk back to the enclosing ``{``, then try ``json.loads`` on progressively
    longer substrings until a valid JSON object is found.  This handles
    nested braces and multi-line formatting correctly.
    """
    marker = '"function_call"'
    idx = text.find(marker)
    if idx == -1:
        return None

    # Walk backward to find the opening brace
    start = text.rfind("{", 0, idx)
    if start == -1:
        return None

    # Try parsing from start, extending end position via brace counting
    depth = 0
    for i in range(start, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                try:
                    obj = json.loads(text[start:i + 1])
                    if "function_call" in obj and "name" in obj["function_call"]:
                        return obj
                except (json.JSONDecodeError, TypeError):
                    pass
                return None
    return None


class ACPLlm(BaseLlm):
    """Adapter for LLMs via ACP CLI subprocesses with connection pooling.

    Supports multiple providers:
    - Claude (claude-acp/*) — via claude-code-acp CLI
    - Gemini (gemini-acp/*) — via gemini CLI
    - OpenCode (opencode-acp/*) — via opencode CLI
    - OpenClaw (openclaw/*) — via openclaw CLI (gateway-backed)
    - Cursor (cursor-cli/*) — via cursor-agent CLI (non-pooled)
    """

    _pools: ClassVar[dict[str, ACPConnectionPool]] = {}
    _provider_session_store: ClassVar[Optional[Any]] = None

    @classmethod
    def set_provider_session_store(cls, store: Any) -> None:
        """Inject a ProviderSessionStore for ACP session reuse (Doc 19)."""
        cls._provider_session_store = store

    @classmethod
    def supported_models(cls) -> list[str]:
        return [
            r"claude-acp/.*",
            r"gemini-acp/.*",
            r"opencode-acp/.*",
            r"openclaw/.*",
            r"cursor-cli/.*",
        ]

    async def generate_content_async(
        self, llm_request: LlmRequest, *, stream: bool = False
    ) -> AsyncGenerator[LlmResponse, None]:
        from ..events.event import Content, Part

        provider = resolve_provider(self.model)
        skip_tools = provider == "openclaw"
        prompt = self._build_prompt(llm_request, skip_tools=skip_tools)
        pool = self._get_pool()

        # --- ProviderSessionStore lookup (Doc 19) ---
        session_id: str | None = None
        user_id = llm_request.metadata.get("user_id")
        store = self._provider_session_store
        if store and user_id:
            try:
                session_id = await store.get_session_id(user_id, provider)
            except Exception:
                pass

        # Doc 10 A2: use config retries + catch TimeoutError + exponential backoff
        max_attempts = pool._config.max_retries
        base_delay = pool._config.retry_base_delay
        primary_err: Exception | None = None

        session_rotated = False  # Track whether we already rotated

        for attempt in range(1, max_attempts + 1):
            try:
                async with pool.acquire(session_id=session_id) as (client, sid):
                    # Detect session change (Doc 10 C3)
                    if session_id and sid != session_id:
                        logger.info("ACP session changed: %s -> %s (resume failed)", session_id, sid)

                    # Save actual session_id back (Doc 19)
                    if store and user_id and sid:
                        try:
                            await store.set_session_id(user_id, provider, sid)
                        except Exception:
                            pass

                    if stream:
                        full_text = ""
                        async for chunk in client.query_stream(prompt):
                            full_text += chunk
                            yield LlmResponse(
                                content=Content(role="model", parts=[Part(text=chunk)]),
                                partial=True,
                            )
                        # Parse final accumulated text for function_call (Doc 25)
                        final = self._parse_response(full_text)
                        final.partial = False
                        yield final
                    else:
                        text = await client.query(prompt)
                        yield self._parse_response(text)
                return  # success — exit
            except (ConnectionError, asyncio.TimeoutError) as ce:
                if attempt < max_attempts:
                    delay = min(base_delay * (2 ** (attempt - 1)), 30.0)
                    logger.warning(
                        "ACP error (attempt %d/%d), retrying in %.1fs: %s",
                        attempt, max_attempts, delay, ce,
                    )
                    # Clear stale session so next acquire creates fresh connection
                    session_id = None
                    # Doc 10 B3: clear store on disconnect
                    if store and user_id:
                        try:
                            await store.clear(user_id, provider)
                        except Exception:
                            pass
                    await asyncio.sleep(delay)
                    continue
                # Last attempt — fall through to fallback/error handling
                primary_err = ce
                break
            except Exception as exc:
                # --- Session rotation on "Prompt is too long" ---
                # CLI session memory is full. Discard the old session and
                # retry once with a fresh session (new conversation).
                # No history injection needed — [MEMORY] hint in sys prompt
                # tells the agent to use search_history when it needs context.
                if not session_rotated and "prompt is too long" in str(exc).lower():
                    logger.warning(
                        "CLI session context overflow (session=%s). "
                        "Rotating to fresh session.",
                        session_id,
                    )
                    session_rotated = True
                    session_id = None
                    if store and user_id:
                        try:
                            await store.clear(user_id, provider)
                        except Exception:
                            pass
                    continue  # retry with fresh session, same prompt
                primary_err = exc
                break

        # Attempt fallback if enabled
        config = self._get_config()
        fallback_model = FALLBACK_MAP.get(config.provider)
        if config.enable_fallback and fallback_model:
            logger.warning(
                "Primary %s failed (%s), falling back to %s",
                config.provider, primary_err, fallback_model,
            )
            try:
                async for resp in self._query_fallback(
                    prompt, fallback_model, stream
                ):
                    yield resp
                return
            except Exception as fallback_err:
                logger.error("Fallback also failed: %s", fallback_err)

        error_msg = str(primary_err)
        error_msg = _enrich_auth_error(error_msg, self.model)
        logger.error("ACP error: %s", error_msg)
        yield LlmResponse(error_code="ACP_ERROR", error_message=error_msg)

    # ------------------------------------------------------------------
    # Fallback
    # ------------------------------------------------------------------

    async def _query_fallback(
        self, prompt: str, fallback_model: str, stream: bool
    ) -> AsyncGenerator[LlmResponse, None]:
        """Execute a query using a fallback model."""
        from ..events.event import Content, Part

        provider = resolve_provider(fallback_model)
        pool = self._get_pool_for(provider, fallback_model)

        async with pool.acquire() as (client, sid):
            if stream:
                full_text = ""
                async for chunk in client.query_stream(prompt):
                    full_text += chunk
                    yield LlmResponse(
                        content=Content(role="model", parts=[Part(text=chunk)]),
                        partial=True,
                    )
                final = self._parse_response(full_text)
                final.partial = False
                yield final
            else:
                text = await client.query(prompt)
                yield self._parse_response(text)

    # ------------------------------------------------------------------
    # Pool management
    # ------------------------------------------------------------------

    def _get_pool(self) -> ACPConnectionPool:
        """Get or create a connection pool for the current provider."""
        provider = resolve_provider(self.model)
        return self._get_pool_for(provider, self.model)

    def _get_config(self) -> ACPConfig:
        """Get config for the current model."""
        provider = resolve_provider(self.model)
        return ACPConfig.from_env(provider=provider, model=self.model)

    @classmethod
    def _get_pool_for(cls, provider: str, model: str) -> ACPConnectionPool:
        """Get or create a pool for a specific provider+model (Doc 10 C5)."""
        pool_key = f"{provider}:{model}"
        if pool_key not in cls._pools:
            config = ACPConfig.from_env(provider=provider, model=model)
            client_class = resolve_client_class(provider)
            pool = ACPConnectionPool(config, client_class)
            pool.start_keepalive()
            cls._pools[pool_key] = pool
        return cls._pools[pool_key]

    @classmethod
    async def close_all_pools(cls) -> None:
        """Close all connection pools. Call on shutdown."""
        for pool in cls._pools.values():
            await pool.close_all()
        cls._pools.clear()

    # ------------------------------------------------------------------
    # Prompt building
    # ------------------------------------------------------------------

    @staticmethod
    def _build_prompt(llm_request: LlmRequest, *, skip_tools: bool = False) -> str:
        """Convert LlmRequest to a plain text prompt for ACP.

        Args:
            llm_request: The request to convert.
            skip_tools: If True, omit tool schemas from the prompt.
                OpenClaw has its own tools via Gateway, so injecting
                SoulBot tool schemas would cause conflicts.
        """
        parts: list[str] = []

        # System instruction
        if llm_request.system_instruction:
            parts.append(llm_request.system_instruction)

        # Tool schemas (embed as instructions)
        tools_schema = llm_request.get_tools_schema() if not skip_tools else None
        if tools_schema:
            tool_desc = json.dumps(tools_schema, ensure_ascii=False, indent=2)
            parts.append(
                "You have access to the following tools. "
                "When you need to call a tool, respond with EXACTLY this JSON format "
                "on a single line:\n"
                '{"function_call": {"name": "tool_name", "arguments": {...}}}\n\n'
                f"Available tools:\n{tool_desc}"
            )

        # Conversation contents
        for content in llm_request.contents:
            role = content.role
            for part in content.parts:
                if part.text:
                    if role == "user":
                        parts.append(f"User: {part.text}")
                    else:
                        parts.append(f"Assistant: {part.text}")
                if part.function_call:
                    parts.append(
                        f'Assistant called tool: {part.function_call.name}'
                        f'({json.dumps(part.function_call.args)})'
                    )
                if part.function_response:
                    parts.append(
                        f'Tool result ({part.function_response.name}): '
                        f'{json.dumps(part.function_response.response)}'
                    )

        return "\n\n".join(parts)

    # ------------------------------------------------------------------
    # Response parsing (Doc 25 — extract function_call from text)
    # ------------------------------------------------------------------

    @staticmethod
    def _parse_response(text: str) -> LlmResponse:
        """Parse LLM text response, extracting function_call JSON if present.

        If the text contains a ``{"function_call": {"name": ..., "arguments": ...}}``
        JSON object, it is extracted and returned as a ``Part(function_call=...)``.
        Otherwise the full text is returned as ``Part(text=...)``.
        """
        from ..events.event import Content, FunctionCall, Part

        parsed = _extract_function_call(text)
        if parsed:
            fc_data = parsed["function_call"]
            fc = FunctionCall(
                name=fc_data["name"],
                args=fc_data.get("arguments", {}),
            )
            return LlmResponse(
                content=Content(role="model", parts=[Part(function_call=fc)])
            )

        return LlmResponse(
            content=Content(role="model", parts=[Part(text=text)])
        )
