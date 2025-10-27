from fastapi import APIRouter

from api.healthcheck import router as healthcheck_router
from api.v1.activity import router as activity_router
from api.v1.building import router as building_router
from api.v1.organization import router as organization_router
from core.config import settings

v1_router = APIRouter(prefix="/v1")

v1_router.include_router(organization_router)
v1_router.include_router(building_router)
v1_router.include_router(activity_router)

project_router = APIRouter(prefix=f"/{settings().PROJECT_NAME}")
project_router.include_router(v1_router)
api_router = APIRouter(prefix="/api")
api_router.include_router(project_router)
api_router.include_router(healthcheck_router)
