# STUB — Implemented by: workstream/1a-backend-core
from typing import AsyncGenerator


class EventBus:
    async def publish(self, stream: str, data: dict) -> None: raise NotImplementedError()
    async def consume(self, stream: str, group: str, consumer: str) -> AsyncGenerator[dict, None]: raise NotImplementedError()
