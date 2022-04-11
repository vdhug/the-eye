from dataclasses import fields
from typing import Type, TypeVar


T = TypeVar("T")


def build_dataclass_from_model_instance(klass: Type[T], instance: "Model", **kwargs) -> T:
    """
    Receives a dataclass, a model instance and other dataclass fields and values
    that are not part of the model.
    """
    # Get the dataclass fields
    dataclass_field_names = set(f.name for f in fields(klass))

    # Exclude given properties
    dataclass_field_names -= kwargs.keys()

    _kwargs = {field: getattr(instance, field) for field in dataclass_field_names}
    _kwargs.update(kwargs)

    return klass(**_kwargs)
