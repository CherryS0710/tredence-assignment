from typing import Any, Dict, Optional
from pydantic import BaseModel

class NodeDef(BaseModel):
    name: str
    func: str
    config: Optional[Dict[str, Any]] = {}

class GraphCreateRequest(BaseModel):
    nodes: Dict[str, NodeDef]
    edges: Dict[str, Any]
    entrypoint: str

class GraphCreateResponse(BaseModel):
    graph_id: str

class RunRequest(BaseModel):
    graph_id: str
    initial_state: Optional[Dict[str, Any]] = {}

class RunResponse(BaseModel):
    run_id: str
    status: str

class RunStateResponse(BaseModel):
    run_id: str
    status: str
    state: Dict[str, Any]
    log: list
