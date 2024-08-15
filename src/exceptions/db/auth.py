from fastapi import HTTPException, status


class SessionNotFoundException(HTTPException):
    def __init__(self, detail: str = "Токен не найден.") -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )