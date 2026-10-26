from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/health/live")
async def liveness_check():
    ...


@router.get("/health/ready")
async def readiness_check():
    ...