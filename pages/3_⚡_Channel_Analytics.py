"""
FinEdge Digital Solutions — Customer Account Activity Analysis (CAAA)
Page 3: Omnichannel Adoption & Technical Failure Alerts (OQ-10)
File: pages/3_⚡_Channel_Analytics.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from src.data_loader import load_analytical_view
from src.data_cleaner import clean_account_data
from src.analytics import compute_channel_failure_rates
from src.ui import render_tailwind_header, render_kpi_row_4, render_insight_box, render_alert_banner

st.set_page_config(page_title="Channel Analytics — FinEdge CAAA", page_icon="⚡", layout="wide")

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
    title="3. Omnichannel Activity & Technical Failure Monitoring",
    subtitle="Operational Question 10: Which channels drive highest volume, and are technical failure rates exceeding the 5.0% operational alert threshold?",
    badge_text="OQ-10 Analysis",
    category="Channel Health"
)

st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

if df.empty:
    render_insight_box("No Records Found", "No channel activity found for the selected filter combination.", "warning")
    st.stop()

# Channel analytics computation
channel_summary = compute_channel_failure_rates(df, alert_threshold=5.0)

total_txns = channel_summary["total_txns"].sum()
top_channel = channel_summary.iloc[0]["channel_name"] if not channel_summary.empty else "N/A"
failed_total = channel_summary["failed_txns"].sum()
overall_failure_rate = (failed_total / total_txns * 100) if total_txns > 0 else 0.0
alert_channels = channel_summary[channel_summary["is_alert"]]

# Top KPIs
kpi_row = [
    {
        "title": "Total Channel Throughput",
        "value": f"{total_txns:,}",
        "delta": f"{len(channel_summary)} Active Channels",
        "is_positive": True,
        "icon": "📱",
        "subtext": "Executed cross-channel txns"
    },
    {
        "title": "Leading Channel",
        "value": str(top_channel),
        "delta": f"{channel_summary.iloc[0]['total_txns']} Txns",
        "is_positive": True,
        "icon": "🏆",
        "subtext": "Highest transaction volume"
    },
    {
        "title": "Overall Technical Failure Rate",
        "value": f"{overall_failure_rate:.1f}%",
        "delta": f"{failed_total} Failed Txns",
        "is_positive": overall_failure_rate < 5.0,
        "icon": "⚠️",
        "subtext": "Failed / Total transactions"
    },
    {
        "title": "Critical Channel Alerts",
        "value": f"{len(alert_channels)}",
        "delta": "≥5.0% Threshold" if len(alert_channels) > 0 else "All Channels Normal",
        "is_positive": len(alert_channels) == 0,
        "icon": "🚨",
        "subtext": "Channels requiring engineering audit"
    }
]
render_kpi_row_4(kpi_row)

st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

# High-priority alert banner if threshold breached
if not alert_channels.empty:
    breached_names = ", ".join([f"{r['channel_name']} ({r['failure_rate_pct']}%)" for _, r in alert_channels.iterrows()])
    render_alert_banner(
        alert_title="OPERATIONAL RISK ALERT: Technical Failure Threshold Exceeded (≥5.0%)",
        alert_message=f"The following delivery channels breached acceptable reliability thresholds: {breached_names}. Engineering Lead Sandeep Rawat (SH-06) must inspect gateway APIs and host latency immediately."
    )
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

# Visualizations Row
col1, col2 = st.columns([1, 1.2])

with col1:
    st.markdown("#### Transaction Volume by Channel")
    fig_bar = px.bar(
        channel_summary,
        x="channel_name",
        y="total_txns",
        color="failure_rate_pct",
        color_continuous_scale="Reds",
        labels={"channel_name": "Channel", "total_txns": "Transaction Count", "failure_rate_pct": "Failure Rate (%)"}
    )
    fig_bar.update_layout(margin=dict(t=15, b=15, l=15, r=15), height=320)
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    st.markdown("#### Channel Adoption by Geographic Region")
    if "region" in df.columns:
        region_channel = df.groupby(["region", "channel_name"], observed=False)["transaction_id"].count().reset_index()
        fig_grouped = px.bar(
            region_channel,
            x="channel_name",
            y="transaction_id",
            color="region",
            barmode="group",
            color_discrete_map={"Urban": "#1B365D", "Semi-Urban": "#2980B9", "Rural": "#10B981"},
            labels={"channel_name": "Channel", "transaction_id": "Count", "region": "Region"}
        )
        fig_grouped.update_layout(margin=dict(t=15, b=15, l=15, r=15), height=320)
        st.plotly_chart(fig_grouped, use_container_width=True)
    else:
        st.info("Region data unavailable for grouping.")

# Detailed Channel Scorecard Table
st.markdown("#### Omnichannel Reliability & Failure Audit Table")
st.dataframe(
    channel_summary.style.format({
        "total_volume": "₹{:,.2f}",
        "failure_rate_pct": "{:.2f}%"
    }),
    use_container_width=True
)
