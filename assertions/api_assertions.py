import json


def assert_status(response, expected_status: int):
    body_preview = response.text[:400] if response.text else ""
    assert response.status_code == expected_status, (
        f"Expected {expected_status}, got {response.status_code}. "
        f"URL: {response.url}. Body: {body_preview}"
    )


def assert_json_content_type(response):
    content_type = response.headers.get("Content-Type", "")
    assert "application/json" in content_type, (
        f"Expected JSON Content-Type, got: {content_type}. URL: {response.url}"
    )


def assert_json_is_list(response):
    try:
        data = response.json()
    except Exception:
        raise AssertionError(f"Response is not valid JSON. URL: {response.url}. Body: {response.text[:400]}")
    assert isinstance(data, list), f"Expected JSON list, got {type(data)}. URL: {response.url}"


def assert_json_has_keys(item: dict, required_keys: list[str]):
    assert isinstance(item, dict), f"Expected dict item, got {type(item)}"
    missing = [k for k in required_keys if k not in item]
    assert not missing, f"Missing keys: {missing}. Item: {json.dumps(item, ensure_ascii=False)[:400]}"
