from datetime import datetime
from uuid import UUID

from apps_data.models import Application, Session, Event


def create_application(name: str) -> Application:
    application = Application.objects.create(
        name=name,
    )
    return application
