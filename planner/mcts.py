from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple
import math

from agent_core.schemas import Plan, PlanStep
from tools.registry import build_registry
from monitor.info import InfoMonitor

@dataclass
class Node:
    state: Dict[str, Any]
    depth: int
    step_index: int
    reward_sum: float = 0.0
    visits: int = 0
    parent: Optional['Node'] = None
    action: Optional[PlanStep] = None
    children: List['Node'] = field(default_factory=list)

class MCTSPlanner:
    def __init__(self, plan: Plan, c_ucb: float = 1.2, lambda_ig: float = 0.4, max_depth: Optional[int]=None):
        self.plan = plan
        self.c_ucb = c_ucb
        self.lambda_ig = lambda_ig
        self.tools = build_registry()
        self.monitor = InfoMonitor()
        self.max_depth = max_depth or len(plan.steps)

    def ucb(self, child: Node, parent: Node, info_gain: float) -> float:
        if child.visits == 0:
            return float('inf')
        exploit = child.reward_sum / child.visits
        explore = self.c_ucb * math.sqrt(math.log(parent.visits + 1) / child.visits)
        return exploit + explore + self.lambda_ig * info_gain

    def select(self, node: Node) -> Node:
        current = node
        while current.children and current.depth < self.max_depth:
            best = max(current.children, key=lambda ch: self.ucb(ch, current, info_gain=0.1))
            current = best
        return current

    def expand(self, node: Node):
        if node.depth >= self.max_depth:
            return
        step = self.plan.steps[node.step_index]
        child_state, reward, info = self.simulate_action(node.state, step)
        child = Node(state=child_state, depth=node.depth + 1, step_index=node.step_index + 1, parent=node, action=step)
        child.reward_sum += reward
        child.visits += 1
        node.children.append(child)

    def rollout(self, node: Node) -> float:
        state = dict(node.state)
        total_reward = 0.0
        step_i = node.step_index
        while step_i < min(self.max_depth, len(self.plan.steps)):
            step = self.plan.steps[step_i]
            state, reward, _ = self.simulate_action(state, step)
            total_reward += reward
            step_i += 1
        return total_reward

    def backprop(self, node: Node, reward: float):
        current = node
        while current is not None:
            current.reward_sum += reward
            current.visits += 1
            current = current.parent

    def simulate_action(self, state: Dict[str, Any], step: PlanStep) -> Tuple[Dict[str, Any], float, Dict[str, Any]]:
        tool = self.tools[step.tool]
        new_state, quality = tool.run(step.params, state)
        info = self.monitor.score_action(quality)
        reward = quality - 0.05 * tool.cost + 0.1 * info["info_gain"]
        return new_state, reward, info

    def run(self, root_state: Dict[str, Any], iters: int = 50):
        root = Node(state=root_state, depth=0, step_index=0)
        evidence = []
        best_leaf = root

        for _ in range(iters):
            leaf = self.select(root)
            if leaf.depth < self.max_depth:
                self.expand(leaf)
                target = leaf.children[-1]
            else:
                target = leaf
            reward = self.rollout(target)
            self.backprop(target, reward)
            if target.reward_sum > getattr(best_leaf, "reward_sum", -1):
                best_leaf = target

        # Execute best path to produce evidence
        state = dict(root_state)
        for i, step in enumerate(self.plan.steps[:best_leaf.depth]):
            tool = self.tools[step.tool]
            new_state, quality = tool.run(step.params, state)
            info = self.monitor.score_action(quality)
            evidence.append({
                "step_index": i, "tool": step.tool,
                "input": {"params": step.params, "state_keys": list(state.keys())},
                "output": {k: new_state.get(k) for k in new_state.keys() - state.keys()},
                "score": round(quality, 3),
                "info_gain": round(info["info_gain"], 3)
            })
            state = new_state
        return state, evidence
