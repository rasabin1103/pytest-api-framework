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

LOG_HTTP=true
LOG_LEVEL=DEBUG
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