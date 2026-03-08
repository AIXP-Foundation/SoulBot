"""Tests for OpenCodeACPClient."""

import json
import sys
import pytest
from unittest.mock import patch, MagicMock

from soulbot.acp.config import ACPConfig
from soulbot.acp.opencode_client import OpenCodeACPClient


class TestOpenCodeACPClient:
    def test_get_acp_command_with_binary(self):
        config = ACPConfig(provider="opencode", model="opencode-acp/default")
        client = OpenCodeACPClient(config)
        with patch("soulbot.acp.opencode_client.find_opencode_binary", return_value="/usr/bin/opencode"):
            cmd = client._get_acp_command()
            assert cmd == ["/usr/bin/opencode", "acp"]

    def test_get_acp_command_not_found(self):
        config = ACPConfig(provider="opencode")
        client = OpenCodeACPClient(config)
        with patch("soulbot.acp.opencode_client.find_opencode_binary", return_value=None):
            with pytest.raises(FileNotFoundError, match="OpenCode CLI not found"):
                client._get_acp_command()

    def test_initial_state(self):
        config = ACPConfig(provider="opencode")
        client = OpenCodeACPClient(config)
        assert client._popen is None
        assert client._reader_thread is None
        assert client._loop is None
        assert client.is_connected is False

    def test_is_connected_with_popen(self):
        config = ACPConfig(provider="opencode")
        client = OpenCodeACPClient(config)
        client._connected = True
        mock_popen = MagicMock()
        mock_popen.poll.return_value = None  # Still running
        client._popen = mock_popen
        assert client.is_connected is True

    def test_is_connected_popen_terminated(self):
        config = ACPConfig(provider="opencode")
        client = OpenCodeACPClient(config)
        client._connected = True
        mock_popen = MagicMock()
        mock_popen.poll.return_value = 1  # Terminated
        client._popen = mock_popen
        assert client.is_connected is False

    def test_sync_write_unix(self):
        config = ACPConfig(provider="opencode")
        client = OpenCodeACPClient(config)
        mock_popen = MagicMock()
        mock_stdin = MagicMock()
        mock_popen.stdin = mock_stdin
        client._popen = mock_popen

        with patch("sys.platform", "linux"):
            client._sync_write(b'test data')
            mock_stdin.write.assert_called_once_with(b'test data')
            mock_stdin.flush.assert_called_once()

    @pytest.mark.skipif(sys.platform != "win32", reason="Windows-specific test")
    def test_sync_write_windows(self):
        config = ACPConfig(provider="opencode")
        client = OpenCodeACPClient(config)
        mock_popen = MagicMock()
        mock_stdin = MagicMock()
        mock_stdin.fileno.return_value = 42
        mock_popen.stdin = mock_stdin
        client._popen = mock_popen

        with patch("os.write") as mock_write:
            client._sync_write(b'test data')
            mock_write.assert_called_once_with(42, b'test data')

    def test_config_model_extraction(self):
        config = ACPConfig(provider="opencode", model="opencode-acp/kimi-k2.5-free")
        client = OpenCodeACPClient(config)
        model_id = config.model.replace("opencode-acp/", "")
        assert model_id == "kimi-k2.5-free"

    async def test_disconnect_with_popen(self):
        config = ACPConfig(provider="opencode")
        client = OpenCodeACPClient(config)
        mock_popen = MagicMock()
        mock_popen.terminate = MagicMock()
        mock_popen.wait = MagicMock()
        client._popen = mock_popen
        client._connected = True

        await client.disconnect()
        assert client._connected is False
        assert client._popen is None
        mock_popen.terminate.assert_called_once()

    async def test_disconnect_no_popen(self):
        config = ACPConfig(provider="opencode")
        client = OpenCodeACPClient(config)
        # Should not raise
        await client.disconnect()
