# STUB — Implemented by: workstream/1a-backend-core
from fastapi import Request


async def get_current_user(request: Request) -> str:
    """Auth dependency extracting JWT credentials."""
    raise NotImplementedError()
