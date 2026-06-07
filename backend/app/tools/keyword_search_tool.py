# STUB — Implemented by: workstream/2b-llm-adapter-tools
from backend.app.tools.base import SwarmTool

class KeywordSearchTool(SwarmTool):
    name = "KeywordSearchTool"
    description = "Full-text Postgres keyword search."
    async def _run(self, input: str) -> str: raise NotImplementedError()
