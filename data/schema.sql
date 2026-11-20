-- ====================================================================
-- ABES MCA CAPSTONE PROJECT: CUSTOMER ACCOUNT ACTIVITY ANALYSIS (CAAA)
-- SQLite Relational Schema Definition (3NF Production DDL)
-- File: data/schema.sql
-- ====================================================================

PRAGMA foreign_keys = ON;

-- 1. MASTER TABLE: Customers Dimension
CREATE TABLE IF NOT EXISTS dim_customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_code VARCHAR(12) NOT NULL UNIQUE,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    age INTEGER NOT NULL CHECK(age >= 18 AND age <= 100),
    age_group VARCHAR(15) NOT NULL CHECK(age_group IN ('18-25', '26-35', '36-50', '50+')),
    gender VARCHAR(10) NOT NULL CHECK(gender IN ('Male', 'Female', 'Other')),
    occupation VARCHAR(30) CHECK(occupation IS NULL OR occupation IN ('Salaried', 'Self-Employed', 'Business', 'Student', 'Retired')),
    annual_income DECIMAL(12,2) CHECK(annual_income IS NULL OR annual_income >= 0),
    credit_score INTEGER NOT NULL CHECK(credit_score BETWEEN 300 AND 900),
    kyc_status VARCHAR(15) NOT NULL CHECK(kyc_status IN ('Verified', 'Pending', 'Re-KYC')),
    branch_id INTEGER NOT NULL,
    branch_name VARCHAR(50) NOT NULL,
    branch_city VARCHAR(50) NOT NULL,
    branch_tier VARCHAR(15) NOT NULL CHECK(branch_tier IN ('Urban', 'Semi-Urban', 'Rural')),
    onboarding_date DATE NOT NULL
);

-- 2. MASTER TABLE: Accounts Dimension
CREATE TABLE IF NOT EXISTS dim_accounts (
    account_id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_number VARCHAR(16) NOT NULL UNIQUE,
    customer_id INTEGER NOT NULL,
    account_type VARCHAR(20) NOT NULL CHECK(account_type IN ('Savings', 'Current', 'Salary')),
    account_tier VARCHAR(15) NOT NULL CHECK(account_tier IN ('Classic', 'Gold', 'Platinum')),
    opening_date DATE NOT NULL,
    current_balance DECIMAL(14,2) NOT NULL CHECK(current_balance >= 0),
    minimum_balance_req DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    status VARCHAR(15) NOT NULL CHECK(status IN ('Active', 'At-Risk', 'Inactive', 'Dormant')),
    last_activity_date DATE NOT NULL,
    days_inactive INTEGER NOT NULL CHECK(days_inactive >= 0),
    inactivity_tier VARCHAR(20) NOT NULL,
    is_mab_compliant INTEGER NOT NULL CHECK(is_mab_compliant IN (0, 1)),
    is_hnw INTEGER NOT NULL CHECK(is_hnw IN (0, 1)),
    FOREIGN KEY (customer_id) REFERENCES dim_customers(customer_id) ON DELETE RESTRICT ON UPDATE CASCADE
);

-- 3. REFERENCE MASTER: Channels Dimension
CREATE TABLE IF NOT EXISTS dim_channels (
    channel_id INTEGER PRIMARY KEY,
    channel_code VARCHAR(10) NOT NULL UNIQUE,
    channel_name VARCHAR(30) NOT NULL,
    channel_type VARCHAR(15) NOT NULL CHECK(channel_type IN ('Digital', 'Self-Service', 'Branch')),
    switch_gateway VARCHAR(30) NOT NULL,
    daily_limit DECIMAL(12,2) NOT NULL DEFAULT 100000.00,
    sla_target_pct DECIMAL(5,2) NOT NULL DEFAULT 99.50,
    is_active INTEGER NOT NULL CHECK(is_active IN (0, 1))
);

-- 4. FACT TABLE: Transactions Ledger
CREATE TABLE IF NOT EXISTS fact_transactions (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    transaction_ref VARCHAR(24) NOT NULL UNIQUE,
    account_id INTEGER NOT NULL,
    channel_id INTEGER NOT NULL,
    transaction_timestamp DATETIME NOT NULL,
    transaction_date DATE NOT NULL,
    transaction_time TIME NOT NULL,
    hour_of_day INTEGER NOT NULL CHECK(hour_of_day BETWEEN 0 AND 23),
    day_of_week VARCHAR(10) NOT NULL CHECK(day_of_week IN ('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday')),
    is_weekend INTEGER NOT NULL CHECK(is_weekend IN (0, 1)),
    transaction_type VARCHAR(10) NOT NULL CHECK(transaction_type IN ('Credit', 'Debit')),
    category VARCHAR(30) NOT NULL,
    amount DECIMAL(12,2) NOT NULL CHECK(amount > 0),
    status VARCHAR(15) NOT NULL CHECK(status IN ('Success', 'Failed', 'Reversed')),
    error_code VARCHAR(20),
    balance_before DECIMAL(14,2) NOT NULL CHECK(balance_before >= 0),
    balance_after DECIMAL(14,2) NOT NULL CHECK(balance_after >= 0),
    FOREIGN KEY (account_id) REFERENCES dim_accounts(account_id) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (channel_id) REFERENCES dim_channels(channel_id) ON DELETE RESTRICT ON UPDATE CASCADE
);

-- 5. PERIODIC FACT TABLE: Monthly Account Snapshots
CREATE TABLE IF NOT EXISTS fact_monthly_snapshots (
    snapshot_id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER NOT NULL,
    year_month VARCHAR(7) NOT NULL CHECK(length(year_month) = 7),
    month_start_date DATE NOT NULL,
    month_end_date DATE NOT NULL,
    opening_balance DECIMAL(14,2) NOT NULL CHECK(opening_balance >= 0),
    closing_balance DECIMAL(14,2) NOT NULL CHECK(closing_balance >= 0),
    average_monthly_balance DECIMAL(14,2) NOT NULL CHECK(average_monthly_balance >= 0),
    total_credit_amount DECIMAL(14,2) NOT NULL DEFAULT 0.00,
    total_debit_amount DECIMAL(14,2) NOT NULL DEFAULT 0.00,
    credit_txn_count INTEGER NOT NULL DEFAULT 0,
    debit_txn_count INTEGER NOT NULL DEFAULT 0,
    net_flow_amount DECIMAL(14,2) NOT NULL,
    velocity_change_pct DECIMAL(6,2),
    status_at_month_end VARCHAR(15) NOT NULL CHECK(status_at_month_end IN ('Active', 'At-Risk', 'Inactive', 'Dormant')),
    FOREIGN KEY (account_id) REFERENCES dim_accounts(account_id) ON DELETE CASCADE ON UPDATE CASCADE
);

-- PERFORMANCE INDEXES
CREATE INDEX IF NOT EXISTS idx_txns_account_timestamp ON fact_transactions(account_id, transaction_timestamp);
CREATE INDEX IF NOT EXISTS idx_txns_date_type ON fact_transactions(transaction_date, transaction_type);
CREATE INDEX IF NOT EXISTS idx_txns_channel_status ON fact_transactions(channel_id, status);
CREATE INDEX IF NOT EXISTS idx_accounts_status ON dim_accounts(status, account_type);
CREATE INDEX IF NOT EXISTS idx_accounts_customer ON dim_accounts(customer_id);
CREATE INDEX IF NOT EXISTS idx_customers_tier ON dim_customers(branch_tier, occupation);
CREATE INDEX IF NOT EXISTS idx_snapshots_account_month ON fact_monthly_snapshots(account_id, year_month);

-- UNIFIED ANALYTICAL VIEW (42 COLUMNS)
CREATE VIEW IF NOT EXISTS vw_customer_account_activity_analysis AS
SELECT
    t.transaction_id,
    t.transaction_ref,
    t.transaction_timestamp,
    t.transaction_date,
    t.transaction_time,
    t.hour_of_day,
    t.day_of_week,
    t.is_weekend,
    t.transaction_type,
    t.category,
    t.amount,
    t.status AS transaction_status,
    t.error_code,
    t.balance_before,
    t.balance_after,
    c.channel_id,
    c.channel_name,
    c.channel_type,
    c.switch_gateway,
    a.account_id,
    a.account_number,
    a.account_type,
    a.account_tier,
    a.opening_date AS account_opening_date,
    a.current_balance,
    a.minimum_balance_req,
    a.status AS account_status,
    a.last_activity_date,
    a.days_inactive,
    a.inactivity_tier,
    a.is_mab_compliant,
    a.is_hnw,
    cust.customer_id,
    (cust.first_name || ' ' || cust.last_name) AS customer_name,
    cust.age,
    cust.age_group,
    cust.gender,
    cust.occupation,
    cust.annual_income,
    cust.branch_city,
    cust.branch_tier,
    CAST(ROUND((JULIANDAY('now') - JULIANDAY(cust.onboarding_date))/30.4375) AS INTEGER) AS customer_tenure_months
FROM fact_transactions t
JOIN dim_accounts a ON t.account_id = a.account_id
JOIN dim_customers cust ON a.customer_id = cust.customer_id
JOIN dim_channels c ON t.channel_id = c.channel_id;
