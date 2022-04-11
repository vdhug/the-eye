from apps_data.exceptions import PayloadValidationError
import pytest
from apps_data.validators import payload_validation


def test_payload_validation__empty_host():
    payload = {
        "host": "",
        "path": "/",
    }
    with pytest.raises(PayloadValidationError):
        payload_validation(category="page interaction", name="pageview", payload=payload)


def test_payload_validation__pageview_validation():
    payload = {
        "host": "www.consumeraffairs.com",
        "path": "/",
    }
    assert None == payload_validation(category="page interaction", name="pageview", payload=payload)


def test_payload_validation__pageview_validation__invalid_payload():
    payload = {
        "path": "/",
    }
    with pytest.raises(PayloadValidationError):
        payload_validation(category="page interaction", name="pageview", payload=payload)


def test_payload_validation__cta_click_validation():
    payload = {"host": "www.consumeraffairs.com", "path": "/", "element": "foo"}
    assert None == payload_validation(
        category="page interaction", name="cta click", payload=payload
    )


def test_payload_validation__cta_click_validation__invalid_payload():
    payload = {
        "host": "www.consumeraffairs.com",
        "path": "/",
    }
    with pytest.raises(PayloadValidationError):
        payload_validation(category="page interaction", name="cta click", payload=payload)


def test_payload_validation__form_submition_validation_validation():
    payload = {
        "host": "www.consumeraffairs.com",
        "path": "/",
        "form": {"first_name": "John", "last_name": "Doe"},
    }
    assert None == payload_validation(category="form interaction", name="submit", payload=payload)


def test_payload_validation__form_submition_validation_validation__invalid_payload():
    payload = {
        "host": "www.consumeraffairs.com",
        "path": "/",
    }
    with pytest.raises(PayloadValidationError):
        payload_validation(category="form interaction", name="submit", payload=payload)
