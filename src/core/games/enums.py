from enum import IntEnum


class GameType(IntEnum):
    SYSTEM_GAME = 0
    USER = 1

    def get_description(self) -> str:
        description = {
            self.USER: "Пользовательская игра",
            self.SYSTEM_GAME: "Системная игра",
        }
        return description[self]
