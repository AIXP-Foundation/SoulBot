"""Tests for TerminalService — create, wait, output, release."""

import asyncio

import pytest

from soulbot.acp.services.terminal_service import TerminalService


@pytest.fixture
async def terminal(tmp_path) -> TerminalService:
    svc = TerminalService(str(tmp_path))
    yield svc
    # Wait for all background subprocesses to finish before loop closes
    for term in svc._terminals.values():
        await term["exit_event"].wait()


class TestTerminalCreate:
    async def test_create_returns_id(self, terminal: TerminalService):
        result = await terminal.create("echo hello")
        assert "terminalId" in result
        assert len(result["terminalId"]) == 8

    async def test_create_multiple(self, terminal: TerminalService):
        r1 = await terminal.create("echo a")
        r2 = await terminal.create("echo b")
        assert r1["terminalId"] != r2["terminalId"]


class TestTerminalWaitAndOutput:
    async def test_wait_for_exit(self, terminal: TerminalService):
        r = await terminal.create("echo done")
        tid = r["terminalId"]
        result = await terminal.wait_for_exit(tid)
        assert result["exitStatus"]["exitCode"] == 0

    async def test_get_output(self, terminal: TerminalService):
        r = await terminal.create("echo hello_world")
        tid = r["terminalId"]
        await terminal.wait_for_exit(tid)
        result = await terminal.get_output(tid)
        assert "hello_world" in result["output"]
        assert result["exitStatus"]["exitCode"] == 0

    async def test_failed_command_exit_code(self, terminal: TerminalService):
        r = await terminal.create("exit 42")
        tid = r["terminalId"]
        result = await terminal.wait_for_exit(tid)
        assert result["exitStatus"]["exitCode"] == 42

    async def test_wait_nonexistent_raises(self, terminal: TerminalService):
        with pytest.raises(KeyError, match="not found"):
            await terminal.wait_for_exit("nope1234")

    async def test_output_nonexistent_raises(self, terminal: TerminalService):
        with pytest.raises(KeyError, match="not found"):
            await terminal.get_output("nope1234")


class TestTerminalRelease:
    async def test_release_cleans_up(self, terminal: TerminalService):
        r = await terminal.create("echo x")
        tid = r["terminalId"]
        await terminal.wait_for_exit(tid)
        result = await terminal.release(tid)
        assert result == {}
        # After release, terminal is gone
        with pytest.raises(KeyError):
            await terminal.get_output(tid)

    async def test_release_nonexistent_noop(self, terminal: TerminalService):
        result = await terminal.release("gone1234")
        assert result == {}
