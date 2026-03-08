"""Tests for FSService — read, write, list, stat, exists."""

from pathlib import Path

import pytest

from soulbot.acp.services.fs_service import FSService


@pytest.fixture
def fs(tmp_path: Path) -> FSService:
    return FSService(str(tmp_path))


class TestReadTextFile:
    async def test_read_simple(self, fs: FSService, tmp_path: Path):
        (tmp_path / "hello.txt").write_text("line1\nline2\nline3", encoding="utf-8")
        result = await fs.read_text_file("hello.txt")
        assert "line1" in result["content"]
        assert "line2" in result["content"]

    async def test_read_with_offset(self, fs: FSService, tmp_path: Path):
        lines = "\n".join(f"line{i}" for i in range(1, 11))
        (tmp_path / "multi.txt").write_text(lines, encoding="utf-8")
        result = await fs.read_text_file("multi.txt", offset=3, limit=2)
        assert "line3" in result["content"]
        assert "line4" in result["content"]
        assert "line5" not in result["content"]

    async def test_read_directory_fallback(self, fs: FSService, tmp_path: Path):
        sub = tmp_path / "mydir"
        sub.mkdir()
        (sub / "a.txt").write_text("")
        (sub / "b.txt").write_text("")
        result = await fs.read_text_file("mydir")
        assert "a.txt" in result["content"]
        assert "b.txt" in result["content"]

    async def test_read_hides_dotfiles_in_dir(self, fs: FSService, tmp_path: Path):
        sub = tmp_path / "dir"
        sub.mkdir()
        (sub / ".hidden").write_text("")
        (sub / "visible.txt").write_text("")
        result = await fs.read_text_file("dir")
        assert ".hidden" not in result["content"]
        assert "visible.txt" in result["content"]

    async def test_read_nonexistent_raises(self, fs: FSService):
        with pytest.raises(FileNotFoundError):
            await fs.read_text_file("nope.txt")


class TestWriteTextFile:
    async def test_write_creates_file(self, fs: FSService, tmp_path: Path):
        result = await fs.write_text_file("new.txt", "hello world")
        assert result["exists"] is True
        assert result["isFile"] is True
        assert (tmp_path / "new.txt").read_text(encoding="utf-8") == "hello world"

    async def test_write_creates_parent_dirs(self, fs: FSService, tmp_path: Path):
        await fs.write_text_file("sub/deep/file.txt", "content")
        assert (tmp_path / "sub" / "deep" / "file.txt").exists()

    async def test_write_returns_size(self, fs: FSService, tmp_path: Path):
        result = await fs.write_text_file("sized.txt", "12345")
        assert result["size"] > 0


class TestListDirectory:
    async def test_list_files(self, fs: FSService, tmp_path: Path):
        (tmp_path / "a.py").write_text("")
        (tmp_path / "b.py").write_text("")
        result = await fs.list_directory(".")
        assert "a.py" in result["files"]
        assert "b.py" in result["files"]

    async def test_list_not_directory(self, fs: FSService, tmp_path: Path):
        (tmp_path / "file.txt").write_text("")
        with pytest.raises(FileNotFoundError, match="Not a directory"):
            await fs.list_directory("file.txt")

    async def test_list_hides_dotfiles(self, fs: FSService, tmp_path: Path):
        (tmp_path / ".git").mkdir()
        (tmp_path / "src").mkdir()
        result = await fs.list_directory(".")
        assert ".git" not in result["files"]
        assert "src" in result["files"]


class TestExists:
    async def test_exists_true(self, fs: FSService, tmp_path: Path):
        (tmp_path / "yes.txt").write_text("")
        result = await fs.exists("yes.txt")
        assert result["exists"] is True

    async def test_exists_false(self, fs: FSService):
        result = await fs.exists("nope.txt")
        assert result["exists"] is False


class TestStat:
    async def test_stat_file(self, fs: FSService, tmp_path: Path):
        (tmp_path / "info.txt").write_text("data")
        result = await fs.stat("info.txt")
        assert result["exists"] is True
        assert result["isFile"] is True
        assert result["isDirectory"] is False
        assert result["size"] > 0
        assert "permissions" in result

    async def test_stat_directory(self, fs: FSService, tmp_path: Path):
        (tmp_path / "mydir").mkdir()
        result = await fs.stat("mydir")
        assert result["exists"] is True
        assert result["isDirectory"] is True
        assert result["type"] == "directory"

    async def test_stat_nonexistent(self, fs: FSService):
        result = await fs.stat("ghost.txt")
        assert result["exists"] is False
        assert result["isFile"] is False
        assert result["size"] == 0
