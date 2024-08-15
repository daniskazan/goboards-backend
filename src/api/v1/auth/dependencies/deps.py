from fastapi import Depends

from api.v1.oauth2.dependencies.oauth import get_session_update_repo
from api.v1.oauth2.dependencies.oauth import get_session_read_repo
from api.v1.oauth2.dependencies.oauth import get_jwt_service
from core.auth.repository.db.read_repo import SessionReadRepository
from core.auth.repository.db.update_repo import SessionUpdateRepository
from core.oauth.services import JWTService
from core.auth.services import ObtainNewTokenPairUseCase


def get_obtain_token_use_case(
    jwt_service: JWTService = Depends(get_jwt_service),
    session_read_repo: SessionReadRepository = Depends(get_session_read_repo),
    session_update_repo: SessionUpdateRepository = Depends(get_session_update_repo)
) -> ObtainNewTokenPairUseCase:
    return ObtainNewTokenPairUseCase(
        jwt_service=jwt_service,
        session_read_repo=session_read_repo,
        session_update_repo=session_update_repo
    )