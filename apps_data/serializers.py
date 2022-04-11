from django.http import JsonResponse
import pytz
from datetime import datetime

from rest_framework import serializers

from django.utils.timezone import make_aware

from apps_data import tasks as apps_data_async_tasks


class EventSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    session_id = serializers.UUIDField()
    name = serializers.CharField(required=True, allow_blank=False, max_length=300)
    category = serializers.CharField(required=True, allow_blank=False, max_length=300)
    payload = serializers.DictField(required=True)
    timestamp = serializers.CharField(required=True, allow_blank=False, max_length=50)
