import streamlit as st
import pandas as pd
import joblib

# Set up the page configuration
st.set_page_config(page_title="AI Credit Risk Assessor", page_icon="🏦", layout="centered")

# Load the lightweight XGBoost model
@st.cache_resource
def load_model():
    return joblib.load('lightweight_bank_model.pkl')

model = load_model()

# Header Section
st.title("🏦 AI Credit Risk Assessor")
st.markdown("""
Enter the financial details of the applicant below. The AI will instantly evaluate their profile 
and predict the probability of loan default using a custom XGBoost classification model.
""")

# Input Form
with st.form("applicant_data"):
    st.header("Applicant Financial Profile")
    
    col1, col2 = st.columns(2)
    with col1:
        person_age = st.number_input("Age", min_value=18, max_value=100, value=25)
        person_income = st.number_input("Annual Income ($)", min_value=0, max_value=5000000, value=50000)
        person_emp_length = st.number_input("Employment Length (Years)", min_value=0.0, max_value=50.0, value=2.0)
        loan_amnt = st.number_input("Loan Amount Requested ($)", min_value=500, max_value=50000, value=10000)
        
    with col2:
        loan_int_rate = st.number_input("Interest Rate (%)", min_value=1.0, max_value=30.0, value=10.5)
        cb_person_cred_hist_length = st.number_input("Credit History Length (Years)", min_value=0, max_value=30, value=3)
        loan_percent_income = loan_amnt / person_income if person_income > 0 else 0.0
        st.info(f"Calculated Debt-to-Income Ratio: {loan_percent_income:.2f}")

    st.header("Categorical Details")
    col3, col4 = st.columns(2)
    with col3:
        person_home_ownership = st.selectbox("Home Ownership", ["RENT", "OWN", "MORTGAGE", "OTHER"])
        loan_intent = st.selectbox("Loan Purpose", ["PERSONAL", "EDUCATION", "MEDICAL", "VENTURE", "HOMEIMPROVEMENT", "DEBTCONSOLIDATION"])
    with col4:
        loan_grade = st.selectbox("Assigned Loan Grade", ["A", "B", "C", "D", "E", "F", "G"])
        cb_person_default_on_file = st.selectbox("Historical Default on File?", ["Y", "N"])

    submit_button = st.form_submit_button(label="Evaluate Risk")

# The Prediction Logic
if submit_button:
    # 1. Package the inputs into a dictionary
    input_dict = {
        'person_age': [person_age],
        'person_income': [person_income],
        'person_home_ownership': [person_home_ownership],
        'person_emp_length': [person_emp_length],
        'loan_intent': [loan_intent],
        'loan_grade': [loan_grade],
        'loan_amnt': [loan_amnt],
        'loan_int_rate': [loan_int_rate],
        'loan_percent_income': [loan_percent_income],
        'cb_person_default_on_file': [cb_person_default_on_file],
        'cb_person_cred_hist_length': [cb_person_cred_hist_length]
    }
    
    # 2. Convert to DataFrame
    input_df = pd.DataFrame(input_dict)
    
    # 3. Match the data types exactly to what XGBoost expects
    for col in input_df.select_dtypes(include=['object']).columns:
        input_df[col] = input_df[col].astype('category')
        
    # 4. Make the Prediction
    prediction = model.predict(input_df)[0]
    probability = model.predict_proba(input_df)[0][1] * 100

    # 5. Display the Results
    st.divider()
    if prediction == 1:
        st.error(f"🚨 HIGH RISK: The AI predicts this applicant will DEFAULT.")
        st.write(f"**Probability of Default:** {probability:.2f}%")
    else:
        st.success(f"✅ LOW RISK: The AI predicts this applicant will PAY OFF the loan.")
        st.write(f"**Probability of Default:** {probability:.2f}%")

# Portfolio Footer
st.sidebar.markdown("---")
st.sidebar.markdown("**Project Developed By:**")
st.sidebar.markdown("Adarsh Kauhik")
st.sidebar.markdown("Roll No: 24155301")
st.sidebar.markdown("B.Tech CSE (AI/ML)")
st.sidebar.markdown("KIIT University")