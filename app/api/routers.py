from fastapi import APIRouter

from app.api.endpoints import tron_router

main_router = APIRouter()
main_router.include_router(tron_router, tags=['Tron'], prefix='/tron')
