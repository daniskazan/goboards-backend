
import uvicorn

from fastapi import FastAPI

from configs.server import ServerConfig
from observers.exception_handler import ExceptionHandler
from observers.interface import ApplicationObserver
from observers.routing_handler import RoutingHandler
from utils.generics.response import APIResponse


class Server:
    app: FastAPI = FastAPI(
        title="PlayGame Service",
        default_response_class=APIResponse,
        docs_url="/docs"
    )
    config: ServerConfig = ServerConfig()
    observers: tuple[ApplicationObserver] = (
        ExceptionHandler(),
        RoutingHandler(),
    )

    def __call__(self) -> FastAPI:
        """
        Need for uvicorn.
        """
        return self.app

    @classmethod
    def notify(cls) -> None:
        for observer in cls.observers:
            observer.notify(sender=cls.app)

    def __new__(cls, *args, **kwargs):
        cls.notify()
        return super().__new__(cls)

    def run(self) -> None:
        uvicorn.run(
            app="main:server",
            factory=True,
            host=self.config.APP_HOST,
            port=self.config.APP_PORT,
            reload=self.config.DEBUG,
            workers=self.config.APP_WORKERS_COUNT,
        )


server = Server()

if __name__ == "__main__":
    server.run()
