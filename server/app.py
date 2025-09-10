from fastapi import FastAPI
from pydantic import BaseModel
from agent_core.schemas import Spec
from agent_core.llm import seq2seq_plan
from planner.mcts import MCTSPlanner
from memory.state import telemetry

app = FastAPI(title="Unified-4P Agent API")

class PlanReq(BaseModel):
    spec: Spec

class ExecReq(BaseModel):
    spec: Spec
    iters: int = 40

@app.post("/plan")
def plan_endpoint(req: PlanReq):
    plan = seq2seq_plan(req.spec)
    telemetry.record(last_plan=plan.model_dump())
    return plan

@app.post("/execute")
def exec_endpoint(req: ExecReq):
    plan = seq2seq_plan(req.spec)
    planner = MCTSPlanner(plan)
    final_state, evidence = planner.run(root_state=req.spec.context, iters=req.iters)
    out = {"success": True, "outputs": final_state, "evidence": evidence, "telemetry": telemetry.get()}
    telemetry.record(last_exec=out)
    return out

@app.get("/telemetry")
def telemetry_endpoint():
    return telemetry.get()
