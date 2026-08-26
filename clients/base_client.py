import time

import requests
from requests.auth import HTTPBasicAuth

from config.settings import (
    API_KEY_HEADER,
    API_KEY_VALUE,
    AUTH_PASSWORD,
    AUTH_TOKEN,
    AUTH_TYPE,
    AUTH_USERNAME,
    BASE_URL,
    EXTRA_HEADERS,
    LOG_BODY_MAX_CHARS,
    LOG_HTTP,
    LOG_REQUEST_BODY,
    LOG_RESPONSE_BODY,
    TIMEOUT,
    VERIFY_SSL,
)
from utils.logger import get_logger

logger = get_logger("api.http")

VALID_METHODS = {"GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"}

# Headers que nunca se imprimen en claro en los logs.
SENSITIVE_HEADER_KEYS = {"authorization", "x-api-key", "api-key", "cookie", "set-cookie"}


def _redact_headers(headers: dict) -> dict:
    if not headers:
        return {}
    redacted = {}
    for key, value in headers.items():
        if key.lower() in SENSITIVE_HEADER_KEYS or key.lower() == API_KEY_HEADER.lower():
            redacted[key] = "***REDACTED***"
        else:
            redacted[key] = value
    return redacted


def _truncate(text: str, limit: int) -> str:
    if not text:
        return ""
    return text if len(text) <= limit else text[:limit] + f"... [truncated, {len(text)} chars total]"


class BaseClient:
    """
    Cliente HTTP generico y parametrizable.

    - Base URL + endpoint: la base sale de config/settings.py (.env);
      el endpoint concreto se pasa por parametro en cada llamada.
    - Operacion (verbo HTTP): se parametriza via request(method=...) o los
      metodos de conveniencia get/post/put/patch/delete/head/options.
    - Body: se pasa por parametro (json= para JSON, data= para form/raw)
      solo cuando la operacion lo necesita.
    - Headers / autenticacion: se resuelven automaticamente segun AUTH_TYPE
      (.env) y se pueden extender o sobreescribir por request con headers=.
    """

    def __init__(self, base_url: str = None, timeout: int = None, auth_type: str = None):
        self.base_url = base_url or BASE_URL
        self.timeout = timeout or TIMEOUT
        self.verify_ssl = VERIFY_SSL
        self.auth_type = (auth_type or AUTH_TYPE or "none").lower()
        self.session = requests.Session()

    # ---- construccion de URL / headers / auth --------------------------
    def _url(self, endpoint: str) -> str:
        if endpoint.startswith("http://") or endpoint.startswith("https://"):
            return endpoint
        return f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"

    def _build_headers(self, headers: dict = None) -> dict:
        final_headers = {}
        final_headers.update(EXTRA_HEADERS or {})

        if self.auth_type == "bearer" and AUTH_TOKEN:
            final_headers["Authorization"] = f"Bearer {AUTH_TOKEN}"
        elif self.auth_type == "api_key" and API_KEY_VALUE:
            final_headers[API_KEY_HEADER] = API_KEY_VALUE
        # "basic" se resuelve via requests' auth=, no como header manual.
        # "none" / "custom": nada automatico; el caller controla los headers.

        if headers:
            final_headers.update(headers)
        return final_headers

    def _build_auth(self):
        if self.auth_type == "basic" and (AUTH_USERNAME or AUTH_PASSWORD):
            return HTTPBasicAuth(AUTH_USERNAME, AUTH_PASSWORD)
        return None

    # ---- request generico ------------------------------------------------
    def request(
        self,
        method: str,
        endpoint: str,
        *,
        params: dict = None,
        json: dict = None,
        data=None,
        headers: dict = None,
        files=None,
        timeout: int = None,
        **kwargs,
    ) -> requests.Response:
        """
        Ejecuta cualquier operacion HTTP contra base_url + endpoint.

        method:   "GET" | "POST" | "PUT" | "PATCH" | "DELETE" | "HEAD" | "OPTIONS"
        endpoint: path relativo a BASE_URL (o una URL absoluta).
        json:     body como dict, se serializa a JSON automaticamente.
        data:     body crudo / form-encoded, alternativa a json.
        headers:  headers puntuales para esta llamada; se combinan con los
                  headers de autenticacion/EXTRA_HEADERS ya resueltos.
        """
        method = method.upper()
        if method not in VALID_METHODS:
            raise ValueError(f"Metodo HTTP no soportado: {method}. Validos: {sorted(VALID_METHODS)}")

        url = self._url(endpoint)
        final_headers = self._build_headers(headers)
        auth = self._build_auth()
        req_timeout = timeout or self.timeout

        if LOG_HTTP:
            body_preview = ""
            if LOG_REQUEST_BODY:
                if json is not None:
                    body_preview = _truncate(str(json), LOG_BODY_MAX_CHARS)
                elif data is not None:
                    body_preview = _truncate(str(data), LOG_BODY_MAX_CHARS)
            logger.info(
                ">>> %s %s | params=%s | headers=%s | body=%s",
                method, url, params, _redact_headers(final_headers), body_preview,
            )

        start = time.perf_counter()
        response = self.session.request(
            method=method,
            url=url,
            params=params,
            json=json,
            data=data,
            headers=final_headers,
            files=files,
            auth=auth,
            timeout=req_timeout,
            verify=self.verify_ssl,
            **kwargs,
        )
        elapsed_ms = (time.perf_counter() - start) * 1000

        if LOG_HTTP:
            resp_body_preview = _truncate(response.text, LOG_BODY_MAX_CHARS) if LOG_RESPONSE_BODY else ""
            logger.info(
                "<<< %s %s %s | %.1f ms | resp_headers=%s | body=%s",
                response.status_code, method, url, elapsed_ms,
                _redact_headers(dict(response.headers)), resp_body_preview,
            )

        return response

    # ---- metodos de conveniencia por verbo ------------------------------
    def get(self, endpoint, params=None, headers=None, **kwargs):
        return self.request("GET", endpoint, params=params, headers=headers, **kwargs)

    def post(self, endpoint, json=None, data=None, params=None, headers=None, **kwargs):
        return self.request("POST", endpoint, json=json, data=data, params=params, headers=headers, **kwargs)

    def put(self, endpoint, json=None, data=None, params=None, headers=None, **kwargs):
        return self.request("PUT", endpoint, json=json, data=data, params=params, headers=headers, **kwargs)

    def patch(self, endpoint, json=None, data=None, params=None, headers=None, **kwargs):
        return self.request("PATCH", endpoint, json=json, data=data, params=params, headers=headers, **kwargs)

    def delete(self, endpoint, params=None, headers=None, **kwargs):
        return self.request("DELETE", endpoint, params=params, headers=headers, **kwargs)

    def head(self, endpoint, params=None, headers=None, **kwargs):
        return self.request("HEAD", endpoint, params=params, headers=headers, **kwargs)

    def options(self, endpoint, params=None, headers=None, **kwargs):
        return self.request("OPTIONS", endpoint, params=params, headers=headers, **kwargs)
