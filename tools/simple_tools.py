from typing import Dict, Any, Tuple
from tools.base import Tool

class InspectSpec(Tool):
    name = "inspect_spec"; cost = 0.5
    def run(self, params: Dict[str, Any], state: Dict[str, Any]) -> Tuple[Dict[str, Any], float]:
        state = dict(state); state.setdefault("inspected", True)
        return state, 0.7

class SampleRows(Tool):
    name = "sample_rows"; cost = 1.0
    def run(self, params: Dict[str, Any], state: Dict[str, Any]) -> Tuple[Dict[str, Any], float]:
        n = params.get("n", 3)
        state = dict(state); state["sample_preview"] = [f"row_{i}" for i in range(n)]
        return state, 0.6

class ValidateSchema(Tool):
    name = "validate_schema"; cost = 1.0
    def run(self, params: Dict[str, Any], state: Dict[str, Any]) -> Tuple[Dict[str, Any], float]:
        state = dict(state); state["schema_ok"] = True
        return state, 0.8

class Transform(Tool):
    name = "transform"; cost = 1.2
    def run(self, params: Dict[str, Any], state: Dict[str, Any]) -> Tuple[Dict[str, Any], float]:
        op = params.get("op", "noop")
        state = dict(state); state.setdefault("transforms", []).append(op)
        return state, 0.75

class Summarize(Tool):
    name = "summarize"; cost = 0.8
    def run(self, params: Dict[str, Any], state: Dict[str, Any]) -> Tuple[Dict[str, Any], float]:
        metric = params.get("metric", "basic")
        state = dict(state); state["summary"] = {"metric": metric, "quality": "ok"}
        return state, 0.65

class Export(Tool):
    name = "export"; cost = 0.5
    def run(self, params: Dict[str, Any], state: Dict[str, Any]) -> Tuple[Dict[str, Any], float]:
        fmt = params.get("format", "csv")
        state = dict(state); state["export_path"] = f"output.{fmt}"
        return state, 0.9
