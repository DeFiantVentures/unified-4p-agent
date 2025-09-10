from typing import Dict
from tools.base import Tool
from tools.simple_tools import InspectSpec, SampleRows, ValidateSchema, Transform, Summarize, Export

def build_registry() -> Dict[str, Tool]:
    tools = [InspectSpec(), SampleRows(), ValidateSchema(), Transform(), Summarize(), Export()]
    return {t.name: t for t in tools}
