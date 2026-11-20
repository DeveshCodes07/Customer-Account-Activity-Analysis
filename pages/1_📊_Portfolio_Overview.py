"""
FinEdge Digital Solutions — Customer Account Activity Analysis (CAAA)
Page 1: Portfolio Overview & HNW Pareto Concentration (OQ-01)
File: pages/1_📊_Portfolio_Overview.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from src.data_loader import load_analytical_view
from src.data_cleaner import clean_account_data
from src.analytics import compute_hnw_cutoff
from src.ui import render_tailwind_header, render_kpi_row_4, render_insight_box

st.set_page_config(page_title="Portfolio Overview — FinEdge CAAA", page_icon="📊", layout="wide")

# Load and clean
raw_df = load_analytical_view()
df_master, _ = clean_account_data(raw_df)

# Read shared filters from st.session_state
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
    title="1. Portfolio Overview & HNW Asset Concentration",
    subtitle="Operational Question 1: How are balances distributed across accounts, and what proportion is concentrated in the top 5% HNW tier?",
    badge_text="OQ-01 Analysis",
    category="Balance Concentration"
)

st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

if df.empty:
    render_insight_box("No Records Found", "Filters produced zero matching accounts. Adjust sidebar filters.", "warning")
    st.stop()

# Deduplicate to account-level
acct_df = df.drop_duplicates(subset=["account_number"]).copy()
total_accounts = len(acct_df)
total_deposits = acct_df["current_balance"].sum()
avg_balance = acct_df["current_balance"].mean() if total_accounts > 0 else 0

# HNW Analytics
cutoff_balance, hnw_df, hnw_share_pct = compute_hnw_cutoff(acct_df, quantile=0.95)
hnw_count = len(hnw_df)

kpi_row = [
    {
        "title": "Total Accounts",
        "value": f"{total_accounts:,}",
        "delta": f"{filter_region} Portfolio",
        "is_positive": True,
        "icon": "📂",
        "subtext": "Unique registered accounts"
    },
    {
        "title": "Total Portfolio Deposits",
        "value": f"₹{total_deposits/1e7:.2f} Cr" if total_deposits >= 1e7 else f"₹{total_deposits/1e5:.2f} L",
        "delta": f"Avg ₹{avg_balance:,.0f}",
        "is_positive": True,
        "icon": "🏦",
        "subtext": "Ledger cleared balance"
    },
    {
        "title": "Top 5% HNW Cutoff",
        "value": f"₹{cutoff_balance:,.0f}",
        "delta": f"95th Percentile",
        "is_positive": True,
        "icon": "💎",
        "subtext": "Minimum balance for HNW tier"
    },
    {
        "title": "HNW Deposit Share",
        "value": f"{hnw_share_pct:.1f}%",
        "delta": f"{hnw_count} HNW Accounts",
        "is_positive": hnw_share_pct >= 25.0,
        "icon": "👑",
        "subtext": "Proportion of total deposits"
    }
]
render_kpi_row_4(kpi_row)

st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

# Visualizations Row 1
col_left, col_right = st.columns([1, 1])

with col_left:
    st.markdown("#### Deposit Share by Account Type")
    acct_type_summary = acct_df.groupby("account_type")["current_balance"].sum().reset_index()
    fig_donut = px.pie(
        acct_type_summary,
        names="account_type",
        values="current_balance",
        hole=0.55,
        color="account_type",
        color_discrete_map={
            "Savings": "#1B365D",
            "Current": "#2980B9",
            "Salary": "#10B981"
        }
    )
    fig_donut.update_traces(textposition='inside', textinfo='percent+label')
    fig_donut.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=320)
    st.plotly_chart(fig_donut, use_container_width=True)

with col_right:
    st.markdown("#### HNW Cumulative Concentration Curve (Pareto)")
    sorted_balances = acct_df["current_balance"].sort_values(ascending=False).values
    cum_balances = np.cumsum(sorted_balances)
    cum_pct = (cum_balances / cum_balances[-1]) * 100 if len(cum_balances) > 0 else []
    account_pct = (np.arange(1, len(sorted_balances) + 1) / len(sorted_balances)) * 100 if len(sorted_balances) > 0 else []

    fig_pareto = go.Figure()
    fig_pareto.add_trace(go.Scatter(
        x=account_pct,
        y=cum_pct,
        mode="lines",
        name="Cumulative Deposits %",
        line=dict(color="#1B365D", width=3)
    ))
    # Benchmark 45-degree parity line
    fig_pareto.add_trace(go.Scatter(
        x=[0, 100],
        y=[0, 100],
        mode="lines",
        name="Equal Distribution Parity",
        line=dict(color="#94A3B8", dash="dash")
    ))
    fig_pareto.add_vline(x=5, line_width=1.5, line_dash="dot", line_color="#E11D48", annotation_text="Top 5% HNW")
    fig_pareto.update_layout(
        xaxis_title="% of Total Accounts (Sorted Highest to Lowest)",
        yaxis_title="Cumulative % of Total Deposits",
        margin=dict(t=20, b=20, l=20, r=20),
        height=320,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_pareto, use_container_width=True)

st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

# Executive Insights
render_insight_box(
    title=f"Strategic Finding for OQ-01: Top 5% HNW Accounts hold {hnw_share_pct:.1f}% of Portfolio Deposits",
    message=f"The top 5% quantile cutoff is established at ₹{cutoff_balance:,.0f}. Exactly {hnw_count} accounts represent ₹{hnw_df['current_balance'].sum():,.0f} in capital. Relationship Managers (SH-03) must apply dedicated retention workflows to these accounts, as attrition in this tier severely impacts liquidity.",
    level="info"
)

# Detailed HNW Drilldown Table
with st.expander(f"💎 View Identified High Net Worth (HNW) Accounts ({hnw_count} records)"):
    display_cols = ["account_number", "customer_name", "account_type", "region", "current_balance", "days_inactive", "inactivity_tier"]
    avail_cols = [c for c in display_cols if c in hnw_df.columns]
    st.dataframe(hnw_df[avail_cols].sort_values("current_balance", ascending=False), use_container_width=True)
