from uuid import UUID

from apps_data.dataclasses import ApplicationData, SessionData
from apps_data import providers as apps_data_providers
from apps_data.models import Application, Session
from apps_data.utils import build_dataclass_from_model_instance


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
