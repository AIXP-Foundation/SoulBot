"""Tests for rewritten ACPLlm adapter with connection pool."""

import asyncio
import time
import pytest

from soulbot.acp.config import ACPConfig
from soulbot.acp.base_client import ACPClientBase
from soulbot.acp.pool import ACPConnectionPool
from soulbot.models.acp_llm import ACPLlm
from soulbot.models.llm_request import LlmRequest, LlmResponse
from soulbot.events.event import Content, Part


# ---------------------------------------------------------------------------
# Mock client for testing ACPLlm without real subprocess
# ---------------------------------------------------------------------------

class MockPoolClient(ACPClientBase):
    """Mock client that returns canned responses."""

    _instance_count = 0

    def __init__(self, config: ACPConfig) -> None:
        super().__init__(config)
        self.response_text = "Mock LLM response"

    @property
    def is_connected(self) -> bool:
        return self._connected

    def _get_acp_command(self) -> list[str]:
        return ["mock"]

    async def _initialize(self) -> None:
        MockPoolClient._instance_count += 1
        self.session_id = f"mock-{MockPoolClient._instance_count}"

    async def connect(self) -> None:
        self._connected = True
        self._last_used = time.time()
        await self._initialize()

    async def disconnect(self) -> None:
        self._connected = False

    async def ping(self) -> bool:
        return self._connected

    async def query(self, prompt: str) -> str:
        self._last_used = time.time()
        return self.response_text

    async def query_stream(self, prompt):
        self._last_used = time.time()
        for word in self.response_text.split():
            yield word + " "


@pytest.fixture(autouse=True)
def reset_pools():
    """Reset ACPLlm pool cache before each test."""
    ACPLlm._pools.clear()
    MockPoolClient._instance_count = 0
    yield
    ACPLlm._pools.clear()


class TestACPLlm:
    def test_supported_models(self):
        models = ACPLlm.supported_models()
        assert r"claude-acp/.*" in models
        assert r"gemini-acp/.*" in models
        assert r"opencode-acp/.*" in models
        assert r"cursor-cli/.*" in models

    def test_resolve_provider(self):
        from soulbot.acp.config import resolve_provider
        assert resolve_provider("claude-acp/sonnet") == "claude"
        assert resolve_provider("gemini-acp/pro") == "gemini"
        assert resolve_provider("opencode-acp/default") == "opencode"
        assert resolve_provider("cursor-cli/gpt-4") == "cursor"
        assert resolve_provider("unknown-model") == "claude"  # default

    def test_build_prompt_simple(self):
        request = LlmRequest(
            contents=[Content(role="user", parts=[Part(text="Hello")])],
        )
        prompt = ACPLlm._build_prompt(request)
        assert "User: Hello" in prompt

    def test_build_prompt_with_system(self):
        request = LlmRequest(
            system_instruction="You are helpful.",
            contents=[Content(role="user", parts=[Part(text="Hi")])],
        )
        prompt = ACPLlm._build_prompt(request)
        assert "You are helpful." in prompt
        assert "User: Hi" in prompt

    def test_build_prompt_with_assistant(self):
        request = LlmRequest(
            contents=[
                Content(role="user", parts=[Part(text="Hello")]),
                Content(role="model", parts=[Part(text="Hi there!")]),
                Content(role="user", parts=[Part(text="How are you?")]),
            ],
        )
        prompt = ACPLlm._build_prompt(request)
        assert "User: Hello" in prompt
        assert "Assistant: Hi there!" in prompt
        assert "User: How are you?" in prompt

    async def test_generate_content_with_mock_pool(self):
        """Test generate_content_async using a mock pool."""
        config = ACPConfig(provider="claude", model="claude-acp/sonnet")
        pool = ACPConnectionPool(config, MockPoolClient)
        llm = ACPLlm(model="claude-acp/sonnet")
        ACPLlm._pools["claude:claude-acp/sonnet"] = pool

        request = LlmRequest(
            contents=[Content(role="user", parts=[Part(text="Hello")])],
        )

        responses = []
        async for resp in llm.generate_content_async(request):
            responses.append(resp)

        assert len(responses) == 1
        assert responses[0].content is not None
        assert responses[0].content.parts[0].text == "Mock LLM response"

    async def test_generate_content_stream_with_mock_pool(self):
        """Test streaming mode."""
        config = ACPConfig(provider="claude", model="claude-acp/sonnet")
        pool = ACPConnectionPool(config, MockPoolClient)
        llm = ACPLlm(model="claude-acp/sonnet")
        ACPLlm._pools["claude:claude-acp/sonnet"] = pool

        request = LlmRequest(
            contents=[Content(role="user", parts=[Part(text="Hello")])],
        )

        responses = []
        async for resp in llm.generate_content_async(request, stream=True):
            responses.append(resp)

        # Should have partial chunks + final
        assert len(responses) >= 2
        assert responses[-1].partial is False
        # At least one partial chunk
        partials = [r for r in responses if r.partial]
        assert len(partials) >= 1

    async def test_close_all_pools(self):
        config = ACPConfig(provider="claude", model="claude-acp/sonnet")
        pool = ACPConnectionPool(config, MockPoolClient)
        ACPLlm._pools["claude:claude-acp/sonnet"] = pool

        # Create a connection in pool
        async with pool.acquire() as (c, _):
            pass
        assert pool.size == 1

        await ACPLlm.close_all_pools()
        assert len(ACPLlm._pools) == 0

    def test_provider_session_store_default_none(self):
        """ProviderSessionStore defaults to None (Doc 19)."""
        assert ACPLlm._provider_session_store is None

    def test_set_provider_session_store(self):
        """set_provider_session_store sets the class attribute (Doc 19)."""
        mock_store = object()
        ACPLlm.set_provider_session_store(mock_store)
        assert ACPLlm._provider_session_store is mock_store
        # Reset
        ACPLlm.set_provider_session_store(None)

    async def test_reconnect_on_disconnect(self):
        """On ConnectionError, should reconnect and retry once."""
        call_count = 0

        class DisconnectOnceClient(MockPoolClient):
            async def query(self, prompt: str) -> str:
                nonlocal call_count
                call_count += 1
                if call_count == 1:
                    self._connected = False
                    raise ConnectionError("ACP disconnected")
                return "Recovered response"

        config = ACPConfig(provider="claude", model="claude-acp/sonnet")
        pool = ACPConnectionPool(config, DisconnectOnceClient)
        llm = ACPLlm(model="claude-acp/sonnet")
        ACPLlm._pools["claude:claude-acp/sonnet"] = pool

        request = LlmRequest(
            contents=[Content(role="user", parts=[Part(text="Hello")])],
        )

        responses = []
        async for resp in llm.generate_content_async(request):
            responses.append(resp)

        # Should have retried and succeeded
        assert call_count == 2
        assert len(responses) == 1
        assert responses[0].content.parts[0].text == "Recovered response"

    async def test_reconnect_on_stream_disconnect(self):
        """On ConnectionError during streaming, should reconnect and retry."""
        call_count = 0

        class DisconnectStreamClient(MockPoolClient):
            async def query_stream(self, prompt):
                nonlocal call_count
                call_count += 1
                if call_count == 1:
                    self._connected = False
                    raise ConnectionError("ACP disconnected")
                for word in "OK now".split():
                    yield word + " "

        config = ACPConfig(provider="claude", model="claude-acp/sonnet")
        pool = ACPConnectionPool(config, DisconnectStreamClient)
        llm = ACPLlm(model="claude-acp/sonnet")
        ACPLlm._pools["claude:claude-acp/sonnet"] = pool

        request = LlmRequest(
            contents=[Content(role="user", parts=[Part(text="Hello")])],
        )

        responses = []
        async for resp in llm.generate_content_async(request, stream=True):
            responses.append(resp)

        assert call_count == 2
        # Should have partial chunks + final from retry
        assert len(responses) >= 2
        assert responses[-1].partial is False

    async def test_disconnect_twice_falls_through(self):
        """If both attempts disconnect, should yield ACP_ERROR."""

        class AlwaysDisconnectClient(MockPoolClient):
            async def query(self, prompt: str) -> str:
                self._connected = False
                raise ConnectionError("ACP disconnected")

        config = ACPConfig(provider="claude", model="claude-acp/sonnet")
        pool = ACPConnectionPool(config, AlwaysDisconnectClient)
        llm = ACPLlm(model="claude-acp/sonnet")
        ACPLlm._pools["claude:claude-acp/sonnet"] = pool

        request = LlmRequest(
            contents=[Content(role="user", parts=[Part(text="Hello")])],
        )

        responses = []
        async for resp in llm.generate_content_async(request):
            responses.append(resp)

        assert len(responses) == 1
        assert responses[0].error_code == "ACP_ERROR"
        assert "disconnected" in responses[0].error_message.lower()

    async def test_session_rotation_on_prompt_too_long(self):
        """'Prompt is too long' triggers session rotation and retry."""
        call_count = 0

        class PromptTooLongClient(MockPoolClient):
            async def query(self, prompt: str) -> str:
                nonlocal call_count
                call_count += 1
                if call_count == 1:
                    raise Exception("Internal error: Prompt is too long")
                return "Fresh session response"

        config = ACPConfig(provider="claude", model="claude-acp/sonnet")
        pool = ACPConnectionPool(config, PromptTooLongClient)
        llm = ACPLlm(model="claude-acp/sonnet")
        ACPLlm._pools["claude:claude-acp/sonnet"] = pool

        request = LlmRequest(
            contents=[Content(role="user", parts=[Part(text="Hello")])],
        )

        responses = []
        async for resp in llm.generate_content_async(request):
            responses.append(resp)

        # Should have retried with a fresh session
        assert call_count == 2
        assert len(responses) == 1
        assert responses[0].content.parts[0].text == "Fresh session response"

    async def test_session_rotation_clears_store(self):
        """Session rotation clears ProviderSessionStore for the user."""
        from soulbot.conversation.store import ProviderSessionStore

        store = ProviderSessionStore()
        await store.set_session_id("user1", "claude", "old-session-abc")
        ACPLlm.set_provider_session_store(store)

        call_count = 0

        class PromptTooLongClient(MockPoolClient):
            async def query(self, prompt: str) -> str:
                nonlocal call_count
                call_count += 1
                if call_count == 1:
                    raise Exception("Internal error: Prompt is too long")
                return "OK after rotation"

        config = ACPConfig(provider="claude", model="claude-acp/sonnet")
        pool = ACPConnectionPool(config, PromptTooLongClient)
        llm = ACPLlm(model="claude-acp/sonnet")
        ACPLlm._pools["claude:claude-acp/sonnet"] = pool

        request = LlmRequest(
            contents=[Content(role="user", parts=[Part(text="Hello")])],
            metadata={"user_id": "user1"},
        )

        responses = []
        async for resp in llm.generate_content_async(request):
            responses.append(resp)

        # Store should be cleared (old session discarded)
        stored_sid = await store.get_session_id("user1", "claude")
        # After rotation, a NEW session_id should be stored (not old-session-abc)
        assert stored_sid != "old-session-abc"
        assert call_count == 2
        assert responses[0].content.parts[0].text == "OK after rotation"

        # Cleanup
        ACPLlm.set_provider_session_store(None)

    async def test_session_rotation_only_once(self):
        """Session rotation only happens once — persistent error falls through."""

        class AlwaysPromptTooLong(MockPoolClient):
            async def query(self, prompt: str) -> str:
                raise Exception("Internal error: Prompt is too long")

        config = ACPConfig(provider="claude", model="claude-acp/sonnet")
        pool = ACPConnectionPool(config, AlwaysPromptTooLong)
        llm = ACPLlm(model="claude-acp/sonnet")
        ACPLlm._pools["claude:claude-acp/sonnet"] = pool

        request = LlmRequest(
            contents=[Content(role="user", parts=[Part(text="Hello")])],
        )

        responses = []
        async for resp in llm.generate_content_async(request):
            responses.append(resp)

        # Should fall through to error after rotation fails
        assert len(responses) == 1
        assert responses[0].error_code == "ACP_ERROR"

    async def test_rotation_uses_original_prompt(self):
        """After rotation, same prompt is sent to fresh session (no history injection)."""
        captured_prompts: list[str] = []

        class CapturePromptClient(MockPoolClient):
            async def query(self, prompt: str) -> str:
                captured_prompts.append(prompt)
                if len(captured_prompts) == 1:
                    raise Exception("Internal error: Prompt is too long")
                return "OK fresh session"

        config = ACPConfig(provider="claude", model="claude-acp/sonnet")
        pool = ACPConnectionPool(config, CapturePromptClient)
        llm = ACPLlm(model="claude-acp/sonnet")
        ACPLlm._pools["claude:claude-acp/sonnet"] = pool

        request = LlmRequest(
            system_instruction="You are helpful.",
            contents=[Content(role="user", parts=[Part(text="latest msg")])],
        )

        responses = []
        async for resp in llm.generate_content_async(request):
            responses.append(resp)

        assert len(captured_prompts) == 2

        # Both prompts should be identical — no history injection
        assert captured_prompts[0] == captured_prompts[1]
        assert "latest msg" in captured_prompts[1]
        assert responses[0].content.parts[0].text == "OK fresh session"
