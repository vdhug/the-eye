import pytest
import pytz

from uuid import UUID
from datetime import datetime, timedelta

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
def test_get_application_by_name(django_assert_num_queries):
    application = apps_data_recipes.application_mommy_recipe.make()
    with django_assert_num_queries(num=1):
        retrieved_application = apps_data_providers.get_application_by_name(
            application_name=application.name
        )
        assert retrieved_application is not None
        assert isinstance(retrieved_application, Application) is True
        assert retrieved_application.id == application.id
        assert retrieved_application.name == application.name


@pytest.mark.django_db
def test_get_application_by_name__application_does_not_exists(django_assert_num_queries):
    with django_assert_num_queries(num=1):
        with pytest.raises(Application.DoesNotExist):
            _ = apps_data_providers.get_application_by_name(application_name="Foo")


@pytest.mark.django_db
def test_create_session(django_assert_num_queries):
    application = apps_data_recipes.application_mommy_recipe.make()
    with django_assert_num_queries(num=1):
        session = apps_data_providers.create_session(
            application_id=application.id, uuid=UUID("188a8f86-75f0-44c9-9db5-f525846249ce")
        )
        assert session is not None
        assert isinstance(session, Session) is True
        assert session.application_id == application.id
        assert session.uuid == UUID("188a8f86-75f0-44c9-9db5-f525846249ce")


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


@pytest.mark.django_db
def test_get_events_by_session_uuid(django_assert_num_queries):
    session_1 = apps_data_recipes.session_mommy_recipe.make(
        uuid=UUID("188a8f86-75f0-44c9-9db5-f525846249ce")
    )
    session_2 = apps_data_recipes.session_mommy_recipe.make(
        uuid=UUID("40c8ab78-4425-4dfd-8295-36092e4dbf4e")
    )
    _ = apps_data_recipes.session_mommy_recipe.make(
        uuid=UUID("3ea3d8f5-442d-453a-b964-01229e087011")
    )
    timestamp = make_aware(
        datetime.strptime("2021-01-04 09:15:27.243860", "%Y-%m-%d %H:%M:%S.%f"), TIMEZONE
    )
    _ = apps_data_recipes.event_mommy_recipe.make(session=session_1, timestamp=timestamp)
    _ = apps_data_recipes.event_mommy_recipe.make(session=session_2, timestamp=timestamp)
    with django_assert_num_queries(num=1):
        events_from_session_1 = apps_data_providers.get_events_by_session_uuid(
            session_uuid=session_1.uuid
        )
        assert events_from_session_1.count() == 1


@pytest.mark.django_db
def test_get_events_by_session_uuid__no_events_found(django_assert_num_queries):
    session_1 = apps_data_recipes.session_mommy_recipe.make(
        uuid=UUID("188a8f86-75f0-44c9-9db5-f525846249ce")
    )
    session_2 = apps_data_recipes.session_mommy_recipe.make(
        uuid=UUID("40c8ab78-4425-4dfd-8295-36092e4dbf4e")
    )
    timestamp = make_aware(
        datetime.strptime("2021-01-04 09:15:27.243860", "%Y-%m-%d %H:%M:%S.%f"), TIMEZONE
    )
    _ = apps_data_recipes.event_mommy_recipe.make(session=session_1, timestamp=timestamp)
    with django_assert_num_queries(num=1):
        events_from_session_2 = apps_data_providers.get_events_by_session_uuid(
            session_uuid=session_2.uuid
        )
        assert events_from_session_2.count() == 0


@pytest.mark.django_db
def test_get_events_on_time_range(django_assert_num_queries):
    since = make_aware(
        datetime.strptime("2021-01-04 09:15:27.243860", "%Y-%m-%d %H:%M:%S.%f"), TIMEZONE
    )
    until = since + timedelta(days=1)

    _ = apps_data_recipes.event_mommy_recipe.make(timestamp=since)
    _ = apps_data_recipes.event_mommy_recipe.make(timestamp=until)
    with django_assert_num_queries(num=1):
        events = apps_data_providers.get_events_on_time_range(since=since, until=until)
        assert events.count() == 2


@pytest.mark.django_db
def test_get_events_on_time_range__events_not_found(django_assert_num_queries):
    since = make_aware(
        datetime.strptime("2021-01-04 09:15:27.243860", "%Y-%m-%d %H:%M:%S.%f"), TIMEZONE
    )
    until = since + timedelta(days=1)

    timestamp = until + timedelta(hours=1)

    _ = apps_data_recipes.event_mommy_recipe.make(timestamp=timestamp)
    with django_assert_num_queries(num=1):
        events = apps_data_providers.get_events_on_time_range(since=since, until=until)
        assert events.count() == 0
