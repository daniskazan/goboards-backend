from api.v1.oauth2.controllers.oauth2 import oauth2 as oauth2_router
from api.v1.games.controllers.games import games as game_router
from api.v1.meetups.controllers.meetups import meetups as meetup_router
from api.v1.users.controllers.users import users as user_router
from api.v1.auth.controllers.auth import auth as auth_router
from api.v1.areas.controllers.areas import areas as area_router
from fastapi import APIRouter

router = APIRouter(prefix="/v1")


router.include_router(oauth2_router)
router.include_router(game_router)
router.include_router(meetup_router)
router.include_router(user_router)
router.include_router(auth_router)
router.include_router(area_router)
