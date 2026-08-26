import json as _json
import os

from dotenv import load_dotenv

load_dotenv()


def _get_bool(name: str, default: str = "false") -> bool:
    return os.getenv(name, default).strip().lower() in ("1", "true", "yes", "on")


def _get_int(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, str(default)))
    except (TypeError, ValueError):
        return default


# --- Base API configuration -------------------------------------------------
# Solo la base comun. Los endpoints concretos se pasan por parametro al client
# (client.get("/fruit/all"), client.post("/orders", json={...}), etc.)
BASE_URL = os.getenv("BASE_URL", "https://fruityvice.com/api")
TIMEOUT = _get_int("TIMEOUT", 10)
VERIFY_SSL = _get_bool("VERIFY_SSL", "true")

# Endpoint(s) usados por los tests de ejemplo/health check.
HEALTH_ENDPOINT = os.getenv("HEALTH_ENDPOINT", "/fruit/all")

# --- Logging ------------------------------------------------------------
LOG_HTTP = _get_bool("LOG_HTTP", "false")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_REQUEST_BODY = _get_bool("LOG_REQUEST_BODY", "true")
LOG_RESPONSE_BODY = _get_bool("LOG_RESPONSE_BODY", "true")
LOG_BODY_MAX_CHARS = _get_int("LOG_BODY_MAX_CHARS", 2000)

# --- Autenticacion ------------------------------------------------------
# AUTH_TYPE: none | bearer | basic | api_key | custom
#   none    -> no se agrega nada automaticamente
#   bearer  -> Authorization: Bearer <AUTH_TOKEN>
#   basic   -> HTTP Basic Auth con AUTH_USERNAME / AUTH_PASSWORD
#   api_key -> header API_KEY_HEADER: API_KEY_VALUE
#   custom  -> el propio test/cliente arma los headers (via EXTRA_HEADERS
#              o pasando headers= directamente en la llamada)
AUTH_TYPE = os.getenv("AUTH_TYPE", "none").strip().lower()

AUTH_TOKEN = os.getenv("AUTH_TOKEN", "")
AUTH_USERNAME = os.getenv("AUTH_USERNAME", "")
AUTH_PASSWORD = os.getenv("AUTH_PASSWORD", "")

API_KEY_HEADER = os.getenv("API_KEY_HEADER", "x-api-key")
API_KEY_VALUE = os.getenv("API_KEY_VALUE", "")

# Headers estaticos adicionales para TODAS las requests, en formato JSON.
# Ej: EXTRA_HEADERS={"X-Client-Id":"qa-suite","Accept-Language":"es"}
try:
    EXTRA_HEADERS = _json.loads(os.getenv("EXTRA_HEADERS", "{}"))
    if not isinstance(EXTRA_HEADERS, dict):
        EXTRA_HEADERS = {}
except (ValueError, TypeError):
    EXTRA_HEADERS = {}
