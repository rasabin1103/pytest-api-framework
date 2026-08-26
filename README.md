# 🚀 Pytest API Framework  
### Scalable REST API Testing Template for Real Engineering Teams

A production-ready API testing framework built on Pytest and Requests, designed for maintainability, scalability, and CI/CD integration from day one.


---

## 🎯 Framework Philosophy

This is not just a collection of tests.

It is designed around clear architectural principles:

- 🧱 Modular architecture
- 📈 Scalable without painful refactors
- 🔌 True Plug & Play
- ⚙️ Configuration over code
- 🔍 Strict separation between HTTP logic and tests
- 📦 CI/CD-ready from day one

---

## 🛠️ Technology Stack

- Python >= 3.10 / Recommended: Python 3.12 
- Pytest  
- Requests  
- python-dotenv  
- pytest-html (reporte opcional)  
- Configurable logging

---

## 📁 Project Structure

```text
pytest-api-framework/
│
├── assertions/
│   ├── __init__.py
│   └── api_assertions.py
│
├── clients/
│   ├── __init__.py
│   └── base_client.py
│
├── config/
│   ├── __init__.py
│   └── settings.py
│
├── utils/
│   ├── __init__.py
│   └── logger.py
│
├── tests/
│   ├── conftest.py
│   ├── health/
│   │   └── test_fruits.py
│   └── fruit/
│       └── test_fruit_all.py
│
├── requirements.txt
├── pytest.ini
├── .gitignore
└── README.md
```

## 🧠 Internal Architecture

### clients/

Contains all HTTP logic.

BaseClient is responsible for:

- Base URL handling
- Timeouts
- Optional HTTP logging
- Request encapsulation

Tests do not build URLs manually.
Tests call the client.

### assertions/

Centralizes reusable validations:

- assert_status
- assert_json_content_type
- Future schema validations

Prevents duplicated assert response.status_code == 200 everywhere.

### config/

Loads configuration from .env using python-dotenv.

The framework is designed so environments change without touching the code.

### tests/

Only tests live here.

No HTTP logic.
No configuration logic.
Only expected behavior.

## ⚡ Quickstart

### 1️⃣ Clone the repository
```bash
git clone <REPOSITORY_URL>
cd pytest-api-framework
```

### 2️⃣ Create virtual environment (venv)

#### Windows (PowerShell)
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```

#### Windows (CMD)
```bash
python -m venv venv
venv\Scripts\activate.bat
```

#### Linux / macOS
```bash
python -m venv venv
source venv/bin/activate
```

## 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

## 4️⃣ Configure environment (.env)
Create a .env file at project root:

```env
BASE_URL=https://fruityvice.com/api
HEALTH_ENDPOINT=/fruit/all
TIMEOUT=10
VERIFY_SSL=true

LOG_HTTP=true
LOG_LEVEL=DEBUG
LOG_REQUEST_BODY=true
LOG_RESPONSE_BODY=true
LOG_BODY_MAX_CHARS=2000

# Autenticacion (ver seccion "Autenticacion y headers especiales")
AUTH_TYPE=none
AUTH_TOKEN=
AUTH_USERNAME=
AUTH_PASSWORD=
API_KEY_HEADER=x-api-key
API_KEY_VALUE=
EXTRA_HEADERS={}
```

Hay un `.env.example` en la raiz con todas las variables documentadas: copialo a `.env` y ajusta valores.
```bash
cp .env.example .env
```

⚠️ Important Rule
```text
BASE_URL must contain only the common base.

Correct:
- BASE_URL=https://fruityvice.com/api
- HEALTH_ENDPOINT=/fruit/all

Incorrect:
- BASE_URL=https://fruityvice.com/api/fruit/all
```

## 🔧 Operaciones HTTP parametrizadas (GET/POST/PUT/PATCH/DELETE...)

El cliente ya no esta limitado a `GET`. Toda operacion se resuelve con un
metodo generico `request(method, endpoint, ...)` mas atajos por verbo:

```python
def test_get_fruit(client):
    r = client.get("/fruit/banana")

def test_create_order(client):
    r = client.post("/orders", json={"item": "banana", "qty": 3})

def test_update_order(client):
    r = client.put("/orders/123", json={"qty": 5})

def test_partial_update(client):
    r = client.patch("/orders/123", json={"qty": 1})

def test_delete_order(client):
    r = client.delete("/orders/123")

# Forma generica (equivalente, util para verbos poco comunes: HEAD, OPTIONS)
def test_generic(client):
    r = client.request("POST", "/orders", json={"item": "banana"}, params={"dryRun": "true"})
```

`endpoint` sigue siendo solo el path relativo: la base sale de `BASE_URL`.
El **body** se pasa por parametro (`json=` para JSON, `data=` para
form-encoded/raw) unicamente cuando la operacion lo requiere; en GET/DELETE
simplemente se omite.

## 🔐 Autenticacion y headers especiales

La autenticacion se resuelve automaticamente en cada request segun
`AUTH_TYPE` en `.env`, sin tocar los tests:

| AUTH_TYPE | Variables usadas | Efecto |
|---|---|---|
| `none` (default) | - | No se agrega nada automatico |
| `bearer` | `AUTH_TOKEN` | Header `Authorization: Bearer <token>` |
| `basic` | `AUTH_USERNAME`, `AUTH_PASSWORD` | HTTP Basic Auth |
| `api_key` | `API_KEY_HEADER`, `API_KEY_VALUE` | Header `<API_KEY_HEADER>: <API_KEY_VALUE>` |
| `custom` | - | El test/cliente arma los headers a mano |

Headers estaticos adicionales para **todas** las requests (cualquier
`AUTH_TYPE`) se definen en `EXTRA_HEADERS` como JSON:

```env
EXTRA_HEADERS={"X-Client-Id":"qa-suite","Accept-Language":"es"}
```

Y headers puntuales para una sola llamada se pasan directo:

```python
def test_with_custom_header(client):
    r = client.get("/secure/data", headers={"X-Trace-Id": "abc-123"})
```

Los headers sensibles (`Authorization`, `x-api-key`, `Cookie`, etc.) nunca
se imprimen en claro en los logs; aparecen como `***REDACTED***`.

Para usar credenciales distintas en un mismo suite (p.ej. un cliente admin
y uno anonimo), instancia clientes adicionales:

```python
admin_client = BaseClient(auth_type="bearer")
public_client = BaseClient(auth_type="none")
```

## 🌐 Ejecucion dinamica disparada desde una plataforma externa (ej. ASE Platform)

Ademas de escribir tests fijos, el framework puede ejecutar UNA peticion
cuya definicion (metodo, endpoint, body, headers, params) llega por
variables de entorno. Esto permite que una plataforma externa que ya sabe
autenticarse contra este repo (ej. via la API de GitHub Actions con un
token de grano fino) dispare `workflow_dispatch` pasando esos valores como
inputs, sin tocar codigo ni tests.

Inputs del workflow (`.github/workflows/run-tests.yml`):

- `base_url`, `auth_type` (igual que antes)
- `method` — GET | POST | PUT | PATCH | DELETE
- `endpoint` — path relativo a `base_url`, ej. `/orders`
- `body` — JSON del body (si el metodo lo requiere)
- `headers` — JSON con headers puntuales para esa llamada
- `params` — JSON con query params
- `expected_status` — opcional; si se deja vacio el test solo reporta el
  resultado, no falla por status

El test `tests/dynamic/test_dynamic_request.py` toma esos valores
(`REQ_METHOD`, `REQ_ENDPOINT`, `REQ_BODY`, `REQ_HEADERS`, `REQ_PARAMS`,
`REQ_EXPECTED_STATUS`), ejecuta la peticion contra `BASE_URL + endpoint`
usando la misma autenticacion configurada (`AUTH_TYPE`), y dos cosas
quedan disponibles para quien disparo la corrida:

1. **`request_result.json`** (raiz del repo, subido como artifact
   `request-result`): request completo, response completo (status,
   headers, body, tiempo en ms) y `result` (`REPORTED` / `PASSED` /
   `FAILED`). Es lo que la plataforma externa deberia leer despues (via la
   API de GitHub: listar artifacts del run y descargar).
2. **Job Summary de GitHub Actions**: el mismo detalle en formato legible,
   visible directo en la pantalla del run sin descargar nada.

Si `REQ_ENDPOINT` no viene definido, el test se salta automaticamente y no
afecta las corridas normales del suite (health check, etc).

## 🪵 Maxima informacion en logs

Con `LOG_HTTP=true` cada request/response queda registrado con: metodo,
URL completa, query params, headers (redactando secretos), body de
request y response (recortado a `LOG_BODY_MAX_CHARS`), status code y
tiempo de respuesta en ms. Es la fuente principal de diagnostico cuando
un test falla.

## 5️⃣ Run tests
```bash
pytest -v
```

6️⃣ Generate HTML report (optional)
```bash
pytest --html=report.html --self-contained-html
```

## 🧪 Pytest Conventions (pytest.ini)
```text
testpaths = tests
→ Tests are discovered only inside /tests

python_files = test_*.py
→ Test files must start with test_

If the convention is to be changed:
- python_files = *_test.py
- python_files = test_*.py *_test.py

The framework has log_cli = true enabled to display logs in console.

```

## 🪵 Configurable Logging
```text
By default, logging is disabled.

Enable in .env:
LOG_HTTP=true
LOG_LEVEL=INFO

LOG_HTTP=true  → habilita logs HTTP
LOG_LEVEL=DEBUG → máximo detalle
LOG_LEVEL=INFO  → recomendado
LOG_LEVEL=WARNING / ERROR → salida mínima

```

## 🔄 How to Add New Tests

### 1️⃣ Create domain-based folder

```text
tests/users/
tests/orders/
tests/auth/
tests/health/
```

### 2️⃣ Create test file following convention

```text
tests/users/test_users.py
tests/orders/test_orders.py
```

### 3️⃣ Use global client fixture

```bash
def test_example(client):
    response = client.get("/endpoint")
    assert response.status_code == 200
```

### 4️⃣ Reuse common assertions

```bash
from assertions.api_assertions import (
    assert_status,
    assert_json_content_type
)
```

## 🌍 Multi-Environment Testing

### Option A — Manually change .env
```text
BASE_URL=https://mi-api.com/api
HEALTH_ENDPOINT=/health
```
```bash
pytest -v
```

### Option B — Multiple .env files (recommended)
```text
.env.fruityvice
.env.staging
.env.prod
```
Example: .env.staging:

```text
BASE_URL=https://staging.mi-api.com/api
HEALTH_ENDPOINT=/health
TIMEOUT=10
LOG_HTTP=false
LOG_LEVEL=INFO
```

```bash
set DOTENV_FILE=.env.staging && pytest -v
```

### Option C — Multiple Clients
```text
clients/mi_api_client.py
clients/otra_api_client.py
```
Y exponer fixtures distintas en conftest.py.

## 🏗️ Design Principles

-  Short and expressive tests

- Reusable HTTP client

- Decoupled configuration

- CI/CD ready

- Reporting friendly

- Easily extendable to:

    - JSON Schema validation

    - Lightweight contract testing

    - Centralized authentication

    - Pipeline integration


## 👤 Maintainer

**Roberto Arce**  
QA Strategy Lead | Quality Engineering & Automation Architecture | Shift-Left & CI/CD Advocate