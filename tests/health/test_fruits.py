from clients.base_client import BaseClient
from config.settings import HEALTH_ENDPOINT
from assertions.api_assertions import (
    assert_status,
    assert_json_content_type,
    assert_json_is_list,
)


def test_api_healthcheck(client: BaseClient):
    r = client.get(HEALTH_ENDPOINT)
    data = r.json()
    assert_status(r, 200)
    assert_json_content_type(r)
    assert_json_is_list(r)
