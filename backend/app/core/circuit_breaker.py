# STUB — Implemented by: workstream/1a-backend-core
class CircuitBreakerOpen(Exception):
    pass


async def check_breaker(redis_client, api_name: str) -> None: raise NotImplementedError()
async def record_failure(redis_client, api_name: str) -> None: raise NotImplementedError()
async def record_success(redis_client, api_name: str) -> None: raise NotImplementedError()
