"""
FinEdge Digital Solutions — Customer Account Activity Analysis (CAAA)
Main Application Entrypoint & Executive Control Tower
File: app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import io

from src.data_loader import load_analytical_view
from src.data_cleaner import clean_account_data
from src.analytics import (
    compute_hnw_cutoff,
    calculate_velocity_drop_churn,
    compute_inactivity_distribution,
    compute_mab_compliance_and_deficit,
    compute_channel_failure_rates
)
from src.ui import render_tailwind_header, render_kpi_row_4, render_insight_box

# -----------------------------------------------------------------------------
# 1. Page Configuration
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="FinEdge CAAA — Customer Account Activity Analysis",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# 2. Global Ingestion & Cleaning
# -----------------------------------------------------------------------------
@st.cache_data(ttl=3600, show_spinner=False)
def get_clean_dataset():
    raw_df = load_analytical_view()
    cleaned_df, summary = clean_account_data(raw_df)
    return cleaned_df, summary

try:
    df_master, clean_meta = get_clean_dataset()
except Exception as e:
    st.error(f"Failed to load banking dataset: {e}")
    st.stop()

# -----------------------------------------------------------------------------
# 3. Shared Global Sidebar Filters (st.session_state)
# -----------------------------------------------------------------------------
st.sidebar.markdown(
    """
    <div style="padding: 10px 0 15px 0;">
        <h2 style="color: #1B365D; margin: 0; font-size: 1.25rem; font-weight: 700;">🏦 FinEdge CAAA</h2>
        <p style="color: #64748B; font-size: 0.8rem; margin: 2px 0 0 0;">Retail Banking Analytics Control</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔍 Global Portfolio Filters")

# Initialize session state defaults if not set
if "filter_region" not in st.session_state:
    st.session_state.filter_region = "All"
if "filter_acct_type" not in st.session_state:
    st.session_state.filter_acct_type = "All"
if "filter_tier" not in st.session_state:
    st.session_state.filter_tier = "All"

regions = ["All"] + sorted([str(x) for x in df_master["region"].dropna().unique() if x])
acct_types = ["All"] + sorted([str(x) for x in df_master["account_type"].dropna().unique() if x])
tiers = ["All", "Active (0-30d)", "At-Risk (31-60d)", "Inactive (61-89d)", "Dormant (90+d)"]

selected_region = st.sidebar.selectbox("Geographic Region", regions, index=regions.index(st.session_state.filter_region))
selected_acct_type = st.sidebar.selectbox("Account Type", acct_types, index=acct_types.index(st.session_state.filter_acct_type))
selected_tier = st.sidebar.selectbox("Inactivity Status Tier", tiers, index=tiers.index(st.session_state.filter_tier))

st.session_state.filter_region = selected_region
st.session_state.filter_acct_type = selected_acct_type
st.session_state.filter_tier = selected_tier

if st.sidebar.button("🔄 Reset All Filters", use_container_width=True):
    st.session_state.filter_region = "All"
    st.session_state.filter_acct_type = "All"
    st.session_state.filter_tier = "All"
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.info(
    "**ABES MCA Capstone Project**\n\n"
    "**Candidate:** Devesh Kumar\n\n"
    "**Roll No:** `2500320140050`\n\n"
    "**Guide:** Prof. Alpna Lodhi\n\n"
    "**Organization:** FinEdge Digital Solutions Pvt. Ltd."
)

# -----------------------------------------------------------------------------
# 4. Filter Application Function
# -----------------------------------------------------------------------------
def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    filtered = df.copy()
    if st.session_state.filter_region != "All":
        filtered = filtered[filtered["region"] == st.session_state.filter_region]
    if st.session_state.filter_acct_type != "All":
        filtered = filtered[filtered["account_type"] == st.session_state.filter_acct_type]
    if st.session_state.filter_tier != "All":
        filtered = filtered[filtered["inactivity_tier"] == st.session_state.filter_tier]
    return filtered

df_filtered = apply_filters(df_master)

# -----------------------------------------------------------------------------
# 5. Home Landing View
# -----------------------------------------------------------------------------
render_tailwind_header(
    title="Customer Account Activity Analysis (CAAA)",
    subtitle="Enterprise Retail Banking Intelligence & Portfolio Risk Monitoring Platform",
    badge_text="ABES MCA Capstone",
    category="Executive Edition"
)

st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

# Contradictory Filter Warning Check
if df_filtered.empty:
    render_insight_box(
        title="No Matching Account Records",
        message="The selected combination of Region, Account Type, and Inactivity Tier yielded zero records. Please reset or broaden your filters.",
        level="warning"
    )
    st.stop()

# Key Portfolio Summary Calculations
unique_accts = df_filtered.drop_duplicates(subset=["account_number"])
total_accts = len(unique_accts)
total_deposits = unique_accts["current_balance"].sum()
avg_balance = unique_accts["current_balance"].mean() if total_accts > 0 else 0
active_accts = (unique_accts["inactivity_tier"] == "Active (0-30d)").sum()
active_pct = (active_accts / total_accts * 100) if total_accts > 0 else 0

churn_df = calculate_velocity_drop_churn(df_filtered)
churn_risk_count = int(churn_df["is_churn_risk"].sum()) if not churn_df.empty else 0
churn_pct = (churn_risk_count / total_accts * 100) if total_accts > 0 else 0

mab_metrics = compute_mab_compliance_and_deficit(df_filtered)
channel_metrics = compute_channel_failure_rates(df_filtered)
overall_fail_rate = (df_filtered["status"] == "FAILED").mean() * 100 if "status" in df_filtered.columns else 0

# Executive Scorecard Row
kpi_data = [
    {
        "title": "Active Portfolio",
        "value": f"{total_accts:,}",
        "delta": f"{active_pct:.1f}% Active",
        "is_positive": active_pct >= 60.0,
        "icon": "👥",
        "subtext": f"{len(df_filtered)} filtered transactions"
    },
    {
        "title": "Total Balances",
        "value": f"₹{total_deposits/1e7:.2f} Cr" if total_deposits >= 1e7 else f"₹{total_deposits/1e5:.2f} L",
        "delta": f"Avg ₹{avg_balance:,.0f}",
        "is_positive": True,
        "icon": "💰",
        "subtext": "Cleared ledger balances"
    },
    {
        "title": "MAB Compliance",
        "value": f"{mab_metrics['compliance_rate_pct']:.1f}%",
        "delta": f"₹{mab_metrics['total_deficit']/1e5:.1f}L Deficit",
        "is_positive": mab_metrics["compliance_rate_pct"] >= 75.0,
        "icon": "⚖️",
        "subtext": f"{mab_metrics['non_compliant_count']} accounts below MAB"
    },
    {
        "title": "Churn Risk Rate",
        "value": f"{churn_pct:.1f}%",
        "delta": f"{churn_risk_count} Attrition Risk",
        "is_positive": churn_pct < 15.0,
        "icon": "🚨",
        "subtext": "≥50% velocity contraction"
    }
]
render_kpi_row_4(kpi_data)

st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 6. Navigation Hub Cards
# -----------------------------------------------------------------------------
st.markdown("### 🧭 Multipage Analytical Modules")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div style="background: white; border: 1px solid #E2E8F0; border-radius: 12px; padding: 18px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
            <h4 style="color: #1B365D; margin: 0 0 6px 0;">📊 1. Portfolio Overview</h4>
            <p style="color: #64748B; font-size: 0.85rem; line-height: 1.4; margin: 0;">
                High-level asset distribution, account types, and top 5% High Net Worth (HNW) Pareto concentration curve (OQ-01).
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="background: white; border: 1px solid #E2E8F0; border-radius: 12px; padding: 18px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
            <h4 style="color: #1B365D; margin: 0 0 6px 0;">👤 4. Customer 360 & MAB</h4>
            <p style="color: #64748B; font-size: 0.85rem; line-height: 1.4; margin: 0;">
                Minimum Average Balance (MAB) shortfall audit, revenue deficit recovery, and dynamic fee simulation (OQ-05).
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div style="background: white; border: 1px solid #E2E8F0; border-radius: 12px; padding: 18px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
            <h4 style="color: #1B365D; margin: 0 0 6px 0;">📈 2. Transaction Trends</h4>
            <p style="color: #64748B; font-size: 0.85rem; line-height: 1.4; margin: 0;">
                Monthly transaction volume trends, average ticket sizes, and deposit vs withdrawal seasonal volatility (OQ-04).
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="background: white; border: 1px solid #E2E8F0; border-radius: 12px; padding: 18px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
            <h4 style="color: #1B365D; margin: 0 0 6px 0;">⚠️ 5. Dormancy & Churn</h4>
            <p style="color: #64748B; font-size: 0.85rem; line-height: 1.4; margin: 0;">
                4-tier inactivity migration tracking, ≥50% velocity contraction flags, and dormant balance recovery (OQ-02, OQ-03).
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        """
        <div style="background: white; border: 1px solid #E2E8F0; border-radius: 12px; padding: 18px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
            <h4 style="color: #1B365D; margin: 0 0 6px 0;">⚡ 3. Channel Analytics</h4>
            <p style="color: #64748B; font-size: 0.85rem; line-height: 1.4; margin: 0;">
                Omnichannel throughput (UPI, NetBanking, ATM, Branch) and automated ≥5.0% technical failure alerting (OQ-10).
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="background: white; border: 1px solid #E2E8F0; border-radius: 12px; padding: 18px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
            <h4 style="color: #1B365D; margin: 0 0 6px 0;">👥 6. Demographic Insights</h4>
            <p style="color: #64748B; font-size: 0.85rem; line-height: 1.4; margin: 0;">
                Robust dispersion boxplots (Median/IQR), tenure vs frequency correlation scatter with OLS regression (OQ-06 to OQ-09).
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 7. Dataset Health & Dual-Format Export
# -----------------------------------------------------------------------------
with st.expander("📥 Data Explorer, Quality Healthcard & Raw Data Export"):
    q_col1, q_col2, q_col3, q_col4 = st.columns(4)
    q_col1.metric("Raw Rows", f"{clean_meta['total_rows_raw']}")
    q_col2.metric("Imputed Incomes", f"{clean_meta['income_nulls_imputed']}")
    q_col3.metric("Filled Occupations", f"{clean_meta['occupation_nulls_filled']}")
    q_col4.metric("Clean Rows", f"{clean_meta['clean_rows_count']}")

    st.markdown("#### Filtered Analytical View (`vw_customer_account_activity_analysis`)")
    st.dataframe(df_filtered.head(100), use_container_width=True, height=280)

    down_col1, down_col2 = st.columns(2)
    with down_col1:
        csv_data = df_filtered.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Download Filtered Data (CSV)",
            data=csv_data,
            file_name="finedge_account_activity_filtered.csv",
            mime="text/csv",
            use_container_width=True
        )
    with down_col2:
        @st.cache_data
        def get_excel_bytes(df_in: pd.DataFrame) -> bytes:
            buf = io.BytesIO()
            with pd.ExcelWriter(buf, engine="openpyxl") as writer:
                df_in.to_excel(writer, index=False, sheet_name="Filtered_Data")
            return buf.getvalue()

        # Generate on demand
        if st.button("Generate Excel File", use_container_width=True):
            excel_bytes = get_excel_bytes(df_filtered)
            st.download_button(
                label="⬇️ Download Filtered Data (Excel .xlsx)",
                data=excel_bytes,
                file_name="finedge_account_activity_filtered.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

