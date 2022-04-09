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


@pytest.mark.django_db
def test_create_event(django_assert_num_queries):
    session = apps_data_recipes.session_mommy_recipe.make()
    with django_assert_num_queries(num=2):
        timestamp = make_aware(
            datetime.strptime("2021-01-01 09:15:27.243860", "%Y-%m-%d %H:%M:%S.%f"), TIMEZONE
        )
        event = apps_data_providers.create_event(
            session_uuid=session.uuid,
            name="cta click",
            category="page interaction",
            payload={"host": "www.consumeraffairs.com", "path": "/", "element": "chat bubble"},
            timestamp=timestamp,
        )
        assert event is not None
        assert isinstance(event, Event) is True
        assert event.session_id == session.uuid
        assert event.name == "cta click"
        assert event.category == "page interaction"
        assert event.payload == {
            "host": "www.consumeraffairs.com",
            "path": "/",
            "element": "chat bubble",
        }
        assert event.timestamp == timestamp


@pytest.mark.django_db
def test_create_event__session_does_not_exists(django_assert_num_queries):
    _ = apps_data_recipes.session_mommy_recipe.make()
    with django_assert_num_queries(num=1):
        with pytest.raises(Session.DoesNotExist):
            timestamp = make_aware(
                datetime.strptime("2021-01-01 09:15:27.243860", "%Y-%m-%d %H:%M:%S.%f"), TIMEZONE
            )
            _ = apps_data_providers.create_event(
                session_uuid=UUID("188a8f86-75f0-44c9-9db5-f525846249ce"),
                name="cta click",
                category="page interaction",
                payload={"host": "www.consumeraffairs.com", "path": "/", "element": "chat bubble"},
                timestamp=timestamp,
            )


@pytest.mark.django_db
def test_get_event_by_id(django_assert_num_queries):
    timestamp = make_aware(
        datetime.strptime("2021-01-04 09:15:27.243860", "%Y-%m-%d %H:%M:%S.%f"), TIMEZONE
    )
    event = apps_data_recipes.event_mommy_recipe.make(timestamp=timestamp)
    with django_assert_num_queries(num=1):
        retrieved_event = apps_data_providers.get_event_by_id(event_id=event.id)
        assert retrieved_event is not None
        assert isinstance(retrieved_event, Event) is True
        assert retrieved_event.id == event.id
        assert retrieved_event.session_id == event.session_id
        assert retrieved_event.name == event.name
        assert retrieved_event.category == event.category
        assert retrieved_event.payload == event.payload
        assert retrieved_event.timestamp == timestamp
