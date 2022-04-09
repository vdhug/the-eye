from uuid import UUID, uuid4
from datetime import datetime
from django.db import models


class Application(models.Model):
    name: str = models.CharField(max_length=300, default=None, blank=True, null=True)


class Session(models.Model):
    application: Application = models.ForeignKey(
        Application, related_name="sessions", on_delete=models.CASCADE, blank=True, null=True
    )
    uuid: UUID = models.UUIDField(primary_key=True, default=uuid4, editable=False)


class Event(models.Model):
    session: Session = models.ForeignKey(
        Session, related_name="events", on_delete=models.CASCADE, blank=True, null=True
    )
    name: str = models.CharField(max_length=300, default=None, blank=True, null=True)
    category: str = models.CharField(max_length=300, default=None, blank=True, null=True)
    payload: dict = models.JSONField()
    timestamp: datetime = models.DateTimeField()

    class Meta:
        ordering = ["-timestamp"]
