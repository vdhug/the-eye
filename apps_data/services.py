from apps_data.dataclasses import ApplicationData
from apps_data import providers as apps_data_providers
from apps_data.utils import build_dataclass_from_model_instance


def create_application(name: str) -> ApplicationData:
    application = apps_data_providers.create_application(name=name)
    application_data = build_dataclass_from_model_instance(
        klass=ApplicationData,
        instance=application,
    )
    return application_data
