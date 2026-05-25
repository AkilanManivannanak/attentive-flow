import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

CUSTOMERS_PATH = DATA_DIR / "synthetic_customers.json"
EVENTS_PATH = DATA_DIR / "synthetic_events.json"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
