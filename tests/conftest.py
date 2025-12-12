import pytest
from clients.base_client import BaseClient

@pytest.fixture(scope="session")
def client():
    return BaseClient()
