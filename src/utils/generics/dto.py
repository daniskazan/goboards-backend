from dataclasses import dataclass
from typing import Generic, Self, TypeVar

Payload = TypeVar("Payload")
Error = TypeVar("Error")


@dataclass(frozen=True, slots=True, match_args=True)
class Result(Generic[Payload, Error]):
    payload: Payload | None
    error: Error | None

    @classmethod
    def success(cls, payload: Payload) -> Self:
        return cls(payload=payload, error=None)

    @classmethod
    def failure(cls, error: Error) -> Self:
        return cls(payload=None, error=error)
