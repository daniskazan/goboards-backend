import uvicorn
from api.routing import router
from configs.server import server as server_settings
from exceptions.app.auth import AuthenticationRequiredHTTPException
from fastapi import (
    FastAPI,
    Request,
    status,
)
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from utils.generics.response import APIResponse

app = FastAPI(title="Goboards Service", default_response_class=APIResponse, docs_url="/docs")
app.include_router(router=router)


@app.exception_handler(RequestValidationError)
def handler_422(request: Request, exc: RequestValidationError):  # noqa
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error": exc.args[0]})


@app.exception_handler(AuthenticationRequiredHTTPException)
def handler_401(request: Request, exc: AuthenticationRequiredHTTPException):  # noqa
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"error": "Пользователь не авторизован."},
    )


@app.exception_handler(Exception)
def handler_500(request: Request, exc: Exception):  # noqa
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": f"Внутренняя ошибка сервера. {exc.args}"},
    )


if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        reload=server_settings.DEBUG,
        host=server_settings.APP_HOST,
        port=server_settings.APP_PORT,
        workers=server_settings.UVICORN_WORKERS,
    )
