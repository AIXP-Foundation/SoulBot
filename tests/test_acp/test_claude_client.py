"""Tests for ClaudeACPClient."""

import pytest
from unittest.mock import patch, AsyncMock, MagicMock

from soulbot.acp.config import ACPConfig
from soulbot.acp.claude_client import ClaudeACPClient


class TestClaudeACPClient:
    def test_get_acp_command_with_acp_binary(self):
        config = ACPConfig()
        client = ClaudeACPClient(config)
        with patch("soulbot.acp.claude_client.find_claude_binary", return_value="/usr/bin/claude-code-acp"):
            cmd = client._get_acp_command()
            assert cmd == ["/usr/bin/claude-code-acp"]
            assert client._is_acp is True

    def test_get_acp_command_with_claude_binary(self):
        config = ACPConfig()
        client = ClaudeACPClient(config)
        with patch("soulbot.acp.claude_client.find_claude_binary", return_value="/usr/bin/claude"):
            cmd = client._get_acp_command()
            assert cmd == ["/usr/bin/claude", "mcp", "serve"]
            assert client._is_acp is False

    def test_get_acp_command_not_found(self):
        config = ACPConfig()
        client = ClaudeACPClient(config)
        with patch("soulbot.acp.claude_client.find_claude_binary", return_value=None):
            with pytest.raises(FileNotFoundError, match="Claude CLI not found"):
                client._get_acp_command()

    def test_properties(self):
        config = ACPConfig(pool_idle_timeout=60)
        client = ClaudeACPClient(config)
        assert client.is_connected is False
        assert client.session_id is None
        assert config.pool_idle_timeout == 60

    def test_config_stored(self):
        config = ACPConfig(provider="claude", model="claude-acp/opus")
        client = ClaudeACPClient(config)
        assert client.config is config
        assert client.config.model == "claude-acp/opus"
