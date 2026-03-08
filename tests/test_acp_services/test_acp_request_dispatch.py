"""Tests for ACPClientBase._handle_request — method alias routing."""

import asyncio
import json
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from soulbot.acp.base_client import ACPClientBase
from soulbot.acp.config import ACPConfig


class StubClient(ACPClientBase):
    """Concrete stub for testing _handle_request."""

    def _get_acp_command(self):
        return ["echo"]

    async def _initialize(self):
        self.session_id = "test-session"


@pytest.fixture
async def client(tmp_path: Path) -> StubClient:
    config = ACPConfig(provider="claude", cwd=str(tmp_path))
    c = StubClient(config)
    # Mock the send methods so we capture responses
    c._send_result = AsyncMock()
    c._send_error = AsyncMock()
    c._connected = True
    yield c
    # Wait for any background terminal subprocesses before loop closes
    for term in c._terminal_service._terminals.values():
        await term["exit_event"].wait()


class TestMethodMap:
    async def test_fs_read(self, client: StubClient, tmp_path: Path):
        (tmp_path / "test.txt").write_text("content here", encoding="utf-8")
        msg = {"id": 1, "method": "fs/read_text_file", "params": {"path": "test.txt"}}
        await client._handle_request(msg)
        client._send_result.assert_called_once()
        result = client._send_result.call_args[0][1]
        assert "content here" in result["content"]

    async def test_fs_read_alias(self, client: StubClient, tmp_path: Path):
        (tmp_path / "test.txt").write_text("hi", encoding="utf-8")
        msg = {"id": 1, "method": "read_text_file", "params": {"path": "test.txt"}}
        await client._handle_request(msg)
        client._send_result.assert_called_once()

    async def test_fs_read_camelcase_alias(self, client: StubClient, tmp_path: Path):
        (tmp_path / "test.txt").write_text("data", encoding="utf-8")
        msg = {"id": 1, "method": "fs/readTextFile", "params": {"path": "test.txt"}}
        await client._handle_request(msg)
        client._send_result.assert_called_once()

    async def test_fs_write(self, client: StubClient, tmp_path: Path):
        msg = {"id": 2, "method": "fs/write_text_file", "params": {"path": "out.txt", "content": "hello"}}
        await client._handle_request(msg)
        client._send_result.assert_called_once()
        assert (tmp_path / "out.txt").read_text(encoding="utf-8") == "hello"

    async def test_fs_stat(self, client: StubClient, tmp_path: Path):
        (tmp_path / "f.txt").write_text("")
        msg = {"id": 3, "method": "fs/stat", "params": {"path": "f.txt"}}
        await client._handle_request(msg)
        result = client._send_result.call_args[0][1]
        assert result["exists"] is True

    async def test_fs_get_file_info_alias(self, client: StubClient, tmp_path: Path):
        (tmp_path / "f.txt").write_text("")
        msg = {"id": 4, "method": "fs/get_file_info", "params": {"path": "f.txt"}}
        await client._handle_request(msg)
        result = client._send_result.call_args[0][1]
        assert result["exists"] is True

    async def test_fs_exists(self, client: StubClient, tmp_path: Path):
        msg = {"id": 5, "method": "fs/exists", "params": {"path": "nope.txt"}}
        await client._handle_request(msg)
        result = client._send_result.call_args[0][1]
        assert result["exists"] is False

    async def test_fs_list_directory(self, client: StubClient, tmp_path: Path):
        (tmp_path / "a.py").write_text("")
        msg = {"id": 6, "method": "fs/list_directory", "params": {"path": "."}}
        await client._handle_request(msg)
        result = client._send_result.call_args[0][1]
        assert "a.py" in result["files"]

    async def test_terminal_create(self, client: StubClient):
        msg = {"id": 7, "method": "terminal/create", "params": {"command": "echo hi"}}
        await client._handle_request(msg)
        result = client._send_result.call_args[0][1]
        assert "terminalId" in result

    async def test_unknown_method_error(self, client: StubClient):
        msg = {"id": 99, "method": "unknown/method", "params": {}}
        await client._handle_request(msg)
        client._send_error.assert_called_once()
        args = client._send_error.call_args[0]
        assert args[1] == -32601
        assert "not supported" in args[2]


class TestPermissionHandling:
    async def test_permission_auto_approve(self, client: StubClient):
        client.config.auto_approve_permissions = True
        msg = {
            "id": 10,
            "method": "session/request_permission",
            "params": {"options": [{"optionId": "opt1"}]},
        }
        await client._handle_request(msg)
        result = client._send_result.call_args[0][1]
        assert result["outcome"]["optionId"] == "opt1"

    async def test_permission_denied(self, client: StubClient):
        client.config.auto_approve_permissions = False
        msg = {
            "id": 11,
            "method": "session/request_permission",
            "params": {"options": [{"optionId": "opt1"}]},
        }
        await client._handle_request(msg)
        client._send_error.assert_called_once()

    async def test_fs_error_returns_error_response(self, client: StubClient):
        """Reading a nonexistent file returns an error response."""
        msg = {"id": 20, "method": "fs/read_text_file", "params": {"path": "missing.txt"}}
        await client._handle_request(msg)
        client._send_error.assert_called_once()
        args = client._send_error.call_args[0]
        assert args[1] == -32603
