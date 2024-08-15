import uuid

from api.v1.oauth2.serializers.response.main import AccessTokenData
from core.auth.models import SessionORM
from core.auth.repository.db.read_repo import SessionReadRepository
from core.auth.repository.db.update_repo import SessionUpdateRepository
from core.oauth.services import JWTService, UserAPIKeyCredentials, GenerateRefreshTokenInputData
from exceptions.db.auth import SessionNotFoundException
from utils.generics.dto import Result


class ObtainNewTokenPairUseCase:

    def __init__(
        self,
        *,
        jwt_service: JWTService,
        session_read_repo: SessionReadRepository,
        session_update_repo: SessionUpdateRepository
    ):
        self._jwt_service = jwt_service
        self._session_read_repo = session_read_repo
        self._session_update_repo = session_update_repo

    async def _get_session(
        self,
        *,
        user_id: uuid.UUID,
        refresh_token: uuid.UUID
    ):
        session = await self._session_read_repo.get_session_by_id(
            user_id=user_id,
            refresh_token=refresh_token
        )
        return session

    async def _delete_session(self, session: SessionORM):
        await self._session_update_repo.delete_session(session=session)

    async def run(
        self,
        *,
        user: UserAPIKeyCredentials,
        refresh_token: uuid.UUID,
        ip: str,
    ) -> tuple[Result[SessionORM, None], Result[AccessTokenData, None]] | Result[None, SessionNotFoundException]:
        result = await self._get_session(user_id=user.sub, refresh_token=refresh_token)
        if not result.payload:
            return result

        await self._delete_session(session=result.payload)
        access_token = self._jwt_service.create_access_token(user=user)
        refresh_token = await self._jwt_service.create_refresh_token(
            data=GenerateRefreshTokenInputData(
                user_id=user.sub,
                ip=ip
            )
        )
        return (
            Result.success(payload=refresh_token),
            Result.success(
                payload=AccessTokenData(
                    access_token=access_token,
                    refresh_token=refresh_token.refresh_token
                )
            )
        )
