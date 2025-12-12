import requests
from config.settings import BASE_URL, TIMEOUT, LOG_HTTP
from utils.logger import get_logger


logger = get_logger("luda.http")

class BaseClient:
    def __init__(self):
        self.base_url = BASE_URL
        self.timeout = TIMEOUT

    def _url(self, endpoint: str) -> str:
        return f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"

    def get(self, endpoint, params=None, headers=None):
        url = self._url(endpoint)
        if LOG_HTTP:
            logger.info(f"GET {url} params={params}")

        response = requests.get(
            url=url,
            params=params,
            headers=headers,
            timeout=self.timeout
        )

        if LOG_HTTP:
            logger.info(f"RESP {response.status_code} {url} body={response.text[:200]}")

        return response