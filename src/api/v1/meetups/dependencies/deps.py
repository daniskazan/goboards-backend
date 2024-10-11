from core.meetups.repository.db.read_repo import MeetupReadRepository
from core.meetups.repository.db.update_repo import MeetupUpdateRepository
from core.meetups.services import MeetupService
from utils.db.session import get_db
from fastapi import Depends


def get_meetup_read_repo(session=Depends(get_db)):
    return MeetupReadRepository(session=session)


def get_meetup_update_repo(session=Depends(get_db)):
    return MeetupUpdateRepository(session=session)


def get_meetup_service(meetup_read_repo=Depends(get_meetup_read_repo), meetup_update_repo=Depends(get_meetup_update_repo)):
    return MeetupService(meetup_read_repo=meetup_read_repo, meetup_update_repo=meetup_update_repo)
