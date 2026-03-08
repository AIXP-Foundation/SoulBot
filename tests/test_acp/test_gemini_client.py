"""Tests for GeminiACPClient."""

import asyncio
import pytest

from soulbot.acp.config import ACPConfig
from soulbot.acp.gemini_client import GeminiACPClient


class TestGeminiACPClient:
    def test_get_acp_command_with_binary(self):
        config = ACPConfig(provider="gemini", model="gemini-acp/pro")
        client = GeminiACPClient(config)
        from unittest.mock import patch
        with patch("soulbot.acp.gemini_client.find_gemini_binary", return_value="/usr/bin/gemini"):
            cmd = client._get_acp_command()
            assert cmd == ["/usr/bin/gemini", "--experimental-acp", "--model", "pro"]

    def test_get_acp_command_not_found(self):
        config = ACPConfig(provider="gemini", model="gemini-acp/flash")
        client = GeminiACPClient(config)
        from unittest.mock import patch
        with patch("soulbot.acp.gemini_client.find_gemini_binary", return_value=None):
            with pytest.raises(FileNotFoundError, match="Gemini CLI not found"):
                client._get_acp_command()

    def test_get_acp_command_with_model_id(self):
        config = ACPConfig(provider="gemini", model="gemini-acp/gemini-2.5-flash")
        client = GeminiACPClient(config)
        from unittest.mock import patch
        with patch("soulbot.acp.gemini_client.find_gemini_binary", return_value="/usr/bin/gemini"):
            cmd = client._get_acp_command()
            assert "--model" in cmd
            assert "gemini-2.5-flash" in cmd

    def test_initial_state(self):
        config = ACPConfig(provider="gemini")
        client = GeminiACPClient(config)
        assert client.session_id is None
        assert client.config.provider == "gemini"

    async def test_ensure_session_creates_session(self):
        """Mock ensure_session to verify it creates a session when None."""
        config = ACPConfig(provider="gemini")
        client = GeminiACPClient(config)
        client._connected = True
        client.session_id = None

        # Mock _rpc to simulate session/new response
        async def mock_rpc(method, params, timeout=None):
            if method == "session/new":
                return {"sessionId": "gemini-session-1"}
            return {}

        client._rpc = mock_rpc
        sid = await client.ensure_session()
        assert sid == "gemini-session-1"
        assert client.session_id == "gemini-session-1"

    async def test_ensure_session_idempotent(self):
        """If session already exists, ensure_session is a no-op."""
        config = ACPConfig(provider="gemini")
        client = GeminiACPClient(config)
        client.session_id = "existing-session"

        sid = await client.ensure_session()
        assert sid == "existing-session"

    async def test_resume_with_session_load(self):
        """Gemini uses session/load for resume."""
        config = ACPConfig(provider="gemini")
        client = GeminiACPClient(config)
        client._connected = True

        calls = []

        async def mock_rpc(method, params, timeout=None):
            calls.append(method)
            if method == "session/list":
                return {"sessions": [{"id": "target-session"}]}
            if method == "session/load":
                return {}
            return {}

        client._rpc = mock_rpc
        result = await client.resume("target-session")
        assert result is True
        assert client.session_id == "target-session"
        assert "session/list" in calls
        assert "session/load" in calls

    async def test_resume_session_not_found(self):
        """Resume fails if session not in list."""
        config = ACPConfig(provider="gemini")
        client = GeminiACPClient(config)
        client._connected = True

        async def mock_rpc(method, params, timeout=None):
            if method == "session/list":
                return {"sessions": [{"id": "other-session"}]}
            return {}

        client._rpc = mock_rpc
        result = await client.resume("nonexistent-session")
        assert result is False

    async def test_resume_load_failure(self):
        """Resume fails gracefully on session/load error."""
        config = ACPConfig(provider="gemini")
        client = GeminiACPClient(config)
        client._connected = True

        async def mock_rpc(method, params, timeout=None):
            if method == "session/list":
                return {"sessions": [{"id": "target-session"}]}
            if method == "session/load":
                raise Exception("Load failed")
            return {}

        client._rpc = mock_rpc
        result = await client.resume("target-session")
        assert result is False
