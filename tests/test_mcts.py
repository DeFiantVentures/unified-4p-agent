from agent_core.schemas import Spec
from agent_core.llm import seq2seq_plan
from planner.mcts import MCTSPlanner


def test_basic_run():
    spec = Spec(goal="demo", constraints={"export": True}, context={})
    plan = seq2seq_plan(spec)
    planner = MCTSPlanner(plan)
    state, evidence = planner.run(root_state=spec.context, iters=10)
    assert isinstance(state, dict)
    assert len(evidence) >= 1
