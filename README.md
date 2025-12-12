# LUDA – API Testing Framework  
### Pytest + Requests | Level Up Digital Academy

Framework base para **testing de APIs REST en Python**, diseñado con mentalidad de ingeniería real:

- 🧱 **Modular** – estructura clara y extensible  
- 📈 **Escalable** – crece sin refactorizaciones dolorosas  
- 🔌 **Plug & Play** – clonas, configuras y ejecutas  
- ⚙️ **Configuración sobre código** – se cambia `.env`, no el core  

---

## 🛠️ Stack Tecnológico

- Python 3.x  
- Pytest  
- Requests  
- python-dotenv  
- pytest-html (reporte opcional)  

---

## 📁 Estructura del Proyecto

```text
luda_api-testing-pytest-framework/
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
│   ├── health_test/
│   │   └── test_fruits.py
│   └── fruit/
│       └── test_fruit_all.py
│
├── requirements.txt
├── pytest.ini
├── .gitignore
└── README.md
```

## ⚡ Quickstart

### 1️⃣ Clonar el repositorio
```bash
git clone <URL_DEL_REPO>
cd luda_api-testing-pytest-framework
```

### 2️⃣ Crear entorno virtual (venv)

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

## 3️⃣ Instalar dependencias
```bash
pip install -r requirements.txt
```

## 4️⃣ Configurar el entorno (.env)
Crear un archivo .env en la raíz del proyecto:

```env
BASE_URL=https://fruityvice.com/api
HEALTH_ENDPOINT=/fruit/all
TIMEOUT=10

LOG_HTTP=true
LOG_LEVEL=DEBUG
```

⚠️ Regla importante sobre BASE_URL
```text
BASE_URL debe ser solo la base común (host + prefijo), sin endpoints finales.

Correcto:
- BASE_URL=https://fruityvice.com/api
- HEALTH_ENDPOINT=/fruit/all

Incorrecto:
- BASE_URL=https://fruityvice.com/api/fruit/all
```

## 5️⃣ Ejecutar los tests
```bash
pytest -v
```

## 6️⃣ Generar reporte HTML (opcional)
```bash
pytest --html=report.html --self-contained-html
```

## 🧪 Pytest – Reglas Importantes (pytest.ini)
```text
testpaths = tests
→ Pytest solo buscará tests dentro de la carpeta tests/

python_files = test_*.py
→ Los archivos de test deben comenzar por test_

Si se desea cambiar la convención:
- python_files = *_test.py
- python_files = test_*.py *_test.py

El framework tiene activado log_cli = true para mostrar logs en consola.

```

## 🪵 Logging (Opcional)
```text
Por defecto el framework funciona sin logs.

Para activarlos:
LOG_HTTP=true
LOG_LEVEL=INFO

LOG_HTTP=true  → habilita logs HTTP
LOG_LEVEL=DEBUG → máximo detalle
LOG_LEVEL=INFO  → recomendado
LOG_LEVEL=WARNING / ERROR → salida mínima

```

## 🔄 Flujo Recomendado para Añadir Nuevas Pruebas

### 1️⃣ Crear carpeta por dominio / feature

```text
tests/users/
tests/orders/
tests/auth/
tests/health/
```

### 2️⃣ Crear archivo de test siguiendo la convención

```text
tests/users/test_users.py
tests/orders/test_orders.py
```

### 3️⃣ Usar el cliente global (fixture)

```bash
def test_example(client):
    response = client.get("/endpoint")
    assert response.status_code == 200
```

### 4️⃣ Reutilizar assertions comunes

```bash
from assertions.api_assertions import (
    assert_status,
    assert_json_content_type
)
```

## 🌍 Cómo Testear Diferentes APIs REST

### Opción A – Cambiar .env y ejecutar
```text
BASE_URL=https://mi-api.com/api
HEALTH_ENDPOINT=/health
```
```bash
pytest -v
```

### Opción B – Múltiples .env por entorno (recomendada)
```text
.env.fruityvice
.env.staging
.env.prod
```
Ejemplo .env.staging:

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

### Opción C – Clientes separados por API
```text
clients/mi_api_client.py
clients/otra_api_client.py
```
Y exponer fixtures distintas en conftest.py.