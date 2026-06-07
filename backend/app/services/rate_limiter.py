# STUB — Implemented by: workstream/1a-backend-core
class RateLimiter:
    async def check_tool_rate_limit(self, redis_client, tool_name: str, user_id: str) -> None: raise NotImplementedError()
    async def check_llm_rate_limit(self, redis_client, provider: str, user_id: str) -> None: raise NotImplementedError()
    async def get_rate_limit_stats(self, redis_client, user_id: str) -> dict: raise NotImplementedError()
