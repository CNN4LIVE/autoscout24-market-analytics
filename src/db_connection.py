import os
import urllib.parse
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

def get_db_engine():
    # 1. Bevorzugt Streamlit Secrets nutzen
    try:
        import streamlit as st
        if "DATABASE_URL" in st.secrets:
            return create_engine(st.secrets["DATABASE_URL"])
    except Exception:
        pass

    # 2. Falls DATABASE_URL in der .env existiert
    if os.getenv("DATABASE_URL"):
        return create_engine(os.getenv("DATABASE_URL"))

    # 3. Fallback
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME", "olympics_db")
    db_user = os.getenv("DB_USER", "postgres")
    db_pass = os.getenv("DB_PASSWORD") or os.getenv("DB_PASS", "")

    safe_password = urllib.parse.quote_plus(db_pass)
    safe_user = urllib.parse.quote_plus(db_user)

    url = f"postgresql://{safe_user}:{safe_password}@{db_host}:{db_port}/{db_name}"
    return create_engine(url)
