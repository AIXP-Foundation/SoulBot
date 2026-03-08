"""AisopLoader — discover and load .aisop.json blueprint files."""

from __future__ import annotations

import json
import logging
from pathlib import Path

from .schema import AisopBlueprint

logger = logging.getLogger(__name__)


class AisopLoader:
    """Load and manage AISOP blueprint files.

    Usage::

        loader = AisopLoader("./aisop")
        blueprints = loader.load_all()
        bp = loader.load("customer_support")
    """

    def __init__(self, aisop_dir: str | Path) -> None:
        self._dir = Path(aisop_dir)
        self._blueprints: dict[str, AisopBlueprint] = {}

    @property
    def blueprints(self) -> dict[str, AisopBlueprint]:
        """Return loaded blueprints."""
        return dict(self._blueprints)

    def has(self, name: str) -> bool:
        """Check if a blueprint with *name* is loaded."""
        return name in self._blueprints

    def list_names(self) -> list[str]:
        """Return names of all loaded blueprints."""
        return list(self._blueprints.keys())

    def get(self, name: str) -> AisopBlueprint | None:
        """Return a loaded blueprint by name, or ``None``."""
        return self._blueprints.get(name)

    def load_all(self) -> dict[str, AisopBlueprint]:
        """Scan directory and load all ``*.aisop.json`` files.

        Returns:
            Mapping of blueprint name to loaded blueprint.
        """
        if not self._dir.is_dir():
            logger.warning("AISOP directory not found: %s", self._dir)
            return {}

        for path in sorted(self._dir.glob("*.aisop.json")):
            try:
                bp = self._load_file(path)
                self._blueprints[bp.name] = bp
            except Exception as exc:
                logger.warning("Skipping %s: %s", path, exc)

        return dict(self._blueprints)

    def load(self, name: str) -> AisopBlueprint:
        """Load a single blueprint by name.

        Returns cached version if already loaded.

        Raises:
            FileNotFoundError: Blueprint file not found.
        """
        if name in self._blueprints:
            return self._blueprints[name]

        path = self._dir / f"{name}.aisop.json"
        if not path.exists():
            raise FileNotFoundError(f"AISOP blueprint not found: {path}")

        bp = self._load_file(path)
        self._blueprints[bp.name] = bp
        return bp

    def reload_all(self) -> int:
        """Clear cache and reload all blueprints.

        Returns:
            Number of blueprints loaded.
        """
        self._blueprints.clear()
        self.load_all()
        return len(self._blueprints)

    @staticmethod
    def _load_file(path: Path) -> AisopBlueprint:
        """Load and parse a single .aisop.json file.

        Supports two formats:
        - Flat dict: ``{name, workflow, functions, ...}`` (legacy)
        - AISOP V1.0.0: ``[{role: "system", content: {...}}, {role: "user", content: {...}}]``
        """
        with open(path, encoding="utf-8-sig") as f:
            data = json.load(f)

        # Standard AISOP V1.0.0 format: list of role/content messages
        if isinstance(data, list):
            data = _aisop_v1_to_flat(data, path)

        return AisopBlueprint(**data)


def _aisop_v1_to_flat(messages: list, path: Path) -> dict:
    """Convert AISOP V1.0.0 ``[{role, content}, ...]`` to flat dict."""
    system_content = {}
    user_content = {}
    for msg in messages:
        role = msg.get("role", "")
        if role == "system":
            system_content = msg.get("content", {})
        elif role == "user":
            user_content = msg.get("content", {})

    # Extract name from file stem or system id
    name = path.stem.removesuffix(".aisop")
    sc = system_content if isinstance(system_content, dict) else {}
    uc = user_content if isinstance(user_content, dict) else {}

    # functions: AISOP V1.0.0 has step dicts; flatten to single strings
    raw_funcs = uc.get("functions", {})
    functions = {}
    for key, val in raw_funcs.items():
        if isinstance(val, dict):
            functions[key] = " ".join(str(v) for v in val.values())
        else:
            functions[key] = str(val)

    # tools: V1.0.0 stores as string list; convert to AisopTool-compatible dicts
    raw_tools = sc.get("tools", [])
    tools = []
    for t in raw_tools:
        if isinstance(t, str):
            tools.append({"name": t})
        elif isinstance(t, dict):
            tools.append(t)

    # v14 optional fields
    capabilities = sc.get("capabilities", None)
    if capabilities and isinstance(capabilities, dict):
        capabilities = {
            "offered": capabilities.get("offered", []),
            "required": capabilities.get("required", []),
        }

    return {
        "name": name,
        "version": sc.get("version", "1.0"),
        "description": sc.get("description", sc.get("summary", "")),
        "workflow": uc.get("aisop", {}).get("main", ""),
        "functions": functions,
        "tools": tools,
        "system_directive": sc.get("system_prompt", ""),
        "metadata": {
            "protocol": sc.get("protocol", ""),
            "id": sc.get("id", ""),
            "verified_on": sc.get("verified_on", []),
        },
        "registry_uri": sc.get("registry_uri", None),
        "capabilities": capabilities,
        "ui": sc.get("ui", None),
        "identity": sc.get("identity", None),
    }
