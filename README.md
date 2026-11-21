# Customer Account Activity Analysis (P063)
### Enterprise Retail Banking Business Intelligence & Risk Monitoring Platform

**Academic Context:** MCA 2nd Year Capstone Project (Data Analytics)  
**Institution:** ABES Engineering College, Ghaziabad  
**Candidate:** Devesh Kumar | **Roll No:** `2500320140050`  
**Faculty Guide & Evaluator:** Mr. Dinesh, Mentor (Data Analytics)  
**Industry Partner Context:** FinEdge Digital Solutions Pvt. Ltd., Sector 62, Noida  

---

## 1. Executive Summary

Customer Account Activity Analysis (P063) is an enterprise retail banking analytics platform engineered for FinEdge Digital Solutions Pvt. Ltd. The system bridges transaction-level data engineering with executive portfolio decision-making across Savings, Current, and Salary accounts.

The platform directly resolves 10 Operational Questions (`OQ-01` through `OQ-10`) addressing high-risk dormancy migration, early-warning churn velocity drops, Minimum Average Balance (MAB) shortfall deficits, omnichannel delivery reliability, and non-parametric demographic balance dispersion.

---

## 2. System Architecture

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        SQLite Relational Storage                       │
│                     (data/app.db, 3NF, Foreign Keys ON)                 │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                       Data Layer & Ingestion Engine                    │
│      src/data_loader.py (URI mode=ro, @st.cache_data memoization)      │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                      Cleaning & Imputation Pipeline                    │
│      src/data_cleaner.py (Median income imputation, deduplication)     │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                   Analytics & Statistical Core Engine                  │
│       src/analytics.py (HNW quantile, Churn velocity, MAB deficit)     │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                     Tailwind CSS Component System                      │
│      src/ui.py (Institutional headers, KPI scorecards, alert banners)  │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                   Streamlit Multipage Presentation                     │
│  app.py ───► pages/1_Portfolio_Overview  ───► pages/2_Trends          │
│         ───► pages/3_Channel_Analytics   ───► pages/4_Customer_360     │
│         ───► pages/5_Dormancy_and_Churn  ───► pages/6_Demographics    │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Technology Stack & Pinned Versions

| Layer | Component | Version | Technical Rationale |
| :--- | :--- | :--- | :--- |
| **Language** | Python | `3.12 / 3.14` | Core execution runtime with modern type annotations |
| **Database** | SQLite 3 | `3.45+` | Serverless, zero-config relational store with foreign key enforcement |
| **Frontend** | Streamlit | `>=1.35.0` | Reactive Python web framework with native multipage support |
| **Styling** | Tailwind CSS | `3.4+ CDN` | Responsive institutional design via `st.components.v1.html` |
| **Visualization**| Plotly Express | `>=5.22.0` | Interactive SVG/WebGL charts (donut, boxplots, scatter, Pareto) |
| **Statistics** | SciPy & NumPy | `>=1.13.0` | Non-parametric dispersion (Median, IQR) and Pearson correlation |
| **Testing** | Pytest & AppTest | `>=8.2.0` | Automated TDD test suite validating schema, math, and UI latency |

---

## 4. Multipage Directory & OQ Coverage Matrix

| Page Module | Screen Name | Mapped OQs | Core Functionality & Output |
| :--- | :--- | :--- | :--- |
| `app.py` | Home & Control Tower | Global | Sidebar filters (`st.session_state`), portfolio scorecard, data export |
| `pages/1_📊_Portfolio_Overview.py` | Portfolio Overview | `OQ-01` | Balance distribution by account type, Top 5% HNW Pareto curve |
| `pages/2_📈_Transaction_Trends.py` | Transaction Trends | `OQ-04` | Monthly throughput, average ticket sizes, credit vs debit flows |
| `pages/3_⚡_Channel_Analytics.py` | Channel Analytics | `OQ-10` | Omnichannel volume, regional adoption, $\ge 5.0\%$ failure rate alert |
| `pages/4_👤_Customer_360.py` | Customer 360 & MAB | `OQ-05` | MAB compliance rate, balance deficit audit, interactive fee slider |
| `pages/5_⚠️_Dormancy_and_Churn.py`| Dormancy & Churn | `OQ-02`, `OQ-03`| 4-tier inactivity migration, $\ge 50\%$ velocity drop churn tags |
| `pages/6_👥_Demographic_Insights.py`| Demographic Insights| `OQ-06` to `09` | Robust boxplots (Median/IQR), tenure vs frequency OLS correlation |

---

## 5. Quickstart & Local Execution

### 1. Environment Setup
```bash
# Clone or navigate to the project directory
cd "c:\Users\alish\OneDrive\Desktop\Costumer Account Activity Analysis"

# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# Linux / macOS:
source .venv/bin/activate

# Install pinned dependencies
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 2. Run Application
```bash
# Start Streamlit multipage application
streamlit run app.py
```
*The web dashboard will launch at `http://localhost:8501`.*

### 3. Run Automated Pytest Harness
```bash
# Execute all 15 unit, analytical, and integration test cases
python -m pytest tests/ -v
```
*Benchmark: All 15 tests pass green with zero errors.*

---

## 6. Cloud Deployment Runbook (Streamlit Community Cloud)

1. Push the repository to GitHub: `https://github.com/<username>/<rollno>-caaa`.
2. Navigate to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Select **New App**:
   - **Repository:** `<username>/<rollno>-caaa`
   - **Branch:** `main` (or `master`)
   - **Main file path:** `app.py`
4. In Advanced Settings, ensure Python version is set to `3.12`.
5. Click **Deploy**. Streamlit Cloud will install `requirements.txt` and launch the app with zero downtime.

---

## 7. Capstone Governance Documents (`docs/`)

- [`docs/01_Project_Understanding.docx`](file:///c:/Users/alish/OneDrive/Desktop/Costumer%20Account%20Activity%20Analysis/01_Customer_Account_Activity_Analysis_Project_Understanding.docx): Project definition, problem statement, SMART goals.
- [`docs/02_HMW_Statements.docx`](file:///c:/Users/alish/OneDrive/Desktop/Costumer%20Account%20Activity%20Analysis/docs/02_HMW_Statements.docx): 10 How-Might-We statements and pain points.
- [`docs/03_Needs_Analysis.docx`](file:///c:/Users/alish/OneDrive/Desktop/Costumer%20Account%20Activity%20Analysis/docs/03_Needs_Analysis.docx): 12 Business Requirements (BR-01 to BR-12).
- [`docs/04_Traceability_Matrix.xlsx`](file:///c:/Users/alish/OneDrive/Desktop/Costumer%20Account%20Activity%20Analysis/docs/04_Traceability_Matrix.xlsx): Master RTM with 100% test mappings.
- [`docs/05_BRD.docx`](file:///c:/Users/alish/OneDrive/Desktop/Costumer%20Account%20Activity%20Analysis/docs/05_BRD.docx): Business Requirements Document v1.0.
- [`docs/07_TRD.docx`](file:///c:/Users/alish/OneDrive/Desktop/Costumer%20Account%20Activity%20Analysis/docs/07_TRD.docx): Technical Requirements Document & SciPy specs.
- [`docs/08_Database_Design.xlsx`](file:///c:/Users/alish/OneDrive/Desktop/Costumer%20Account%20Activity%20Analysis/docs/08_Database_Design.xlsx): 3NF schema, DDL, 42-column analytical view.
- [`docs/09_ER_Diagram.docx`](file:///c:/Users/alish/OneDrive/Desktop/Costumer%20Account%20Activity%20Analysis/docs/09_ER_Diagram.docx): High-resolution ER diagram & relationship rules.
- [`docs/10_Dataset_Validation_Report.docx`](file:///c:/Users/alish/OneDrive/Desktop/Costumer%20Account%20Activity%20Analysis/docs/10_Dataset_Validation_Report.docx): Ingestion & audit report.
- [`docs/11_User_Stories.docx`](file:///c:/Users/alish/OneDrive/Desktop/Costumer%20Account%20Activity%20Analysis/docs/11_User_Stories.docx): 15 User Stories (US-01 to US-15) with Gherkin criteria.
- [`docs/12_UI_Framework.docx`](file:///c:/Users/alish/OneDrive/Desktop/Costumer%20Account%20Activity%20Analysis/docs/12_UI_Framework.docx): UI wireframes and Tailwind styling library.
- [`docs/13_Test_Cases.docx`](file:///c:/Users/alish/OneDrive/Desktop/Costumer%20Account%20Activity%20Analysis/docs/13_Test_Cases.docx): 13 Functional & 15 Technical test specifications.
- [`docs/14_BUILD_PLAN.docx`](file:///c:/Users/alish/OneDrive/Desktop/Costumer%20Account%20Activity%20Analysis/docs/14_BUILD_PLAN.docx): Phased implementation blueprint and DoD.
- [`docs/15_Build_and_Test_Report.docx`](file:///c:/Users/alish/OneDrive/Desktop/Costumer%20Account%20Activity%20Analysis/docs/15_Build_and_Test_Report.docx): Build execution log and pytest verification report.
