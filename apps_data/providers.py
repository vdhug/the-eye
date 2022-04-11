from datetime import datetime
from uuid import UUID

from apps_data.models import Application, Session, Event


def create_application(name: str) -> Application:
    application = Application.objects.create(
        name=name,
    )
    return application


def update_application(application_id: int, name: str) -> Application:
    application = Application.objects.get(id=application_id)
    application.name = name
    application.save(update_fields=["name"])
    return application


def get_application_by_id(application_id: int) -> Application:
    application = Application.objects.get(id=application_id)
    return application


def create_session(application_id: int, uuid: UUID) -> Session:
    _ = get_application_by_id(application_id=application_id)
    session = Session.objects.create(uuid=uuid, application_id=application_id)
    return session


def get_session_by_uuid(session_uuid: int) -> Session:
    session = Session.objects.get(uuid=session_uuid)
    return session


def create_event(
    session_uuid: UUID, name: str, category: str, payload: dict, timestamp: datetime
) -> Event:
    _ = get_session_by_uuid(session_uuid=session_uuid)
    event = Event.objects.create(
        session_id=session_uuid,
        name=name,
        category=category,
        payload=payload,
        timestamp=timestamp,
    )
    return event


def get_event_by_id(event_id: int) -> Event:
    event = Event.objects.get(id=event_id)
    return event


def get_events_by_session_uuid(session_uuid: UUID) -> "QuerySet":
    events = Event.objects.filter(session_id=session_uuid)
    return events


def get_events_on_time_range(since: datetime, until: datetime) -> "QuerySet":
    events = Event.objects.filter(
        timestamp__gte=since,
        timestamp__lte=until,
    )
    return events
