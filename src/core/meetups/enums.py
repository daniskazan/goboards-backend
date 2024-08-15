from enum import IntEnum, auto


class MeetupStatus(IntEnum):
    NEW = auto()
    DISCUSSION = auto()
    CLOSED = auto()
    FINISHED = auto()


class UserMeetupStatus(IntEnum):
    INITIATOR = auto()
    PARTICIPANT = auto()
