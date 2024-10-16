import abc

from fastapi import FastAPI


class ApplicationObserver(abc.ABC):

    @abc.abstractmethod
    def notify(self, *, sender: FastAPI) -> None:
        """
        Each ApplicationObserver should define its own logic when applications starts.
        """
        raise NotImplementedError
