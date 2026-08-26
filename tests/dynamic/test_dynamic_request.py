"""
Ejecuta UNA peticion HTTP definida 100% por variables de entorno.

Pensado para ser disparado desde una plataforma externa (ASE Platform u
otra) que ya sabe autenticarse contra este repo (ej. via GitHub Actions
workflow_dispatch con un token de grano fino) y que envia: metodo, endpoint,
body, headers y opcionalmente los query params y el status esperado.

Variables de entrada:
    REQ_METHOD           GET | POST | PUT | PATCH | DELETE (default GET)
    REQ_ENDPOINT         path relativo a BASE_URL. Si no viene, el test se
                          salta (para no romper corridas normales del suite).
    REQ_BODY              JSON del body (opcional)
    REQ_HEADERS            JSON de headers puntuales (opcional)
    REQ_PARAMS             JSON de query params (opcional)
    REQ_EXPECTED_STATUS    status esperado, ej "201" (opcional; si se omite
                            el test solo reporta el detalle, no falla por status)

Salida:
    request_result.json en la raiz del repo, con el detalle completo de
    request/response/resultado, listo para que quien disparo la corrida
    lo recupere despues (ej. como artifact de GitHub Actions).
    Si corre dentro de GitHub Actions tambien escribe un resumen legible
    en el Job Summary ($GITHUB_STEP_SUMMARY).
"""
import json
import os
import time

import pytest

from clients.base_client import BaseClient
from utils.logger import get_logger

logger = get_logger("api.dynamic")

RESULT_FILE = os.path.join(os.getcwd(), "request_result.json")


def _load_json_env(name: str, default=None):
    raw = os.getenv(name, "")
    if not raw or not raw.strip():
        return default
    try:
        return json.loads(raw)
    except (ValueError, TypeError) as exc:
        pytest.fail(f"{name} no es JSON valido: {raw!r} ({exc})")


@pytest.mark.skipif(
    not os.getenv("REQ_ENDPOINT"),
    reason="No se definio REQ_ENDPOINT: este test solo corre en ejecuciones "
           "dinamicas disparadas con method/endpoint/body por variables.",
)
def test_dynamic_request(client: BaseClient):
    method = os.getenv("REQ_METHOD", "GET").upper()
    endpoint = os.getenv("REQ_ENDPOINT")
    body = _load_json_env("REQ_BODY")
    headers = _load_json_env("REQ_HEADERS")
    params = _load_json_env("REQ_PARAMS")
    expected_status_raw = os.getenv("REQ_EXPECTED_STATUS", "").strip()

    start = time.perf_counter()
    response = client.request(method, endpoint, json=body, headers=headers, params=params)
    elapsed_ms = (time.perf_counter() - start) * 1000

    try:
        response_body = response.json()
    except ValueError:
        response_body = response.text

    result = {
        "request": {
            "method": method,
            "url": response.url,
            "endpoint": endpoint,
            "params": params,
            "body": body,
        },
        "response": {
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "body": response_body,
            "elapsed_ms": round(elapsed_ms, 1),
        },
        "result": "REPORTED",
    }

    if expected_status_raw:
        expected_status = int(expected_status_raw)
        result["expected_status"] = expected_status
        result["result"] = "PASSED" if response.status_code == expected_status else "FAILED"

    with open(RESULT_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    logger.info("Resultado dinamico: %s", json.dumps(result, ensure_ascii=False)[:1500])

    summary_path = os.getenv("GITHUB_STEP_SUMMARY")
    if summary_path:
        body_preview = json.dumps(response_body, ensure_ascii=False, indent=2)[:4000] \
            if not isinstance(response_body, str) else response_body[:4000]
        with open(summary_path, "a", encoding="utf-8") as f:
            f.write("## Resultado de la peticion dinamica\n\n")
            f.write(f"- **Metodo:** {method}\n")
            f.write(f"- **URL:** {response.url}\n")
            f.write(f"- **Status:** {response.status_code}\n")
            f.write(f"- **Tiempo:** {elapsed_ms:.1f} ms\n")
            f.write(f"- **Resultado:** {result['result']}\n\n")
            f.write("### Body de respuesta\n\n```json\n")
            f.write(body_preview)
            f.write("\n```\n")

    if expected_status_raw:
        assert response.status_code == int(expected_status_raw), (
            f"Se esperaba status {expected_status_raw}, se obtuvo {response.status_code}. "
            f"Body: {str(response_body)[:400]}"
        )
