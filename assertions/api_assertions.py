import json


def assert_status(response, expected_status: int):
    body_preview = response.text[:400] if response.text else ""
    assert response.status_code == expected_status, (
        f"Expected {expected_status}, got {response.status_code}. "
        f"URL: {response.url}. Body: {body_preview}"
    )


def assert_status_in(response, expected_statuses: list[int]):
    body_preview = response.text[:400] if response.text else ""
    assert response.status_code in expected_statuses, (
        f"Expected one of {expected_statuses}, got {response.status_code}. "
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


def assert_header_present(response, header_name: str):
    assert header_name in response.headers, (
        f"Missing expected header '{header_name}'. URL: {response.url}. "
        f"Headers present: {list(response.headers.keys())}"
    )


def assert_header_value(response, header_name: str, expected_value: str):
    assert_header_present(response, header_name)
    actual = response.headers.get(header_name)
    assert actual == expected_value, (
        f"Header '{header_name}' expected '{expected_value}', got '{actual}'. URL: {response.url}"
    )


def assert_response_time_below(response, max_seconds: float):
    elapsed = response.elapsed.total_seconds()
    assert elapsed <= max_seconds, (
        f"Response took {elapsed:.3f}s, expected <= {max_seconds}s. URL: {response.url}"
    )
