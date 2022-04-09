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


@pytest.mark.django_db
def test_update_application(django_assert_num_queries):
    application = apps_data_recipes.application_mommy_recipe.make()
    assert application.name == "Web App"
    with django_assert_num_queries(num=2):
        application_edited = apps_data_providers.update_application(
            application_id=application.id, name="Web App Edited"
        )
        assert isinstance(application_edited, Application) is True
        assert application.id == application_edited.id
        assert application_edited.name == "Web App Edited"


@pytest.mark.django_db
def test_update_application__application_does_not_exists(django_assert_num_queries):
    application = apps_data_recipes.application_mommy_recipe.make()
    assert application.name == "Web App"
    with django_assert_num_queries(num=1):
        with pytest.raises(Application.DoesNotExist):
            _ = apps_data_providers.update_application(application_id=0, name="Foo")
