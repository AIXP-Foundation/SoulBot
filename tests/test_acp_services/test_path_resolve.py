"""Tests for secure path resolution."""

import os
from pathlib import Path

import pytest

from soulbot.acp.services.path_utils import resolve_path


class TestResolvePath:
    def test_relative_path(self, tmp_path: Path):
        (tmp_path / "hello.txt").write_text("hi")
        result = resolve_path("hello.txt", str(tmp_path))
        assert result == (tmp_path / "hello.txt").resolve()

    def test_nested_relative(self, tmp_path: Path):
        sub = tmp_path / "src"
        sub.mkdir()
        (sub / "main.py").write_text("")
        result = resolve_path("src/main.py", str(tmp_path))
        assert result == (sub / "main.py").resolve()

    def test_pseudo_absolute_unix(self, tmp_path: Path):
        """Unix-style /src/main.py treated as relative to cwd."""
        sub = tmp_path / "src"
        sub.mkdir()
        (sub / "main.py").write_text("")
        result = resolve_path("/src/main.py", str(tmp_path))
        assert result == (sub / "main.py").resolve()

    def test_pseudo_absolute_backslash(self, tmp_path: Path):
        sub = tmp_path / "src"
        sub.mkdir()
        (sub / "main.py").write_text("")
        result = resolve_path("\\src\\main.py", str(tmp_path))
        assert result == (sub / "main.py").resolve()

    def test_windows_absolute_stays(self, tmp_path: Path):
        """Real Windows absolute paths (C:\\...) are used directly."""
        target = tmp_path / "file.txt"
        target.write_text("")
        result = resolve_path(str(target), str(tmp_path))
        assert result == target.resolve()

    def test_traversal_blocked(self, tmp_path: Path):
        with pytest.raises(PermissionError, match="escapes workspace"):
            resolve_path("../../etc/passwd", str(tmp_path))

    def test_traversal_dot_dot(self, tmp_path: Path):
        with pytest.raises(PermissionError, match="escapes workspace"):
            resolve_path("../secret.txt", str(tmp_path))

    def test_traversal_absolute_outside(self, tmp_path: Path):
        """Absolute path outside cwd is blocked."""
        # Use a path that's definitely outside tmp_path
        outside = Path(os.path.expanduser("~")).resolve()
        if str(outside).startswith(str(tmp_path.resolve())):
            pytest.skip("Home is under tmp_path")
        with pytest.raises(PermissionError, match="escapes workspace"):
            resolve_path(str(outside / "secret.txt"), str(tmp_path))

    def test_cwd_root_itself(self, tmp_path: Path):
        result = resolve_path(".", str(tmp_path))
        assert result == tmp_path.resolve()

    def test_leading_slashes_stripped(self, tmp_path: Path):
        (tmp_path / "file.txt").write_text("")
        result = resolve_path("///file.txt", str(tmp_path))
        assert result == (tmp_path / "file.txt").resolve()
