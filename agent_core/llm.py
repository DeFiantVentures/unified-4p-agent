# Rule-based Seq2Seq planner stub. Replace with a real LLM later.
from typing import List
from agent_core.schemas import Spec, Plan, PlanStep

DEFAULT_PIPELINE = [
    {"tool": "inspect_spec", "params": {}},
    {"tool": "sample_rows", "params": {"n": 5}},
    {"tool": "validate_schema", "params": {}},
    {"tool": "transform", "params": {"op": "dedupe"}},
    {"tool": "summarize", "params": {"metric": "basic"}},
]

def seq2seq_plan(spec: Spec) -> Plan:
    steps: List[PlanStep] = []
    if spec.constraints.get("quick"):
        pipeline = DEFAULT_PIPELINE[:3] + [{"tool": "summarize", "params": {"metric": "basic"}}]
    else:
        pipeline = DEFAULT_PIPELINE
    if spec.constraints.get("export"):
        pipeline.append({"tool": "export", "params": {"format": "csv"}})
    for block in pipeline:
        steps.append(PlanStep(tool=block["tool"], params=block.get("params", {})))
    return Plan(steps=steps, notes="Rule-based plan; replace with real Seq2Seq later.")
