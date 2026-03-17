"""
AISIP Runtime — AI Standard Instruction Protocol

Protocol (two sentences):
  1. JSON defines the flow
  2. AI uses {} to read the next node

This is the complete, standalone runtime. Zero dependencies beyond Python stdlib.

Supported node types:
  - process:  Execute task, then go to next
  - decision: AI outputs branch value, Runtime routes
  - parallel: Fork into multiple nodes, join when all done
  - delegate: Call a sub-flow, return when it completes
  - end:      Terminate the flow

Error handling:
  - Any node can define "error" field → Runtime routes there on failure
  - Default: skip failed node and continue
"""

import json
import re

from ..aisop_aisip.extensions import infer_node_type, AisopExtensions


# ── Parse AI output ──────────────────────────────────────────

def parse_command(ai_output: str) -> dict | None:
    """Extract the last {method: ...} JSON block from AI output text."""
    positions = [m.start() for m in re.finditer(r'\{\s*"?method"?\s*:', ai_output)]
    if not positions:
        return None

    start = positions[-1]
    depth = 0
    end = start
    for i in range(start, len(ai_output)):
        if ai_output[i] == '{':
            depth += 1
        elif ai_output[i] == '}':
            depth -= 1
            if depth == 0:
                end = i + 1
                break

    raw = ai_output[start:end]

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass

    fixed = re.sub(r'(?<!["\w])(\w+)\s*:', r'"\1":', raw)
    fixed = fixed.replace("'", '"')
    try:
        return json.loads(fixed)
    except json.JSONDecodeError:
        return None


# ── Flow Executor (state machine) ────────────────────────────

class FlowExecutor:
    """AISIP state machine — full control flow support."""

    def __init__(self, flow: dict, functions: dict = None):
        self.flow = flow
        # Support "nodes" (legacy), "main" (AISOP-aligned), or "T0" (V2) keys
        if "nodes" not in flow:
            if "T0" in flow:
                flow["nodes"] = flow["T0"]
            elif "main" in flow:
                flow["nodes"] = flow["main"]
        self.functions = functions or {}  # {node_name: task_body}
        self.state = {}           # {node_name: result}
        self.trace = []           # execution trace
        self.loops = {}           # loop counters
        self.stack = []           # delegate stack: [(parent_flow, parent_functions, return_node)]
        self.pending = {}         # parallel join: {join_node: {waiting: set, done: {}}}
        self.sub_flows = {}       # sub-flow registry: {name: flow_dict}

    def register_sub_flow(self, name: str, flow: dict):
        """Register a sub-flow for delegate nodes."""
        self.sub_flows[name] = flow

    def start(self) -> dict:
        start_node = self.flow.get("start") or next(iter(self.flow["nodes"]), None)
        return self._pack(start_node)

    def done(self, node: str, result: dict) -> dict:
        self.state[node] = result
        self.trace.append(node)

        nd = self.flow["nodes"].get(node, {})
        node_type = nd.get("type") or infer_node_type(nd)

        # ── Extension: on_error from functions layer ──────
        func_body = self.functions.get(node, {})
        if isinstance(func_body, dict):
            _, exts = AisopExtensions.extract(func_body)
        else:
            exts = {}

        # ── Error handling (node-level or function-level) ─
        if result.get("error"):
            # Try function-layer on_error first
            if "on_error" in exts:
                target = AisopExtensions.resolve_error_target(
                    str(result["error"]), exts["on_error"])
                if target:
                    return self._pack(target)
            # Fallback to node-level error routing
            if nd.get("error"):
                return self._pack(nd["error"])

        # ── End node ──────────────────────────────────────
        if node_type == "end":
            # If inside a delegate, pop the stack and return
            if self.stack:
                parent_flow, parent_functions, return_node = self.stack.pop()
                self.flow = parent_flow
                self.functions = parent_functions
                return self._pack(return_node)
            return {"status": "complete", "trace": self.trace}

        # ── Resolve next nodes ────────────────────────────
        nxt = self._next(node, result)
        if not nxt:
            if self.stack:
                parent_flow, parent_functions, return_node = self.stack.pop()
                self.flow = parent_flow
                self.functions = parent_functions
                return self._pack(return_node)
            return {"status": "complete", "trace": self.trace}

        # ── Delegate node ─────────────────────────────────
        if node_type == "delegate":
            sub_name = nd.get("delegate_to", "")
            sub_flow = self.sub_flows.get(sub_name)
            if not sub_flow:
                return {"error": f"Sub-flow not found: {sub_name}"}
            return_node = nxt[0] if nxt else None
            self.stack.append((self.flow, self.functions, return_node))
            if "task" in sub_flow:
                self.flow = sub_flow["task"]
                self.functions = sub_flow.get("functions", {})
            else:
                self.flow = sub_flow
                self.functions = {}
            sub_start = self.flow.get("start") or next(iter(self.flow["nodes"]), None)
            return self._pack(sub_start)

        # ── Single next ───────────────────────────────────
        if len(nxt) == 1:
            target = nxt[0]
            target_nd = self.flow["nodes"].get(target, {})

            # Check if target is a join node (convergence)
            # Infer type — works with or without explicit "type" field
            target_type = target_nd.get("type") or infer_node_type(target_nd)
            if target_type == "join":
                wait_for = set(target_nd.get("wait_for", []))
                if target not in self.pending:
                    self.pending[target] = {"waiting": wait_for, "done": {}}
                self.pending[target]["done"][node] = result
                remaining = self.pending[target]["waiting"] - set(self.pending[target]["done"].keys())
                if remaining:
                    return {"status": "waiting", "node": target, "remaining": list(remaining)}
                # All arrived — proceed past the join
                join_result = self.pending.pop(target)
                self.state[target] = join_result["done"]
                self.trace.append(target)
                join_nxt = target_nd.get("next", [])
                if not join_nxt:
                    return {"status": "complete", "trace": self.trace}
                return self._pack(join_nxt[0])

            return self._pack(target)

        # ── Parallel fork ─────────────────────────────────
        return {"parallel": True, "nodes": [self._pack(n) for n in nxt]}

    def _next(self, node: str, result: dict) -> list:
        nd = self.flow["nodes"].get(node, {})
        node_type = nd.get("type") or infer_node_type(nd)

        if node_type == "end":
            return []

        if node_type == "decision":
            branch = result.get("branch", "")
            targets = nd.get("branches", {})
            target = targets.get(branch, list(targets.values())[0] if targets else None)
            if not target:
                return []
            # Loop protection
            key = f"{node}->{target}"
            if target in self.trace:
                self.loops[key] = self.loops.get(key, 0) + 1
                if self.loops[key] >= 3:
                    others = [v for v in targets.values() if v != target]
                    return [others[0]] if others else []
            return [target]

        if node_type == "delegate":
            return nd.get("next", [])

        return nd.get("next", [])

    def _pack(self, node_name: str) -> dict:
        nd = self.flow["nodes"].get(node_name, {})
        # Task lookup: node inline "task" → top-level "functions" → empty
        task = nd.get("task") or self.functions.get(node_name, {})
        info = {
            "node": node_name,
            "task": task,
            "upstream": {n: self.state[n] for n in self.trace[-3:] if n in self.state}
        }
        pack_type = nd.get("type") or infer_node_type(nd)
        if pack_type == "decision" and nd.get("branches"):
            info["branches"] = list(nd["branches"].keys())
        return info


# ── Main loop ────────────────────────────────────────────────

SYSTEM_PROMPT = (
    "You are a program executor. You execute nodes one by one.\n"
    "RULES:\n"
    '1. To start: {"method": "start"}\n'
    '2. After completing a node: {"method": "done", "node": "NodeName", "result": {your output}}\n'
    '3. For decision nodes, you MUST include "branch" key in result with one of the allowed values shown in the task.\n'
    '4. If a node fails, include "error" key in result: {"method": "done", "node": "X", "result": {"error": "reason"}}\n'
    '5. If you receive parallel nodes, execute each one and submit done for each.\n'
    '6. If you receive a "waiting" status, just wait for the next instruction.\n'
    "7. Every response MUST end with exactly one JSON {} command.\n"
    "8. Keep responses short. Focus on the task."
)


def run_flow(flow_json: dict, ai_fn, user_input: str, sub_flows: dict = None) -> dict:
    """
    Run an AISIP flow with an AI function.

    ai_fn(prompt: str) -> str
    sub_flows: {"name": flow_dict} for delegate nodes

    Returns: {"trace": [...], "state": {...}}
    """
    executor = FlowExecutor(flow_json["task"], flow_json.get("functions", {}))

    if sub_flows:
        for name, sf in sub_flows.items():
            executor.register_sub_flow(name, sf)

    prompt = f"{SYSTEM_PROMPT}\n\nUser request: {user_input}\nNow begin."

    for _ in range(50):
        ai_output = ai_fn(prompt)

        cmd = parse_command(ai_output)
        if not cmd:
            break

        method = cmd.get("method")
        if method == "start":
            resp = executor.start()
        elif method == "done":
            resp = executor.done(cmd.get("node", ""), cmd.get("result", {}))
        else:
            resp = {"error": f"Unknown method: {method}"}

        prompt = json.dumps(resp, ensure_ascii=False)

        if resp.get("status") == "complete":
            break
        if resp.get("status") == "waiting":
            continue

    return {"trace": executor.trace, "state": executor.state}
