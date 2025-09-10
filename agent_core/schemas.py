from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional

class Spec(BaseModel):
    goal: str
    constraints: Dict[str, Any] = Field(default_factory=dict)
    context: Dict[str, Any] = Field(default_factory=dict)

class PlanStep(BaseModel):
    tool: str
    params: Dict[str, Any] = Field(default_factory=dict)
    success_criteria: Optional[str] = None

class Plan(BaseModel):
    steps: List[PlanStep]
    notes: Optional[str] = None

class EvidenceItem(BaseModel):
    step_index: int
    tool: str
    input: Dict[str, Any]
    output: Any
    score: float
    info_gain: float

class ExecutionResult(BaseModel):
    success: bool
    outputs: Dict[str, Any]
    evidence: List[EvidenceItem]
    telemetry: Dict[str, Any]
