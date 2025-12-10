from fastapi import FastAPI, BackgroundTasks, HTTPException
from . import storage, engine
from . import tools as tools_module
from .schemas import GraphCreateRequest, GraphCreateResponse, RunRequest, RunResponse, RunStateResponse
from typing import Any, Dict
import uvicorn

app = FastAPI(title="Minimal Workflow Engine")

@app.post("/graph/create", response_model=GraphCreateResponse)
async def create_graph(req: GraphCreateRequest):
    nodes = {}
    for k, node in req.nodes.items():
        nodes[k] = {"name": node.name, "func": node.func, "config": node.config or {}}
    graph_obj = {
        "nodes": nodes,
        "edges": req.edges,
        "entrypoint": req.entrypoint,
        "max_steps": 500
    }
    graph_id = storage.new_graph(graph_obj)
    return {"graph_id": graph_id}

@app.post("/graph/run", response_model=RunResponse)
async def run_graph(req: RunRequest, background_tasks: BackgroundTasks):
    graph = storage.get_graph(req.graph_id)
    if not graph:
        raise HTTPException(status_code=404, detail="graph not found")
    run_id = storage.create_run(req.graph_id, req.initial_state or {})
    background_tasks.add_task(engine.execute_graph, run_id)
    return {"run_id": run_id, "status": "started"}

@app.get("/graph/state/{run_id}", response_model=RunStateResponse)
async def graph_state(run_id: str):
    run = storage.get_run(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="run not found")
    return {
        "run_id": run_id,
        "status": run["status"],
        "state": run["state"],
        "log": run["log"]
    }

@app.get("/tools")
def list_tools() -> Dict[str, Any]:
    return {"tools": list(tools_module.TOOLS.keys())}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
