from enum import IntEnum, auto


class MeetupStatus(IntEnum):
    NEW = auto()
    DISCUSSION = auto()
    CLOSED = auto()
    FINISHED = auto()


class UserMeetupStatus(IntEnum):
    INITIATOR = auto()
    PARTICIPANT = auto()

    def display(self):
        mapping = {
            self.INITIATOR: "Инициатор",
            self.PARTICIPANT: "Участник"
        }
        return mapping[self]
