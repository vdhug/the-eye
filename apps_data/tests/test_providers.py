import pytest
import pytz

from uuid import UUID
from datetime import datetime

from django.utils.timezone import make_aware

from apps_data.models import Application, Session, Event
from apps_data import providers as apps_data_providers
from apps_data.tests import recipes as apps_data_recipes


TIMEZONE = pytz.timezone("GMT")


@pytest.mark.django_db
def test_create_application(django_assert_num_queries):
    with django_assert_num_queries(num=1):
        application = apps_data_providers.create_application(name="Web App")
        assert application is not None
        assert isinstance(application, Application) is True
        assert application.name == "Web App"
