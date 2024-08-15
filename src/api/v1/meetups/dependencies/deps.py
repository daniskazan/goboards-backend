from core.meetups.repository.db.read_repo import MeetupReadRepository
from core.meetups.services import MeetupService
from utils.db.session import get_db
from fastapi import Depends


def get_meetup_read_repo(session=Depends(get_db)):
    return MeetupReadRepository(session=session)


def get_meetup_service(meetup_read_repo=Depends(get_meetup_read_repo)):
    return MeetupService(meetup_read_repo=meetup_read_repo)
