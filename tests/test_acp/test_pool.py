"""Tests for ACPConnectionPool."""

import asyncio
import time
import pytest

from soulbot.acp.config import ACPConfig
from soulbot.acp.base_client import ACPClientBase
from soulbot.acp.pool import ACPConnectionPool


# ---------------------------------------------------------------------------
# Mock client for testing pool behavior
# ---------------------------------------------------------------------------

class MockACPClient(ACPClientBase):
    """Mock ACP client that simulates connect/disconnect without subprocesses."""

    _connect_count: int = 0  # class-level counter

    def __init__(self, config: ACPConfig) -> None:
        super().__init__(config)
        self._query_response = "mock response"

    @property
    def is_connected(self) -> bool:
        return self._connected

    def _get_acp_command(self) -> list[str]:
        return ["mock-cli"]

    async def _initialize(self) -> None:
        MockACPClient._connect_count += 1
        self.session_id = f"mock-session-{MockACPClient._connect_count}"

    async def connect(self) -> None:
        """Simplified connect without subprocess."""
        self._connected = True
        self._last_used = time.time()
        await self._initialize()

    async def disconnect(self) -> None:
        self._connected = False
        self.process = None

    async def query(self, prompt: str) -> str:
        self._last_used = time.time()
        return self._query_response

    async def ping(self) -> bool:
        return self._connected

    async def resume(self, session_id: str) -> bool:
        self.session_id = session_id
        return True


@pytest.fixture(autouse=True)
def reset_connect_count():
    MockACPClient._connect_count = 0
    yield


@pytest.fixture
def config():
    return ACPConfig(pool_size=3, pool_idle_timeout=3600)


@pytest.fixture
def pool(config):
    return ACPConnectionPool(config, MockACPClient)


class TestACPConnectionPool:
    async def test_acquire_creates_new_client(self, pool):
        async with pool.acquire() as (client, sid):
            assert client.is_connected
            assert sid is not None
            assert sid.startswith("mock-session-")
        # Client returned to pool
        assert pool.size == 1

    async def test_acquire_reuses_pooled_client(self, pool):
        # First acquire creates a new client
        async with pool.acquire() as (client1, sid1):
            pass

        # Second acquire should reuse the pooled client
        async with pool.acquire() as (client2, sid2):
            assert sid2 == sid1  # Same session
        assert MockACPClient._connect_count == 1  # Only one connect

    async def test_session_id_matching(self, pool):
        # Create two clients in pool
        async with pool.acquire() as (c1, sid1):
            pass
        async with pool.acquire() as (c2, sid2):
            pass
        # Pool now has 2 clients

        # Request specific session
        async with pool.acquire(session_id=sid1) as (client, sid):
            assert sid == sid1

    async def test_pool_max_size(self, pool):
        # Acquire and release more clients than pool_size
        clients_sids = []
        for _ in range(5):
            async with pool.acquire() as (client, sid):
                clients_sids.append(sid)
        # Pool capped at pool_size=3
        assert pool.size <= 3

    async def test_idle_timeout_cleanup(self):
        config = ACPConfig(pool_size=3, pool_idle_timeout=0)  # Immediate timeout
        pool = ACPConnectionPool(config, MockACPClient)

        # Acquire and release a client
        async with pool.acquire() as (client, sid):
            pass

        # Force _last_used to the past
        if pool._pool:
            pool._pool[0]._last_used = time.time() - 10

        # Next acquire should create a new client (old one expired)
        async with pool.acquire() as (client, sid):
            assert MockACPClient._connect_count == 2

    async def test_close_all(self, pool):
        # Create some pooled connections
        async with pool.acquire() as (c1, _):
            pass
        async with pool.acquire() as (c2, _):
            pass
        assert pool.size >= 1

        await pool.close_all()
        assert pool.size == 0

    async def test_error_disconnects_client(self, pool):
        """On error during use, client should not be returned to pool."""
        class BrokenClient(MockACPClient):
            @property
            def is_connected(self) -> bool:
                return self._connected

            async def query(self, prompt: str) -> str:
                raise RuntimeError("broken")

        broken_pool = ACPConnectionPool(
            ACPConfig(pool_size=3), BrokenClient
        )

        with pytest.raises(RuntimeError, match="broken"):
            async with broken_pool.acquire() as (client, sid):
                await client.query("test")

        assert broken_pool.size == 0  # Not returned to pool

    async def test_get_stats(self, pool):
        async with pool.acquire() as (c, _):
            pass

        stats = pool.get_stats()
        assert stats["pool_size"] == 1
        assert stats["max_pool_size"] == 3
        assert stats["connected"] == 1
        assert stats["provider"] == "claude"

    async def test_concurrent_acquire(self, pool):
        """Multiple concurrent acquires should each get their own client."""
        results = []

        async def worker(i):
            async with pool.acquire() as (client, sid):
                await asyncio.sleep(0.01)  # Simulate work
                results.append(sid)

        await asyncio.gather(*[worker(i) for i in range(3)])
        assert len(results) == 3
        # All should have connected
        assert MockACPClient._connect_count >= 1
