from fastapi import APIRouter

from f1api.api import drivers, events, seasons, teams

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(seasons.router)
api_router.include_router(teams.router)
api_router.include_router(drivers.router)
api_router.include_router(events.router)
