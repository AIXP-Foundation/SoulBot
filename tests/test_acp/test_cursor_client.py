"""Tests for CursorCLIClient."""

import asyncio
import json
import os
import pytest
from unittest.mock import patch, MagicMock, AsyncMock

from soulbot.acp.config import ACPConfig
from soulbot.acp.cursor_client import CursorCLIClient, _PROMPT_FILE_THRESHOLD


class TestCursorCLIClient:
    def test_initial_state(self):
        config = ACPConfig(provider="cursor", model="cursor-cli/gpt-4")
        client = CursorCLIClient(config)
        assert client.is_connected is True  # Always "connected"
        assert client.is_idle_timeout is False
        assert client.session_id is None

    async def test_connect_with_binary(self):
        config = ACPConfig(provider="cursor")
        client = CursorCLIClient(config)
        with patch("soulbot.acp.cursor_client.find_cursor_binary", return_value="/usr/bin/cursor-agent"):
            await client.connect()
            assert client._binary == "/usr/bin/cursor-agent"

    async def test_connect_not_found(self):
        config = ACPConfig(provider="cursor")
        client = CursorCLIClient(config)
        with patch("soulbot.acp.cursor_client.find_cursor_binary", return_value=None):
            with pytest.raises(FileNotFoundError, match="Cursor CLI not found"):
                await client.connect()

    async def test_disconnect_is_noop(self):
        config = ACPConfig(provider="cursor")
        client = CursorCLIClient(config)
        # Should not raise
        await client.disconnect()

    async def test_resume_always_true(self):
        config = ACPConfig(provider="cursor")
        client = CursorCLIClient(config)
        result = await client.resume("any-session")
        assert result is True

    async def test_query_short_prompt(self):
        config = ACPConfig(provider="cursor", model="cursor-cli/gpt-4")
        client = CursorCLIClient(config)
        client._binary = "/usr/bin/cursor-agent"

        mock_result = MagicMock()
        mock_result.stdout = "Hello response"
        mock_result.stderr = ""
        mock_result.returncode = 0

        with patch("asyncio.to_thread", return_value=mock_result) as mock_thread:
            result = await client.query("short prompt")
            assert result == "Hello response"
            # Verify subprocess.run was called with correct args
            call_args = mock_thread.call_args
            cmd = call_args[0][1]
            assert "/usr/bin/cursor-agent" in cmd
            assert "-p" in cmd
            assert "--model" in cmd
            assert "gpt-4" in cmd
            assert "short prompt" in cmd

    async def test_query_long_prompt_uses_temp_file(self):
        config = ACPConfig(provider="cursor", model="cursor-cli/gpt-4")
        client = CursorCLIClient(config)
        client._binary = "/usr/bin/cursor-agent"

        long_prompt = "x" * (_PROMPT_FILE_THRESHOLD + 100)

        mock_result = MagicMock()
        mock_result.stdout = "Long response"
        mock_result.stderr = ""
        mock_result.returncode = 0

        temp_files_created = []

        original_named_temp = __builtins__  # just for tracking
        with patch("asyncio.to_thread", return_value=mock_result) as mock_thread:
            result = await client.query(long_prompt)
            assert result == "Long response"
            # Verify -f flag was used
            call_args = mock_thread.call_args
            cmd = call_args[0][1]
            assert "-f" in cmd

    async def test_query_with_session_id(self):
        config = ACPConfig(provider="cursor", model="cursor-cli/gpt-4")
        client = CursorCLIClient(config)
        client._binary = "/usr/bin/cursor-agent"

        mock_result = MagicMock()
        mock_result.stdout = "Resumed response"
        mock_result.stderr = ""
        mock_result.returncode = 0

        with patch("asyncio.to_thread", return_value=mock_result) as mock_thread:
            result = await client.query("test", session_id="chat-123")
            assert result == "Resumed response"
            call_args = mock_thread.call_args
            cmd = call_args[0][1]
            assert "--resume" in cmd
            assert "chat-123" in cmd

    def test_prompt_threshold_value(self):
        assert _PROMPT_FILE_THRESHOLD == 500

    def test_model_id_extraction(self):
        config = ACPConfig(provider="cursor", model="cursor-cli/claude-3.5-sonnet")
        model_id = config.model.replace("cursor-cli/", "")
        assert model_id == "claude-3.5-sonnet"
