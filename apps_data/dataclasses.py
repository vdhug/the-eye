from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class ApplicationData:
    id: int
    name: str


@dataclass
class SessionData:
    application: ApplicationData
    uuid: UUID


@dataclass
class EventData:
    id: int
    session: SessionData
    name: str
    category: str
    payload: dict
    timestamp: datetime
