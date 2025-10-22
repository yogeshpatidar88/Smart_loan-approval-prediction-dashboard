import streamlit as st
import pandas as pd
import pickle as pk
import plotly.express as px
import plotly.graph_objects as go

# ---------------- Load model and scaler ----------------
model = pk.load(open('model.pkl','rb'))
scaler = pk.load(open('scaler.pkl','rb'))

# ---------------- Page Configuration ----------------
st.set_page_config(page_title="Loan Prediction App", layout="wide")

# ---------------- Custom Dark Theme Styling ----------------
st.markdown(
    """
    <style>
    body, .stApp, .main, .block-container { 
        background-color: #000000 !important; 
        color: #ffffff !important; 
    }
    [data-testid='stSidebar'] { 
        background-color: #0b0b0b !important; 
        color: #e6e6e6 !important;
    }
    h1, h2, h3, h4, h5, h6 { color: #ffffff !important; }
    .stMetric label, .stMetric div { color: #ffffff !important; }
    </style>
    """, unsafe_allow_html=True
)

# ---------------- App Header ----------------
st.title("🏦 Loan Prediction Dashboard")

# ---------------- Sidebar for Inputs ----------------
st.sidebar.header("Applicant Information")

# Input widgets
no_of_dep = st.sidebar.slider('Number of Dependents', 0, 5)
grad = st.sidebar.selectbox('Education', ['Graduated', 'Not Graduated'])
self_emp = st.sidebar.selectbox('Self Employed?', ['Yes', 'No'])

annual_income = st.sidebar.slider('Annual Income (₹)', 0, 5000000, 500000, step=10000)
loan_amount = st.sidebar.slider('Loan Amount (₹)', 0, 2000000, 200000, step=5000)
loan_dur = st.sidebar.slider('Loan Duration (Years)', 1, 30)
cibil = st.sidebar.slider('CIBIL Score', 0, 1000)
assets = st.sidebar.slider('Assets Value (₹)', 0, 5000000, 100000, step=10000)

# Encode categorical variables
grad_s = 0 if grad == 'Graduated' else 1
emp_s = 0 if self_emp == 'No' else 1

# ---------------- Display Key Metrics ----------------
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Selected Income (₹)", value=f"{annual_income:,}")
with col2:
    st.metric(label="Requested Loan (₹)", value=f"{loan_amount:,}")
with col3:
    st.metric(label="Assets (₹)", value=f"{assets:,}")

# ---------------- Prediction Section ----------------
predict_button = st.button("🔮 Predict Loan Approval")

if predict_button:
    # Prepare data
    pred_data = pd.DataFrame([[no_of_dep, grad_s, emp_s, annual_income, loan_amount, loan_dur, cibil, assets]],
                             columns=['no_of_dependents','education','self_employed','income_annum',
                                      'loan_amount','loan_term','cibil_score','Assets'])
    
    # Scale and predict
    pred_scaled = scaler.transform(pred_data)
    predict = model.predict(pred_scaled)
    
    # If model supports probability
    if hasattr(model, "predict_proba"):
        prob = model.predict_proba(pred_scaled)[0]
        approval_prob = prob[1] if len(prob) > 1 else prob[0]
    else:
        approval_prob = None

    # ---------------- Display Prediction ----------------
    if predict[0] == 1:
        st.success("✅ Loan Approved")
        st.markdown("Your financial profile looks strong and meets eligibility criteria.")
    else:
        st.error("❌ Loan Rejected")
        st.markdown("Your current profile might not meet loan eligibility thresholds.")

    # ---------------- Probability Gauge ----------------
    if approval_prob is not None:
        st.subheader("Approval Probability")
        fig_prob = go.Figure(go.Indicator(
            mode="gauge+number",
            value=round(approval_prob * 100, 2),
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': '#1f77b4'},
                'steps': [
                    {'range': [0, 40], 'color': 'red'},
                    {'range': [40, 70], 'color': 'orange'},
                    {'range': [70, 100], 'color': 'green'}
                ]
            }
        ))
        st.plotly_chart(fig_prob, use_container_width=True)

    # ---------------- Financial Overview ----------------
    st.markdown("---")
    st.subheader("💰 Financial Overview")
    finance_data = pd.DataFrame({
        'Parameter': ['Annual Income', 'Loan Amount', 'Loan Duration (Yrs)', 'CIBIL Score', 'Assets'],
        'Value': [annual_income, loan_amount, loan_dur, cibil, assets]
    })
    fig1 = px.bar(finance_data, x='Parameter', y='Value', color='Value',
                 text='Value', color_continuous_scale='Viridis', height=400)
    st.plotly_chart(fig1, use_container_width=True)

    # ---------------- Dependents Pie Chart ----------------
    st.markdown("---")
    st.subheader("👨‍👩‍👧 Dependents Overview")
    pie_data = pd.DataFrame({
        'Category': ['Dependents', 'Remaining (up to 5)'],
        'Count': [no_of_dep, max(0, 5 - no_of_dep)]
    })
    fig2 = px.pie(pie_data, names='Category', values='Count', hole=0.4,
                  color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig2, use_container_width=True)

    # ---------------- Loan Term Impact on EMI ----------------
    st.markdown("---")
    st.subheader("📈 Loan Term Impact on EMI")

    interest_rate = 0.10  # 10% annual interest (example)
    months = list(range(1, loan_dur * 12 + 1))
    emi_values = []

    for m in months:
        r = interest_rate / 12
        emi = (loan_amount * r * (1 + r) ** m) / ((1 + r) ** m - 1)
        emi_values.append(round(emi, 2))

    emi_df = pd.DataFrame({'Month': months, 'EMI (₹)': emi_values})
    fig3 = px.line(emi_df, x='Month', y='EMI (₹)', title='EMI vs Loan Duration (Months)',
                   color_discrete_sequence=['#00CC96'])
    st.plotly_chart(fig3, use_container_width=True)

    # ---------------- CIBIL Score Visualization ----------------
    st.markdown("---")
    st.subheader("💳 CIBIL Score Status")

    if cibil < 300:
        score_color = "red"
        score_label = "Very Poor"
    elif cibil < 600:
        score_color = "orange"
        score_label = "Poor"
    elif cibil < 750:
        score_color = "yellow"
        score_label = "Good"
    else:
        score_color = "green"
        score_label = "Excellent"

    fig4 = go.Figure(go.Indicator(
        mode="gauge+number",
        value=cibil,
        domain={'x':[0,1],'y':[0,1]},
        title={'text': f"CIBIL Score: {score_label}"},
        gauge={
            'axis': {'range':[0, 1000]},
            'bar': {'color': score_color},
            'steps': [
                {'range':[0,300],'color':'red'},
                {'range':[300,600],'color':'orange'},
                {'range':[600,750],'color':'yellow'},
                {'range':[750,1000],'color':'green'}
            ]
        }
    ))
    st.plotly_chart(fig4, use_container_width=True)

    # ---------------- Loan Improvement Suggestions ----------------
    st.markdown("---")
    st.subheader("💡 Suggestions to Improve Loan Approval Chances")

    st.markdown("""
    - **Improve your CIBIL score** → Keep it above 700 by paying dues on time.  
    - **Increase declared income** → Add co-applicant or secondary income proof.  
    - **Lower loan amount or extend tenure** → Reduces EMI and improves eligibility.  
    - **Maintain low existing debts** → Keep debt-to-income ratio below 30%.  
    - **Provide collateral or fixed assets** → Boosts lender confidence.  
    """)

    st.caption("Tip: Adjust the sliders in the sidebar to see how different inputs affect approval and EMI.")

