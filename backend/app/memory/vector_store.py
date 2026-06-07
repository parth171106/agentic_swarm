# STUB — Implemented by: workstream/2a-memory-system
class VectorStore:
    def get_or_create_collection(self):
        raise NotImplementedError()

    def upsert_memory(self, memory_event_id: str, content: str, metadata: dict) -> None:
        raise NotImplementedError()

    def query_memory(
        self, user_id: str, query_embedding: list[float], n_results: int = 50
    ) -> list[dict]:
        raise NotImplementedError()


# Module-level convenience used by memory.repository
def upsert_memory(memory_event_id: str, content: str, metadata: dict) -> None:
    store = VectorStore()
    return store.upsert_memory(memory_event_id, content, metadata)
