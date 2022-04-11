from unittest import mock

from apps_data import services as apps_data_services
from apps_data.exceptions import ApplicationDoesNotExists
from apps_data.models import Application, Session


@mock.patch("apps_data.services.apps_data_providers.get_application_by_name")
@mock.patch("apps_data.services.build_dataclass_from_model_instance")
def test_mock_get_or_create_application__application_exists(
    mock_build_dataclass_from_model_instance, mock_get_application_by_name
):
    # Argument
    application_name = mock.Mock()

    # Setup
    application = mock.Mock()
    application_data = mock.Mock()

    mock_get_application_by_name.return_value = application
    mock_build_dataclass_from_model_instance.return_value = application_data

    # Execution
    result = apps_data_services.get_or_create_application_by_name(application_name=application_name)

    # Assertions
    mock_get_application_by_name.assert_called_once_with(
        application_name=application_name,
    )
    mock_build_dataclass_from_model_instance.assert_called_once()

    assert result == application_data


@mock.patch("apps_data.services.apps_data_providers.get_application_by_name")
@mock.patch("apps_data.services.apps_data_providers.create_application")
@mock.patch("apps_data.services.build_dataclass_from_model_instance")
def test_mock_get_or_create_application__application_does_not_exists(
    mock_build_dataclass_from_model_instance, mock_create_application, mock_get_application_by_name
):
    # Argument
    application_name = mock.Mock()

    # Setup
    application = mock.Mock()
    application_data = mock.Mock()

    mock_get_application_by_name.side_effect = Application.DoesNotExist()
    mock_create_application.return_value = application
    mock_build_dataclass_from_model_instance.return_value = application_data

    # Execution
    result = apps_data_services.get_or_create_application_by_name(application_name=application_name)

    # Assertions
    mock_get_application_by_name.assert_called_once_with(
        application_name=application_name,
    )
    mock_build_dataclass_from_model_instance.assert_called_once()

    assert result == application_data


@mock.patch("apps_data.services.get_or_create_application_by_name")
@mock.patch("apps_data.services.apps_data_providers.get_session_by_uuid")
@mock.patch("apps_data.services.build_dataclass_from_model_instance")
def test_mock_get_or_create_session_by_application_name_and_session_id__session_exists(
    mock_build_dataclass_from_model_instance,
    mock_get_session_by_uuid,
    mock_get_or_create_application_by_name,
):
    # Argument
    application_name = mock.Mock()
    session_id = mock.Mock()

    # Setup
    application_data = mock.Mock()
    session = mock.Mock()
    session_data = mock.Mock()

    mock_get_or_create_application_by_name.return_value = application_data
    mock_get_session_by_uuid.return_value = session
    mock_build_dataclass_from_model_instance.return_value = session_data

    # Execution
    result = apps_data_services.get_or_create_session_by_application_name_and_session_id(
        application_name=application_name, session_id=session_id
    )

    # Assertions
    mock_get_or_create_application_by_name.assert_called_once_with(
        application_name=application_name,
    )
    mock_get_session_by_uuid.assert_called_once_with(session_uuid=session_id)
    mock_build_dataclass_from_model_instance.assert_called_once()

    assert result == session_data


@mock.patch("apps_data.services.get_or_create_application_by_name")
@mock.patch("apps_data.services.apps_data_providers.get_session_by_uuid")
@mock.patch("apps_data.services.apps_data_providers.create_session")
@mock.patch("apps_data.services.build_dataclass_from_model_instance")
def test_mock_get_or_create_session_by_application_name_and_session_id__session_does_not_exists(
    mock_build_dataclass_from_model_instance,
    mock_create_session,
    mock_get_session_by_uuid,
    mock_get_or_create_application_by_name,
):
    # Argument
    application_name = mock.Mock()
    session_id = mock.Mock()

    # Setup
    application_data = mock.Mock()
    session = mock.Mock()
    session_data = mock.Mock()

    mock_get_or_create_application_by_name.return_value = application_data
    mock_get_session_by_uuid.side_effect = Session.DoesNotExist()
    mock_create_session.return_value = session
    mock_build_dataclass_from_model_instance.return_value = session_data

    # Execution
    result = apps_data_services.get_or_create_session_by_application_name_and_session_id(
        application_name=application_name, session_id=session_id
    )

    # Assertions
    mock_get_or_create_application_by_name.assert_called_once_with(
        application_name=application_name,
    )
    mock_get_session_by_uuid.assert_called_once_with(session_uuid=session_id)
    mock_create_session.assert_called_once_with(application_id=application_data.id, uuid=session_id)
    mock_build_dataclass_from_model_instance.assert_called_once()

    assert result == session_data


@mock.patch("apps_data.services.payload_validation")
@mock.patch("apps_data.services.get_or_create_session_by_application_name_and_session_id")
@mock.patch("apps_data.services.apps_data_providers.create_event")
@mock.patch("apps_data.services.build_dataclass_from_model_instance")
def test_register_event(
    mock_build_dataclass_from_model_instance,
    mock_create_event,
    mock_get_or_create_session_by_application_name_and_session_id,
    mock_payload_validation,
):
    # Arguments
    session_id = mock.Mock()
    category = mock.Mock()
    name = mock.Mock()
    payload = mock.MagicMock()
    timestamp = mock.Mock()

    session_data = mock.Mock()
    event = mock.Mock()
    event_data = mock.Mock()

    # Setup
    payload.__getitem__.side_effect = {"host": "www.consumeraffairs.com"}.__getitem__
    mock_payload_validation.return_value = None
    mock_get_or_create_session_by_application_name_and_session_id.return_value = session_data
    mock_create_event.return_value = event
    mock_build_dataclass_from_model_instance.return_value = event_data

    # Execution
    result = apps_data_services.register_event(
        session_id=session_id, category=category, name=name, payload=payload, timestamp=timestamp
    )

    # Assertions
    mock_payload_validation.assert_called_once_with(
        category=category,
        name=name,
        payload=payload,
    )

    mock_get_or_create_session_by_application_name_and_session_id.assert_called_once_with(
        application_name=payload.get("host"), session_id=session_id
    )

    mock_create_event.assert_called_once_with(
        session_uuid=session_data.uuid,
        name=name,
        category=category,
        payload=payload,
        timestamp=timestamp,
    )

    mock_build_dataclass_from_model_instance.assert_called_once()

    assert result == event_data
