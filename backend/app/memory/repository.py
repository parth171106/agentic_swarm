# STUB — Implemented by: workstream/2a-memory-system
class SupabaseRepository:
    async def insert_swarm_run(self, client, data: dict) -> dict:
        raise NotImplementedError()

    async def update_swarm_run_status(
        self, client, run_id: str, status: str, output_summary: str | None = None
    ) -> dict:
        raise NotImplementedError()

    async def get_swarm_run(self, client, run_id: str) -> dict | None:
        raise NotImplementedError()

    async def insert_memory_event(self, client, data: dict) -> dict:
        raise NotImplementedError()

    async def insert_memory_entity(self, client, data: dict) -> dict:
        raise NotImplementedError()

    async def search_memory_keyword(
        self, client, user_id: str, query: str, limit: int = 50
    ) -> list[dict]:
        raise NotImplementedError()

    async def insert_audit_log(self, client, data: dict) -> dict:
        raise NotImplementedError()

    async def insert_approval_request(self, client, data: dict) -> dict:
        raise NotImplementedError()

    async def update_approval_request(
        self, client, request_id: str, status: str, rejection_reason: str | None = None
    ) -> dict:
        raise NotImplementedError()


# Module-level convenience wrappers used by crew_executor
_repo = SupabaseRepository()


async def insert_swarm_run(client, data: dict) -> dict:
    return await _repo.insert_swarm_run(client, data)


async def upsert_memory(client, data: dict) -> dict:
    return await _repo.insert_memory_event(client, data)
