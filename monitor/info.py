import numpy as np
from typing import Dict, Any

def entropy(probs):
    probs = np.clip(np.asarray(probs, dtype=float), 1e-9, 1.0)
    probs = probs / probs.sum()
    return float(-(probs * np.log2(probs)).sum())

def expected_info_gain(before_entropy: float, posterior_probs):
    after = entropy(posterior_probs)
    return max(0.0, before_entropy - after)

class InfoMonitor:
    def __init__(self):
        self.last_entropy = 1.0

    def score_action(self, action_quality: float) -> Dict[str, Any]:
        posterior = [1 - action_quality, action_quality]
        e_before = self.last_entropy
        e_after = entropy(posterior)
        ig = max(0.0, e_before - e_after)
        self.last_entropy = e_after
        return {"entropy_before": e_before, "entropy_after": e_after, "info_gain": ig}
