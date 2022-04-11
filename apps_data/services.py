import logging
from uuid import UUID
from datetime import datetime

from apps_data.dataclasses import ApplicationData, EventData, SessionData
from apps_data import providers as apps_data_providers
from apps_data.exceptions import PayloadValidationError
from apps_data.models import Application, Session
from apps_data.utils import build_dataclass_from_model_instance
from apps_data.validators import payload_validation


def get_or_create_application_by_name(application_name: str) -> ApplicationData:
    try:
        application = apps_data_providers.get_application_by_name(application_name=application_name)
    except Application.DoesNotExist:
        application = apps_data_providers.create_application(name=application_name)
    application_data = build_dataclass_from_model_instance(
        klass=ApplicationData,
        instance=application,
    )
    return application_data


def get_or_create_session_by_application_name_and_session_id(
    application_name: str, session_id: UUID
) -> SessionData:
    application_data = get_or_create_application_by_name(application_name=application_name)
    try:
        session = apps_data_providers.get_session_by_uuid(session_uuid=session_id)
    except Session.DoesNotExist:
        session = apps_data_providers.create_session(
            application_id=application_data.id, uuid=session_id
        )
    application_data = build_dataclass_from_model_instance(
        klass=SessionData, instance=session, application=application_data
    )
    return application_data


def register_event(session_id: UUID, category: str, name: str, payload: dict, timestamp: datetime):
    try:
        payload_validation(category=category, name=name, payload=payload)
    except PayloadValidationError:
        logging.error(
            msg=f"Payload validation error. Session id {session_id} and payload {payload}",
        )
    application_name = payload.get("host")

    if not session_id or not category or not name or not application_name or not timestamp:
        logging.error(msg="Missing required info to register event")
        raise ValueError
    session_data = get_or_create_session_by_application_name_and_session_id(
        application_name=application_name, session_id=session_id
    )
    event = apps_data_providers.create_event(
        session_uuid=session_data.uuid,
        name=name,
        category=category,
        payload=payload,
        timestamp=timestamp,
    )

    event_data = build_dataclass_from_model_instance(
        klass=EventData, instance=event, session=session_data
    )
    return event_data
