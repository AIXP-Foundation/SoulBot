"""Tests for ACPConfig."""

import os
import pytest
from soulbot.acp.config import ACPConfig


class TestACPConfig:
    def test_defaults(self):
        config = ACPConfig()
        assert config.provider == "claude"
        assert config.model == "claude-acp/sonnet"
        assert config.pool_size == 10
        assert config.pool_idle_timeout == 1800
        assert config.pool_keepalive_interval == 300
        assert config.timeout_connect == 30
        assert config.timeout_prompt == 3600
        assert config.timeout_stream == 3600
        assert config.auto_approve_permissions is True
        assert config.cwd  # Should default to os.getcwd()

    def test_custom_values(self):
        config = ACPConfig(
            provider="gemini",
            model="gemini-acp/pro",
            pool_size=5,
            timeout_prompt=120,
        )
        assert config.provider == "gemini"
        assert config.model == "gemini-acp/pro"
        assert config.pool_size == 5
        assert config.timeout_prompt == 120

    def test_from_env(self, monkeypatch):
        monkeypatch.setenv("ACP_PROVIDER", "gemini")
        monkeypatch.setenv("ACP_MODEL", "gemini-acp/flash")
        monkeypatch.setenv("ACP_POOL_SIZE", "5")
        monkeypatch.setenv("ACP_POOL_IDLE_TIMEOUT", "3600")
        monkeypatch.setenv("ACP_TIMEOUT_CONNECT", "15")
        monkeypatch.setenv("ACP_TIMEOUT_PROMPT", "120")
        monkeypatch.setenv("ACP_TIMEOUT_STREAM", "60")
        monkeypatch.setenv("ACP_CWD", "/tmp/test")
        monkeypatch.setenv("ACP_AUTO_APPROVE", "false")

        config = ACPConfig.from_env()
        assert config.provider == "gemini"
        assert config.model == "gemini-acp/flash"
        assert config.pool_size == 5
        assert config.pool_idle_timeout == 3600
        assert config.timeout_connect == 15
        assert config.timeout_prompt == 120
        assert config.timeout_stream == 60
        assert config.cwd == "/tmp/test"
        assert config.auto_approve_permissions is False

    def test_from_env_defaults(self):
        """Without env vars, from_env returns defaults."""
        config = ACPConfig.from_env()
        assert config.provider == "claude"
        assert config.pool_size == 10

    def test_from_env_with_overrides(self, monkeypatch):
        monkeypatch.setenv("ACP_PROVIDER", "gemini")
        config = ACPConfig.from_env(provider="cursor", pool_size=3)
        assert config.provider == "cursor"  # override wins
        assert config.pool_size == 3

    def test_from_env_auto_approve_truthy(self, monkeypatch):
        for val in ("true", "1", "yes", "True", "YES"):
            monkeypatch.setenv("ACP_AUTO_APPROVE", val)
            config = ACPConfig.from_env()
            assert config.auto_approve_permissions is True

    def test_from_env_auto_approve_falsy(self, monkeypatch):
        for val in ("false", "0", "no", "anything"):
            monkeypatch.setenv("ACP_AUTO_APPROVE", val)
            config = ACPConfig.from_env()
            assert config.auto_approve_permissions is False
