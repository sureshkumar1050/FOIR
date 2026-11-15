import streamlit as st

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="FOIR Calculator",
    page_icon="💰",
    layout="centered"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.main {
    background-color: #f7f9fc;
}

.title {
    text-align: center;
    font-size: 34px;
    font-weight: 700;
}

.subtitle {
    text-align: center;
    color: #666;
    margin-bottom: 30px;
}

.result-box {
    padding: 20px;
    border-radius: 12px;
    background-color: white;
    border: 1px solid #ddd;
    margin-bottom: 15px;
}

.safe {
    padding: 15px;
    border-radius: 10px;
    background-color: #e8f5e9;
    border-left: 6px solid #2e7d32;
}

.acceptable {
    padding: 15px;
    border-radius: 10px;
    background-color: #fff8e1;
    border-left: 6px solid #f9a825;
}

.risk {
    padding: 15px;
    border-radius: 10px;
    background-color: #ffebee;
    border-left: 6px solid #c62828;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="title">💰 FOIR Calculator</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Financial Obligation to Income Ratio – Preliminary Loan Screening'
    '</div>',
    unsafe_allow_html=True
)

st.divider()

# ============================================================
# 1. CUSTOMER INCOME
# ============================================================

st.subheader("1️⃣ Customer Income")

monthly_gross_income = st.number_input(
    "Monthly Gross Income (₹)",
    min_value=0.0,
    value=50000.0,
    step=1000.0,
    format="%.0f"
)

# ============================================================
# 2. EXISTING EMIs
# ============================================================

st.subheader("2️⃣ Existing Monthly Obligations")

num_emis = st.number_input(
    "Number of Existing EMIs",
    min_value=0,
    max_value=20,
    value=2,
    step=1
)

existing_emi_total = 0.0

for i in range(int(num_emis)):

    emi = st.number_input(
        f"Existing EMI {i + 1} (₹)",
        min_value=0.0,
        value=5000.0,
        step=500.0,
        format="%.0f",
        key=f"existing_emi_{i}"
    )

    existing_emi_total += emi

# ============================================================
# 3. PROPOSED LOAN
# ============================================================

st.subheader("3️⃣ Proposed Loan")

proposed_emi = st.number_input(
    "Proposed New Loan EMI (₹)",
    min_value=0.0,
    value=10000.0,
    step=500.0,
    format="%.0f"
)

# ============================================================
# 4. FOIR CALCULATION
# ============================================================

total_obligation = existing_emi_total + proposed_emi

if monthly_gross_income > 0:

    foir = (
        total_obligation / monthly_gross_income
    ) * 100

else:

    foir = 0

remaining_income = monthly_gross_income - total_obligation

# ============================================================
# FOIR CLASSIFICATION
# ============================================================

if monthly_gross_income == 0:

    status = "⚪ Unable to Calculate"
    message = "Please enter a valid monthly gross income."
    css_class = "result-box"

elif foir < 40:

    status = "🟢 Low / Safe Zone"
    message = (
        "Strong repayment capacity based on FOIR. "
        "The customer's debt obligation is relatively low."
    )
    css_class = "safe"

elif foir <= 50:

    status = "🟡 Standard / Acceptable Range"
    message = (
        "FOIR is within the commonly used acceptable range. "
        "Final approval depends on the lender's credit policy and other factors."
    )
    css_class = "acceptable"

else:

    status = "🔴 High Risk / Strain Zone"
    message = (
        "A large portion of income is committed to debt obligations. "
        "The application may face stricter eligibility criteria or a lower sanctioned amount."
    )
    css_class = "risk"

# ============================================================
# RESULTS
# ============================================================

st.subheader("📊 FOIR Result")

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "FOIR",
        f"{foir:.2f}%"
    )

with col2:

    st.metric(
        "Total Obligations",
        f"₹{total_obligation:,.0f}"
    )

with col3:

    st.metric(
        "Remaining Gross Income",
        f"₹{remaining_income:,.0f}"
    )

st.markdown(
    f"""
    <div class="{css_class}">
        <h3>{status}</h3>
        <p>{message}</p>
    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# FOIR RANGE GUIDE
# ============================================================

st.subheader("📋 FOIR Risk Classification")

st.markdown("""
| FOIR | Classification | Interpretation |
|---|---|---|
| **Below 40%** | 🟢 Low / Safe | Strong repayment capacity |
| **40% – 50%** | 🟡 Standard / Acceptable | Generally acceptable range |
| **Above 50%** | 🔴 High Risk / Strain | Higher debt burden |
""")

# ============================================================
# ADDITIONAL EMI CAPACITY
# ============================================================

st.subheader("💡 Additional EMI Capacity")

# 50% is used as the upper boundary
maximum_total_emi = monthly_gross_income * 0.50

maximum_additional_emi = (
    maximum_total_emi - existing_emi_total
)

if maximum_additional_emi > 0:

    st.success(
        f"Maximum additional EMI to remain within 50% FOIR: "
        f"₹{maximum_additional_emi:,.0f}"
    )

else:

    st.error(
        "The customer's existing obligations already exceed "
        "the 50% FOIR threshold."
    )

# ============================================================
# EXISTING EMI FOIR
# ============================================================

if monthly_gross_income > 0:

    existing_foir = (
        existing_emi_total / monthly_gross_income
    ) * 100

    st.info(
        f"Existing EMI FOIR: **{existing_foir:.2f}%**"
    )

# ============================================================
# CALCULATION DETAILS
# ============================================================

with st.expander("🔎 View Calculation Details"):

    st.write(
        f"**Monthly Gross Income:** "
        f"₹{monthly_gross_income:,.2f}"
    )

    st.write(
        f"**Existing EMI:** "
        f"₹{existing_emi_total:,.2f}"
    )

    st.write(
        f"**Proposed EMI:** "
        f"₹{proposed_emi:,.2f}"
    )

    st.write(
        f"**Total Monthly Obligation:** "
        f"₹{total_obligation:,.2f}"
    )

    st.write(
        f"**FOIR:** "
        f"({total_obligation:,.2f} ÷ "
        f"{monthly_gross_income:,.2f}) × 100"
    )

    st.write(
        f"**Calculated FOIR:** "
        f"{foir:.2f}%"
    )

# ============================================================
# IMPORTANT DISCLAIMER
# ============================================================

st.divider()

st.warning(
    "⚠️ This is a preliminary FOIR assessment tool. "
    "FOIR thresholds vary between banks/NBFCs and loan products. "
    "Actual approval depends on the lender's credit policy, "
    "credit history, income verification, employment/business profile, "
    "existing liabilities and other underwriting criteria."
)

st.caption(
    "FOIR = Total Monthly Debt Obligations ÷ Monthly Gross Income × 100"
)