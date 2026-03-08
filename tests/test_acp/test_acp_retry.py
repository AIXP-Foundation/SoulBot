"""Tests for ACP retry integration (Doc 25).

Verifies that:
- pool._create_client() retries on transient connection errors
- Non-retryable errors are raised immediately
- Retry exhaustion raises the last error
- ACPConfig retry fields have correct defaults and env var mapping
- Fallback streaming fix — no empty final text
"""

import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from soulbot.acp.config import ACPConfig
from soulbot.acp.pool import ACPConnectionPool


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_config(**overrides) -> ACPConfig:
    defaults = {
        "provider": "claude",
        "model": "claude-acp/sonnet",
        "max_retries": 3,
        "retry_base_delay": 0,  # no delay in tests
    }
    defaults.update(overrides)
    return ACPConfig(**defaults)


def _mock_client_class(connect_side_effects=None):
    """Create a mock client class whose connect() has side effects."""

    class MockClient:
        def __init__(self, config):
            self.config = config
            self.session_id = "mock-session"
            self._connected = True
            self._last_used = 0
            self.is_connected = True
            self.is_idle_timeout = False
            self.process = MagicMock()
            self.process.returncode = None

        async def connect(self):
            if connect_side_effects:
                effect = connect_side_effects.pop(0)
                if isinstance(effect, Exception):
                    raise effect

        async def disconnect(self):
            self._connected = False

    return MockClient


# ---------------------------------------------------------------------------
# TestPoolRetry
# ---------------------------------------------------------------------------


class TestPoolRetry:
    """pool._create_client() retries on transient errors."""

    async def test_retries_on_connection_error(self):
        """connect() fails twice with connection error, then succeeds."""
        effects = [
            ConnectionError("Connection refused"),
            ConnectionError("Connection reset"),
            None,  # success
        ]
        config = _make_config(max_retries=3)
        pool = ACPConnectionPool(config, _mock_client_class(effects))

        client = await pool._create_client()
        assert client is not None
        assert client._connected

    async def test_exhausts_retries(self):
        """connect() always fails → raises after max_retries."""
        effects = [
            ConnectionError("Connection refused"),
            ConnectionError("Connection refused"),
            ConnectionError("Connection refused"),
        ]
        config = _make_config(max_retries=3)
        pool = ACPConnectionPool(config, _mock_client_class(effects))

        with pytest.raises(ConnectionError, match="Connection refused"):
            await pool._create_client()

    async def test_non_retryable_error_immediate(self):
        """Non-retryable error (ValueError) is raised immediately."""
        effects = [ValueError("Invalid config")]
        config = _make_config(max_retries=3)
        pool = ACPConnectionPool(config, _mock_client_class(effects))

        with pytest.raises(ValueError, match="Invalid config"):
            await pool._create_client()

    async def test_single_retry_disabled(self):
        """max_retries=1 means no retry, fail immediately."""
        effects = [ConnectionError("Connection refused")]
        config = _make_config(max_retries=1)
        pool = ACPConnectionPool(config, _mock_client_class(effects))

        with pytest.raises(ConnectionError):
            await pool._create_client()


# ---------------------------------------------------------------------------
# TestRetryConfig
# ---------------------------------------------------------------------------


class TestRetryConfig:
    """ACPConfig retry fields."""

    def test_defaults(self):
        config = ACPConfig()
        assert config.max_retries == 3
        assert config.retry_base_delay == 1.0

    def test_from_env(self):
        with patch.dict(os.environ, {
            "ACP_MAX_RETRIES": "5",
            "ACP_RETRY_BASE_DELAY": "2.5",
        }):
            config = ACPConfig.from_env()
            assert config.max_retries == 5
            assert config.retry_base_delay == 2.5

    def test_override_in_constructor(self):
        config = ACPConfig(max_retries=10, retry_base_delay=0.5)
        assert config.max_retries == 10
        assert config.retry_base_delay == 0.5


# ---------------------------------------------------------------------------
# TestFallbackFix
# ---------------------------------------------------------------------------


class TestFallbackFix:
    """Fallback streaming fix — parse_response instead of empty text."""

    def test_parse_response_used_for_final(self):
        """_parse_response returns proper content even for plain text."""
        from soulbot.models.acp_llm import ACPLlm

        resp = ACPLlm._parse_response("Hello world")
        assert resp.content is not None
        assert resp.content.parts[0].text == "Hello world"
        # Not empty string like the old bug
        assert resp.content.parts[0].text != ""
