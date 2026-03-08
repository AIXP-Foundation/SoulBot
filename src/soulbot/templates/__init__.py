"""Agent template scaffolding utilities.

Shared by both ``soulbot create`` CLI command and ``POST /agents/create`` API.
"""

from __future__ import annotations

import re
import shutil
from pathlib import Path

TEMPLATES_DIR = Path(__file__).parent

#: Agent name must start with a lowercase letter, contain only [a-z0-9_], max 50 chars.
AGENT_NAME_RE = re.compile(r"^[a-z][a-z0-9_]{0,49}$")

_DEFAULT_ENV = """\
# Telegram Bot Token (get from @BotFather)
TELEGRAM_BOT_TOKEN=

# CLI Configuration Identity
# Used for session grouping — all agents under the same CLI_NAME share sessions
# Leave empty to auto-detect from *_CLI=true flags
CLI_NAME=

# AI Provider Configuration (CLI Mode)
CLAUDE_CLI=true
GEMINI_CLI=false
OPENCODE_CLI=false
OPENCLAW_CLI=false

# Model Configuration
CLAUDE_MODEL=claude-acp/sonnet
GEMINI_MODEL=gemini-acp/gemini-2.5-flash
OPENCODE_MODEL=opencode-acp/opencode/kimi-k2.5-free
OPENCLAW_MODEL=openclaw/default

# Model Fallback — auto-switch to fallback model on failure
ENABLE_FALLBACK=false

# Permissions — auto-approve CLI subprocess permission requests
AUTO_APPROVE_PERMISSIONS=true

# Workspace — agent working directory
WORKSPACE_DIR=aiap

# Show AI thinking process
SHOW_THOUGHTS=false
"""


def list_templates() -> list[dict[str, str]]:
    """Return available templates as ``[{name, description}]``."""
    result: list[dict[str, str]] = []
    if not TEMPLATES_DIR.is_dir():
        return result
    for child in sorted(TEMPLATES_DIR.iterdir()):
        if child.is_dir() and not child.name.startswith("_"):
            if (child / "agent.py").exists() or (child / "__init__.py").exists():
                result.append({
                    "name": child.name,
                    "description": _read_template_description(child),
                })
    return result


def scaffold_agent(name: str, template: str, output_dir: Path) -> Path:
    """Create a new agent directory from *template*.

    Returns the created directory path.
    Raises ``ValueError`` for invalid name/template, ``FileExistsError`` if target exists.
    """
    if not AGENT_NAME_RE.match(name):
        raise ValueError(
            f"Invalid agent name '{name}': must match [a-z][a-z0-9_]{{0,49}}"
        )

    template_dir = TEMPLATES_DIR / template
    if not template_dir.is_dir():
        raise ValueError(f"Template '{template}' not found")

    target = Path(output_dir) / name
    if target.exists():
        raise FileExistsError(f"'{target}' already exists")

    # Copy template (ignore __pycache__)
    shutil.copytree(
        template_dir, target, ignore=shutil.ignore_patterns("__pycache__")
    )

    # Replace placeholders in text files
    name_title = name.replace("_", " ").title()
    for f in target.rglob("*"):
        if f.is_file() and f.suffix in (".py", ".json", ".md"):
            content = f.read_text(encoding="utf-8")
            content = content.replace("template_agent", name)
            content = content.replace("Template Agent", name_title)
            f.write_text(content, encoding="utf-8")

    # Generate .env
    generate_agent_env(target)

    return target


def generate_agent_env(target: Path) -> None:
    """Write a default ``.env`` file into *target* directory."""
    env_file = target / ".env"
    env_file.write_text(_DEFAULT_ENV, encoding="utf-8")


def _read_template_description(template_dir: Path) -> str:
    """Extract a one-line description from the template's agent.py docstring."""
    agent_py = template_dir / "agent.py"
    if not agent_py.exists():
        return ""
    try:
        text = agent_py.read_text(encoding="utf-8")
        for line in text.splitlines():
            stripped = line.strip()
            if stripped.startswith('"""') or stripped.startswith("'''"):
                # Single-line docstring
                doc = stripped.strip("\"'").strip()
                if doc:
                    return doc
                # Multi-line: read next line
                continue
            if stripped and not line.startswith("#") and not line.startswith("from") and not line.startswith("import"):
                # First non-empty, non-import line after opening quote
                return stripped.strip("\"'").strip()
    except Exception:
        pass
    return ""
