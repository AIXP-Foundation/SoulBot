"""FastAPI API Server for SoulBot agents.

Provides HTTP endpoints for running agents, managing sessions,
and serving the dev web UI.
"""

from __future__ import annotations

import json
import shutil
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from ..agents.base_agent import BaseAgent
from ..runners import Runner
from ..sessions import InMemorySessionService
from ..sessions.base_session_service import BaseSessionService
from .agent_loader import AgentLoader

# ---------------------------------------------------------------------------
# Request / Response models
# ---------------------------------------------------------------------------


class RunAgentRequest(BaseModel):
    app_name: str
    user_id: str
    session_id: str
    new_message: Optional[dict] = None  # {"role": "user", "parts": [{"text": "..."}]}
    streaming: bool = False


class CreateSessionRequest(BaseModel):
    session_id: Optional[str] = None
    state: Optional[dict] = None
    title: Optional[str] = None


class CreateAgentRequest(BaseModel):
    name: str
    template: str = "basic"


class DeleteAisopRequest(BaseModel):
    path: str


class AddFromLibraryRequest(BaseModel):
    group: str


class DownloadFromStoreRequest(BaseModel):
    program: str


class InstallFromStoreRequest(BaseModel):
    program: str
    agent_name: str


# ---------------------------------------------------------------------------
# Server factory
# ---------------------------------------------------------------------------


STATIC_DIR = Path(__file__).parent / "static"


def create_app(
    *,
    agents_dir: str | Path | None = None,
    agents: dict[str, BaseAgent] | None = None,
    session_service: BaseSessionService | None = None,
    schedule_service: object | None = None,
    heartbeat_store: object | None = None,
    cli_name: str | None = None,
    dev_ui: bool = True,
) -> FastAPI:
    """Create a FastAPI application wired with agent runners.

    Args:
        agents_dir: Directory to discover agents from.
        agents: Pre-built dict of {name: agent}.  Mutually exclusive with *agents_dir*.
        session_service: Session backend (defaults to DatabaseSessionService).
        schedule_service: Optional ScheduleService for schedule query endpoints.
        cli_name: CLI identity for session grouping (Doc 21).
        dev_ui: Whether to mount the dev web UI at ``/dev-ui``.
    """
    app = FastAPI(title="SoulBot API Server", version="0.1.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ---- Shared state ---------------------------------------------------
    if session_service is None:
        from ..sessions.constants import resolve_db_path
        from ..sessions.database_session_service import DatabaseSessionService
        session_service = DatabaseSessionService(resolve_db_path())
    svc = session_service

    # Resolve cli_name for runner app_name (Doc 21)
    _cli_name = cli_name

    # Save for agent CRUD endpoints
    _agents_dir: Path | None = Path(agents_dir).resolve() if agents_dir else None
    _loader: AgentLoader | None = None

    runners: dict[str, Runner] = {}

    # ---- AIAP Store cache -----------------------------------------------
    _store_cache: dict = {"data": None, "expires": 0.0}
    GITHUB_REPO = "AIXP-Foundation/AIAP-Store"
    GITHUB_API = f"https://api.github.com/repos/{GITHUB_REPO}/contents"
    GITHUB_STORE_API = f"{GITHUB_API}/aiap_store"
    GITHUB_RAW = f"https://raw.githubusercontent.com/{GITHUB_REPO}/main/aiap_store"
    CACHE_TTL = 300  # 5 minutes

    if agents:
        for name, agent in agents.items():
            runners[name] = Runner(
                agent=agent, app_name=_cli_name or name, session_service=svc,
            )
    elif agents_dir:
        import logging
        _log = logging.getLogger(__name__)
        _loader = AgentLoader(agents_dir)
        for name in _loader.list_agents():
            try:
                agent = _loader.load_agent(name)
            except (AttributeError, TypeError) as exc:
                _log.warning("Skipping '%s': %s", name, exc)
                continue
            runners[name] = Runner(
                agent=agent, app_name=_cli_name or name, session_service=svc,
            )

    # ---- System endpoints -----------------------------------------------

    @app.get("/health")
    async def health():
        return {"status": "ok"}

    @app.get("/version")
    async def version():
        return {"version": "0.1.0"}

    @app.get("/list-apps")
    async def list_apps():
        return list(runners.keys())

    @app.get("/cli-info")
    async def cli_info():
        """Return CLI name for frontend session management (Doc 21)."""
        return {"cli_name": _cli_name or ""}

    # ---- Agent info ------------------------------------------------------

    @app.get("/apps/{app_name}")
    async def get_app_info(app_name: str):
        runner = _get_runner(app_name)
        agent = runner.agent
        return {
            "name": agent.name,
            "description": agent.description or "",
            "sub_agents": [a.name for a in (agent.sub_agents or [])],
        }

    # ---- Agent CRUD (template system) ------------------------------------

    @app.get("/templates")
    async def get_templates():
        from ..templates import list_templates
        return list_templates()

    @app.post("/agents/create")
    async def create_agent(req: CreateAgentRequest):
        if _agents_dir is None:
            raise HTTPException(400, "Agent creation requires agents_dir mode")
        from ..templates import scaffold_agent, AGENT_NAME_RE
        if not AGENT_NAME_RE.match(req.name):
            raise HTTPException(
                400,
                f"Invalid agent name '{req.name}': must match [a-z][a-z0-9_]{{0,49}}",
            )
        if req.name in runners:
            raise HTTPException(409, f"Agent '{req.name}' already exists")
        try:
            target = scaffold_agent(req.name, req.template, _agents_dir)
        except ValueError as exc:
            raise HTTPException(400, str(exc))
        except FileExistsError as exc:
            raise HTTPException(409, str(exc))
        except Exception as exc:
            raise HTTPException(500, f"Failed to create agent: {exc}")
        # Hot reload: load new agent into runners
        try:
            loader = _loader or AgentLoader(_agents_dir)
            agent = loader.load_agent(req.name)
            runners[req.name] = Runner(
                agent=agent, app_name=_cli_name or req.name, session_service=svc,
            )
        except Exception as exc:
            shutil.rmtree(target, ignore_errors=True)
            raise HTTPException(500, f"Agent created but failed to load: {exc}")
        return {"name": req.name, "status": "created"}

    @app.delete("/agents/{agent_name}")
    async def delete_agent(agent_name: str):
        if _agents_dir is None:
            raise HTTPException(400, "Agent deletion requires agents_dir mode")
        from ..templates import AGENT_NAME_RE
        if not AGENT_NAME_RE.match(agent_name):
            raise HTTPException(400, "Invalid agent name")
        if agent_name not in runners:
            raise HTTPException(404, f"Agent '{agent_name}' not found")
        runners.pop(agent_name)
        # Clean sys.modules cache
        keys_to_remove = [
            k for k in sys.modules
            if agent_name in k and k.startswith("_adk_agents_")
        ]
        for k in keys_to_remove:
            sys.modules.pop(k, None)
        # Remove agent directory
        agent_dir = _agents_dir / agent_name
        if agent_dir.is_dir():
            shutil.rmtree(agent_dir, ignore_errors=True)
        # Clear loader cache
        if _loader and agent_name in _loader._agent_envs:
            del _loader._agent_envs[agent_name]
        return {"name": agent_name, "status": "deleted"}

    @app.get("/agents/{agent_name}/aisops")
    async def list_agent_aisops(agent_name: str):
        if _agents_dir is None:
            raise HTTPException(400, "Requires agents_dir mode")
        if agent_name not in runners:
            raise HTTPException(404, f"Agent '{agent_name}' not found")
        aisop_dir = _agents_dir / agent_name / "aiap"
        if not aisop_dir.is_dir():
            return []
        return _scan_aisops(aisop_dir)

    @app.post("/agents/{agent_name}/aisops/delete")
    async def delete_agent_aisop(agent_name: str, req: DeleteAisopRequest):
        if _agents_dir is None:
            raise HTTPException(400, "Requires agents_dir mode")
        if agent_name not in runners:
            raise HTTPException(404, f"Agent '{agent_name}' not found")
        p = req.path.replace("\\", "/")
        if not p.startswith("aiap/"):
            raise HTTPException(400, "Invalid AISOP path")
        if ".." in p:
            raise HTTPException(400, "Path traversal not allowed")
        # Resolve and verify within agent directory
        target = (_agents_dir / agent_name / p).resolve()
        agent_dir = (_agents_dir / agent_name).resolve()
        if not str(target).startswith(str(agent_dir)):
            raise HTTPException(400, "Path outside agent directory")
        # Case 1: Delete a single file
        if p.endswith(".aisop.json"):
            if p.split("/")[-1] == "main.aisop.json":
                raise HTTPException(400, "Cannot delete main.aisop.json (entry point)")
            if not target.is_file():
                raise HTTPException(404, f"AISOP file not found: {req.path}")
            target.unlink()
            return {"path": req.path, "status": "deleted"}
        # Case 2: Delete an entire group folder (e.g. "aiap/code_creator_aiap")
        if not target.is_dir():
            raise HTTPException(404, f"AISOP group not found: {req.path}")
        shutil.rmtree(target, ignore_errors=True)
        return {"path": req.path, "status": "deleted"}

    @app.get("/aisop-library")
    async def list_aiap_store():
        if _agents_dir is None:
            raise HTTPException(400, "Requires agents_dir mode")
        lib_dir = _agents_dir / "aiap_store"
        if not lib_dir.is_dir():
            return []
        return _scan_aisops(lib_dir)

    @app.post("/agents/{agent_name}/aisops/add-from-library")
    async def add_aisop_from_library(agent_name: str, req: AddFromLibraryRequest):
        if _agents_dir is None:
            raise HTTPException(400, "Requires agents_dir mode")
        if agent_name not in runners:
            raise HTTPException(404, f"Agent '{agent_name}' not found")
        if ".." in req.group or "/" in req.group or "\\" in req.group:
            raise HTTPException(400, "Invalid group name")
        src = _agents_dir / "aiap_store" / req.group
        if not src.is_dir():
            raise HTTPException(404, f"Library package '{req.group}' not found")
        dest = _agents_dir / agent_name / "aiap" / req.group
        if dest.exists():
            raise HTTPException(409, f"'{req.group}' already exists in this agent")
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(src, dest)
        return {"group": req.group, "status": "added"}

    # ---- AIAP Store endpoints -------------------------------------------

    @app.get("/aiap-store/programs")
    async def list_store_programs():
        """List available AIAP programs from the GitHub AIAP-Store repo."""
        import logging
        _log = logging.getLogger(__name__)

        now = time.time()
        if _store_cache["data"] is not None and now < _store_cache["expires"]:
            return _store_cache["data"]

        try:
            req = urllib.request.Request(
                GITHUB_STORE_API,
                headers={"Accept": "application/vnd.github.v3+json",
                         "User-Agent": "SoulBot/1.0"},
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                contents = json.loads(resp.read().decode())
        except (urllib.error.URLError, urllib.error.HTTPError) as exc:
            _log.warning("Failed to fetch AIAP Store listing: %s", exc)
            raise HTTPException(502, f"Failed to reach GitHub API: {exc}")

        programs = []
        for item in contents:
            if item.get("type") != "dir":
                continue
            name = item["name"]
            if not name.endswith("_aiap"):
                continue
            meta = _fetch_aiap_metadata(name, _log)
            programs.append(meta)

        _store_cache["data"] = programs
        _store_cache["expires"] = now + CACHE_TTL
        return programs

    def _fetch_aiap_metadata(program_name: str, _log) -> dict:
        """Fetch and parse AIAP.md YAML frontmatter for a program."""
        import yaml

        meta = {
            "name": program_name,
            "version": "",
            "pattern": "",
            "summary": "",
            "tools": [],
            "quality_grade": "",
            "quality_score": 0.0,
            "trust_level": "",
            "module_count": 0,
            "github_url": f"https://github.com/{GITHUB_REPO}/tree/main/aiap_store/{program_name}",
        }

        try:
            url = f"{GITHUB_RAW}/{program_name}/AIAP.md"
            req = urllib.request.Request(
                url, headers={"User-Agent": "SoulBot/1.0"}
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                content = resp.read().decode()
        except (urllib.error.URLError, urllib.error.HTTPError):
            _log.debug("No AIAP.md found for %s", program_name)
            return meta

        # Parse YAML frontmatter (between --- delimiters)
        try:
            if content.startswith("---"):
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    data = yaml.safe_load(parts[1])
                    if isinstance(data, dict):
                        meta["name"] = data.get("name", program_name)
                        meta["version"] = str(data.get("version", ""))
                        meta["pattern"] = str(data.get("pattern", ""))
                        meta["summary"] = str(data.get("summary", ""))

                        # trust_level.level → "T3"
                        tl = data.get("trust_level")
                        if isinstance(tl, dict) and "level" in tl:
                            meta["trust_level"] = f"T{tl['level']}"
                        elif isinstance(tl, (int, str)):
                            meta["trust_level"] = f"T{tl}"

                        # quality.grade / quality.weighted_score
                        quality = data.get("quality")
                        if isinstance(quality, dict):
                            meta["quality_grade"] = str(quality.get("grade", ""))
                            try:
                                meta["quality_score"] = float(quality.get("weighted_score", 0))
                            except (ValueError, TypeError):
                                pass

                        # tools[] → extract name from each
                        tools = data.get("tools")
                        if isinstance(tools, list):
                            meta["tools"] = [
                                t["name"] for t in tools
                                if isinstance(t, dict) and "name" in t
                            ]

                        # modules[] → count
                        modules = data.get("modules")
                        if isinstance(modules, list):
                            meta["module_count"] = len(modules)
        except Exception as exc:
            _log.debug("Failed to parse AIAP.md YAML for %s: %s", program_name, exc)

        return meta

    @app.post("/aiap-store/download")
    async def download_from_store(req: DownloadFromStoreRequest):
        """Download an AIAP program from GitHub to local aiap_store/ library."""
        import logging
        _log = logging.getLogger(__name__)

        if _agents_dir is None:
            raise HTTPException(400, "Requires agents_dir mode")

        if ".." in req.program or "/" in req.program or "\\" in req.program:
            raise HTTPException(400, "Invalid program name")
        if not req.program.endswith("_aiap"):
            raise HTTPException(400, "Program name must end with '_aiap'")

        dest = _agents_dir / "aiap_store" / req.program
        if dest.exists():
            raise HTTPException(409, f"'{req.program}' already exists in local library")

        try:
            files_count = _download_github_dir(
                f"{GITHUB_STORE_API}/{req.program}", dest, _log
            )
        except Exception as exc:
            if dest.exists():
                shutil.rmtree(dest, ignore_errors=True)
            _log.error("Failed to download %s: %s", req.program, exc)
            raise HTTPException(502, f"Failed to download from GitHub: {exc}")

        return {
            "program": req.program,
            "files_downloaded": files_count,
            "status": "downloaded",
        }

    @app.post("/aiap-store/install")
    async def install_from_store(req: InstallFromStoreRequest):
        """Download an AIAP program from GitHub and install to agent's aiap/ dir."""
        import logging
        _log = logging.getLogger(__name__)

        if _agents_dir is None:
            raise HTTPException(400, "Requires agents_dir mode")
        if req.agent_name not in runners:
            raise HTTPException(404, f"Agent '{req.agent_name}' not found")

        if ".." in req.program or "/" in req.program or "\\" in req.program:
            raise HTTPException(400, "Invalid program name")
        if not req.program.endswith("_aiap"):
            raise HTTPException(400, "Program name must end with '_aiap'")

        dest = _agents_dir / req.agent_name / "aiap" / req.program
        if dest.exists():
            raise HTTPException(
                409, f"'{req.program}' already exists in agent '{req.agent_name}'"
            )

        try:
            files_count = _download_github_dir(
                f"{GITHUB_STORE_API}/{req.program}", dest, _log
            )
        except Exception as exc:
            if dest.exists():
                shutil.rmtree(dest, ignore_errors=True)
            _log.error("Failed to install %s: %s", req.program, exc)
            raise HTTPException(502, f"Failed to download from GitHub: {exc}")

        return {
            "program": req.program,
            "agent": req.agent_name,
            "files_installed": files_count,
            "status": "installed",
        }

    def _download_github_dir(api_url: str, dest: Path, _log) -> int:
        """Recursively download a directory from GitHub API."""
        req = urllib.request.Request(
            api_url,
            headers={
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": "SoulBot/1.0",
            },
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            items = json.loads(resp.read().decode())

        dest.mkdir(parents=True, exist_ok=True)
        count = 0

        for item in items:
            name = item["name"]
            if item["type"] == "file":
                download_url = item.get("download_url")
                if not download_url:
                    continue
                file_req = urllib.request.Request(
                    download_url,
                    headers={"User-Agent": "SoulBot/1.0"},
                )
                with urllib.request.urlopen(file_req, timeout=15) as file_resp:
                    file_content = file_resp.read()
                (dest / name).write_bytes(file_content)
                count += 1
                _log.debug("Downloaded: %s", dest / name)
            elif item["type"] == "dir":
                sub_url = item.get("url", f"{api_url}/{name}")
                count += _download_github_dir(sub_url, dest / name, _log)

        return count

    # ---- Session CRUD ---------------------------------------------------

    @app.post("/apps/{app_name}/users/{user_id}/sessions")
    async def create_session(app_name: str, user_id: str, req: CreateSessionRequest):
        _get_runner(app_name)  # validate app exists
        # Use cli_name as the real app_name for DB (Doc 21)
        real_app = _cli_name or app_name
        session = await svc.create_session(
            real_app, user_id,
            agent_name=app_name,
            session_id=req.session_id,
            state=req.state,
            title=req.title,
        )
        return _session_summary(session)

    @app.get("/apps/{app_name}/users/{user_id}/sessions")
    async def list_sessions(app_name: str, user_id: str):
        _get_runner(app_name)
        real_app = _cli_name or app_name
        sessions = await svc.list_sessions(real_app, user_id, agent_name=app_name)
        return [_session_summary(s) for s in sessions]

    @app.get("/apps/{app_name}/users/{user_id}/sessions/{session_id}")
    async def get_session(app_name: str, user_id: str, session_id: str):
        _get_runner(app_name)
        real_app = _cli_name or app_name
        session = await svc.get_session(real_app, user_id, session_id)
        if session is None:
            raise HTTPException(404, f"Session '{session_id}' not found")
        return _session_detail(session)

    @app.delete("/apps/{app_name}/users/{user_id}/sessions/{session_id}")
    async def delete_session(app_name: str, user_id: str, session_id: str):
        _get_runner(app_name)
        real_app = _cli_name or app_name
        await svc.delete_session(real_app, user_id, session_id)
        return {"status": "deleted"}

    # ---- Execution endpoints --------------------------------------------

    @app.post("/run")
    async def run_agent(req: RunAgentRequest):
        runner = _get_runner(req.app_name)
        message = _extract_message(req)

        events = []
        async for event in runner.run(
            user_id=req.user_id,
            session_id=req.session_id,
            message=message,
        ):
            if not event.partial:
                events.append(json.loads(event.model_dump_json()))
        return events

    @app.post("/run_sse")
    async def run_agent_sse(req: RunAgentRequest):
        from sse_starlette.sse import EventSourceResponse
        from ..agents.invocation_context import RunConfig

        runner = _get_runner(req.app_name)
        message = _extract_message(req)

        async def event_generator():
            async for event in runner.run(
                user_id=req.user_id,
                session_id=req.session_id,
                message=message,
                run_config=RunConfig(streaming=True),
            ):
                yield {"data": event.model_dump_json()}

        return EventSourceResponse(event_generator())

    # ---- Schedule endpoints (Doc 17.5) -----------------------------------

    if schedule_service is not None:
        @app.get("/schedule/list")
        async def schedule_list(status: Optional[str] = None):
            return schedule_service.list(status=status)

        @app.get("/schedule/{entry_id}")
        async def schedule_get(entry_id: str):
            try:
                return schedule_service.get(id=entry_id)
            except ValueError as exc:
                raise HTTPException(404, str(exc))

    # ---- Heartbeat endpoints (Doc 12) ------------------------------------

    if heartbeat_store is not None:
        @app.get("/heartbeat/history")
        async def heartbeat_history(
            agent: Optional[str] = None,
            limit: int = Query(default=50, ge=1, le=1000),
            offset: int = Query(default=0, ge=0),
        ):
            return heartbeat_store.query(agent_name=agent, limit=limit, offset=offset)

        @app.get("/heartbeat/count")
        async def heartbeat_count(agent: Optional[str] = None):
            return {"count": heartbeat_store.count(agent_name=agent)}

    # ---- Dev Web UI -----------------------------------------------------

    if dev_ui and STATIC_DIR.is_dir():
        @app.get("/")
        async def redirect_to_dev_ui():
            return RedirectResponse("/dev-ui/")

        app.mount(
            "/dev-ui",
            StaticFiles(directory=str(STATIC_DIR), html=True),
            name="dev-ui",
        )

    # ---- Helpers --------------------------------------------------------

    def _get_runner(app_name: str) -> Runner:
        if app_name not in runners:
            raise HTTPException(404, f"App '{app_name}' not found")
        return runners[app_name]

    return app


def _extract_message(req: RunAgentRequest) -> str:
    """Extract plain text from the request message."""
    if req.new_message:
        parts = req.new_message.get("parts", [])
        texts = [p.get("text", "") for p in parts if p.get("text")]
        if texts:
            return " ".join(texts)
    return ""


def _session_summary(session) -> dict:
    return {
        "id": session.id,
        "app_name": session.app_name,
        "user_id": session.user_id,
        "agent_name": session.agent_name,
        "last_agent": session.last_agent,
        "title": session.title,
        "created_at": session.created_at,
        "last_update_time": session.last_update_time,
    }


def _session_detail(session) -> dict:
    return {
        "id": session.id,
        "app_name": session.app_name,
        "user_id": session.user_id,
        "agent_name": session.agent_name,
        "last_agent": session.last_agent,
        "title": session.title,
        "created_at": session.created_at,
        "state": dict(session.state),
        "events": [json.loads(e.model_dump_json()) for e in session.events],
        "last_update_time": session.last_update_time,
    }


def _scan_aisops(aisop_dir: Path) -> list[dict]:
    """Scan an aisop/ directory for .aisop.json files and extract summaries."""
    import logging
    _log = logging.getLogger(__name__)
    results: list[dict] = []

    for f in sorted(aisop_dir.rglob("*.aisop.json")):
        rel = f.relative_to(aisop_dir.parent)
        # Determine group: if file is nested in a subfolder under aisop/
        parts = rel.parts  # e.g. ("aiap", "sub_group", "main.aisop.json")
        group = parts[1] if len(parts) > 2 else None

        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            sys_content = data[0]["content"] if isinstance(data, list) and data else {}
        except Exception as exc:
            _log.warning("Skipping AISOP %s: %s", f, exc)
            continue

        results.append({
            "path": str(rel).replace("\\", "/"),
            "group": group,
            "name": sys_content.get("name", f.stem),
            "version": sys_content.get("version", ""),
            "summary": sys_content.get("summary", ""),
            "protocol": sys_content.get("protocol", ""),
            "tools": sys_content.get("tools", []),
        })

    return results
