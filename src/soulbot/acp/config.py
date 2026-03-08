"""ACP connection configuration and provider routing."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .base_client import ACPClientBase


# ---------------------------------------------------------------------------
# Provider routing
# ---------------------------------------------------------------------------

def resolve_provider(model: str) -> str:
    """Extract provider name from a model identifier.

    Examples:
        ``claude-acp/sonnet`` → ``claude``
        ``gemini-acp/pro`` → ``gemini``
        ``opencode-acp/default`` → ``opencode``
        ``cursor-cli/gpt-4`` → ``cursor``
    """
    model_lower = model.lower()
    if model_lower.startswith("claude"):
        return "claude"
    if model_lower.startswith("gemini"):
        return "gemini"
    if model_lower.startswith("opencode"):
        return "opencode"
    if model_lower.startswith("openclaw"):
        return "openclaw"
    if model_lower.startswith("cursor"):
        return "cursor"
    return "claude"  # default


def resolve_client_class(provider: str) -> type[ACPClientBase]:
    """Return the client class for a given provider name.

    Lazy imports to avoid circular dependencies.
    """
    if provider == "claude":
        from .claude_client import ClaudeACPClient
        return ClaudeACPClient
    if provider == "gemini":
        from .gemini_client import GeminiACPClient
        return GeminiACPClient
    if provider == "opencode":
        from .opencode_client import OpenCodeACPClient
        return OpenCodeACPClient
    if provider == "openclaw":
        from .openclaw_client import OpenClawACPClient
        return OpenClawACPClient
    if provider == "cursor":
        from .cursor_client import CursorCLIClient
        return CursorCLIClient  # type: ignore[return-value]
    raise ValueError(f"Unknown provider: {provider}")


# ---------------------------------------------------------------------------
# Fallback configuration
# ---------------------------------------------------------------------------

FALLBACK_MAP: dict[str, str] = {
    "claude": "gemini-acp/gemini-2.5-flash",
    "gemini": "claude-acp/sonnet",
    "opencode": "claude-acp/sonnet",
    "openclaw": "claude-acp/sonnet",
    "cursor": "claude-acp/sonnet",
}


# ---------------------------------------------------------------------------
# Config dataclass
# ---------------------------------------------------------------------------

@dataclass
class ACPConfig:
    """Configuration for an ACP CLI subprocess connection.

    All settings can be overridden via environment variables with the
    ``ACP_`` prefix (e.g. ``ACP_POOL_SIZE=5``).
    """

    provider: str = "claude"
    """Provider name: claude / gemini / opencode / cursor."""

    model: str = "claude-acp/sonnet"
    """Full model identifier used by ModelRegistry."""

    pool_size: int = 10
    """Maximum number of idle connections kept in the pool."""

    pool_idle_timeout: int = 1800
    """Idle timeout in seconds before a pooled connection is closed (30min)."""

    pool_keepalive_interval: int = 300
    """Keepalive check interval in seconds (5min). 0 = disabled."""

    timeout_connect: int = 30
    """Timeout in seconds for subprocess startup + initialize."""

    timeout_prompt: int = 3600
    """Timeout in seconds for a single prompt/response cycle (60min)."""

    timeout_stream: int = 3600
    """Timeout in seconds for individual stream chunks (60min)."""

    cwd: str = field(default_factory=os.getcwd)
    """Working directory for the CLI subprocess."""

    auto_approve_permissions: bool = True
    """Automatically approve permission requests from the CLI."""

    enable_fallback: bool = False
    """Enable automatic fallback to another provider on failure."""

    max_retries: int = 3
    """Maximum retry attempts for transient errors (Doc 25)."""

    retry_base_delay: float = 1.0
    """Base delay in seconds for exponential backoff (Doc 25)."""

    @classmethod
    def from_env(cls, **overrides) -> ACPConfig:
        """Create config from environment variables.

        Environment variables (all optional):
            ACP_PROVIDER          — provider name
            ACP_MODEL             — model identifier
            ACP_POOL_SIZE         — max idle connections
            ACP_POOL_IDLE_TIMEOUT — idle timeout seconds
            ACP_TIMEOUT_CONNECT   — connect timeout
            ACP_TIMEOUT_PROMPT    — prompt timeout
            ACP_TIMEOUT_STREAM    — stream timeout
            ACP_CWD               — working directory
            ACP_AUTO_APPROVE      — auto-approve permissions (true/false)
        """
        def _env(key: str, default=None):
            return os.environ.get(f"ACP_{key}", default)

        kwargs: dict = {}

        v = _env("PROVIDER")
        if v:
            kwargs["provider"] = v

        v = _env("MODEL")
        if v:
            kwargs["model"] = v

        v = _env("POOL_SIZE")
        if v:
            kwargs["pool_size"] = int(v)

        v = _env("POOL_IDLE_TIMEOUT")
        if v:
            kwargs["pool_idle_timeout"] = int(v)

        v = _env("POOL_KEEPALIVE_INTERVAL")
        if v:
            kwargs["pool_keepalive_interval"] = int(v)

        v = _env("TIMEOUT_CONNECT")
        if v:
            kwargs["timeout_connect"] = int(v)

        v = _env("TIMEOUT_PROMPT")
        if v:
            kwargs["timeout_prompt"] = int(v)

        v = _env("TIMEOUT_STREAM")
        if v:
            kwargs["timeout_stream"] = int(v)

        v = _env("CWD")
        if v:
            kwargs["cwd"] = v

        v = _env("AUTO_APPROVE")
        if v:
            kwargs["auto_approve_permissions"] = v.lower() in ("true", "1", "yes")

        v = _env("ENABLE_FALLBACK")
        if v:
            kwargs["enable_fallback"] = v.lower() in ("true", "1", "yes")

        v = _env("MAX_RETRIES")
        if v:
            kwargs["max_retries"] = int(v)

        v = _env("RETRY_BASE_DELAY")
        if v:
            kwargs["retry_base_delay"] = float(v)

        kwargs.update(overrides)
        return cls(**kwargs)
