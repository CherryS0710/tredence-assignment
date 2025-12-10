from typing import Dict, Any
import asyncio

TOOLS = {}

def register(name):
    def _wrap(fn):
        TOOLS[name] = fn
        return fn
    return _wrap

@register("detect_smells")
def detect_smells(code: str) -> Dict[str, Any]:
    issues = code.count("TODO") + sum(1 for line in code.splitlines() if len(line) > 120)
    return {"issues": issues}

@register("compute_complexity")
def compute_complexity(func_source: str) -> Dict[str, Any]:
    keywords = ["if ", "for ", "while ", "try:", "except", "else:"]
    cnt = sum(func_source.count(k) for k in keywords)
    return {"complexity_score": cnt}

@register("suggest_improvement")
def suggest_improvement(state: Dict[str, Any]) -> Dict[str, Any]:
    suggestions = []
    if state.get("issues", 0) > 0:
        suggestions.append("Address TODOs and long lines.")
    if state.get("complexity_score", 0) > 3:
        suggestions.append("Refactor large functions into smaller ones.")
    return {"suggestions": suggestions}

@register("long_running_check")
async def long_running_check(payload: Dict[str, Any]) -> Dict[str, Any]:
    await asyncio.sleep(0.2)
    return {"checked": True}
