"""Tests for FSService content truncation and line range slicing."""

from pathlib import Path

import pytest

from soulbot.acp.services.fs_service import FSService


@pytest.fixture
def fs(tmp_path: Path) -> FSService:
    return FSService(str(tmp_path))


class TestTruncation:
    async def test_long_content_truncated(self, fs: FSService, tmp_path: Path):
        # Create a file exceeding MAX_READ_CHARS
        long_line = "x" * 200
        lines = [long_line] * 100  # 100 * 200 = 20,000 chars
        (tmp_path / "big.txt").write_text("\n".join(lines), encoding="utf-8")

        result = await fs.read_text_file("big.txt")
        assert "truncated" in result["content"]
        assert len(result["content"]) <= FSService.MAX_READ_CHARS + 200  # plus truncation message

    async def test_short_content_not_truncated(self, fs: FSService, tmp_path: Path):
        (tmp_path / "small.txt").write_text("short content", encoding="utf-8")
        result = await fs.read_text_file("small.txt")
        assert "truncated" not in result["content"]
        assert result["content"] == "short content"


class TestLineRange:
    async def test_offset_1_is_first_line(self, fs: FSService, tmp_path: Path):
        lines = "\n".join(f"L{i}" for i in range(1, 6))
        (tmp_path / "f.txt").write_text(lines, encoding="utf-8")
        result = await fs.read_text_file("f.txt", offset=1, limit=2)
        assert "L1" in result["content"]
        assert "L2" in result["content"]
        assert "L3" not in result["content"]

    async def test_offset_beyond_file(self, fs: FSService, tmp_path: Path):
        (tmp_path / "f.txt").write_text("one\ntwo\nthree", encoding="utf-8")
        result = await fs.read_text_file("f.txt", offset=100, limit=5)
        assert result["content"] == ""

    async def test_limit_zero_uses_default(self, fs: FSService, tmp_path: Path):
        lines = "\n".join(f"L{i}" for i in range(1, 10))
        (tmp_path / "f.txt").write_text(lines, encoding="utf-8")
        result = await fs.read_text_file("f.txt", offset=1, limit=0)
        # Should return all lines (less than DEFAULT_LINE_LIMIT)
        assert "L1" in result["content"]
        assert "L9" in result["content"]

    async def test_limit_clips_to_file_length(self, fs: FSService, tmp_path: Path):
        (tmp_path / "f.txt").write_text("a\nb\nc", encoding="utf-8")
        result = await fs.read_text_file("f.txt", offset=1, limit=100)
        assert result["content"] == "a\nb\nc"
