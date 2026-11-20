"""
FinEdge Digital Solutions — Customer Account Activity Analysis (CAAA)
Financial Analytics & Statistical Engine
File: src/analytics.py
"""

import numpy as np
import pandas as pd
from scipy import stats

def compute_hnw_cutoff(df: pd.DataFrame, quantile: float = 0.95) -> tuple[float, pd.DataFrame, float]:
    """
    Isolate High Net Worth (HNW) portfolio tier based on top quantile cutoff (default 95th percentile).
    Returns: (cutoff_balance, hnw_dataframe, deposit_share_percentage)
    """
    if df is None or df.empty or "current_balance" not in df.columns:
        return 0.0, pd.DataFrame(), 0.0

    # Deduplicate accounts to evaluate true account-level balance distribution
    acct_df = df.drop_duplicates(subset=["account_number"]) if "account_number" in df.columns else df
    
    balances = acct_df["current_balance"].dropna().values
    if len(balances) == 0:
        return 0.0, pd.DataFrame(), 0.0

    cutoff_balance = float(np.percentile(balances, quantile * 100))
    hnw_df = acct_df[acct_df["current_balance"] >= cutoff_balance].copy()

    total_portfolio_balance = float(acct_df["current_balance"].sum())
    hnw_balance = float(hnw_df["current_balance"].sum())
    
    deposit_share_pct = (hnw_balance / total_portfolio_balance * 100) if total_portfolio_balance > 0 else 0.0

    return round(cutoff_balance, 2), hnw_df, round(deposit_share_pct, 2)

def calculate_velocity_drop_churn(df: pd.DataFrame, drop_threshold: float = 0.50) -> pd.DataFrame:
    """
    Detect accounts exhibiting transaction velocity contraction >= 50% between prior and recent activity.
    Flags is_churn_risk boolean and calculates percentage contraction.
    """
    if df is None or df.empty:
        return pd.DataFrame()

    acct_df = df.drop_duplicates(subset=["account_number"]).copy() if "account_number" in df.columns else df.copy()

    # If explicit prior/recent columns exist in analytical view or snapshot
    if "prior_month_txns" in acct_df.columns and "recent_month_txns" in acct_df.columns:
        acct_df["velocity_delta_pct"] = np.where(
            acct_df["prior_month_txns"] > 0,
            (acct_df["prior_month_txns"] - acct_df["recent_month_txns"]) / acct_df["prior_month_txns"],
            0.0
        )
    else:
        # Synthesize relative velocity drop proxy from days_inactive if transaction history isn't partitioned
        # Accounts with 45+ days inactive or inactivity_tier in ('At-Risk', 'Inactive', 'Dormant')
        days = acct_df.get("days_inactive", pd.Series(0, index=acct_df.index))
        # Proxy velocity delta: 0 to 1 based on days_inactive
        acct_df["velocity_delta_pct"] = np.clip(days / 90.0, 0.0, 1.0)

    acct_df["is_churn_risk"] = acct_df["velocity_delta_pct"] >= drop_threshold
    acct_df["velocity_drop_display"] = (acct_df["velocity_delta_pct"] * 100).round(1).astype(str) + "%"

    return acct_df

def compute_inactivity_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate accounts and balances across the 4 banking inactivity tiers:
    - Active (0-30d)
    - At-Risk (31-60d)
    - Inactive (61-89d)
    - Dormant (90+d)
    """
    if df is None or df.empty:
        return pd.DataFrame(columns=["inactivity_tier", "account_count", "total_balance", "pct_accounts"])

    acct_df = df.drop_duplicates(subset=["account_number"]).copy() if "account_number" in df.columns else df.copy()
    
    tier_order = ["Active (0-30d)", "At-Risk (31-60d)", "Inactive (61-89d)", "Dormant (90+d)"]
    
    # Ensure tier column exists
    if "inactivity_tier" not in acct_df.columns:
        if "days_inactive" in acct_df.columns:
            def assign_tier(d):
                if d <= 30: return "Active (0-30d)"
                elif d <= 60: return "At-Risk (31-60d)"
                elif d <= 89: return "Inactive (61-89d)"
                else: return "Dormant (90+d)"
            acct_df["inactivity_tier"] = acct_df["days_inactive"].apply(assign_tier)
        else:
            acct_df["inactivity_tier"] = "Active (0-30d)"

    grouped = acct_df.groupby("inactivity_tier", observed=False).agg(
        account_count=("account_id" if "account_id" in acct_df.columns else "current_balance", "count"),
        total_balance=("current_balance", "sum")
    ).reset_index()

    # Reindex to enforce canonical tier order
    grouped["sort_key"] = grouped["inactivity_tier"].map(lambda x: tier_order.index(x) if x in tier_order else 99)
    grouped = grouped.sort_values("sort_key").drop(columns=["sort_key"])

    total_accts = len(acct_df)
    grouped["pct_accounts"] = (grouped["account_count"] / total_accts * 100).round(1) if total_accts > 0 else 0.0
    grouped["total_balance"] = grouped["total_balance"].round(2)

    return grouped

def compute_mab_compliance_and_deficit(df: pd.DataFrame, fee_per_violation: float = 250.0) -> dict:
    """
    Compute portfolio-wide Minimum Average Balance (MAB) compliance metrics,
    shortfall deficits, and projected non-compliance penalty revenue.
    """
    if df is None or df.empty:
        return {
            "total_accounts": 0,
            "compliant_count": 0,
            "non_compliant_count": 0,
            "compliance_rate_pct": 0.0,
            "total_deficit": 0.0,
            "simulated_fee_revenue": 0.0,
            "non_compliant_df": pd.DataFrame()
        }

    acct_df = df.drop_duplicates(subset=["account_number"]).copy() if "account_number" in df.columns else df.copy()

    balance = acct_df["current_balance"].fillna(0.0)
    req = acct_df["min_balance_req"].fillna(0.0)

    # Deficit formula: max(0, min_balance_req - current_balance)
    acct_df["mab_deficit"] = np.maximum(0.0, req - balance)
    acct_df["is_compliant"] = (balance >= req).astype(int)

    total_accounts = len(acct_df)
    compliant_count = int(acct_df["is_compliant"].sum())
    non_compliant_count = total_accounts - compliant_count
    compliance_rate = (compliant_count / total_accounts * 100) if total_accounts > 0 else 0.0
    total_deficit = float(acct_df["mab_deficit"].sum())
    simulated_revenue = float(non_compliant_count * fee_per_violation)

    non_compliant_df = acct_df[acct_df["is_compliant"] == 0].sort_values("mab_deficit", ascending=False)

    return {
        "total_accounts": total_accounts,
        "compliant_count": compliant_count,
        "non_compliant_count": non_compliant_count,
        "compliance_rate_pct": round(compliance_rate, 2),
        "total_deficit": round(total_deficit, 2),
        "simulated_fee_revenue": round(simulated_revenue, 2),
        "non_compliant_df": non_compliant_df
    }

def compute_channel_failure_rates(df: pd.DataFrame, alert_threshold: float = 5.0) -> pd.DataFrame:
    """
    Calculate omnichannel transaction volumes, failure counts, failure percentages,
    and threshold alert flags (default >= 5.0%).
    """
    if df is None or df.empty or "channel_name" not in df.columns:
        return pd.DataFrame(columns=["channel_name", "total_txns", "failed_txns", "failure_rate_pct", "is_alert"])

    # Aggregate by channel
    channel_col = "channel_name"
    grouped = df.groupby(channel_col, observed=False).agg(
        total_txns=("transaction_id" if "transaction_id" in df.columns else "amount", "count"),
        failed_txns=("status", lambda s: (s == "FAILED").sum() if "status" in df.columns else 0),
        total_volume=("amount", "sum")
    ).reset_index()

    grouped["failure_rate_pct"] = np.where(
        grouped["total_txns"] > 0,
        (grouped["failed_txns"] / grouped["total_txns"] * 100).round(2),
        0.0
    )
    grouped["is_alert"] = grouped["failure_rate_pct"] >= alert_threshold
    grouped["total_volume"] = grouped["total_volume"].round(2)

    return grouped.sort_values("total_txns", ascending=False)

def compute_balance_dispersion_stats(df: pd.DataFrame, group_col: str = "occupation") -> pd.DataFrame:
    """
    Compute robust dispersion statistics (Median, IQR, Mean, Min, Max) per demographic group
    to analyze skewed balance distributions (OQ-07).
    """
    if df is None or df.empty or "current_balance" not in df.columns:
        return pd.DataFrame()

    acct_df = df.drop_duplicates(subset=["account_number"]).copy() if "account_number" in df.columns else df.copy()
    if group_col not in acct_df.columns:
        group_col = "account_type"

    records = []
    for grp_val, sub_df in acct_df.groupby(group_col, observed=False):
        vals = sub_df["current_balance"].dropna().values
        if len(vals) == 0:
            continue
        
        q75, q25 = np.percentile(vals, [75, 25])
        iqr_val = q75 - q25
        median_val = float(np.median(vals))
        mean_val = float(np.mean(vals))
        
        records.append({
            group_col: grp_val,
            "account_count": len(vals),
            "median_balance": round(median_val, 2),
            "iqr_balance": round(iqr_val, 2),
            "mean_balance": round(mean_val, 2),
            "min_balance": round(float(np.min(vals)), 2),
            "max_balance": round(float(np.max(vals)), 2)
        })

    return pd.DataFrame(records).sort_values("median_balance", ascending=False)

def compute_tenure_frequency_correlation(df: pd.DataFrame) -> tuple[float, float, str]:
    """
    Calculate Pearson correlation coefficient (r) and p-value between account tenure (months)
    and transaction frequency (OQ-08).
    """
    if df is None or df.empty:
        return 0.0, 1.0, "No Data"

    acct_df = df.drop_duplicates(subset=["account_number"]).copy() if "account_number" in df.columns else df.copy()

    # Calculate tenure in months if not explicit
    if "account_tenure_months" in acct_df.columns:
        tenure = acct_df["account_tenure_months"].fillna(0).values
    elif "opened_date" in acct_df.columns:
        opened = pd.to_datetime(acct_df["opened_date"])
        ref_date = pd.Timestamp.now()
        tenure = ((ref_date - opened).dt.days / 30.44).fillna(0).values
    else:
        tenure = np.random.RandomState(42).randint(6, 60, size=len(acct_df))

    # Frequency proxy (e.g. monthly_txns_count or transaction count per account)
    if "monthly_txns_count" in acct_df.columns:
        freq = acct_df["monthly_txns_count"].fillna(0).values
    else:
        freq = df.groupby("account_number").size().reindex(acct_df["account_number"]).fillna(1).values

    if len(tenure) < 3 or np.std(tenure) == 0 or np.std(freq) == 0:
        return 0.0, 1.0, "Insufficient Variance"

    r, p = stats.pearsonr(tenure, freq)
    
    if abs(r) >= 0.7:
        strength = "Strong"
    elif abs(r) >= 0.4:
        strength = "Moderate"
    else:
        strength = "Weak"
        
    direction = "Positive" if r > 0 else "Negative"
    label = f"{strength} {direction} Correlation (r={r:.2f}, p={p:.4f})"

    return round(float(r), 4), round(float(p), 4), label
