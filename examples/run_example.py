from agent_core.schemas import Spec
from agent_core.llm import seq2seq_plan
from planner.mcts import MCTSPlanner

spec = Spec(
    goal="Summarize and export a dataset with basic validation",
    constraints={"export": True},
    context={"dataset_name": "demo_billing", "rows": 1000},
)

plan = seq2seq_plan(spec)
print("Draft Plan:")
for i, s in enumerate(plan.steps):
    print(f"{i+1:02d}. {s.tool} {s.params}")

planner = MCTSPlanner(plan)
state, evidence = planner.run(root_state=spec.context, iters=60)
print("\nFinal State:", state)
print("\nEvidence:")
for e in evidence:
    print(e)
