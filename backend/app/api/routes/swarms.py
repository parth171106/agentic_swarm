# STUB — Implemented by: workstream/2c-crew-registry-ingestion
from fastapi import APIRouter, Depends
from backend.app.models.swarm_models import (
    CreateSwarmRequest,
    CreateSwarmResponse,
    SwarmRunResponse,
)
from backend.app.core.dependencies import get_current_user

router = APIRouter(prefix="/swarms", tags=["swarms"])


@router.post("", response_model=CreateSwarmResponse, status_code=202)
async def create_swarm(
    request: CreateSwarmRequest, user_id: str = Depends(get_current_user)
):
    raise NotImplementedError()


@router.get("/{id}", response_model=SwarmRunResponse)
async def get_swarm_run(id: str, user_id: str = Depends(get_current_user)):
    raise NotImplementedError()


@router.get("/{id}/report")
async def get_swarm_report(
    id: str, format: str = "markdown", user_id: str = Depends(get_current_user)
):
    raise NotImplementedError()


@router.get("/{id}/resume", status_code=202)
async def resume_swarm_run(id: str, user_id: str = Depends(get_current_user)):
    raise NotImplementedError()
