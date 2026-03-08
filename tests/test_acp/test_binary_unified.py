"""Tests for unified find_binary() function."""

import os
import sys
import pytest
from unittest.mock import patch

from soulbot.acp.binary import find_binary, find_cursor_binary


class TestFindBinary:
    def test_found_first_name(self):
        with patch("shutil.which") as mock_which:
            mock_which.return_value = "/usr/bin/my-tool"
            result = find_binary(["my-tool", "other-tool"])
            assert result == "/usr/bin/my-tool"

    def test_found_second_name(self):
        def mock_which(name):
            if name == "first":
                return None
            if name == "second":
                return "/usr/bin/second"
            return None

        with patch("shutil.which", side_effect=mock_which):
            with patch("os.path.exists", return_value=False):
                result = find_binary(["first", "second"])
                assert result == "/usr/bin/second"

    def test_not_found(self):
        with patch("shutil.which", return_value=None):
            with patch("os.path.exists", return_value=False):
                result = find_binary(["nonexistent"])
                assert result is None

    def test_empty_names_list(self):
        result = find_binary([])
        assert result is None

    @pytest.mark.skipif(sys.platform != "win32", reason="Windows-specific")
    def test_windows_appdata_fallback(self, tmp_path):
        npm_dir = tmp_path / "npm"
        npm_dir.mkdir()
        cmd_file = npm_dir / "my-tool.cmd"
        cmd_file.write_text("@echo off")

        with patch("shutil.which", return_value=None):
            with patch.dict(os.environ, {"APPDATA": str(tmp_path)}):
                result = find_binary(["my-tool"])
                assert result is not None
                assert "my-tool.cmd" in result

    @pytest.mark.skipif(sys.platform != "win32", reason="Windows-specific")
    def test_windows_localappdata_fallback(self, tmp_path):
        npm_dir = tmp_path / "npm"
        npm_dir.mkdir()
        cmd_file = npm_dir / "my-tool.cmd"
        cmd_file.write_text("@echo off")

        with patch("shutil.which", return_value=None):
            with patch.dict(os.environ, {"APPDATA": "", "LOCALAPPDATA": str(tmp_path)}):
                result = find_binary(["my-tool"])
                assert result is not None
                assert "my-tool.cmd" in result


class TestFindCursorBinary:
    def test_found_cursor_agent(self):
        with patch("shutil.which") as mock_which:
            mock_which.return_value = "/usr/bin/cursor-agent"
            result = find_cursor_binary()
            assert result == "/usr/bin/cursor-agent"

    def test_found_agent_fallback(self):
        def mock_which(name):
            if name == "cursor-agent":
                return None
            if name == "agent":
                return "/usr/bin/agent"
            return None

        with patch("shutil.which", side_effect=mock_which):
            with patch("os.path.exists", return_value=False):
                result = find_cursor_binary()
                assert result == "/usr/bin/agent"

    def test_not_found(self):
        with patch("shutil.which", return_value=None):
            with patch("os.path.exists", return_value=False):
                assert find_cursor_binary() is None
