"""
FinEdge Digital Solutions — Customer Account Activity Analysis (CAAA)
Data Ingestion & Caching Layer
File: src/data_loader.py
"""

import os
import sqlite3
from pathlib import Path
import pandas as pd
import streamlit as st

def get_default_db_path() -> str:
    """Resolve cross-platform path to data/app.db using pathlib."""
    # Resolve relative to src/ directory: Path(__file__).resolve().parent.parent / "data" / "app.db"
    db_file = Path(__file__).resolve().parent.parent / "data" / "app.db"
    if db_file.exists():
        return str(db_file)
    
    # Fallback to working directory relative path
    local_db = Path("data/app.db").resolve()
    if local_db.exists():
        return str(local_db)
        
    return str(db_file)

def get_db_connection(db_path: str = None) -> sqlite3.Connection:
    """
    Establish a thread-safe, read-only SQLite connection.
    Uses URI read-only mode to prevent unintended database writes.
    Compatible across Windows and Linux (Streamlit Community Cloud).
    """
    if db_path is None:
        db_path = get_default_db_path()
        
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database file not found at: {db_path}")

    # Standardize cross-platform posix path for URI syntax
    clean_path = Path(db_path).resolve().as_posix()
    uri_str = f"file:{clean_path}?mode=ro"
    
    try:
        conn = sqlite3.connect(uri_str, uri=True, check_same_thread=False)
    except sqlite3.OperationalError:
        # Fallback if URI mode fails on specific OS configurations
        conn = sqlite3.connect(db_path, check_same_thread=False)
        
    return conn

@st.cache_data(ttl=3600, show_spinner="Loading customer account records...")
def load_analytical_view(db_path: str = None) -> pd.DataFrame:
    """
    Load the unified 42-column analytical view (vw_customer_account_activity_analysis)
    from SQLite into a cached pandas DataFrame.
    """
    conn = get_db_connection(db_path)
    try:
        query = "SELECT * FROM vw_customer_account_activity_analysis;"
        df = pd.read_sql_query(query, conn)
    finally:
        conn.close()

    if df.empty:
        raise ValueError("Analytical view returned zero records.")

    # Parse standard date fields
    date_columns = ["opened_date", "txn_date", "snapshot_month", "last_active_date", "transaction_date"]
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    # Enforce numeric types on financial columns
    monetary_cols = ["current_balance", "amount", "min_balance_req", "minimum_balance_req", "monthly_income", "annual_income"]
    for col in monetary_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df

@st.cache_data(ttl=3600, show_spinner="Loading table...")
def load_table(table_name: str, db_path: str = None) -> pd.DataFrame:
    """
    Load individual master or fact tables with whitelist SQL injection prevention.
    """
    valid_tables = {
        "dim_customers",
        "dim_accounts",
        "dim_channels",
        "fact_transactions",
        "fact_monthly_snapshots",
        "vw_customer_account_activity_analysis"
    }
    if table_name not in valid_tables:
        raise ValueError(f"Unauthorized table requested: {table_name}. Allowed: {valid_tables}")

    conn = get_db_connection(db_path)
    try:
        query = f"SELECT * FROM {table_name};"
        df = pd.read_sql_query(query, conn)
    finally:
        conn.close()

    return df
