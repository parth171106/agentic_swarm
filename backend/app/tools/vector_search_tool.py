# STUB — Implemented by: workstream/2b-llm-adapter-tools
from backend.app.tools.base import SwarmTool


class VectorSearchTool(SwarmTool):
    name = "VectorSearchTool"
    description = "RAG vector retrieval query."

    async def _run(self, input: str) -> str:
        raise NotImplementedError()
