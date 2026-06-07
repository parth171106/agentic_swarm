# STUB — Implemented by: workstream/2b-llm-adapter-tools
from backend.app.tools.base import SwarmTool

class WebSearchTool(SwarmTool):
    name = "WebSearchTool"
    description = "Searches the web via Serper."
    async def _run(self, input: str) -> str: raise NotImplementedError()
