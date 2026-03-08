"""CLI binary discovery utilities."""

from __future__ import annotations

import os
import shutil
import sys
from typing import Optional


def find_binary(names: list[str]) -> Optional[str]:
    """Find a CLI binary by searching PATH and common install locations.

    Args:
        names: Binary names to search for, in priority order.

    Returns:
        Absolute path to the binary, or ``None`` if not found.
    """
    for name in names:
        cmd = shutil.which(name)
        if cmd:
            return cmd
        # Windows: check npm global install locations
        if sys.platform == "win32":
            for base_var in ("APPDATA", "LOCALAPPDATA"):
                base = os.environ.get(base_var, "")
                if base:
                    for suffix in (".cmd", ".exe", ""):
                        path = os.path.join(base, "npm", f"{name}{suffix}")
                        if os.path.exists(path):
                            return path
    return None


def find_claude_binary() -> Optional[str]:
    """Find the Claude CLI binary (claude-code-acp or claude)."""
    return find_binary(["claude-code-acp", "claude"])


def find_gemini_binary() -> Optional[str]:
    """Find the Gemini CLI binary."""
    return find_binary(["gemini"])


def find_opencode_binary() -> Optional[str]:
    """Find the OpenCode CLI binary."""
    return find_binary(["opencode"])


def find_openclaw_binary() -> Optional[str]:
    """Find the OpenClaw CLI binary."""
    return find_binary(["openclaw"])


def find_cursor_binary() -> Optional[str]:
    """Find the Cursor CLI binary (cursor-agent or agent)."""
    return find_binary(["cursor-agent", "agent"])
