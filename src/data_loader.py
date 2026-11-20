"""
FinEdge Digital Solutions — Customer Account Activity Analysis (CAAA)
Data Ingestion & Caching Layer
File: src/data_loader.py
"""

import os
import sqlite3
import pandas as pd
import streamlit as st

def get_default_db_path() -> str:
    """Resolve absolute path to data/app.db across root, tests, or subpages."""
    # Look for data/app.db relative to current file or working directory
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_path = os.path.join(base_dir, "data", "app.db")
    if os.path.exists(target_path):
        return target_path
    
    # Fallback to relative path
    if os.path.exists("data/app.db"):
        return os.path.abspath("data/app.db")
        
    return target_path

def get_db_connection(db_path: str = None) -> sqlite3.Connection:
    """
    Establish a thread-safe, read-only SQLite connection.
    Uses URI read-only mode to prevent unintended database writes.
    """
    if db_path is None:
        db_path = get_default_db_path()
        
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database file not found at: {db_path}")

    # Standardize Windows backslashes for URI syntax
    clean_path = os.path.abspath(db_path).replace("\\", "/")
    uri_str = f"file:///{clean_path}?mode=ro"
    
    try:
        conn = sqlite3.connect(uri_str, uri=True, check_same_thread=False)
    except sqlite3.OperationalError:
        # Fallback if URI mode fails on specific Windows configurations
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
    date_columns = ["opened_date", "txn_date", "snapshot_month", "last_active_date"]
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    # Enforce numeric types on financial columns
    monetary_cols = ["current_balance", "amount", "min_balance_req", "monthly_income", "annual_income"]
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
