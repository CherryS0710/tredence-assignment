import asyncio
from typing import Dict, Any, Callable, Optional
from . import tools, storage

# Helper to resolve function from tools registry
def resolve_func(name: str) -> Optional[Callable]:
    return tools.TOOLS.get(name)

async def run_node(fn, state: Dict[str, Any], config: Dict[str, Any]):
    # If function is async, await it; it may accept full state or specific args.
    try:
        if asyncio.iscoroutinefunction(fn):
            res = await fn(state if config.get("pass_state", True) else config)
        else:
            res = fn(state if config.get("pass_state", True) else config)
        if isinstance(res, dict):
            state.update(res)
        return state
    except Exception as e:
        # propagate error into state
        state.setdefault("_errors", []).append(str(e))
        return state

def eval_condition(cond: str, state: Dict[str, Any]) -> bool:
    # Very simple eval with only 'state' in globals. For assignment usage only.
    try:
        return bool(eval(cond, {"__builtins__": {}}, {"state": state}))
    except Exception:
        return False

async def execute_graph(run_id: str):
    run = storage.get_run(run_id)
    if not run:
        return
    graph = storage.get_graph(run["graph_id"])
    if not graph:
        storage.update_run(run_id, status="error")
        storage.append_log(run_id, f"graph not found")
        return

    state = run["state"]
    entry = graph.get("entrypoint")
    edges = graph.get("edges", {})
    nodes = graph.get("nodes", {})

    current = entry
    storage.update_run(run_id, status="running")
    storage.append_log(run_id, f"starting run at {current}")

    steps = 0
    max_steps = graph.get("max_steps", 500)

    while current and steps < max_steps:
        steps += 1
        ndef = nodes.get(current)
        if not ndef:
            storage.append_log(run_id, f"node '{current}' not found; stopping")
            break

        storage.append_log(run_id, f"running node: {current}")
        func_name = ndef.get("func")
        config = ndef.get("config", {})
        fn = resolve_func(func_name)
        if not fn:
            storage.append_log(run_id, f"function '{func_name}' not found for node '{current}'; stopping")
            storage.update_run(run_id, status="error")
            break

        # run node (allow async)
        await run_node(fn, state, config)
        storage.append_log(run_id, f"state after {current}: {state}")

        # determine next
        edge = edges.get(current)
        next_node = None
        if edge is None:
            storage.append_log(run_id, f"no edge from {current}; finishing")
            next_node = None
        elif isinstance(edge, str):
            next_node = edge
        elif isinstance(edge, list):
            for branch in edge:
                cond = branch.get("cond", "False")
                if eval_condition(cond, state):
                    next_node = branch.get("next")
                    break
        elif isinstance(edge, dict):
            cond = edge.get("cond", "False")
            if eval_condition(cond, state):
                next_node = edge.get("next")
            else:
                next_node = edge.get("else")
        else:
            next_node = None

        storage.update_run(run_id, state=state)
        if not next_node:
            storage.append_log(run_id, f"no next node -> stopping at {current}")
            break

        current = next_node

    if steps >= max_steps:
        storage.update_run(run_id, status="failed")
        storage.append_log(run_id, "max steps reached; possible infinite loop")
    else:
        storage.update_run(run_id, status="finished")
        storage.append_log(run_id, "run finished")
