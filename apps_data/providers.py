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
