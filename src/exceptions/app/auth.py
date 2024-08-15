from fastapi import HTTPException, status


class AuthenticationRequiredHTTPException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не авторизован.",
        )


class VKBadRequestException(HTTPException):
    def __init__(self, detail: str = "Что-то пошло не так 🚀") -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )


class VKBadCodeException(VKBadRequestException):
    def __init__(self, detail: str = "Плохой код авторизации 🚀") -> None:
        super().__init__(detail)


class ForbiddenHTTPException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав.",
        )
