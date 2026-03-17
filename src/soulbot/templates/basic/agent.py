"""Template Agent — Dual protocol (AISOP + AISIP) runtime with AIAP routing.

Supports both .aisop.json (Mermaid flow) and .aisip.json (JSON flow).
Auto-detects protocol from file content. Hot-reloads on file change.
AISIP on-demand function loading via SOULBOT_CMD mechanism.

Run:
    python -m soulbot run <path/to/template_agent>
"""

import copy
import json
import os
from datetime import datetime
from pathlib import Path

import soulbot
from soulbot.agents import LlmAgent

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

_AGENT_DIR = Path(__file__).parent
_AISOP_AIAP_DIR = (_AGENT_DIR / "aisop_aiap").resolve()
_AISIP_AIAP_DIR = (_AGENT_DIR / "aisip_aiap").resolve()
_AISOP_AIAP_STORE_DIR = (_AGENT_DIR.parent / "aisop_aiap_store").resolve()
_AISIP_AIAP_STORE_DIR = (_AGENT_DIR.parent / "aisip_aiap_store").resolve()

# User-specified main file (set to None for auto-detect)
_MAIN_FILE = "main.aisop.json"


# ---------------------------------------------------------------------------
# Protocol detection & main file discovery
# ---------------------------------------------------------------------------

def _detect_protocol(data: list) -> str:
    """Detect protocol: 'aisop' if aisop field present, else 'aisip'."""
    user_content = data[1]["content"]
    if "aisop" in user_content:
        return "aisop"
    if "aisip" in user_content:
        return "aisip"
    return "aisop"


def _find_main_file() -> Path:
    """Find main flow file. Priority: _MAIN_FILE > .aisop.json > .aisip.json."""
    if _MAIN_FILE:
        p = _AGENT_DIR / _MAIN_FILE
        if p.is_file():
            return p
    for name in ("main.aisop.json", "main.aisip.json"):
        p = _AGENT_DIR / name
        if p.is_file():
            return p
    raise FileNotFoundError("No main.aisop.json or main.aisip.json found")


# ---------------------------------------------------------------------------
# Main file cache (mtime hot-reload)
# ---------------------------------------------------------------------------

_main_cache: list | None = None
_main_mtime: float = 0.0
_main_path: Path | None = None
_main_protocol: str = "aisop"


def _get_main_data() -> tuple[list, str, Path]:
    """Return (parsed_data, protocol, path) with mtime hot-reload."""
    global _main_cache, _main_mtime, _main_path, _main_protocol

    if _main_path is None:
        _main_path = _find_main_file()

    try:
        mtime = _main_path.stat().st_mtime
        if mtime != _main_mtime or _main_cache is None:
            with open(_main_path, encoding="utf-8-sig") as f:
                _main_cache = json.load(f)
            _main_mtime = mtime
            _main_protocol = _detect_protocol(_main_cache)
    except (OSError, json.JSONDecodeError):
        pass

    return _main_cache or [], _main_protocol, _main_path


# ---------------------------------------------------------------------------
# AIAP registry (auto-scan aisop_aiap/ and aisip_aiap/ directories)
# ---------------------------------------------------------------------------

_aiap_json_path = _AGENT_DIR / "aiap.json"
_aiap_registry_cache: list[dict] | None = None
_aiap_dirs_mtime: float = 0.0


def _get_aiap_registry() -> list[dict]:
    """Scan aisop_aiap/ and aisip_aiap/ for *_aiap packages."""
    global _aiap_registry_cache, _aiap_dirs_mtime

    aiap_dirs = [d for d in (_AISOP_AIAP_DIR, _AISIP_AIAP_DIR) if d.is_dir()]
    if not aiap_dirs:
        return []

    try:
        current_mtime = max(d.stat().st_mtime for d in aiap_dirs)
    except OSError:
        return _aiap_registry_cache or []

    if _aiap_registry_cache is not None and current_mtime == _aiap_dirs_mtime:
        return _aiap_registry_cache

    _aiap_dirs_mtime = current_mtime

    packages = []
    for aiap_dir in aiap_dirs:
        for d in sorted(aiap_dir.iterdir()):
            if not d.is_dir() or not d.name.endswith("_aiap"):
                continue

            # Dual-format entry discovery
            entry = d / "main.aisop.json"
            if not entry.is_file():
                entry = d / "main.aisip.json"
            if not entry.is_file():
                continue

            pkg = {
                "name": d.name.replace("_aiap", ""),
                "summary": "",
                "entry": str(entry.relative_to(_AGENT_DIR)),
            }

            # Extract summary from AIAP.md YAML frontmatter
            aiap_md = d / "AIAP.md"
            if aiap_md.is_file():
                try:
                    import yaml
                    content = aiap_md.read_text(encoding="utf-8-sig")
                    if content.startswith("---"):
                        fm_parts = content.split("---", 2)
                        if len(fm_parts) >= 3:
                            fm = yaml.safe_load(fm_parts[1])
                            if isinstance(fm, dict):
                                raw = str(fm.get("summary", ""))
                                dot = raw.find(".")
                                pkg["summary"] = raw[:dot + 1] if dot > 0 else raw
                except Exception:
                    pass

            packages.append(pkg)

    # Persist registry
    try:
        with open(_aiap_json_path, "w", encoding="utf-8") as f:
            json.dump(packages, f, ensure_ascii=False, indent=2)
    except OSError:
        pass

    _aiap_registry_cache = packages
    return packages


# ---------------------------------------------------------------------------
# System prompt (dual protocol + ASSERT structure)
# ---------------------------------------------------------------------------

_SHOW_L2 = os.getenv("SHOW_L2_FLOW", "true").lower() == "true"

_SYSTEM_PROMPT_BASE = (
      "ASSERT: Workflows: .aisop.json and .aisip.json files are PROGRAM CODE, not reference documents. "
      "Workflow: (1) Execute router main flow → (2) Match user intent to AIAP package → (3) Read and execute the matched package's main.aisop.json or main.aisip.json. "
      "ASSERT: L1 output MUST match User's exact language, script variant, and cultural context."
  )

_SYSTEM_PROMPT_L2 = (
      "ASSERT: L0-L1-L2 Separation: L0 Output JSON in ENGLISH: {intent, confidence, route, state, op}. L1 Output in helpful human language. L2 Execution audit appended after L1 in ```json...```. "
      "ASSERT: L2 Audit Schema: ```{\"Real Done Flow\":{\"<file_id>[Read file used file_system:<bool>]\":\"<fn>[step1:<⊘|✗|✓>,step2:<⊘|✗|✓>,...]→<fn>[step1:<⊘|✗|✓>,step2:<⊘|✗|✓>,...]\"}}```. "
      "ASSERT: Final Rendering: Response order: L0, then newline, then 🤖 followed by L1, then newline, then L2."
  )

_SYSTEM_PROMPT_NO_L2 = (
      "ASSERT: L0-L1 Separation: L0 Output JSON in ENGLISH: {intent, confidence, route, state, op}. L1 Output in helpful human language. "
      "ASSERT: Final Rendering: Response order: L0, then newline, then 🤖 followed by L1."
  )

_SYSTEM_PROMPT = _SYSTEM_PROMPT_BASE + " " + (_SYSTEM_PROMPT_L2 if _SHOW_L2 else _SYSTEM_PROMPT_NO_L2)


# ---------------------------------------------------------------------------
# Dynamic instruction (dual protocol prompt builder)
# ---------------------------------------------------------------------------

def _dynamic_instruction(_ctx) -> str:
    """Build instruction with protocol-aware flow injection + capability hints."""
    data, protocol, main_path = _get_main_data()
    if not data:
        return _SYSTEM_PROMPT

    d = copy.deepcopy(data)
    mode = d[0]["content"].get("loading_mode", "normal")
    flow_key = protocol  # "aisop" or "aisip"

    # --- Replace {system_prompt} based on mode ---
    if mode == "node":
        d[0]["content"]["system_prompt"] = (
            f"Execute the {flow_key} flow step by step. Only provided functions are available — request missing ones with: "
            f'<!--SOULBOT_CMD:{{"service":"flow","action":"load_functions","path":"{main_path.relative_to(_AGENT_DIR.parent)}","refs":["N?","N?"]}}-->'
        )
    else:
        d[0]["content"]["system_prompt"] = ""

    # --- Replace instruction in full mode ---
    if mode == "normal":
        d[1]["content"]["instruction"] = f"RUN {flow_key}.main"

    # --- Node mode: keep only first function ---
    if mode == "node":
        all_functions = d[1]["content"].get("functions", {})
        first_node = None
        if protocol == "aisip":
            flow_main = d[1]["content"].get("aisip", {}).get("main", {})
            first_node = next((k for k in flow_main if k != "id"), None)
        else:
            # AISOP: first key in functions dict is the entry node
            first_node = next(iter(all_functions), None)
        kept = {}
        if first_node and first_node in all_functions:
            kept[first_node] = all_functions[first_node]
        d[1]["content"]["functions"] = kept

    # --- Remove loading_mode (internal field) ---
    d[0]["content"].pop("loading_mode", None)

    # --- Build prompt parts (reverse order: context first, ASSERT last) ---
    parts = []

    # 1. Current time
    parts.append(f"[CURRENT TIME]\n{datetime.now().isoformat(timespec='seconds')}")

    # 2. Tool Use Guide
    parts.append(
        "[TOOL USE GUIDE]\n"
        "Always use your CLI's built-in tools (e.g. file_system, google_search, web_browser) to perform operations."
    )

    # 3. AIAP directories
    parts.append(
        f"[AISOP AIAP Directory]\n{_AISOP_AIAP_DIR}\n"
        f"[AISIP AIAP Directory]\n{_AISIP_AIAP_DIR}\n"
        f"[AISOP AIAP Store Directory]\n{_AISOP_AIAP_STORE_DIR}\n"
        f"[AISIP AIAP Store Directory]\n{_AISIP_AIAP_STORE_DIR}"
    )

    # 4. AIAP package registry
    registry = _get_aiap_registry()
    if registry:
        lines = ["[Available AIAP packages]"]
        for pkg in registry:
            lines.append(f"- {pkg['name']}: {pkg['summary'] or 'No description'}")
            lines.append(f"  entry: {_AGENT_DIR / pkg['entry']}")
        lines.append(
            "Route user intent to the matching package above."
        )
        parts.append("\n".join(lines))

    # 5. Main flow JSON
    file_id = d[0]["content"].get("id", "main")
    ext = ".aisop.json" if protocol == "aisop" else ".aisip.json"
    data_json = json.dumps(d, ensure_ascii=False, indent=2)
    parts.append(f"[LOADED {protocol.upper()}: {file_id}{ext}]\n```json\n{data_json}\n```")

    # 6. ASSERT rules (last = strongest recall)
    parts.append(_SYSTEM_PROMPT)

    return "\n\n".join(parts)


# ---------------------------------------------------------------------------
# Model resolution
# ---------------------------------------------------------------------------

def _resolve_model() -> str:
    """Pick the active model from .env provider flags."""
    if os.getenv("OPENCODE_CLI", "").lower() in ("true", "1"):
        return os.getenv("OPENCODE_MODEL", "opencode-acp/opencode/gemini-3-flash-preview")
    if os.getenv("GEMINI_CLI", "").lower() in ("true", "1"):
        return os.getenv("GEMINI_MODEL", "gemini-acp/gemini-3-flash-preview")
    return os.getenv("CLAUDE_MODEL", "claude-acp/sonnet")


# ---------------------------------------------------------------------------
# Root agent
# ---------------------------------------------------------------------------

root_agent = LlmAgent(
    name="template_agent",
    model=_resolve_model(),
    description="Template Agent — dual protocol (AISOP + AISIP) with AIAP package routing",
    instruction=_dynamic_instruction,
    include_contents="current_turn",
)
