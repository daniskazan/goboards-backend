from fastapi import Depends

from api.v1.oauth2.dependencies.oauth import (
    get_jwt_service,
    get_session_read_repo,
    get_session_update_repo,
)
from core.auth.repository.db.read_repo import SessionReadRepository
from core.auth.repository.db.update_repo import SessionUpdateRepository
from core.auth.services import LogoutUseCase, ObtainNewTokenPairUseCase
from core.oauth.services import JWTService


def get_obtain_token_use_case(
    jwt_service: JWTService = Depends(get_jwt_service),
    session_read_repo: SessionReadRepository = Depends(get_session_read_repo),
    session_update_repo: SessionUpdateRepository = Depends(get_session_update_repo),
) -> ObtainNewTokenPairUseCase:
    return ObtainNewTokenPairUseCase(jwt_service=jwt_service, session_read_repo=session_read_repo, session_update_repo=session_update_repo)


def get_logout_use_case(session_update_repo: SessionUpdateRepository = Depends(get_session_update_repo)) -> LogoutUseCase:
    return LogoutUseCase(session_update_repo=session_update_repo)
