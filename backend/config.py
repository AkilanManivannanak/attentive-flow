import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

CUSTOMERS_PATH = DATA_DIR / "synthetic_customers.json"
EVENTS_PATH = DATA_DIR / "synthetic_events.json"


def get_secret_value(key: str, default: str | None = None) -> str | None:
    """
    Read config from environment first, then Streamlit secrets if available.

    This keeps the project runnable in:
    - local CLI / FastAPI
    - local Streamlit
    - Streamlit Community Cloud
    """

    value = os.getenv(key)
    if value:
        return value

    try:
        import streamlit as st

        if hasattr(st, "secrets") and key in st.secrets:
            return st.secrets[key]
    except Exception:
        pass

    return default


OPENAI_API_KEY = get_secret_value("OPENAI_API_KEY")
MODEL_NAME = get_secret_value("MODEL_NAME", "gpt-4o-mini")
USE_LLM_COPY = get_secret_value("USE_LLM_COPY", "true").lower() == "true"
