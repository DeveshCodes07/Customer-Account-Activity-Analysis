"""
FinEdge Digital Solutions — Customer Account Activity Analysis (CAAA)
Quality Assurance Test Suite: Analytical & Statistical Formulations
File: tests/test_analysis.py
"""

import pytest
import numpy as np
import pandas as pd
from scipy import stats

# ---------------------------------------------------------------------
# TC-T-07: Top 5% HNW Quantile Cutoff Formula
# ---------------------------------------------------------------------
def test_hnw_quantile_calculation():
    """TC-T-07: Verify 95th percentile quantile cutoff formula on known balances."""
    # Known dataset of 20 accounts
    balances = np.array([
        1000, 2500, 3000, 4200, 5000, 
        6000, 7500, 8000, 9500, 12000,
        15000, 18000, 22000, 28000, 35000,
        45000, 50000, 75000, 150000, 500000
    ])
    p95 = np.percentile(balances, 95)
    hnw_flags = (balances >= p95).astype(int)
    # 5% of 20 = 1 account (500,000)
    assert p95 > 150000
    assert np.sum(hnw_flags) >= 1

# ---------------------------------------------------------------------
# TC-T-08: Velocity Drop Early Churn Warning Formula
# ---------------------------------------------------------------------
def test_velocity_drop_churn_formula():
    """TC-T-08: Verify relative velocity drop formula flags >= 50% declines."""
    # Test cases: (prior_count, recent_count, expected_flag)
    test_cases = [
        (20, 5, True),    # -75% drop -> Flagged
        (10, 4, True),    # -60% drop -> Flagged
        (10, 5, True),    # -50% drop -> Boundary Flagged
        (10, 6, False),   # -40% drop -> Not flagged
        (15, 15, False),  # 0% change  -> Not flagged
        (5, 12, False),   # +140% surge -> Not flagged
    ]
    for prior, recent, expected_flag in test_cases:
        delta_v = (prior - recent) / prior
        is_churn_alert = bool(delta_v >= 0.50)
        assert is_churn_alert == expected_flag, f"Failed for prior={prior}, recent={recent}"

# ---------------------------------------------------------------------
# TC-T-09: 4-Tier Inactivity Classification Logic
# ---------------------------------------------------------------------
def test_inactivity_tier_classification():
    """TC-T-09: Verify inactivity day buckets correctly assign status tiers."""
    def classify_inactivity(days):
        if days <= 30:
            return "Active", "0-30 Days"
        elif days <= 60:
            return "At-Risk", "31-60 Days"
        elif days < 90:
            return "Inactive", "61-89 Days"
        else:
            return "Dormant", "90+ Days"
            
    assert classify_inactivity(0) == ("Active", "0-30 Days")
    assert classify_inactivity(30) == ("Active", "0-30 Days")
    assert classify_inactivity(31) == ("At-Risk", "31-60 Days")
    assert classify_inactivity(60) == ("At-Risk", "31-60 Days")
    assert classify_inactivity(61) == ("Inactive", "61-89 Days")
    assert classify_inactivity(89) == ("Inactive", "61-89 Days")
    assert classify_inactivity(90) == ("Dormant", "90+ Days")
    assert classify_inactivity(180) == ("Dormant", "90+ Days")

# ---------------------------------------------------------------------
# TC-T-10: Minimum Average Balance (MAB) Deficit Calculation
# ---------------------------------------------------------------------
def test_mab_compliance_and_deficit():
    """TC-T-10: Verify MAB compliance boolean and shortfall calculation."""
    def eval_mab(balance, req):
        is_comp = 1 if balance >= req else 0
        deficit = max(0.0, req - balance)
        return is_comp, deficit

    assert eval_mab(5500.0, 5000.0) == (1, 0.0)
    assert eval_mab(5000.0, 5000.0) == (1, 0.0) # Boundary
    assert eval_mab(3200.0, 5000.0) == (0, 1800.0)
    assert eval_mab(0.0, 10000.0) == (0, 10000.0)
    assert eval_mab(15000.0, 0.0) == (1, 0.0)   # Salary zero-balance

# ---------------------------------------------------------------------
# TC-T-11: Channel Failure Rate Formula
# ---------------------------------------------------------------------
def test_channel_failure_rate_calculation():
    """TC-T-11: Verify channel failure percentage and >5% alert threshold."""
    # 200 transactions: 190 Success, 10 Failed (5.0%)
    total_txns = 200
    failed_txns = 10
    failure_rate_pct = (failed_txns / total_txns) * 100
    assert failure_rate_pct == 5.0
    is_alert = (failure_rate_pct >= 5.0)
    assert is_alert is True

# ---------------------------------------------------------------------
# TC-T-12: Statistical Dispersion & Pearson Correlation Math
# ---------------------------------------------------------------------
def test_statistical_dispersion_and_correlation():
    """TC-T-12: Verify IQR calculation and Pearson correlation coefficient."""
    # Sample known array
    data = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
    q75, q25 = np.percentile(data, [75, 25])
    iqr = q75 - q25
    assert iqr == 45.0
    
    # Perfectly correlated tenure vs transactions
    tenure = np.array([6, 12, 18, 24, 30, 36])
    txns = np.array([10, 15, 20, 25, 30, 35])
    r, p = stats.pearsonr(tenure, txns)
    assert np.isclose(r, 1.0)
    assert p < 0.01
