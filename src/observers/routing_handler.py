from functools import cached_property

from fastapi import APIRouter, FastAPI

from api.v1.areas.controllers.areas import areas as area_router
from api.v1.auth.controllers.auth import auth as auth_router
from api.v1.games.controllers.games import games as game_router
from api.v1.meetups.controllers.meetups import meetups as meetup_router
from api.v1.oauth2.controllers.oauth2 import oauth2 as oauth2_router
from api.v1.users.controllers.users import users as user_router
from observers.interface import ApplicationObserver


class RoutingHandler(ApplicationObserver):

    def __init__(self):
        self._router = APIRouter(prefix="/api")

    @cached_property
    def v1(self) -> APIRouter:
        router = APIRouter(prefix="/v1")
        routes: list[APIRouter] = [
            oauth2_router,
            game_router,
            meetup_router,
            user_router,
            auth_router,
            area_router
        ]
        for route in routes:
            router.include_router(route)

        return router

    def notify(self, *, sender: FastAPI):
        for router in (
            self.v1,
        ):
            self._router.include_router(router=router)
        sender.include_router(router=self._router)
