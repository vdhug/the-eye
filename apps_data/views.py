import pytz
from datetime import datetime
from uuid import UUID

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import make_aware
from apps_data.serializers import EventSerializer

from rest_framework.parsers import JSONParser

from apps_data import tasks as apps_data_async_tasks
from apps_data import providers as apps_data_providers


@csrf_exempt
def register_event(request):
    """
    Register new event via POST request via async task
    """
    if request.method == "POST":
        data = JSONParser().parse(request)
        session_id = data.get("session_id")
        name = data.get("name")
        category = data.get("category")
        payload = data.get("data")
        timestamp = make_aware(
            datetime.strptime(data.get("timestamp"), "%Y-%m-%d %H:%M:%S.%f"), pytz.timezone("GMT")
        )
        apps_data_async_tasks.register_event.delay(
            session_id=session_id,
            category=category,
            name=name,
            payload=payload,
            timestamp=timestamp,
        )
        return JsonResponse(data={"result": "Ok"})

    if request.method == "GET":
        session_id = request.GET.get("session_id", "")
        since = request.GET.get("since", "")
        until = request.GET.get("until", "")
        events = []
        if session_id:
            session_id = UUID(session_id)
            events = apps_data_providers.get_events_by_session_uuid(session_uuid=session_id)
        elif since and until:
            print("here")
            since = make_aware(datetime.strptime(since, "%Y-%m-%d %H:%M:%S"), pytz.timezone("GMT"))
            until = make_aware(datetime.strptime(until, "%Y-%m-%d %H:%M:%S"), pytz.timezone("GMT"))
            events = apps_data_providers.get_events_on_time_range(
                since=since,
                until=until,
            )
        serialized_events = EventSerializer(events, many=True)
        return JsonResponse(data={"result": serialized_events.data})
