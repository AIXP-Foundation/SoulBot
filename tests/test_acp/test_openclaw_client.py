"""Tests for OpenClaw ACP client and provider integration."""

import pytest
from unittest.mock import patch

from soulbot.acp.config import (
    ACPConfig,
    FALLBACK_MAP,
    resolve_client_class,
    resolve_provider,
)
from soulbot.acp.openclaw_client import (
    OpenClawACPClient,
    _parse_thinking_level,
    VALID_THINKING_LEVELS,
)
from soulbot.conversation.store import ProviderSessionStore


# ---------------------------------------------------------------------------
# _parse_thinking_level
# ---------------------------------------------------------------------------

class TestParseThinkingLevel:
    def test_three_segments_valid(self):
        assert _parse_thinking_level("openclaw/default/high") == "high"
        assert _parse_thinking_level("openclaw/default/low") == "low"
        assert _parse_thinking_level("openclaw/default/xhigh") == "xhigh"

    def test_three_segments_off(self):
        assert _parse_thinking_level("openclaw/default/off") == "off"

    def test_three_segments_all_valid_levels(self):
        for level in VALID_THINKING_LEVELS:
            result = _parse_thinking_level(f"openclaw/default/{level}")
            assert result == level

    def test_three_segments_invalid(self):
        assert _parse_thinking_level("openclaw/default/detailed") is None
        assert _parse_thinking_level("openclaw/default/invalid") is None
        assert _parse_thinking_level("openclaw/default/extreme") is None

    def test_two_segments_shorthand(self):
        assert _parse_thinking_level("openclaw/high") == "high"
        assert _parse_thinking_level("openclaw/medium") == "medium"

    def test_two_segments_not_a_level(self):
        """When second segment is a model name, not a thinking level."""
        assert _parse_thinking_level("openclaw/default") is None
        assert _parse_thinking_level("openclaw/gpt-4") is None

    def test_one_segment(self):
        assert _parse_thinking_level("openclaw") is None

    def test_case_insensitive(self):
        assert _parse_thinking_level("openclaw/default/HIGH") == "high"
        assert _parse_thinking_level("openclaw/default/Medium") == "medium"
        assert _parse_thinking_level("openclaw/XHIGH") == "xhigh"


# ---------------------------------------------------------------------------
# Provider routing
# ---------------------------------------------------------------------------

class TestProviderRouting:
    def test_openclaw_resolved(self):
        assert resolve_provider("openclaw/default") == "openclaw"
        assert resolve_provider("openclaw/default/high") == "openclaw"

    def test_openclaw_case_insensitive(self):
        assert resolve_provider("OpenClaw/default") == "openclaw"
        assert resolve_provider("OPENCLAW/default/high") == "openclaw"

    def test_no_confusion_with_opencode(self):
        """openclaw and opencode must resolve to different providers."""
        assert resolve_provider("opencode-acp/default") == "opencode"
        assert resolve_provider("openclaw/default") == "openclaw"


class TestResolveClientClass:
    def test_openclaw(self):
        assert resolve_client_class("openclaw") is OpenClawACPClient


class TestFallbackMap:
    def test_openclaw_falls_to_claude(self):
        assert "openclaw" in FALLBACK_MAP
        assert "claude" in FALLBACK_MAP["openclaw"]


# ---------------------------------------------------------------------------
# OpenClawACPClient._get_acp_command
# ---------------------------------------------------------------------------

class TestGetAcpCommand:
    def test_basic_command(self):
        config = ACPConfig(provider="openclaw", model="openclaw/default")
        client = OpenClawACPClient(config)
        with patch("soulbot.acp.openclaw_client.find_openclaw_binary", return_value="/usr/bin/openclaw"):
            cmd = client._get_acp_command()
            assert cmd[:3] == ["/usr/bin/openclaw", "acp", "--no-prefix-cwd"]

    def test_binary_not_found(self):
        config = ACPConfig(provider="openclaw")
        client = OpenClawACPClient(config)
        with patch("soulbot.acp.openclaw_client.find_openclaw_binary", return_value=None):
            with pytest.raises(FileNotFoundError, match="OpenClaw CLI not found"):
                client._get_acp_command()

    def test_with_url(self, monkeypatch):
        monkeypatch.setenv("OPENCLAW_URL", "ws://localhost:3000")
        config = ACPConfig(provider="openclaw")
        client = OpenClawACPClient(config)
        with patch("soulbot.acp.openclaw_client.find_openclaw_binary", return_value="/usr/bin/openclaw"):
            cmd = client._get_acp_command()
            assert "--url" in cmd
            assert "ws://localhost:3000" in cmd

    def test_auth_token_file_priority(self, monkeypatch):
        """token-file takes priority over token, password-file, password."""
        monkeypatch.setenv("OPENCLAW_TOKEN_FILE", "/path/to/token")
        monkeypatch.setenv("OPENCLAW_TOKEN", "direct-token")
        monkeypatch.setenv("OPENCLAW_PASSWORD", "mypass")
        config = ACPConfig(provider="openclaw")
        client = OpenClawACPClient(config)
        with patch("soulbot.acp.openclaw_client.find_openclaw_binary", return_value="/usr/bin/openclaw"):
            cmd = client._get_acp_command()
            assert "--token-file" in cmd
            assert "/path/to/token" in cmd
            assert "--token" not in cmd
            assert "--password" not in cmd

    def test_auth_token(self, monkeypatch):
        monkeypatch.setenv("OPENCLAW_TOKEN", "my-token")
        config = ACPConfig(provider="openclaw")
        client = OpenClawACPClient(config)
        with patch("soulbot.acp.openclaw_client.find_openclaw_binary", return_value="/usr/bin/openclaw"):
            cmd = client._get_acp_command()
            assert "--token" in cmd
            assert "my-token" in cmd

    def test_auth_password_file(self, monkeypatch):
        monkeypatch.setenv("OPENCLAW_PASSWORD_FILE", "/path/to/pass")
        config = ACPConfig(provider="openclaw")
        client = OpenClawACPClient(config)
        with patch("soulbot.acp.openclaw_client.find_openclaw_binary", return_value="/usr/bin/openclaw"):
            cmd = client._get_acp_command()
            assert "--password-file" in cmd
            assert "/path/to/pass" in cmd

    def test_auth_password(self, monkeypatch):
        monkeypatch.setenv("OPENCLAW_PASSWORD", "secret")
        config = ACPConfig(provider="openclaw")
        client = OpenClawACPClient(config)
        with patch("soulbot.acp.openclaw_client.find_openclaw_binary", return_value="/usr/bin/openclaw"):
            cmd = client._get_acp_command()
            assert "--password" in cmd
            assert "secret" in cmd

    def test_session_key(self, monkeypatch):
        monkeypatch.setenv("OPENCLAW_SESSION_KEY", "my-session")
        config = ACPConfig(provider="openclaw")
        client = OpenClawACPClient(config)
        with patch("soulbot.acp.openclaw_client.find_openclaw_binary", return_value="/usr/bin/openclaw"):
            cmd = client._get_acp_command()
            assert "--session" in cmd
            assert "my-session" in cmd

    def test_verbose(self, monkeypatch):
        monkeypatch.setenv("OPENCLAW_VERBOSE", "true")
        config = ACPConfig(provider="openclaw")
        client = OpenClawACPClient(config)
        with patch("soulbot.acp.openclaw_client.find_openclaw_binary", return_value="/usr/bin/openclaw"):
            cmd = client._get_acp_command()
            assert "--verbose" in cmd

    def test_no_require_existing(self):
        """OpenClaw should NOT use --require-existing (breaks session/new)."""
        config = ACPConfig(provider="openclaw")
        client = OpenClawACPClient(config)
        with patch("soulbot.acp.openclaw_client.find_openclaw_binary", return_value="/usr/bin/openclaw"):
            cmd = client._get_acp_command()
            assert "--require-existing" not in cmd


# ---------------------------------------------------------------------------
# Initialize & resume (async, mocked _rpc)
# ---------------------------------------------------------------------------

class TestInitialize:
    async def test_initialize_creates_session(self):
        config = ACPConfig(provider="openclaw", model="openclaw/default")
        client = OpenClawACPClient(config)
        client._connected = True

        calls = []

        async def mock_rpc(method, params, timeout=None):
            calls.append((method, params))
            if method == "session/new":
                return {"sessionId": "oc-session-1"}
            return {}

        client._rpc = mock_rpc
        await client._initialize()
        assert client.session_id == "oc-session-1"
        methods = [c[0] for c in calls]
        assert "initialize" in methods
        assert "session/new" in methods

    async def test_initialize_with_thinking_level(self):
        config = ACPConfig(provider="openclaw", model="openclaw/default/high")
        client = OpenClawACPClient(config)
        client._connected = True

        calls = []

        async def mock_rpc(method, params, timeout=None):
            calls.append((method, params))
            if method == "session/new":
                return {"sessionId": "oc-session-2"}
            return {}

        client._rpc = mock_rpc
        await client._initialize()
        # session/set_mode should be called with modeId
        set_mode_calls = [(m, p) for m, p in calls if m == "session/set_mode"]
        assert len(set_mode_calls) == 1
        assert set_mode_calls[0][1]["modeId"] == "high"

    async def test_initialize_no_thinking_when_off(self):
        config = ACPConfig(provider="openclaw", model="openclaw/default/off")
        client = OpenClawACPClient(config)
        client._connected = True

        calls = []

        async def mock_rpc(method, params, timeout=None):
            calls.append((method, params))
            if method == "session/new":
                return {"sessionId": "oc-session-3"}
            return {}

        client._rpc = mock_rpc
        await client._initialize()
        methods = [c[0] for c in calls]
        assert "session/set_mode" not in methods

    async def test_initialize_no_session_id_raises(self):
        config = ACPConfig(provider="openclaw", model="openclaw/default")
        client = OpenClawACPClient(config)
        client._connected = True

        async def mock_rpc(method, params, timeout=None):
            if method == "session/new":
                return {}  # No sessionId
            return {}

        client._rpc = mock_rpc
        with pytest.raises(ConnectionError, match="sessionId"):
            await client._initialize()


class TestResume:
    async def test_resume_uses_session_load(self):
        """OpenClaw uses session/load (not session/resume like Claude)."""
        config = ACPConfig(provider="openclaw")
        client = OpenClawACPClient(config)
        client._connected = True

        calls = []

        async def mock_rpc(method, params, timeout=None):
            calls.append((method, params))
            return {}

        client._rpc = mock_rpc
        result = await client.resume("target-session")
        assert result is True
        assert client.session_id == "target-session"
        methods = [c[0] for c in calls]
        assert "session/load" in methods
        assert "session/resume" not in methods

    async def test_resume_failure_returns_false(self):
        config = ACPConfig(provider="openclaw")
        client = OpenClawACPClient(config)
        client._connected = True

        async def mock_rpc(method, params, timeout=None):
            if method == "session/load":
                raise Exception("Session not found")
            return {}

        client._rpc = mock_rpc
        result = await client.resume("nonexistent")
        assert result is False


# ---------------------------------------------------------------------------
# ProviderSessionStore includes openclaw
# ---------------------------------------------------------------------------

class TestProviderSessionStore:
    def test_openclaw_in_providers(self):
        assert "openclaw" in ProviderSessionStore.PROVIDERS

    async def test_clear_all_includes_openclaw(self):
        store = ProviderSessionStore()
        await store.set_session_id("user1", "openclaw", "oc-1")
        await store.clear("user1")
        assert await store.get_session_id("user1", "openclaw") is None


# ---------------------------------------------------------------------------
# ModelRegistry resolves openclaw pattern
# ---------------------------------------------------------------------------

class TestModelRegistry:
    def test_openclaw_resolves_to_acp_llm(self):
        from soulbot.models import ModelRegistry, ACPLlm

        llm = ModelRegistry.resolve("openclaw/default/high")
        assert isinstance(llm, ACPLlm)
        assert llm.model == "openclaw/default/high"

    def test_openclaw_shorthand_resolves(self):
        from soulbot.models import ModelRegistry, ACPLlm

        llm = ModelRegistry.resolve("openclaw/default")
        assert isinstance(llm, ACPLlm)


# ---------------------------------------------------------------------------
# ACPLlm.supported_models includes openclaw
# ---------------------------------------------------------------------------

class TestACPLlmSupport:
    def test_openclaw_in_supported_models(self):
        from soulbot.models.acp_llm import ACPLlm

        patterns = ACPLlm.supported_models()
        assert r"openclaw/.*" in patterns


# ---------------------------------------------------------------------------
# _build_prompt skip_tools for OpenClaw
# ---------------------------------------------------------------------------

class TestBuildPromptSkipTools:
    def test_skip_tools_omits_tool_schemas(self):
        from soulbot.models.acp_llm import ACPLlm
        from unittest.mock import MagicMock

        llm_request = MagicMock()
        llm_request.system_instruction = "System prompt"
        llm_request.contents = []
        llm_request.get_tools_schema.return_value = [{"name": "tool1"}]

        prompt_with = ACPLlm._build_prompt(llm_request, skip_tools=False)
        prompt_without = ACPLlm._build_prompt(llm_request, skip_tools=True)

        assert "tool1" in prompt_with
        assert "tool1" not in prompt_without

    def test_default_includes_tools(self):
        from soulbot.models.acp_llm import ACPLlm
        from unittest.mock import MagicMock

        llm_request = MagicMock()
        llm_request.system_instruction = ""
        llm_request.contents = []
        llm_request.get_tools_schema.return_value = [{"name": "my_tool"}]

        prompt = ACPLlm._build_prompt(llm_request)
        assert "my_tool" in prompt
