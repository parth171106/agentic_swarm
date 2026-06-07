# STUB — Implemented by: workstream/2a-memory-system
class KnowledgeGraph:
    async def upsert_node(self, client, entity_type: str, label: str, swarm_run_id: str) -> str: raise NotImplementedError()
    async def upsert_edge(self, client, source_id: str, target_id: str, relationship_type: str, weight: int = 1) -> None: raise NotImplementedError()
    async def get_node_degree(self, client, node_id: str) -> int: raise NotImplementedError()
    async def path_query(self, client, start_label: str, max_degrees: int = 2) -> list[dict]: raise NotImplementedError()
