import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://fruityvice.com/api")
TIMEOUT = int(os.getenv("TIMEOUT", 10))
HEALTH_ENDPOINT = os.getenv("HEALTH_ENDPOINT", "/fruit/all")

LOG_HTTP = os.getenv("LOG_HTTP", "false").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
