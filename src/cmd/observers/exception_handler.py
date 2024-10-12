import enum

from cmd.observers.interface import ApplicationObserver

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError
from starlette.responses import JSONResponse

from exceptions.app.auth import AuthenticationRequiredHTTPException


class ExceptionCodeEnum(enum.StrEnum):
    """Error codes to generate user-friendly messages on client-side."""

    HTTP_500_INTERNAL_SERVER_ERROR: str = "INTERNAL_SERVER_ERROR"
    HTTP_400_BAD_REQUEST_ERROR: str = "BAD_REQUEST_ERROR"
    HTTP_401_NOT_AUTHORIZED_ERROR: str = "NOT_AUTHORIZED_ERROR"
    HTTP_409_CONFLICT_ERROR: str = "CONFLICT_ERROR"


class ExceptionHandler(ApplicationObserver):
    """
    Class to bind app`s exceptions with default responses while app starts.
    """

    @staticmethod
    def handler_401(request: Request, exc: AuthenticationRequiredHTTPException) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"code": ExceptionCodeEnum.HTTP_401_NOT_AUTHORIZED_ERROR},
        )

    @staticmethod
    def handler_500(request: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"code": ExceptionCodeEnum.HTTP_500_INTERNAL_SERVER_ERROR})

    @staticmethod
    def handler_400(request: Request, exc: RequestValidationError) -> JSONResponse:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"code": ExceptionCodeEnum.HTTP_400_BAD_REQUEST_ERROR})

    @staticmethod
    def handler_integrity_error(request: Request, exc: IntegrityError) -> JSONResponse:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"code": ExceptionCodeEnum.HTTP_409_CONFLICT_ERROR})

    def notify(self, *, sender: FastAPI):
        for handler, exc in [
            (self.handler_500, Exception),
            (self.handler_400, RequestValidationError),
            (self.handler_401, AuthenticationRequiredHTTPException),
            (self.handler_integrity_error, IntegrityError)
        ]:
            sender.add_exception_handler(exc_class_or_status_code=exc, handler=handler)
