from apps_data.dataclasses import ApplicationData
from apps_data import providers as apps_data_providers
from apps_data.exceptions import ApplicationDoesNotExists
from apps_data.models import Application
from apps_data.utils import build_dataclass_from_model_instance


def get_or_create_application_by_name(application_name: str) -> ApplicationData:
    try:
        application = apps_data_providers.get_application_by_name(application_name=application_name)
    except Application.DoesNotExist:
        application = apps_data_providers.create_application(name=application_name)
    application_data = build_dataclass_from_model_instance(
        klass=ApplicationData,
        instance=application,
    )
    return application_data
