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


@pytest.mark.django_db
def test_get_application_by_id(django_assert_num_queries):
    application = apps_data_recipes.application_mommy_recipe.make()
    with django_assert_num_queries(num=1):
        retrieved_application = apps_data_providers.get_application_by_id(
            application_id=application.id
        )
        assert retrieved_application is not None
        assert isinstance(retrieved_application, Application) is True
        assert retrieved_application.id == application.id


@pytest.mark.django_db
def test_get_application_by_id__application_does_not_exists(django_assert_num_queries):
    with django_assert_num_queries(num=1):
        with pytest.raises(Application.DoesNotExist):
            _ = apps_data_providers.get_application_by_id(application_id=0)


@pytest.mark.django_db
def test_create_session(django_assert_num_queries):
    application = apps_data_recipes.application_mommy_recipe.make()
    with django_assert_num_queries(num=2):
        session = apps_data_providers.create_session(
            application_id=application.id, uuid=UUID("188a8f86-75f0-44c9-9db5-f525846249ce")
        )
        assert session is not None
        assert isinstance(session, Session) is True
        assert session.application_id == application.id
        assert session.uuid == UUID("188a8f86-75f0-44c9-9db5-f525846249ce")


@pytest.mark.django_db
def test_create_session__application_does_not_exists(django_assert_num_queries):
    _ = apps_data_recipes.application_mommy_recipe.make()
    with django_assert_num_queries(num=1):
        with pytest.raises(Application.DoesNotExist):
            _ = apps_data_providers.create_session(
                application_id=0, uuid=UUID("188a8f86-75f0-44c9-9db5-f525846249ce")
            )


@pytest.mark.django_db
def test_get_session_by_uuid(django_assert_num_queries):
    session = apps_data_recipes.session_mommy_recipe.make()
    with django_assert_num_queries(num=1):
        retrieved_session = apps_data_providers.get_session_by_uuid(session_uuid=session.uuid)
        assert retrieved_session is not None
        assert isinstance(retrieved_session, Session) is True
        assert retrieved_session.uuid == session.uuid


@pytest.mark.django_db
def test_get_session_by_uuid__session_does_not_exists(django_assert_num_queries):
    _ = apps_data_recipes.session_mommy_recipe.make()
    with django_assert_num_queries(num=1):
        with pytest.raises(Session.DoesNotExist):
            _ = apps_data_providers.get_session_by_uuid(
                session_uuid=UUID("188a8f86-75f0-44c9-9db5-f525846249ce")
            )
