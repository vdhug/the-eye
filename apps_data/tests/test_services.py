import pytest
from unittest import mock

from apps_data import services as apps_data_services
from apps_data.exceptions import ApplicationDoesNotExists
from apps_data.models import Application


@mock.patch("apps_data.services.apps_data_providers.create_application")
@mock.patch("apps_data.services.build_dataclass_from_model_instance")
def test_mock_create_application(mock_build_dataclass_from_model_instance, mock_create_application):
    # Argument
    name = mock.Mock()

    # Setup
    application = mock.Mock()
    application_data = mock.Mock()

    mock_create_application.return_value = application
    mock_build_dataclass_from_model_instance.return_value = application_data

    # Execution
    result = apps_data_services.create_application(name=name)

    # Assertions
    mock_create_application.assert_called_once_with(
        name=name,
    )
    mock_build_dataclass_from_model_instance.assert_called_once()

    assert result == application_data


@mock.patch("apps_data.services.apps_data_providers.get_application_by_name")
@mock.patch("apps_data.services.build_dataclass_from_model_instance")
def test_mock_get_application_by_name(
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
    result = apps_data_services.get_application_by_name(application_name=application_name)

    # Assertions
    mock_get_application_by_name.assert_called_once_with(
        application_name=application_name,
    )
    mock_build_dataclass_from_model_instance.assert_called_once()

    assert result == application_data


@mock.patch("apps_data.services.apps_data_providers.get_application_by_name")
@mock.patch("apps_data.services.build_dataclass_from_model_instance")
def test_mock_get_application_by_name__application_does_not_exists(
    mock_build_dataclass_from_model_instance, mock_get_application_by_name
):
    # Argument
    application_name = mock.Mock()

    # Setup
    mock_get_application_by_name.side_effect = Application.DoesNotExist()

    # Execution
    with pytest.raises(ApplicationDoesNotExists):
        _ = apps_data_services.get_application_by_name(application_name=application_name)
        # Assertions
        mock_get_application_by_name.assert_called_once_with(
            application_name=application_name,
        )
