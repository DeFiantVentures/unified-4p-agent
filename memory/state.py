from typing import Any, Dict

class Telemetry:
    def __init__(self):
        self.last = {}
    def record(self, **kwargs):
        self.last.update(kwargs)
    def get(self) -> Dict[str, Any]:
        return dict(self.last)

telemetry = Telemetry()
