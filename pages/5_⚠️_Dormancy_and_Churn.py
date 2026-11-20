"""
FinEdge Digital Solutions — Customer Account Activity Analysis (CAAA)
Page 5: Inactivity Migration & Attrition Early Warning System (OQ-02, OQ-03)
File: pages/5_⚠️_Dormancy_and_Churn.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from src.data_loader import load_analytical_view
from src.data_cleaner import clean_account_data
from src.analytics import compute_inactivity_distribution, calculate_velocity_drop_churn
from src.ui import render_tailwind_header, render_kpi_row_4, render_insight_box, render_alert_banner

st.set_page_config(page_title="Dormancy & Churn — FinEdge CAAA", page_icon="⚠️", layout="wide")

raw_df = load_analytical_view()
df_master, _ = clean_account_data(raw_df)

filter_region = st.session_state.get("filter_region", "All")
filter_acct_type = st.session_state.get("filter_acct_type", "All")
filter_tier = st.session_state.get("filter_tier", "All")

df = df_master.copy()
if filter_region != "All":
    df = df[df["region"] == filter_region]
if filter_acct_type != "All":
    df = df[df["account_type"] == filter_acct_type]
if filter_tier != "All":
    df = df[df["inactivity_tier"] == filter_tier]

render_tailwind_header(
    title="5. Inactivity Migration & Early Churn Warning System",
    subtitle="Operational Questions 2 & 3: How many accounts are dormant, and which active accounts exhibit ≥50% velocity contraction?",
    badge_text="OQ-02 & OQ-03",
    category="Risk Mitigation"
)

st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

if df.empty:
    render_insight_box("No Records Found", "No accounts match current filter parameters.", "warning")
    st.stop()

acct_df = df.drop_duplicates(subset=["account_number"]).copy()
total_accts = len(acct_df)

# Inactivity Tier Aggregation
inactivity_summary = compute_inactivity_distribution(acct_df)
dormant_row = inactivity_summary[inactivity_summary["inactivity_tier"] == "Dormant (90+d)"]
dormant_cnt = int(dormant_row["account_count"].iloc[0]) if not dormant_row.empty else 0
dormant_balance = float(dormant_row["total_balance"].iloc[0]) if not dormant_row.empty else 0.0

inactive_row = inactivity_summary[inactivity_summary["inactivity_tier"] == "Inactive (61-89d)"]
inactive_cnt = int(inactive_row["account_count"].iloc[0]) if not inactive_row.empty else 0

# Velocity Drop Churn Modeling
churn_df = calculate_velocity_drop_churn(acct_df, drop_threshold=0.50)
churn_risk_accounts = churn_df[churn_df["is_churn_risk"]]
churn_cnt = len(churn_risk_accounts)
churn_rate = (churn_cnt / total_accts * 100) if total_accts > 0 else 0.0

kpi_row = [
    {
        "title": "Inactive Accounts",
        "value": f"{inactive_cnt:,}",
        "delta": "61-89 Days Inactive",
        "is_positive": inactive_cnt == 0,
        "icon": "⏳",
        "subtext": "Pre-dormancy intervention tier"
    },
    {
        "title": "Dormant Accounts",
        "value": f"{dormant_cnt:,}",
        "delta": "90+ Days Inactive",
        "is_positive": dormant_cnt == 0,
        "icon": "🛑",
        "subtext": "Regulatory dormancy threshold"
    },
    {
        "title": "Locked Dormant Balances",
        "value": f"₹{dormant_balance/1e5:.2f} L" if dormant_balance >= 1e5 else f"₹{dormant_balance:,.0f}",
        "delta": "Unproductive Capital",
        "is_positive": False,
        "icon": "🔒",
        "subtext": "Capital trapped in dormant accounts"
    },
    {
        "title": "Velocity Drop Churn Alert",
        "value": f"{churn_cnt:,}",
        "delta": f"{churn_rate:.1f}% Attrition Risk",
        "is_positive": churn_rate < 15.0,
        "icon": "🚨",
        "subtext": "≥50% transaction contraction"
    }
]
render_kpi_row_4(kpi_row)

st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

if churn_cnt > 0:
    render_alert_banner(
        alert_title=f"CUSTOMER RETENTION ALERT: {churn_cnt} Accounts Flagged for Imminent Churn Risk",
        alert_message=f"Retention Lead Neha Gupta (SH-04) must dispatch re-engagement nudges immediately. These accounts have suffered a ≥50% velocity drop or entered late-stage inactivity."
    )
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

# Visualizations Row
col1, col2 = st.columns([1, 1.2])

with col1:
    st.markdown("#### 4-Tier Inactivity Distribution")
    fig_funnel = px.bar(
        inactivity_summary,
        x="inactivity_tier",
        y="account_count",
        color="inactivity_tier",
        color_discrete_map={
            "Active (0-30d)": "#10B981",
            "At-Risk (31-60d)": "#F59E0B",
            "Inactive (61-89d)": "#F97316",
            "Dormant (90+d)": "#EF4444"
        },
        labels={"inactivity_tier": "Inactivity Tier", "account_count": "Accounts"}
    )
    fig_funnel.update_layout(margin=dict(t=15, b=15, l=15, r=15), height=320, showlegend=False)
    st.plotly_chart(fig_funnel, use_container_width=True)

with col2:
    st.markdown("#### Days Inactive vs Account Balance")
    fig_scatter = px.scatter(
        acct_df,
        x="days_inactive",
        y="current_balance",
        color="inactivity_tier",
        hover_data=["customer_name", "account_type", "region"],
        color_discrete_map={
            "Active (0-30d)": "#10B981",
            "At-Risk (31-60d)": "#F59E0B",
            "Inactive (61-89d)": "#F97316",
            "Dormant (90+d)": "#EF4444"
        },
        labels={"days_inactive": "Days Inactive", "current_balance": "Current Balance (INR)"}
    )
    fig_scatter.add_vline(x=90, line_dash="dash", line_color="#EF4444", annotation_text="Dormancy (90d)")
    fig_scatter.update_layout(margin=dict(t=15, b=15, l=15, r=15), height=320)
    st.plotly_chart(fig_scatter, use_container_width=True)

# Churn Risk Action List Table
st.markdown("#### 📋 Prioritized High-Risk Attrition Intervention Grid")
display_cols = ["account_number", "customer_name", "account_type", "region", "current_balance", "days_inactive", "velocity_drop_display"]
avail_cols = [c for c in display_cols if c in churn_risk_accounts.columns]
st.dataframe(churn_risk_accounts[avail_cols].sort_values("days_inactive", ascending=False), use_container_width=True)
