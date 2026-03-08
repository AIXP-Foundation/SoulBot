"""Tests for CLI binary discovery."""

import os
import sys
import pytest
from unittest.mock import patch

from soulbot.acp.binary import find_claude_binary, find_gemini_binary, find_opencode_binary


class TestFindClaudeBinary:
    def test_found_via_shutil_which(self):
        with patch("shutil.which") as mock_which:
            mock_which.return_value = "/usr/local/bin/claude-code-acp"
            result = find_claude_binary()
            assert result == "/usr/local/bin/claude-code-acp"

    def test_claude_fallback(self):
        def mock_which(name):
            if name == "claude-code-acp":
                return None
            if name == "claude":
                return "/usr/local/bin/claude"
            return None

        with patch("shutil.which", side_effect=mock_which):
            # On Windows, also mock os.path.exists to prevent APPDATA fallback
            with patch("os.path.exists", return_value=False):
                result = find_claude_binary()
                assert result == "/usr/local/bin/claude"

    def test_not_found(self):
        with patch("shutil.which", return_value=None):
            with patch("sys.platform", "linux"):
                result = find_claude_binary()
                assert result is None

    @pytest.mark.skipif(sys.platform != "win32", reason="Windows-specific test")
    def test_windows_appdata_fallback(self, tmp_path):
        appdata = str(tmp_path)
        npm_dir = tmp_path / "npm"
        npm_dir.mkdir()
        cmd_file = npm_dir / "claude-code-acp.cmd"
        cmd_file.write_text("@echo off")

        with patch("shutil.which", return_value=None):
            with patch.dict(os.environ, {"APPDATA": appdata}):
                result = find_claude_binary()
                assert result is not None
                assert "claude-code-acp.cmd" in result


class TestFindGeminiBinary:
    def test_found(self):
        with patch("shutil.which", return_value="/usr/bin/gemini"):
            assert find_gemini_binary() == "/usr/bin/gemini"

    def test_not_found(self):
        with patch("shutil.which", return_value=None):
            with patch("sys.platform", "linux"):
                assert find_gemini_binary() is None


class TestFindOpenCodeBinary:
    def test_found(self):
        with patch("shutil.which", return_value="/usr/bin/opencode"):
            assert find_opencode_binary() == "/usr/bin/opencode"

    def test_not_found(self):
        with patch("shutil.which", return_value=None):
            with patch("sys.platform", "linux"):
                assert find_opencode_binary() is None
