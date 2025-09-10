from typing import Dict, Any, Tuple

class Tool:
    name: str = "base"
    cost: float = 1.0
    def run(self, params: Dict[str, Any], state: Dict[str, Any]) -> Tuple[Dict[str, Any], float]:
        """Execute the tool. Return (new_state, quality_score[0..1])."""
        raise NotImplementedError
