from apps_data.exceptions import PayloadValidationError


def pageview_validation(payload: dict) -> None:
    payload_keys = payload.keys()
    if set(payload_keys) != set(["host", "path"]):
        raise PayloadValidationError


def cta_click_validation(payload: dict) -> None:
    payload_keys = payload.keys()
    if set(payload_keys) != set(["host", "path", "element"]):
        raise PayloadValidationError


def form_submition_validation(payload: dict) -> None:
    payload_keys = payload.keys()
    if set(payload_keys) != set(["host", "path", "form"]):
        raise PayloadValidationError


VALIDATORS_MAPPING = {
    "page interaction": {
        "pageview": pageview_validation,
        "cta click": cta_click_validation,
    },
    "form interaction": {
        "submit": form_submition_validation,
    },
}


def payload_validation(category: str, name: str, payload: dict) -> None:
    """If there is any payload validation associated to events with the given category and name,
    run the validation before saving the event. If no host is provided in the payload, this payload is already invalid

    Args:
        category (str): category of event
        name (str): name of event
        payload (dict): payload of event
    """
    if not payload.get("host"):
        raise PayloadValidationError
    func = VALIDATORS_MAPPING.get(category, {}).get(name, {})
    if func:
        func(payload=payload)
