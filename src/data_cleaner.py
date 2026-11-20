"""
FinEdge Digital Solutions — Customer Account Activity Analysis (CAAA)
Data Cleaning & Preprocessing Pipeline
File: src/data_cleaner.py
"""

import pandas as pd
import numpy as np

def clean_account_data(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """
    Clean and preprocess banking activity dataset:
    - Handle missing annual_income and occupation.
    - Remove duplicate transactions by transaction_id.
    - Enforce non-negative monetary boundaries (balance >= 0, amount > 0).
    - Map canonical aliases for region, status, dates, and minimum balance.
    - Returns cleaned DataFrame and cleaning audit summary metrics.
    """
    if df is None or df.empty:
        return df, {
            "total_rows_raw": 0,
            "duplicates_removed": 0,
            "income_nulls_imputed": 0,
            "occupation_nulls_filled": 0,
            "negative_balances_clipped": 0,
            "clean_rows_count": 0,
            "is_healthy": False
        }

    clean_df = df.copy()
    total_rows_raw = len(clean_df)

    # 1. Deduplication by transaction_id if present
    duplicates_removed = 0
    if "transaction_id" in clean_df.columns:
        initial_count = len(clean_df)
        clean_df = clean_df.drop_duplicates(subset=["transaction_id"], keep="first")
        duplicates_removed = initial_count - len(clean_df)

    # 2. Imputation: Occupation
    occupation_nulls_filled = 0
    if "occupation" in clean_df.columns:
        occupation_nulls_filled = int(clean_df["occupation"].isna().sum())
        clean_df["occupation"] = clean_df["occupation"].fillna("Unknown")

    # 3. Imputation: Annual Income (Median by Occupation)
    income_nulls_imputed = 0
    if "annual_income" in clean_df.columns:
        income_nulls_imputed = int(clean_df["annual_income"].isna().sum())
        if income_nulls_imputed > 0:
            occupation_medians = clean_df.groupby("occupation")["annual_income"].transform("median")
            overall_median = clean_df["annual_income"].median()
            if pd.isna(overall_median) or overall_median <= 0:
                overall_median = 600000.0

            clean_df["annual_income"] = clean_df["annual_income"].fillna(occupation_medians).fillna(overall_median)

    # 4. Boundary Enforcement: Balances & Amounts
    negative_balances_clipped = 0
    if "current_balance" in clean_df.columns:
        neg_mask = clean_df["current_balance"] < 0
        negative_balances_clipped = int(neg_mask.sum())
        if negative_balances_clipped > 0:
            clean_df.loc[neg_mask, "current_balance"] = 0.0

    if "amount" in clean_df.columns:
        clean_df["amount"] = clean_df["amount"].apply(lambda x: abs(x) if pd.notna(x) else 0.0)

    # Format numeric columns to 2 decimal places
    for col in ["current_balance", "annual_income", "amount", "minimum_balance_req"]:
        if col in clean_df.columns:
            clean_df[col] = clean_df[col].round(2)

    # 5. Canonical Aliases & Compatibility Mapping
    if "branch_tier" in clean_df.columns and "region" not in clean_df.columns:
        clean_df["region"] = clean_df["branch_tier"]

    if "transaction_status" in clean_df.columns and "status" not in clean_df.columns:
        clean_df["status"] = clean_df["transaction_status"]

    if "transaction_type" in clean_df.columns and "txn_type" not in clean_df.columns:
        clean_df["txn_type"] = clean_df["transaction_type"]

    if "transaction_date" in clean_df.columns and "txn_date" not in clean_df.columns:
        clean_df["txn_date"] = pd.to_datetime(clean_df["transaction_date"], errors="coerce")

    if "minimum_balance_req" in clean_df.columns and "min_balance_req" not in clean_df.columns:
        clean_df["min_balance_req"] = clean_df["minimum_balance_req"]

    if "customer_tenure_months" in clean_df.columns and "account_tenure_months" not in clean_df.columns:
        clean_df["account_tenure_months"] = clean_df["customer_tenure_months"]

    # Inactivity tier verification
    if "inactivity_tier" not in clean_df.columns and "days_inactive" in clean_df.columns:
        def get_inactivity_tier(days):
            if days <= 30:
                return "Active (0-30d)"
            elif days <= 60:
                return "At-Risk (31-60d)"
            elif days <= 89:
                return "Inactive (61-89d)"
            else:
                return "Dormant (90+d)"
        clean_df["inactivity_tier"] = clean_df["days_inactive"].apply(get_inactivity_tier)

    cleaning_summary = {
        "total_rows_raw": total_rows_raw,
        "duplicates_removed": duplicates_removed,
        "income_nulls_imputed": income_nulls_imputed,
        "occupation_nulls_filled": occupation_nulls_filled,
        "negative_balances_clipped": negative_balances_clipped,
        "clean_rows_count": len(clean_df),
        "is_healthy": (len(clean_df) > 0 and clean_df["current_balance"].min() >= 0.0)
    }

    return clean_df, cleaning_summary
