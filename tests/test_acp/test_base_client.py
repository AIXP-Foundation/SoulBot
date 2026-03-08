"""Tests for ACPClientBase."""

import asyncio
import json
import time
import pytest

from soulbot.acp.config import ACPConfig
from soulbot.acp.base_client import ACPClientBase


class ConcreteClient(ACPClientBase):
    """Concrete implementation for testing base class methods."""

    def _get_acp_command(self) -> list[str]:
        return ["mock-cli"]

    async def _initialize(self) -> None:
        self.session_id = "test-session-1"


class TestACPClientBase:
    def test_initial_state(self):
        config = ACPConfig()
        client = ConcreteClient(config)
        assert client.is_connected is False
        assert client.session_id is None
        assert client._msg_id == 0
        assert client._pending == {}
        assert client._chunks == []
        assert client._streaming is False

    def test_is_idle_timeout(self):
        config = ACPConfig(pool_idle_timeout=1)
        client = ConcreteClient(config)
        client._last_used = time.time() - 2  # 2 seconds ago
        assert client.is_idle_timeout is True

    def test_not_idle_timeout(self):
        config = ACPConfig(pool_idle_timeout=3600)
        client = ConcreteClient(config)
        client._last_used = time.time()
        assert client.is_idle_timeout is False

    def test_parse_json_clean(self):
        msg = '{"jsonrpc": "2.0", "id": 1, "result": {}}'
        result = ACPClientBase._parse_json(msg)
        assert result == {"jsonrpc": "2.0", "id": 1, "result": {}}

    def test_parse_json_with_prefix(self):
        msg = 'some prefix {"id": 1, "method": "test"} trailing'
        result = ACPClientBase._parse_json(msg)
        assert result["id"] == 1
        assert result["method"] == "test"

    def test_parse_json_invalid(self):
        assert ACPClientBase._parse_json("not json at all") is None
        assert ACPClientBase._parse_json("") is None
        assert ACPClientBase._parse_json("no braces here") is None

    def test_parse_json_malformed(self):
        assert ACPClientBase._parse_json("{broken json") is None

    def test_handle_stream_update_agent_message_chunk(self):
        config = ACPConfig()
        client = ConcreteClient(config)
        client._chunks = []

        msg = {
            "method": "session/update",
            "params": {
                "update": {
                    "sessionUpdate": "agent_message_chunk",
                    "content": {"type": "text", "text": "Hello"},
                }
            },
        }
        client._handle_stream_update(msg)
        assert client._chunks == ["Hello"]

    def test_handle_stream_update_text_message_content(self):
        config = ACPConfig()
        client = ConcreteClient(config)
        client._chunks = []

        msg = {
            "method": "session/update",
            "params": {
                "update": {
                    "sessionUpdate": "text_message_content",
                    "text": "World",
                }
            },
        }
        client._handle_stream_update(msg)
        assert client._chunks == ["World"]

    def test_handle_stream_update_end(self):
        config = ACPConfig()
        client = ConcreteClient(config)
        client._complete = asyncio.Event()

        msg = {
            "method": "session/update",
            "params": {
                "update": {"sessionUpdate": "agent_message_end"}
            },
        }
        client._handle_stream_update(msg)
        assert client._complete.is_set()

    def test_handle_stream_update_with_queue(self):
        config = ACPConfig()
        client = ConcreteClient(config)
        client._chunks = []
        client._streaming = True
        client._stream_queue = asyncio.Queue()

        msg = {
            "method": "session/update",
            "params": {
                "update": {
                    "sessionUpdate": "agent_message_chunk",
                    "content": {"type": "text", "text": "chunk1"},
                }
            },
        }
        client._handle_stream_update(msg)
        assert client._chunks == ["chunk1"]
        assert not client._stream_queue.empty()

    def test_handle_stream_end_with_queue(self):
        config = ACPConfig()
        client = ConcreteClient(config)
        client._streaming = True
        client._stream_queue = asyncio.Queue()
        client._complete = asyncio.Event()

        msg = {
            "method": "session/update",
            "params": {
                "update": {"sessionUpdate": "session_end"}
            },
        }
        client._handle_stream_update(msg)
        assert client._complete.is_set()
        # Queue should have None sentinel
        assert client._stream_queue.get_nowait() is None

    async def test_dispatch_rpc_response(self):
        config = ACPConfig()
        client = ConcreteClient(config)
        loop = asyncio.get_running_loop()
        future = loop.create_future()
        client._pending[42] = future

        msg = {"id": 42, "result": {"sessionId": "abc"}}
        await client._dispatch(msg)

        assert future.done()
        assert future.result() == {"sessionId": "abc"}

    async def test_dispatch_rpc_error(self):
        config = ACPConfig()
        client = ConcreteClient(config)
        loop = asyncio.get_running_loop()
        future = loop.create_future()
        client._pending[42] = future

        msg = {"id": 42, "error": {"code": -32600, "message": "Invalid request"}}
        await client._dispatch(msg)

        assert future.done()
        with pytest.raises(Exception, match="Invalid request"):
            future.result()

    async def test_dispatch_stop_reason(self):
        config = ACPConfig()
        client = ConcreteClient(config)
        client._complete = asyncio.Event()
        loop = asyncio.get_running_loop()
        future = loop.create_future()
        client._pending[42] = future

        msg = {"id": 42, "result": {"stopReason": "end_turn"}}
        await client._dispatch(msg)

        assert client._complete.is_set()

    async def test_resume_default_returns_false(self):
        config = ACPConfig()
        client = ConcreteClient(config)
        assert await client.resume("some-session") is False

    async def test_disconnect_when_no_process(self):
        config = ACPConfig()
        client = ConcreteClient(config)
        # Should not raise
        await client.disconnect()
        assert client.is_connected is False
