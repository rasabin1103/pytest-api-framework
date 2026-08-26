from clients.base_client import BaseClient
from config.settings import HEALTH_ENDPOINT
from assertions.api_assertions import (
    assert_status
)


def test_api_healthcheck(client: BaseClient):
    r = client.get(HEALTH_ENDPOINT)
    assert_status(r, 200)
