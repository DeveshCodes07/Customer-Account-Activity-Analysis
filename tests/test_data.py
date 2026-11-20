"""
FinEdge Digital Solutions — Customer Account Activity Analysis (CAAA)
Quality Assurance Test Suite: Data Layer & Relational Integrity
File: tests/test_data.py
"""

import os
import sqlite3
import pytest
import pandas as pd

@pytest.fixture(scope="module")
def db_conn():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "data", "app.db")
    assert os.path.exists(db_path), f"Database not found at {db_path}"
    con = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    yield con
    con.close()

# ---------------------------------------------------------------------
# TC-T-01: SQLite Database Connectivity
# ---------------------------------------------------------------------
def test_db_connection(db_conn):
    """TC-T-01: Verify connection to data/app.db in read-only mode."""
    cur = db_conn.cursor()
    cur.execute("SELECT 1;")
    res = cur.fetchone()[0]
    assert res == 1

# ---------------------------------------------------------------------
# TC-T-02: Table Existence & Row Counts
# ---------------------------------------------------------------------
def test_table_row_counts(db_conn):
    """TC-T-02: Verify master and fact tables satisfy volume planning thresholds."""
    cur = db_conn.cursor()
    tables_min = {
        "dim_customers": 50,
        "dim_accounts": 75,
        "dim_channels": 5,
        "fact_transactions": 150,
        "fact_monthly_snapshots": 150
    }
    for tbl, min_rows in tables_min.items():
        cur.execute(f"SELECT COUNT(*) FROM {tbl};")
        count = cur.fetchone()[0]
        assert count >= min_rows, f"Table {tbl} has {count} rows, expected >= {min_rows}"

# ---------------------------------------------------------------------
# TC-T-03: Primary Key Uniqueness
# ---------------------------------------------------------------------
def test_primary_key_uniqueness(db_conn):
    """TC-T-03: Verify primary keys are unique and non-null across all entities."""
    cur = db_conn.cursor()
    pk_checks = [
        ("dim_customers", "customer_id"),
        ("dim_accounts", "account_id"),
        ("dim_channels", "channel_id"),
        ("fact_transactions", "transaction_id"),
        ("fact_monthly_snapshots", "snapshot_id")
    ]
    for tbl, pk_col in pk_checks:
        cur.execute(f"SELECT COUNT(*), COUNT(DISTINCT {pk_col}), SUM(CASE WHEN {pk_col} IS NULL THEN 1 ELSE 0 END) FROM {tbl};")
        total, distinct_cnt, null_cnt = cur.fetchone()
        assert total == distinct_cnt, f"Duplicate PKs detected in {tbl}.{pk_col}"
        assert null_cnt == 0, f"Null PKs detected in {tbl}.{pk_col}"

# ---------------------------------------------------------------------
# TC-T-04: Referential Integrity (Foreign Keys)
# ---------------------------------------------------------------------
def test_foreign_key_integrity(db_conn):
    """TC-T-04: Verify zero orphaned foreign keys using SQLite PRAGMA check."""
    cur = db_conn.cursor()
    cur.execute("PRAGMA foreign_key_check;")
    errors = cur.fetchall()
    assert len(errors) == 0, f"Foreign key constraint violations found: {errors}"

# ---------------------------------------------------------------------
# TC-T-05: Non-Negative Financial Balance Check
# ---------------------------------------------------------------------
def test_non_negative_balances(db_conn):
    """TC-T-05: Ensure cleared balances and transaction amounts are strictly valid."""
    cur = db_conn.cursor()
    cur.execute("SELECT COUNT(*) FROM dim_accounts WHERE current_balance < 0;")
    negative_accts = cur.fetchone()[0]
    assert negative_accts == 0, f"Found {negative_accts} accounts with negative balances"
    
    cur.execute("SELECT COUNT(*) FROM fact_transactions WHERE amount <= 0;")
    invalid_txns = cur.fetchone()[0]
    assert invalid_txns == 0, f"Found {invalid_txns} transactions with non-positive amounts"

# ---------------------------------------------------------------------
# TC-T-06: Unified Analytical View Verification
# ---------------------------------------------------------------------
def test_analytical_view(db_conn):
    """TC-T-06: Verify vw_customer_account_activity_analysis returns valid columns and records."""
    df = pd.read_sql_query("SELECT * FROM vw_customer_account_activity_analysis LIMIT 10;", db_conn)
    assert len(df) == 10
    # Must have 42 columns as specified in Step 8
    assert len(df.columns) == 42, f"View has {len(df.columns)} columns, expected 42"
    expected_cols = ["transaction_id", "account_number", "customer_name", "channel_name", "current_balance", "is_hnw"]
    for col in expected_cols:
        assert col in df.columns, f"Expected column {col} missing in analytical view"
