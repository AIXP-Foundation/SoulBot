"""Tests for provider routing and fallback configuration."""

import pytest

from soulbot.acp.config import (
    ACPConfig,
    FALLBACK_MAP,
    resolve_client_class,
    resolve_provider,
)
from soulbot.acp.claude_client import ClaudeACPClient
from soulbot.acp.gemini_client import GeminiACPClient
from soulbot.acp.opencode_client import OpenCodeACPClient
from soulbot.acp.cursor_client import CursorCLIClient


class TestResolveProvider:
    def test_claude(self):
        assert resolve_provider("claude-acp/sonnet") == "claude"
        assert resolve_provider("claude-acp/opus") == "claude"

    def test_gemini(self):
        assert resolve_provider("gemini-acp/pro") == "gemini"
        assert resolve_provider("gemini-acp/gemini-2.5-flash") == "gemini"

    def test_opencode(self):
        assert resolve_provider("opencode-acp/default") == "opencode"
        assert resolve_provider("opencode-acp/kimi-k2.5-free") == "opencode"

    def test_cursor(self):
        assert resolve_provider("cursor-cli/gpt-4") == "cursor"
        assert resolve_provider("cursor-cli/claude-3.5-sonnet") == "cursor"

    def test_default_to_claude(self):
        assert resolve_provider("unknown-model") == "claude"
        assert resolve_provider("some-random") == "claude"

    def test_case_insensitive(self):
        assert resolve_provider("Claude-ACP/Sonnet") == "claude"
        assert resolve_provider("GEMINI-ACP/pro") == "gemini"


class TestResolveClientClass:
    def test_claude(self):
        assert resolve_client_class("claude") is ClaudeACPClient

    def test_gemini(self):
        assert resolve_client_class("gemini") is GeminiACPClient

    def test_opencode(self):
        assert resolve_client_class("opencode") is OpenCodeACPClient

    def test_cursor(self):
        assert resolve_client_class("cursor") is CursorCLIClient

    def test_unknown_raises(self):
        with pytest.raises(ValueError, match="Unknown provider"):
            resolve_client_class("unknown")


class TestFallbackMap:
    def test_claude_falls_to_gemini(self):
        assert "gemini" in FALLBACK_MAP["claude"]

    def test_gemini_falls_to_claude(self):
        assert "claude" in FALLBACK_MAP["gemini"]

    def test_opencode_falls_to_claude(self):
        assert "claude" in FALLBACK_MAP["opencode"]

    def test_cursor_falls_to_claude(self):
        assert "claude" in FALLBACK_MAP["cursor"]

    def test_all_providers_have_fallback(self):
        for provider in ("claude", "gemini", "opencode", "cursor"):
            assert provider in FALLBACK_MAP


class TestACPConfigFallback:
    def test_default_fallback_disabled(self):
        config = ACPConfig()
        assert config.enable_fallback is False

    def test_enable_fallback(self):
        config = ACPConfig(enable_fallback=True)
        assert config.enable_fallback is True

    def test_from_env_fallback(self, monkeypatch):
        monkeypatch.setenv("ACP_ENABLE_FALLBACK", "true")
        config = ACPConfig.from_env()
        assert config.enable_fallback is True

    def test_from_env_fallback_disabled(self, monkeypatch):
        monkeypatch.setenv("ACP_ENABLE_FALLBACK", "false")
        config = ACPConfig.from_env()
        assert config.enable_fallback is False
