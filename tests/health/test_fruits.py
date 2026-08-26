from clients.base_client import BaseClient
from config.settings import HEALTH_ENDPOINT
from assertions.api_assertions import (
    assert_status,
    assert_json_content_type
)


def test_api_healthcheck(client: BaseClient):
    r = client.get(HEALTH_ENDPOINT)
    data = r.json()
    assert_status(r, 200)
    assert_json_content_type(r)
