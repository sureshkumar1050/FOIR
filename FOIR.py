import streamlit as st

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Loan & Credit Card Eligibility",
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
    '<div class="title">💰 Financial Eligibility Calculator</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Loan FOIR Calculation & Credit Card Eligibility Screening'
    '</div>',
    unsafe_allow_html=True
)

st.divider()

# ============================================================
# SELECT CALCULATOR
# ============================================================

calculator_type = st.selectbox(
    "Select an Option",
    [
        "Loan FOIR Calculator",
        "Credit Card Eligibility",
        "Product Links"
    ]
)

st.divider()

# ============================================================
# SHARED INPUTS (ONLY FOR CALCULATORS, HIDDEN FOR PRODUCT LINKS)
# ============================================================

if calculator_type != "Product Links":

    # 1. CUSTOMER INCOME
    st.subheader("1️⃣ Customer Income")

    monthly_gross_income = st.number_input(
        "Monthly Gross Income (₹)",
        min_value=0.0,
        value=50000.0,
        step=1000.0,
        format="%.0f"
    )

    # 2. EXISTING EMIs
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
# 3. LOAN FOIR CALCULATOR
# ============================================================

if calculator_type == "Loan FOIR Calculator":

    st.subheader("3️⃣ Proposed Loan")

    proposed_emi = st.number_input(
        "Proposed New Loan EMI (₹)",
        min_value=0.0,
        value=10000.0,
        step=500.0,
        format="%.0f"
    )

    # FOIR CALCULATION

    total_obligation = existing_emi_total + proposed_emi

    if monthly_gross_income > 0:
        foir = (total_obligation / monthly_gross_income) * 100
        existing_foir = (
            existing_emi_total / monthly_gross_income
        ) * 100
    else:
        foir = 0
        existing_foir = 0

    remaining_income = monthly_gross_income - total_obligation

    # FOIR CLASSIFICATION

    if monthly_gross_income == 0:

        status = "⚪ Unable to Calculate"
        message = "Please enter a valid monthly gross income."
        css_class = "risk"

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
            "FOIR is within the illustrative acceptable range. "
            "Final approval depends on the lender's credit policy."
        )
        css_class = "acceptable"

    else:

        status = "🔴 High Risk / Strain Zone"
        message = (
            "A large portion of income is committed to debt obligations. "
            "The application may face stricter eligibility criteria."
        )
        css_class = "risk"

    # RESULTS

    st.divider()
    st.subheader("📊 Loan FOIR Result")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("FOIR", f"{foir:.2f}%")

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

    st.subheader("📋 FOIR Risk Classification")

    st.markdown("""
    | FOIR | Classification | Interpretation |
    |---|---|---|
    | Below 40% | 🟢 Low / Safe | Lower debt burden |
    | 40%–50% | 🟡 Acceptable | Moderate debt burden |
    | Above 50% | 🔴 High Risk | Higher debt burden |
    """)

    st.info(
        "💡 **Tip:** Alongside a healthy FOIR, most Indian banks require a **750+ CIBIL score** for instant loan approval. "
        "[Check your Free CIBIL Score here ↗](https://www.cibil.com/freecibilscore)"
    )

    # ADDITIONAL EMI CAPACITY

    st.subheader("💡 Additional EMI Capacity")

    if monthly_gross_income > 0:

        maximum_total_emi = monthly_gross_income * 0.50

        maximum_additional_emi = (
            maximum_total_emi - existing_emi_total
        )

        if maximum_additional_emi > 0:

            st.success(
                "Maximum additional EMI to remain within "
                f"50% FOIR: ₹{maximum_additional_emi:,.0f}"
            )

        else:

            st.error(
                "Existing obligations already meet or exceed "
                "the 50% FOIR threshold."
            )

        st.info(
            f"Existing EMI FOIR: **{existing_foir:.2f}%**"
        )

    else:
        st.warning("Enter income above zero to calculate EMI capacity.")

    # CALCULATION DETAILS

    with st.expander("🔎 View Calculation Details"):

        st.write(
            f"**Monthly Gross Income:** ₹{monthly_gross_income:,.2f}"
        )

        st.write(
            f"**Existing EMI:** ₹{existing_emi_total:,.2f}"
        )

        st.write(
            f"**Proposed EMI:** ₹{proposed_emi:,.2f}"
        )

        st.write(
            f"**Total Monthly Obligation:** ₹{total_obligation:,.2f}"
        )

        if monthly_gross_income > 0:
            st.write(
                f"**FOIR Formula:** "
                f"({total_obligation:,.2f} ÷ "
                f"{monthly_gross_income:,.2f}) × 100"
            )
            st.write(f"**Calculated FOIR:** {foir:.2f}%")
        else:
            st.write("FOIR cannot be calculated because income is zero.")

# ============================================================
# 4. CREDIT CARD ELIGIBILITY
# ============================================================

elif calculator_type == "Credit Card Eligibility":

    st.subheader("3️⃣ Credit Card Applicant Details")

    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input(
            "Applicant Age",
            min_value=18,
            max_value=100,
            value=30,
            step=1
        )

    with col2:
        credit_score = st.number_input(
            "Credit Score (300–900)",
            min_value=300,
            max_value=900,
            value=750,
            step=1
        )
        st.caption(
            "Don't know your score? [Check Free CIBIL Score ↗](https://www.cibil.com/freecibilscore)"
        )

    employment_type = st.selectbox(
        "Employment Type",
        [
            "Salaried",
            "Self-Employed"
        ]
    )

    repayment_history = st.selectbox(
        "Recent Credit Repayment History",
        [
            "No missed payments",
            "One or more recent missed payments",
            "Credit card / loan default",
            "No credit history"
        ]
    )

    # --------------------------------------------------------
    # SCREENING THRESHOLDS
    # --------------------------------------------------------

    st.subheader("4️⃣ Screening Criteria")

    st.caption(
        "These are editable example thresholds for preliminary "
        "screening, not universal bank requirements."
    )

    with st.expander("⚙️ Configure Screening Criteria"):

        minimum_income = st.number_input(
            "Illustrative Minimum Monthly Income (₹)",
            min_value=0,
            value=15000,
            step=1000
        )

        minimum_credit_score = st.number_input(
            "Illustrative Minimum Credit Score",
            min_value=300,
            max_value=900,
            value=700,
            step=10
        )

        maximum_foir = st.slider(
            "Maximum Existing EMI-to-Income Ratio (%)",
            min_value=20,
            max_value=80,
            value=50,
            step=5
        )

        minimum_age = st.number_input(
            "Illustrative Minimum Age",
            min_value=18,
            max_value=100,
            value=21,
            step=1
        )

        maximum_age = st.number_input(
            "Illustrative Maximum Age",
            min_value=18,
            max_value=100,
            value=60,
            step=1
        )

    # --------------------------------------------------------
    # CREDIT CARD ASSESSMENT
    # --------------------------------------------------------

    if monthly_gross_income > 0:

        existing_foir = (
            existing_emi_total / monthly_gross_income
        ) * 100

        remaining_income = (
            monthly_gross_income - existing_emi_total
        )

    else:

        existing_foir = 0
        remaining_income = 0

    checks = {
        "Monthly income meets the selected minimum":
            monthly_gross_income >= minimum_income
            and monthly_gross_income > 0,

        "Credit score meets the selected threshold":
            credit_score >= minimum_credit_score,

        "Age is within the selected range":
            minimum_age <= age <= maximum_age,

        "Existing EMI burden is within the selected limit":
            monthly_gross_income > 0
            and existing_foir <= maximum_foir,

        "Repayment history is satisfactory":
            repayment_history == "No missed payments"
    }

    # --------------------------------------------------------
    # RESULTS
    # --------------------------------------------------------

    st.divider()
    st.subheader("💳 Credit Card Eligibility Result")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Existing EMI Ratio",
            f"{existing_foir:.2f}%"
        )

    with col2:
        st.metric(
            "Monthly Income",
            f"₹{monthly_gross_income:,.0f}"
        )

    with col3:
        st.metric(
            "Income After EMIs",
            f"₹{remaining_income:,.0f}"
        )

    passed_checks = sum(checks.values())
    total_checks = len(checks)

    if monthly_gross_income <= 0:

        st.error(
            "Unable to assess eligibility. Please enter a valid income."
        )

    elif passed_checks == total_checks:

        st.markdown("""
        <div class="safe">
            <h3>🟢 Preliminary Screening: Meets Selected Criteria</h3>
            <p>The applicant meets all the screening conditions entered.
            This does not guarantee credit card approval.</p>
        </div>
        """, unsafe_allow_html=True)

    else:

        st.markdown("""
        <div class="risk">
            <h3>🔴 Preliminary Screening: Further Review Required</h3>
            <p>One or more selected screening conditions have not been met.
            The applicant may need further review.</p>
        </div>
        """, unsafe_allow_html=True)

    # INDIVIDUAL CHECKS

    st.subheader("📋 Eligibility Checklist")

    for description, passed in checks.items():

        if passed:
            st.success(f"✅ {description}")
        else:
            st.error(f"❌ {description}")
            if "Credit score" in description:
                st.link_button(
                    "📊 Verify Your Free CIBIL Score",
                    "https://www.cibil.com/freecibilscore"
                )

    st.write(
        f"**Screening conditions met:** "
        f"{passed_checks} out of {total_checks}"
    )

    # CREDIT CARD GUIDANCE

    with st.expander("🔎 View Credit Card Assessment Details"):

        st.write(f"**Applicant Age:** {age}")

        st.write(f"**Credit Score:** {credit_score}")

        st.write(f"**Employment Type:** {employment_type}")

        st.write(f"**Monthly Gross Income:** ₹{monthly_gross_income:,.2f}")

        st.write(f"**Existing Monthly EMIs:** ₹{existing_emi_total:,.2f}")

        st.write(f"**Existing EMI-to-Income Ratio:** {existing_foir:.2f}%")

        st.write(f"**Income Remaining After EMIs:** ₹{remaining_income:,.2f}")

        st.write(f"**Repayment History:** {repayment_history}")

        st.write(f"**Selected Minimum Income:** ₹{minimum_income:,.2f}")

        st.write(f"**Selected Minimum Credit Score:** {minimum_credit_score}")

        st.write(f"**Selected Maximum EMI Ratio:** {maximum_foir}%")

# ============================================================
# 5. PRODUCT LINKS
# ============================================================

elif calculator_type == "Product Links":

    st.subheader("🔗 Financial Product Links")

    product_category = st.selectbox(
        "Select Product Category",
        [
            "Credit Cards"
        ]
    )

    st.divider()

    # ========================================================
    # CREDIT CARDS
    # ========================================================

    if product_category == "Credit Cards":

        st.subheader("💳 Credit Card Products")

        st.caption(
            "Select a card below to view the available application/product link."
        )

        products = [
            {
                "name": "BOB Eterna Credit Card",
                "url": "https://bitli.in/dopaulw"
            },
            {
                "name": "IDFC Credit Card",
                "url": "https://bitli.in/p6aOmkW"
            },
            {
                "name": "Axis Neo RuPay Credit Card",
                "url": "https://bitli.in/pJwn1Ph"
            },
            {
                "name": "Scapia Co-branded Credit Card",
                "url": "https://bitli.in/5448inS"
            },
            {
                "name": "Uni GoldX Credit Card",
                "url": "https://bitli.in/gT5li6y"
            },
            {
                "name": "HDFC Pixel Play Credit Card",
                "url": "https://bitli.in/gj6asSH"
            },
            {
                "name": "Kotak League Platinum Credit Card",
                "url": "https://bitli.in/jqrDj8E"
            },
            {
                "name": "Axis Flipkart Credit Card",
                "url": "https://bitli.in/5gbo0dk"
            },
            {
                "name": "IndusInd Tiger Credit Card",
                "url": "https://bitli.in/9uPfKe3"
            },
            {
                "name": "SBI Cashback Credit Card",
                "url": "https://bitli.in/kfeV1sZ"
            },
            {
                "name": "SBI Flipkart Credit Card",
                "url": "https://bitli.in/WLK8XQP"
            },
            {
                "name": "RBL Bank Shoprite Credit Card",
                "url": "https://bitli.in/gho4vkd"
            }
        ]

        for product in products:

            with st.container(border=True):

                st.markdown(
                    f"### {product['name']}"
                )

                st.link_button(
                    "🔗 Apply / View Card",
                    product["url"],
                    use_container_width=True
                )

# ============================================================
# DISCLAIMER
# ============================================================

st.divider()

st.warning(
    "⚠️ IMPORTANT DISCLAIMER: This application is a preliminary "
    "financial screening tool for educational and indicative purposes. "
    "FOIR, minimum income, age and credit score requirements vary "
    "between banks, NBFCs, card issuers and financial products. "
    "Actual credit card or loan approval depends on the issuer's "
    "underwriting policy, verified income, credit bureau report, "
    "repayment history, existing liabilities and other factors. "
    "This application does not guarantee approval or a credit limit."
)

st.caption(
    "Loan FOIR = Total Monthly Debt Obligations ÷ Monthly Gross Income × 100"
)

st.caption(
    "Credit Card Screening = Indicative assessment using selected "
    "income, credit score, age, repayment history and EMI criteria."
)
