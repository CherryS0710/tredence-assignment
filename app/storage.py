from typing import Dict, Any
import uuid
from threading import Lock

_lock = Lock()
GRAPHS: Dict[str, Dict[str, Any]] = {}
RUNS: Dict[str, Dict[str, Any]] = {}

def new_graph(graph_obj: Dict[str, Any]) -> str:
    graph_id = str(uuid.uuid4())
    with _lock:
        GRAPHS[graph_id] = graph_obj
    return graph_id

def get_graph(graph_id: str):
    return GRAPHS.get(graph_id)

def create_run(graph_id: str, initial_state: Dict[str, Any]) -> str:
    run_id = str(uuid.uuid4())
    run = {
        "run_id": run_id,
        "graph_id": graph_id,
        "state": dict(initial_state or {}),
        "status": "pending",
        "log": []
    }
    with _lock:
        RUNS[run_id] = run
    return run_id

def update_run(run_id: str, **kwargs):
    with _lock:
        r = RUNS.get(run_id)
        if not r:
            return
        r.update(kwargs)

def append_log(run_id: str, message: str):
    with _lock:
        r = RUNS.get(run_id)
        if r is not None:
            r["log"].append(message)

def get_run(run_id: str):
    return RUNS.get(run_id)
