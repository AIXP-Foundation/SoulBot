"""ACP (Agent Communication Protocol) — CLI subprocess connection management.

This package provides:
- ACPConfig: Configuration for ACP connections
- ACPClientBase: Base class for CLI subprocess clients
- ClaudeACPClient: Claude Code CLI client
- GeminiACPClient: Gemini CLI client (delayed session)
- OpenCodeACPClient: OpenCode CLI client (Windows compatible)
- OpenClawACPClient: OpenClaw CLI client (gateway-backed)
- CursorCLIClient: Cursor CLI client (non-pooled)
- ACPConnectionPool: Connection pooling with session reuse
- Binary discovery utilities
- Provider routing and fallback
"""

from .config import (
    ACPConfig,
    FALLBACK_MAP,
    resolve_client_class,
    resolve_provider,
)
from .binary import (
    find_binary,
    find_claude_binary,
    find_cursor_binary,
    find_gemini_binary,
    find_openclaw_binary,
    find_opencode_binary,
)
from .base_client import ACPClientBase
from .claude_client import ClaudeACPClient
from .gemini_client import GeminiACPClient
from .opencode_client import OpenCodeACPClient
from .openclaw_client import OpenClawACPClient
from .cursor_client import CursorCLIClient
from .pool import ACPConnectionPool

__all__ = [
    # Config & routing
    "ACPConfig",
    "FALLBACK_MAP",
    "resolve_client_class",
    "resolve_provider",
    # Clients
    "ACPClientBase",
    "ClaudeACPClient",
    "GeminiACPClient",
    "OpenCodeACPClient",
    "OpenClawACPClient",
    "CursorCLIClient",
    # Pool
    "ACPConnectionPool",
    # Binary discovery
    "find_binary",
    "find_claude_binary",
    "find_gemini_binary",
    "find_opencode_binary",
    "find_openclaw_binary",
    "find_cursor_binary",
]
