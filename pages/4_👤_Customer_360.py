"""
FinEdge Digital Solutions — Customer Account Activity Analysis (CAAA)
Page 4: Customer 360 & Minimum Average Balance (MAB) Deficit Tracker (OQ-05)
File: pages/4_👤_Customer_360.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from src.data_loader import load_analytical_view
from src.data_cleaner import clean_account_data
from src.analytics import compute_mab_compliance_and_deficit
from src.ui import render_tailwind_header, render_kpi_row_4, render_insight_box

st.set_page_config(page_title="Customer 360 & MAB — FinEdge CAAA", page_icon="👤", layout="wide")

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
    title="4. Customer 360 & MAB Deficit Simulator",
    subtitle="Operational Question 5: What proportion of accounts violate MAB rules, and what is the projected fee revenue?",
    badge_text="OQ-05 Analysis",
    category="Regulatory & Revenue"
)

st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

if df.empty:
    render_insight_box("No Records Found", "No accounts match current filter parameters.", "warning")
    st.stop()

# Interactive Penalty Fee Simulation Slider
st.markdown("### 🎛️ Dynamic Non-Compliance Penalty Fee Simulator")
col_slider, col_info = st.columns([2, 1])
with col_slider:
    simulated_fee = st.slider(
        "Simulated Monthly Penalty Fee per Violation (INR)",
        min_value=100,
        max_value=1000,
        value=250,
        step=50,
        help="Adjust the regulatory non-maintenance penalty fee to evaluate projected fee recovery."
    )
with col_info:
    st.info(f"Simulating penalty recovery at **₹{simulated_fee} / month** across all non-compliant accounts.")

# Compute MAB Metrics
mab_results = compute_mab_compliance_and_deficit(df, fee_per_violation=float(simulated_fee))

total_accts = mab_results["total_accounts"]
compliant_cnt = mab_results["compliant_count"]
non_compliant_cnt = mab_results["non_compliant_count"]
comp_rate = mab_results["compliance_rate_pct"]
total_deficit = mab_results["total_deficit"]
projected_revenue = mab_results["simulated_fee_revenue"]

kpi_row = [
    {
        "title": "Portfolio Compliance",
        "value": f"{comp_rate:.1f}%",
        "delta": f"{compliant_cnt} Compliant",
        "is_positive": comp_rate >= 75.0,
        "icon": "🛡️",
        "subtext": "Balance ≥ Minimum Requirement"
    },
    {
        "title": "Non-Compliant Accounts",
        "value": f"{non_compliant_cnt:,}",
        "delta": f"{100-comp_rate:.1f}% Deficit",
        "is_positive": non_compliant_cnt == 0,
        "icon": "⚠️",
        "subtext": "Accounts violating MAB"
    },
    {
        "title": "Total Deposit Deficit",
        "value": f"₹{total_deficit/1e5:.2f} L" if total_deficit >= 1e5 else f"₹{total_deficit:,.0f}",
        "delta": "Shortfall to MAB",
        "is_positive": False,
        "icon": "📉",
        "subtext": "Sum of (Req - Balance)"
    },
    {
        "title": "Simulated Penalty Revenue",
        "value": f"₹{projected_revenue/1e5:.2f} L" if projected_revenue >= 1e5 else f"₹{projected_revenue:,.0f}",
        "delta": f"@ ₹{simulated_fee}/mo",
        "is_positive": True,
        "icon": "💵",
        "subtext": "Monthly recovery potential"
    }
]
render_kpi_row_4(kpi_row)

st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

# Visualizations Row
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("#### Compliance Rate by Account Type")
    acct_df = df.drop_duplicates(subset=["account_number"]).copy()
    acct_df["is_comp_bool"] = acct_df["current_balance"] >= acct_df["min_balance_req"]
    type_comp = acct_df.groupby(["account_type", "is_comp_bool"], observed=False).size().reset_index(name="count")
    type_comp["Status"] = type_comp["is_comp_bool"].map({True: "Compliant", False: "Non-Compliant"})
    
    fig_comp = px.bar(
        type_comp,
        x="account_type",
        y="count",
        color="Status",
        barmode="stack",
        color_discrete_map={"Compliant": "#10B981", "Non-Compliant": "#EF4444"}
    )
    fig_comp.update_layout(margin=dict(t=15, b=15, l=15, r=15), height=300)
    st.plotly_chart(fig_comp, use_container_width=True)

with col2:
    st.markdown("#### Deposit Shortfall (Deficit) Distribution")
    non_comp_df = mab_results["non_compliant_df"]
    if not non_comp_df.empty:
        fig_hist = px.histogram(
            non_comp_df,
            x="mab_deficit",
            nbins=15,
            color_discrete_sequence=["#F43F5E"],
            labels={"mab_deficit": "Deficit Amount (INR)"}
        )
        fig_hist.update_layout(margin=dict(t=15, b=15, l=15, r=15), height=300)
        st.plotly_chart(fig_hist, use_container_width=True)
    else:
        st.success("All accounts in this segment are 100% MAB compliant!")

# Customer 360 Individual Drilldown
st.markdown("### 🔍 Customer 360 Individual Profile Drilldown")
customer_names = sorted(df["customer_name"].dropna().unique())
selected_customer = st.selectbox("Select Customer to Inspect Profile & History", customer_names)

if selected_customer:
    cust_records = df[df["customer_name"] == selected_customer]
    first_row = cust_records.iloc[0]
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Account Number", str(first_row.get("account_number", "N/A")))
    c2.metric("Account Type", str(first_row.get("account_type", "N/A")))
    c3.metric("Current Balance", f"₹{first_row.get('current_balance', 0):,.2f}")
    c4.metric("Inactivity Status", str(first_row.get("inactivity_tier", "N/A")))
    
    st.markdown("##### Recent Account Transactions")
    show_cols = ["transaction_id", "txn_date", "txn_type", "amount", "channel_name", "status"]
    avail = [c for c in show_cols if c in cust_records.columns]
    st.dataframe(cust_records[avail].sort_values("txn_date", ascending=False), use_container_width=True)
