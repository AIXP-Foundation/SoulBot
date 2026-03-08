"""AISOP blueprint schema — Pydantic models for .aisop.json files."""

from typing import Any

from pydantic import BaseModel, Field


class AisopToolAnnotations(BaseModel):
    """Tool behavior annotations (AIAP v14 P2-1)."""

    read_only: bool = False
    destructive: bool = False
    idempotent: bool = False
    open_world: bool = False


class AisopTool(BaseModel):
    """A tool declaration within an AISOP blueprint."""

    name: str
    description: str = ""
    parameters: dict[str, Any] = Field(default_factory=dict)
    required: bool = True
    fallback: str | None = None
    annotations: AisopToolAnnotations | None = None
    mcp_server: dict[str, Any] | None = None


class AisopCapabilities(BaseModel):
    """Runtime capability declaration (AIAP v14 P2-3)."""

    offered: list[str] = Field(default_factory=list)
    required: list[str] = Field(default_factory=list)


class AisopBlueprint(BaseModel):
    """An AISOP blueprint defining agent behavior via JSON.

    Attributes:
        name: Unique blueprint identifier.
        version: Semantic version string.
        description: Human-readable description.
        workflow: Mermaid flowchart string defining the execution graph.
        functions: Mapping of node name to natural-language action description.
        tools: List of tool declarations available to the agent.
        system_directive: Additional system-level instructions.
        metadata: Arbitrary key-value metadata.
        registry_uri: Optional federated registry endpoint (AIAP v14 P2-2).
        capabilities: Runtime capability declaration (AIAP v14 P2-3).
        ui: UI component declarations (AIAP v14 P3-4).
        identity: Program identity verification (AIAP v13 P1-1).
    """

    name: str
    version: str = "1.0"
    description: str = ""
    workflow: str = ""
    functions: dict[str, str] = Field(default_factory=dict)
    tools: list[AisopTool] = Field(default_factory=list)
    system_directive: str = ""
    metadata: dict[str, Any] = Field(default_factory=dict)
    registry_uri: str | None = None
    capabilities: AisopCapabilities | None = None
    ui: dict[str, Any] | None = None
    identity: dict[str, Any] | None = None
