# Master Build Plan: Customer Account Activity Analysis (CAAA)
**Target Platform:** Streamlit Multipage Web Application (Python 3.12/3.14)  
**Academic Context:** MCA 2nd Year Capstone Project, ABES Engineering College  
**Candidate:** Devesh Kumar (Roll No: 2500320140050) | **Guide:** Prof. Alpna Lodhi  
**Industry Partner Case:** FinEdge Digital Solutions Pvt. Ltd., Sector 62, Noida  

---

## 1. Project Summary & Document Index

### Project Summary (10 Lines)
1. Customer Account Activity Analysis (CAAA) is an enterprise-grade retail banking business intelligence system engineered for FinEdge Digital Solutions Pvt. Ltd.
2. The platform bridges transaction-level data engineering with executive portfolio decision-making across Savings, Current, and Salary accounts.
3. The system tracks 10 Operational Questions (OQ-01 to OQ-10) addressing dormant accounts, churn risk, MAB deficits, channel technical failures, and demographic balance skewness.
4. Built upon a 3NF relational SQLite database (`data/app.db`) featuring 5 tables and an indexed 42-column denormalized analytical view (`vw_customer_account_activity_analysis`).
5. Implements a resilient 5-tier architecture: Ingestion (`src/data_loader.py`), Cleaning & Imputation (`src/data_cleaner.py`), Statistical Analytics (`src/analytics.py`), Tailwind UI Components (`src/ui.py`), and Multipage Presentation (`pages/`).
6. Core analytics utilize robust statistics (Median, IQR, MAD, and Pearson correlation with OLS trendlines) to neutralize the extreme right-skew of the top 5% High Net Worth (HNW) balances.
7. Advanced business logic models 4-tier inactivity migration (Active, At-Risk, Inactive, Dormant) and a $\ge 50\%$ monthly transaction velocity contraction churn early warning flag.
8. The front-end leverages Streamlit multipage navigation combined with custom Tailwind CSS via CDN inside `st.components.v1.html` for high-impact responsive KPI scorecards.
9. Fully covered by a 15-test automated `pytest` test harness and 13 functional acceptance test cases ensuring zero database violations and sub-3-second rendering latency.
10. Engineered for seamless zero-downtime deployment on Streamlit Community Cloud with pinned dependencies and enterprise documentation.

### Master Document Index
- **Step 01 — Project Understanding:** [`01_Customer_Account_Activity_Analysis_Project_Understanding.docx`](file:///c:/Users/alish/OneDrive/Desktop/Costumer%20Account%20Activity%20Analysis/01_Customer_Account_Activity_Analysis_Project_Understanding.docx)
- **Step 02 — How Might We Statements:** [`docs/02_HMW_Statements.docx`](file:///c:/Users/alish/OneDrive/Desktop/Costumer%20Account%20Activity%20Analysis/docs/02_HMW_Statements.docx)
- **Step 03 — Needs Analysis:** [`docs/03_Needs_Analysis.docx`](file:///c:/Users/alish/OneDrive/Desktop/Costumer%20Account%20Activity%20Analysis/docs/03_Needs_Analysis.docx)
- **Step 04 — Requirements Traceability Matrix:** [`docs/04_Traceability_Matrix.xlsx`](file:///c:/Users/alish/OneDrive/Desktop/Costumer%20Account%20Activity%20Analysis/docs/04_Traceability_Matrix.xlsx)
- **Step 05 — Business Requirements Document (BRD):** [`docs/05_BRD.docx`](file:///c:/Users/alish/OneDrive/Desktop/Costumer%20Account%20Activity%20Analysis/docs/05_BRD.docx)
- **Step 07 — Technical Requirements Document (TRD):** [`docs/07_TRD.docx`](file:///c:/Users/alish/OneDrive/Desktop/Costumer%20Account%20Activity%20Analysis/docs/07_TRD.docx)
- **Step 08 — Database Design & Data Dictionaries:** [`docs/08_Database_Design.xlsx`](file:///c:/Users/alish/OneDrive/Desktop/Costumer%20Account%20Activity%20Analysis/docs/08_Database_Design.xlsx)
- **Step 09 — Entity-Relationship Diagram:** [`docs/09_ER_Diagram.docx`](file:///c:/Users/alish/OneDrive/Desktop/Costumer%20Account%20Activity%20Analysis/docs/09_ER_Diagram.docx) | [`docs/09_ER_Diagram.png`](file:///c:/Users/alish/OneDrive/Desktop/Costumer%20Account%20Activity%20Analysis/docs/09_ER_Diagram.png)
- **Step 10 — Synthetic Dataset & Audit Report:** [`data/caaa_data.xlsx`](file:///c:/Users/alish/OneDrive/Desktop/Costumer%20Account%20Activity%20Analysis/data/caaa_data.xlsx) | [`docs/10_Dataset_Validation_Report.docx`](file:///c:/Users/alish/OneDrive/Desktop/Costumer%20Account%20Activity%20Analysis/docs/10_Dataset_Validation_Report.docx)
- **Step 11 — User Stories & Acceptance Criteria:** [`docs/11_User_Stories.docx`](file:///c:/Users/alish/OneDrive/Desktop/Costumer%20Account%20Activity%20Analysis/docs/11_User_Stories.docx)
- **Step 12 — UI Framework & Design System:** [`docs/12_UI_Framework.docx`](file:///c:/Users/alish/OneDrive/Desktop/Costumer%20Account%20Activity%20Analysis/docs/12_UI_Framework.docx)
- **Step 13 — Functional & Technical Test Cases:** [`docs/13_Test_Cases.docx`](file:///c:/Users/alish/OneDrive/Desktop/Costumer%20Account%20Activity%20Analysis/docs/13_Test_Cases.docx)

---

## 2. Final Folder Structure

```text
Costumer Account Activity Analysis/
├── .streamlit/
│   └── config.toml                  # Theme colors (Primary: #1B365D), layout wide, font sans-serif
├── data/
│   ├── app.db                       # Relational SQLite database with foreign keys & 42-col analytical view
│   ├── schema.sql                   # Physical DDL table schema and view definitions
│   ├── caaa_data.xlsx               # Master multi-tab Excel workbook of all generated tables
│   ├── dim_customers.csv            # 100 customer dimension records
│   ├── dim_accounts.csv             # 150 account dimension records
│   ├── dim_channels.csv             # 5 delivery channel dimension records
│   ├── fact_transactions.csv        # 600 transaction fact records
│   └── fact_monthly_snapshots.csv   # 300 monthly snapshot records
├── docs/
│   ├── 02_HMW_Statements.docx
│   ├── 03_Needs_Analysis.docx
│   ├── 04_Traceability_Matrix.xlsx
│   ├── 05_BRD.docx
│   ├── 07_TRD.docx
│   ├── 08_Database_Design.xlsx
│   ├── 09_ER_Diagram.docx
│   ├── 09_ER_Diagram.png
│   ├── 10_Dataset_Validation_Report.docx
│   ├── 11_User_Stories.docx
│   ├── 12_UI_Framework.docx
│   ├── 13_Test_Cases.docx
│   └── 14_BUILD_PLAN.docx           # Executive Word copy of this build plan
├── pages/
│   ├── 1_Executive_Overview.py       # UI-01 & UI-02: Portfolio metrics, HNW isolation, executive filters
│   ├── 2_Activity_and_Channels.py    # UI-03 & UI-04: Omnichannel volume, failure rate alerts (OQ-04, OQ-10)
│   ├── 3_Inactivity_and_Churn.py     # UI-05: 4-tier inactivity migration, velocity drop churn risk (OQ-02, OQ-03)
│   ├── 4_MAB_Compliance.py           # UI-06: MAB non-compliance, fee deficit simulations (OQ-05)
│   ├── 5_Demographics_and_EDA.py     # UI-07: Skewed balance boxplots, tenure vs frequency scatter (OQ-06 to OQ-09)
│   └── 6_Data_Explorer_and_Quality.py# UI-08: Analytical view grid, missing/outlier audit, CSV/XLSX download
├── src/
│   ├── __init__.py
│   ├── generate_data.py             # Synthetic data generator engine (seed=42)
│   ├── data_loader.py               # Database connector, view extraction, st.cache_data caching
│   ├── data_cleaner.py              # Null imputation, boundary validation, anomaly flagging
│   ├── analytics.py                 # Mathematical & statistical computations (HNW, churn, MAB, IQR, OLS)
│   └── ui.py                        # Tailwind CSS CDN components (headers, KPI cards, insight callouts)
├── tests/
│   ├── __init__.py
│   ├── test_data.py                 # SQLite integrity, schema constraints, 42-col view tests
│   ├── test_analysis.py             # Unit tests for statistical formulas and banking logic
│   └── test_app.py                  # AppTest integration tests, component callables, latency benchmarks
├── .gitignore                       # Git exclusions (venv, __pycache__, temporary caches)
├── app.py                           # Application entry point, landing hero banner, shared sidebar routing
├── BUILD_PLAN.md                    # This master build plan specification
├── requirements.txt                 # Pinned dependencies for local and cloud execution
└── README.md                        # Enterprise repository documentation and quickstart guide
```

---

## 3. Step-by-Step Build Tasks

```
Sequence:
BUILD-01 (Setup & Deps) ───────► BUILD-02 (Data Loader) ───────► BUILD-03 (Cleaner)
                                                                        │
BUILD-06 (Overview UI) ◄─────── BUILD-05 (UI Components) ◄───── BUILD-04 (Analytics)
       │
BUILD-07 (Channels UI) ───────► BUILD-08 (Churn UI) ──────────► BUILD-09 (MAB UI)
                                                                        │
BUILD-12 (Pytest 100%) ◄─────── BUILD-11 (Explorer UI) ◄─────── BUILD-10 (EDA UI)
       │
BUILD-13 (README & Deploy Ready)
```

---

### Task BUILD-01: Environment Setup & Pinned Dependencies
- **Goal:** Codify the runtime environment, pin Python package versions, establish Git exclusions, and ensure Streamlit theme settings are configured.
- **Files Affected:** `requirements.txt`, `.gitignore`, `.streamlit/config.toml`
- **User Stories & Features:** Foundational to all stories (`US-01` to `US-15`), `F-01`
- **Exact Prompt for AI:**
  ```text
  Create requirements.txt pinned to compatible versions:
  streamlit>=1.35.0, pandas>=2.2.0, numpy>=1.26.0, scipy>=1.13.0, statsmodels>=0.14.0, plotly>=5.22.0, openpyxl>=3.1.2, pytest>=8.2.0.
  Create a production .gitignore excluding .pytest_cache/, __pycache__/, .venv/, *.pyc, and OS metadata.
  Ensure .streamlit/config.toml defines primaryColor="#1B365D", backgroundColor="#F8FAFC", secondaryBackgroundColor="#FFFFFF", textColor="#1E293B", and font="sans serif".
  ```
- **How to Check It:** Verify file presence and inspect contents. Run `python -c "import streamlit, pandas, numpy, scipy, plotly; print('Dependencies verified')"`
- **Tests That Must Pass:** Environment initialization check; existing `tests/test_data.py` must run without module import errors.

---

### Task BUILD-02: Data Ingestion & Caching Layer
- **Goal:** Build `src/data_loader.py` to connect to `data/app.db` via URI read-only mode (`mode=ro`), fetch the 42-column analytical view `vw_customer_account_activity_analysis` into a Pandas DataFrame, and cache it using `@st.cache_data`.
- **Files Affected:** `src/data_loader.py`, `src/__init__.py`
- **User Stories & Features:** `US-02`, `F-01`
- **Exact Prompt for AI:**
  ```text
  Implement src/data_loader.py with:
  1. get_db_connection(db_path="data/app.db"): returns sqlite3.connect with uri=True, mode=ro, check_same_thread=False.
  2. @st.cache_data(ttl=3600, show_spinner="Loading customer account records...")
     def load_analytical_view(db_path="data/app.db") -> pd.DataFrame:
     Queries SELECT * FROM vw_customer_account_activity_analysis. Parses dates (opened_date, txn_date, snapshot_month) to pd.to_datetime. Asserts shape >= (150, 40).
  3. @st.cache_data
     def load_table(table_name: str, db_path="data/app.db") -> pd.DataFrame:
     Allows loading individual dim or fact tables with SQL injection sanitization (validates table_name against whitelist).
  ```
- **How to Check It:** Execute `python -c "from src.data_loader import load_analytical_view; df = load_analytical_view(); print(df.shape)"` in terminal. Must output `(600, 42)` without error.
- **Tests That Must Pass:** `tests/test_data.py::test_db_connection`, `tests/test_data.py::test_analytical_view` (`TC-T-01`, `TC-T-06`).

---

### Task BUILD-03: Data Cleaning & Preprocessing Pipeline
- **Goal:** Build `src/data_cleaner.py` to handle deliberate real-world data quality anomalies (2-3% missing `annual_income`, missing `occupation`, duplicate transaction IDs, and negative balance boundaries) while logging cleaning metrics.
- **Files Affected:** `src/data_cleaner.py`
- **User Stories & Features:** `US-02`, `US-15`, `F-01`, `F-06`
- **Exact Prompt for AI:**
  ```text
  Implement src/data_cleaner.py with clean_account_data(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
  1. Imputation: Fill missing annual_income with the median income segmented by occupation. If occupation is null, label as 'Unknown' / 'Unspecified'.
  2. De-duplication: Detect and remove exact duplicate transaction records based on txn_id, keeping the first occurrence and recording duplicate count in metadata.
  3. Boundary Enforcement: Clip negative balances at 0.0 with a logged audit entry. Ensure all financial monetary fields are converted to float64 rounded to 2 decimal places.
  4. Metric Tracking: Return a cleaning_summary dictionary containing: total_rows_raw, duplicates_removed, income_nulls_imputed, occupation_nulls_filled, clean_rows_count.
  ```
- **How to Check It:** Run a python snippet cleaning the loaded analytical view; assert zero nulls in imputed columns and confirm `cleaning_summary` dictionary keys.
- **Tests That Must Pass:** `tests/test_data.py::test_non_negative_balances` (`TC-T-05`), data integrity assertions.

---

### Task BUILD-04: Core Financial Analytics & Statistical Engine
- **Goal:** Build `src/analytics.py` implementing all banking formulas, quantile isolations, churn triggers, and statistical routines for OQ-01 through OQ-10.
- **Files Affected:** `src/analytics.py`
- **User Stories & Features:** `US-03`, `US-04`, `US-05`, `US-06`, `US-08`, `US-11`, `US-12`, `US-13`, `F-02`, `F-03`, `F-04`, `F-05`, `F-06`
- **Exact Prompt for AI:**
  ```text
  Implement src/analytics.py with pure, vectorized mathematical functions:
  1. compute_hnw_cutoff(df, quantile=0.95) -> tuple[float, pd.DataFrame, float]: Returns cutoff_balance, hnw_df, hnw_deposit_share_pct.
  2. calculate_velocity_drop_churn(df, drop_threshold=0.50) -> pd.DataFrame: Compares prior_month_txns vs recent_month_txns; flags is_churn_risk if (prior - recent)/prior >= drop_threshold.
  3. compute_inactivity_distribution(df) -> pd.DataFrame: Aggregates counts and balance totals across 'Active (0-30d)', 'At-Risk (31-60d)', 'Inactive (61-89d)', 'Dormant (90+d)'.
  4. compute_mab_compliance_and_deficit(df, fee_per_violation=250.0) -> dict: Computes compliance rate (%), total deposit deficit (sum of max(0, min_req - balance)), and projected fee revenue (INR).
  5. compute_channel_failure_rates(df, alert_threshold=5.0) -> pd.DataFrame: Calculates failure_rate_pct = (failed_txns / total_txns) * 100 per channel; adds is_alert boolean.
  6. compute_balance_dispersion_stats(df, group_col='occupation') -> pd.DataFrame: Returns count, median, IQR (scipy.stats.iqr), min, max for current_balance per segment.
  7. compute_tenure_frequency_correlation(df) -> tuple[float, float, str]: Calculates scipy.stats.pearsonr(tenure_months, txn_frequency); returns r, p_value, and statistical strength label.
  ```
- **How to Check It:** Run `pytest tests/test_analysis.py`. All 6 unit tests must pass with 100% precision.
- **Tests That Must Pass:** `tests/test_analysis.py::test_hnw_quantile_calculation` (`TC-T-07`), `test_velocity_drop_churn_formula` (`TC-T-08`), `test_inactivity_tier_classification` (`TC-T-09`), `test_mab_compliance_and_deficit` (`TC-T-10`), `test_channel_failure_rate_calculation` (`TC-T-11`), `test_statistical_dispersion_and_correlation` (`TC-T-12`).

---

### Task BUILD-05: Reusable Tailwind UI Component Library
- **Goal:** Enhance `src/ui.py` to render responsive, institutional banking components via Tailwind CSS CDN (`https://cdn.tailwindcss.com`) wrapped in `st.components.v1.html`.
- **Files Affected:** `src/ui.py`
- **User Stories & Features:** `US-01`, `US-03`, `F-02`
- **Exact Prompt for AI:**
  ```text
  Extend src/ui.py with enterprise styling functions:
  1. render_header(title, subtitle, badge_text="ABES Capstone"): Renders institutional navy (#1B365D) top header banner with metadata badge.
  2. render_kpi_card(title, value, delta_text, delta_positive=True, icon_name="currency-dollar"): Renders crisp KPI card with emerald/rose delta badge and subtle shadow.
  3. render_insight_box(title, message, severity="info"): Renders callout box (blue for info, amber for warning, red for critical, green for success).
  4. render_alert_banner(alert_title, alert_message): Renders prominent danger banner for channel failures >= 5.0% or high churn alerts.
  Ensure components specify appropriate fixed heights in st.components.v1.html to eliminate internal scrollbars.
  ```
- **How to Check It:** Run `pytest tests/test_app.py -k test_ui_module_components`.
- **Tests That Must Pass:** `tests/test_app.py::test_ui_module_components` (`TC-T-13`).

---

### Task BUILD-06: Main Entrypoint & Page 1 (Executive Overview)
- **Goal:** Implement `app.py` (entrypoint, global session state, sidebar filters, navigation) and `pages/1_Executive_Overview.py` (executive scorecard, HNW Pareto concentration, portfolio breakdown).
- **Files Affected:** `app.py`, `pages/1_Executive_Overview.py`
- **User Stories & Features:** `US-01`, `US-02`, `US-03`, `US-04`, `F-01`, `F-02`, `UI-01`, `UI-02`
- **Exact Prompt for AI:**
  ```text
  Implement app.py and pages/1_Executive_Overview.py:
  1. app.py: Set st.set_page_config(page_title="CAAA - FinEdge Banking", layout="wide", page_icon="🏦").
     Establish shared session_state filters in sidebar: Region (All, Urban, Semi-Urban, Rural), Account Type (All, Savings, Current, Salary), Inactivity Tier (All, Active, At-Risk, Inactive, Dormant).
     Display landing hero with project metadata, FinEdge context, and navigation links.
  2. pages/1_Executive_Overview.py:
     Fetch cached data, apply sidebar filters. Render 4 Tailwind KPI cards: Total Customers, Total Balance, Active Account %, High-Risk Churn Rate.
     Render Plotly donut chart of Balance by Account Type.
     Render HNW Pareto Analysis: top 5% threshold, total balance share metric, and cumulative balance percentage curve.
  ```
- **How to Check It:** Run `streamlit run app.py` and inspect in browser; verify filters reactively re-render KPI metrics and charts without errors.
- **Tests That Must Pass:** `TC-F-01`, `TC-F-02`, `TC-F-03`, `TC-T-14`.

---

### Task BUILD-07: Page 2 (Omnichannel Activity & Failure Monitoring)
- **Goal:** Implement `pages/2_Activity_and_Channels.py` tracking transaction volumes, channel adoption, failure rates, and threshold alerts for OQ-04 and OQ-10.
- **Files Affected:** `pages/2_Activity_and_Channels.py`
- **User Stories & Features:** `US-10`, `US-11`, `US-14`, `F-05`, `UI-03`, `UI-04`
- **Exact Prompt for AI:**
  ```text
  Implement pages/2_Activity_and_Channels.py:
  1. Top KPI Row: Total Transactions, Total Volume (INR), Overall Failure Rate (%), Most Popular Channel.
  2. Channel Failure Monitoring: Render table/cards with failure percentages. Highlight any channel with failure rate >= 5.0% using render_alert_banner.
  3. Interactive Visuals:
     - Plotly Bar Chart: Transaction volume by channel (UPI, NetBanking, Mobile App, ATM, Branch).
     - Plotly Grouped Bar Chart: Channel adoption broken down by region (Urban vs Semi-Urban vs Rural).
     - Time Series Trend: Monthly transaction volume progression.
  ```
- **How to Check It:** Navigate to Page 2; verify failure alert displays if any channel exceeds 5% failure rate; confirm charts render smoothly.
- **Tests That Must Pass:** `TC-F-07`, `TC-F-11`, `TC-T-11`.

---

### Task BUILD-08: Page 3 (Inactivity Segmentation & Churn Risk Engine)
- **Goal:** Implement `pages/3_Inactivity_and_Churn.py` to identify dormant accounts, early churn indicators, and velocity drops for OQ-02 and OQ-03.
- **Files Affected:** `pages/3_Inactivity_and_Churn.py`
- **User Stories & Features:** `US-05`, `US-06`, `US-07`, `F-03`, `UI-05`
- **Exact Prompt for AI:**
  ```text
  Implement pages/3_Inactivity_and_Churn.py:
  1. Scorecard: Inactive Accounts (61-89d), Dormant Accounts (90+d), Total Balance Locked in Dormancy, Accounts with >= 50% Velocity Drop.
  2. Visualizations:
     - Plotly Sunburst / Funnel Chart: Inactivity tier breakdown (Active -> At-Risk -> Inactive -> Dormant).
     - Scatter Plot: Days Inactive vs Current Balance, color-coded by Inactivity Tier.
     - Velocity Contraction Table: Filterable grid showing accounts flagged for churn risk with prior vs recent transaction counts and percentage decline.
  ```
- **How to Check It:** Navigate to Page 3; verify accounts with velocity drop $\ge 50\%$ are isolated in the table with red risk tags.
- **Tests That Must Pass:** `TC-F-04`, `TC-F-05`, `TC-T-08`, `TC-T-09`.

---

### Task BUILD-09: Page 4 (Minimum Average Balance Compliance & Deficit)
- **Goal:** Implement `pages/4_MAB_Compliance.py` detailing MAB non-compliance, aggregate balance deficits, and fee simulations for OQ-05.
- **Files Affected:** `pages/4_MAB_Compliance.py`
- **User Stories & Features:** `US-08`, `US-09`, `F-04`, `UI-06`
- **Exact Prompt for AI:**
  ```text
  Implement pages/4_MAB_Compliance.py:
  1. Metrics Row: Non-Compliant Account Count, Portfolio Compliance %, Total MAB Deficit (INR), Simulated Penalty Revenue.
  2. Simulation Slider: st.slider for Monthly Penalty Fee per violation (INR 100 to INR 1,000, default 250), dynamically updating projected fee revenue.
  3. Visualizations:
     - Grouped Bar Chart: Compliance rate by Account Type (Savings vs Current vs Salary).
     - Deficit Distribution Histogram: Balance shortfall across non-compliant accounts.
     - Branch / Region Deficit Breakdown: Highlighting branches with the highest non-compliance risk.
  ```
- **How to Check It:** Move the fee slider; confirm fee revenue metric dynamically recalculates instantly.
- **Tests That Must Pass:** `TC-F-06`, `TC-T-10`.

---

### Task BUILD-10: Page 5 (Customer Demographics & Statistical EDA)
- **Goal:** Implement `pages/5_Demographics_and_EDA.py` providing rigorous statistical exploration of balance distributions, tenure correlation, and occupation comparisons for OQ-06, OQ-07, OQ-08, and OQ-09.
- **Files Affected:** `pages/5_Demographics_and_EDA.py`
- **User Stories & Features:** `US-12`, `US-13`, `US-14`, `F-06`, `UI-07`
- **Exact Prompt for AI:**
  ```text
  Implement pages/5_Demographics_and_EDA.py:
  1. Balance Dispersion (OQ-07): Render Plotly Boxplots of Current Balance by Occupation (Salaried, Self-Employed, Business, Student, Retired) and Region. Display Median and IQR statistics table.
  2. Account Tenure vs Frequency (OQ-08): Render Plotly Scatter plot of Account Age (Months) vs Transaction Frequency with OLS linear trendline. Annotate Pearson correlation coefficient (r) and p-value.
  3. Demographic Analysis (OQ-06, OQ-09):
     - Bar chart comparing average and median balance by Gender and Age Groups.
     - Heatmap of account concentration by City and Region.
  ```
- **How to Check It:** Verify boxplots properly display median and IQR without skew distortion; verify scatter plot shows trendline and correlation metrics.
- **Tests That Must Pass:** `TC-F-09`, `TC-F-10`, `TC-T-12`.

---

### Task BUILD-11: Page 6 (Data Explorer, Quality Audit & Export)
- **Goal:** Implement `pages/6_Data_Explorer_and_Quality.py` exposing the full 42-column analytical dataset, missing/duplicate quality audit findings, and CSV/Excel download capabilities.
- **Files Affected:** `pages/6_Data_Explorer_and_Quality.py`
- **User Stories & Features:** `US-02`, `US-15`, `F-01`, `UI-08`
- **Exact Prompt for AI:**
  ```text
  Implement pages/6_Data_Explorer_and_Quality.py:
  1. Data Quality Healthcard: Display total records, null counts by column, duplicates detected, and boundary validation status.
  2. Interactive Table: Render st.dataframe of filtered analytical view with search and sort capabilities.
  3. Export Actions:
     - st.download_button for CSV format.
     - st.download_button for Excel format (generated in-memory via io.BytesIO and openpyxl).
  4. Graceful Empty State: If filters yield 0 records, display render_insight_box(severity='warning', message='No records match current filter criteria. Adjust your filters.').
  ```
- **How to Check It:** Download both CSV and Excel files; verify file integrity. Test contradictory filters to verify zero-record warning is handled cleanly.
- **Tests That Must Pass:** `TC-F-12`, `TC-F-13`, `TC-T-02`.

---

### Task BUILD-12: Full Automated Test Suite Verification & Bug Squashing
- **Goal:** Execute the complete `pytest` test suite across `test_data.py`, `test_analysis.py`, and `test_app.py`, remediating any regressions until all 15 tests pass green (100% pass rate).
- **Files Affected:** `tests/test_app.py`, `app.py`, `pages/*.py`
- **User Stories & Features:** Quality Assurance across all stories (`US-01` to `US-15`)
- **Exact Prompt for AI:**
  ```text
  Run python -m pytest tests/ -v.
  Verify that:
  1. TC-T-14 (test_streamlit_app_starts) executes AppTest.from_file('app.py') without uncaught exceptions.
  2. TC-T-15 (test_multipage_pages_structure) executes all page modules and validates that query execution latency is < 3.0 seconds.
  3. All 15 unit and integration tests return PASSED. Fix any syntax, import, or logical issues.
  ```
- **How to Check It:** Run `python -m pytest tests/`; assert terminal outputs `15 passed in X.XXs` with 0 failures and 0 skipped.
- **Tests That Must Pass:** All 15 tests (`TC-T-01` to `TC-T-15`).

---

### Task BUILD-13: Production Readme, Project Architecture & Cloud Deployment
- **Goal:** Author the comprehensive project `README.md` with complete architecture diagrams, installation instructions, execution commands, and cloud deployment steps for Streamlit Community Cloud.
- **Files Affected:** `README.md`, `requirements.txt`
- **User Stories & Features:** Deployment & Documentation Readiness
- **Exact Prompt for AI:**
  ```text
  Generate an enterprise-grade README.md with:
  1. Project Title, Student details, ABES Engineering College attribution.
  2. System Architecture (ASCII / Mermaid diagram).
  3. Tech Stack table with pinned versions and rationale.
  4. Quickstart installation and run instructions (virtual environment, pip install, streamlit run app.py).
  5. Test execution instructions (pytest tests/).
  6. Multipage Navigation summary and OQ coverage matrix.
  7. Streamlit Community Cloud deployment runbook.
  ```
- **How to Check It:** Preview `README.md` in markdown viewer; verify all links and commands are accurate.
- **Tests That Must Pass:** App runs cleanly with `streamlit run app.py --server.headless=true`.

---

## 4. Definition of Done (DoD)

To declare the Customer Account Activity Analysis platform complete and ready for ABES viva defense, the project must satisfy all of the following conditions:

1. **Requirements Coverage:** 100% of "Must" Business Requirements (`BR-01` through `BR-07`, `BR-10`) and "Should" requirements (`BR-08`, `BR-09`, `BR-11`) are fully implemented and verified against the RTM.
2. **Automated Test Verification:** All 15 `pytest` test cases in `tests/` pass with zero failures and zero skipped tests (`15 passed in < 5.0s`).
3. **Operational Question Resolution:** All 10 Operational Questions (`OQ-01` to `OQ-10`) have dedicated interactive visualizations, KPIs, and analytical outputs.
4. **Resilience & Error Handling:** Zero unhandled runtime exceptions. Contradictory filters display user-friendly warning callouts rather than application crashes.
5. **Performance Benchmark:** Every dashboard page loads and executes filtering queries within the 3.0-second SLA.
6. **Code Quality & Documentation:** All source modules in `src/` and `pages/` include docstrings, type annotations, and clean architectural separation.
7. **Production Assets:** `README.md`, `requirements.txt`, and deployment configurations are complete and tested.

---

## 5. Execution Commands

### Environment Setup & Dependency Installation
```bash
# 1. Create and activate a Python virtual environment
python -m venv .venv
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# Linux / macOS:
source .venv/bin/activate

# 2. Upgrade pip and install pinned dependencies
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Running the Application
```bash
# Run the Streamlit Multipage Application locally
streamlit run app.py
```

### Running Automated Test Suites
```bash
# Run all unit, analytical, and integration tests
python -m pytest tests/ -v

# Run with execution duration benchmarks
python -m pytest tests/ --durations=5
```

---

## 6. Viva Voce Notes: 10 Likely Questions & Short Answers

1. **Q: What is the core business problem FinEdge Digital Solutions is solving with this platform?**  
   *A:* Mitigating customer churn, identifying silent account dormancy, recovering Minimum Average Balance (MAB) deposit deficits, and detecting omnichannel technical failures across retail banking accounts.

2. **Q: Why did you use SQLite for this capstone project instead of PostgreSQL or MySQL?**  
   *A:* SQLite provides a serverless, zero-configuration relational database stored directly in the repository (`data/app.db`), guaranteeing self-contained portability, ACID compliance, and sub-millisecond query execution for our analytical dataset.

3. **Q: How does the application handle extreme balance outliers caused by High Net Worth (HNW) customers?**  
   *A:* By utilizing non-parametric, robust statistics—specifically Median, Interquartile Range (IQR), and Median Absolute Deviation (MAD)—which prevent the top 5% HNW balances from skewing central tendency metrics.

4. **Q: What criteria define an account as being at risk of churning?**  
   *A:* An account exhibiting a monthly transaction velocity contraction of $\ge 50\%$ compared to its historical baseline, or migrating into the "Inactive (61-89d)" inactivity tier before reaching regulatory dormancy at 90+ days.

5. **Q: Why wrap Tailwind CSS via CDN inside `st.components.v1.html` instead of standard Streamlit metrics?**  
   *A:* Native `st.metric` has rigid styling and lacks custom layout flexibility; Tailwind CSS provides responsive grid control, custom institutional navy palettes (`#1B365D`), and distinct color-coded delta pills (+emerald / -rose).

6. **Q: What purpose does the 42-column analytical view (`vw_customer_account_activity_analysis`) serve?**  
   *A:* It pre-joins customer, account, channel, and transaction dimensions with pre-aggregated metrics, decoupling the presentation layer from backend join operations and ensuring sub-second dashboard rendering.

7. **Q: How does `@st.cache_data` improve application responsiveness?**  
   *A:* It memoizes DataFrame outputs of database queries in memory; subsequent filter interactions reuse cached data without re-executing disk reads, keeping page response time under 3 seconds.

8. **Q: What happens when contradictory filters yield zero matching records?**  
   *A:* The application intercepts the empty DataFrame and displays a styled warning alert (`render_insight_box`) prompting the user to broaden criteria, preventing runtime exceptions.

9. **Q: How did you validate data integrity during dataset generation?**  
   *A:* By enforcing relational primary keys, non-negative balance checks, and verifying with SQLite's `PRAGMA foreign_key_check`, which confirmed zero constraint violations across all tables.

10. **Q: How does this project satisfy the ABES MCA capstone evaluation criteria?**  
    *A:* It follows a rigorous 18-step engineering lifecycle spanning stakeholder analysis, MoSCoW prioritization, 3NF schema design, automated TDD testing, responsive UI architecture, and cloud deployment.
