from __future__ import absolute_import, unicode_literals

from celery import shared_task
from uuid import UUID
from datetime import datetime

from apps_data import services as apps_data_services


@shared_task
def register_event(session_id: UUID, category: str, name: str, payload: dict, timestamp: datetime):
    apps_data_services.register_event(
        session_id=session_id, category=category, name=name, payload=payload, timestamp=timestamp
    )
