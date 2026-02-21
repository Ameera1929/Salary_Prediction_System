# -*- coding: utf-8 -*-
import streamlit as st
import pickle
import pandas as pd
import re

st.set_page_config(page_title="Salary Prediction System", layout="wide")

# -------- LOAD FILES --------
model = pickle.load(open("Final_model_SPS.pkl", "rb"))
df = pd.read_csv("Salary_prediction.csv")
roles = sorted(df["Role"].unique())

#--------SESSION STATE --------

if "show_result" not in st.session_state:
    st.session_state.show_result = False

if "years_input" not in st.session_state:
    st.session_state.years_input = 0.0

if "role_input" not in st.session_state:
    st.session_state.role_input = roles[0]

if "expected_salary_input" not in st.session_state:
    st.session_state.expected_salary_input = ""
    
if "last_years" not in st.session_state:
    st.session_state.last_years = 0.0

if "last_expected" not in st.session_state:
    st.session_state.last_expected = ""    

# -------- CSS --------
st.markdown("""
<style>
.stApp {background-color:#272757;}

/* Title */
.title {text-align:center; font-size:48px; font-weight:900; color:white; margin-bottom:30px;}

/* Input boxes */
div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div {
    width:100% !important;
    background-color:#ffffff !important;
    border-radius:8px;
    margin-bottom:10px;
}

/* 🔥 Make alert text white (keep emoji same) */
div[data-testid="stAlert"] p {
    color: white !important;
}

/* Icon color white */
div[data-testid="stAlert"] svg {
    fill: white !important;
}


/* Hide dropdown arrow completely */
div[data-baseweb="select"] svg {
    display: none !important;
}

div[data-baseweb="input"] input {
    color:black !important;
    font-weight:bold;
    height:35px !important;
    font-size:16px !important;
    padding:5px 10px !important;
}

/* Labels text white */
.stTextInput label, .stNumberInput label, .stSelectbox label {
    color: white !important;
    font-weight: bold;
}

/* Button */
.stButton>button {
    background-color:#8686AC;
    color:white;
    font-weight:bold;
    border-radius:8px;
    width:40%;
    height:40px;
    margin-top:10px;
}

/* Predicted salary box */
.salary-box {
    background-color:#8686AC;
    color:white;
    font-weight:bold;
    font-size:18px;
    padding:12px;
    border-radius:10px;
    text-align:center;
    margin-top:20px;
}

.salary-box {
    background-color:#8686AC;
    color:white;
    font-weight:bold;
    font-size:18px;
    padding:12px;
    border-radius:10px;
    text-align:center;
    margin-top:25px;
    margin-bottom:15px;   /* 👈 ADD THIS */
}



/* Sidebar news */
section[data-testid="stSidebar"] {background-color: #8686AC;}
section[data-testid="stSidebar"] * {color: white !important;}
.sidebar-news ul {padding-left:15px; margin-top:5px; margin-bottom:5px;}
.sidebar-news li {margin-bottom:5px; font-size:14px;}

/* ---------------- DARK MODE ---------------- */
@media (prefers-color-scheme: dark) {

    .stApp {
        background-color:#1c1c3a !important;
    }

    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div {
        background-color:#2a2a55 !important;
     
    }

    div[data-baseweb="input"] input {
        background-color:#2a2a55 !important;
        color:#ffffff !important;
    }

    .stTextInput label, 
    .stNumberInput label, 
    .stSelectbox label {
        color:#e0e0ff !important;
    }

    .salary-box {
        background-color:#6f6fb2;
    }

    section[data-testid="stSidebar"] {
        background-color:#2a2a55 !important;
    }

}

/* ---------------- RESPONSIVE ---------------- */
@media (max-width:768px) {

    .title {
        font-size:30px;
    }

    .stButton>button {
        width:100% !important;
    }

}

</style>
""", unsafe_allow_html=True)

# -------- SIDEBAR --------
st.sidebar.title("📰 Updated News")
st.sidebar.markdown("""
🔹 **IT Industry Update**  
Average salary hike for 2026 expected around **8–10%**.

🔹 **AI & Data Science**  
AI roles demand increased by **35%** in the last year.

🔹 **Freshers Market**  
Entry-level packages now start from **₹4–6 LPA**.

🔹 **Senior Professionals**  
10+ years experience roles crossing **₹30 LPA** in top firms.

🔹 **Remote Jobs**  
Remote-friendly salaries increased by **12% globally**.
""")

st.sidebar.markdown("---")
st.sidebar.markdown("📌 *News updates are refreshed periodically*")

# -------- PAGE TITLE --------
st.markdown('<div class="title">💼 SALARY PREDICTION SYSTEM 💸</div>', unsafe_allow_html=True)



# -------- CENTERED NARROW INPUT SECTION --------
col1, col2, col3 = st.columns([1, 2, 1])

with col2:

    role = st.selectbox(
        "👔 Select Your Designation",
        roles,
        key="role_input"
    )

    years = st.number_input(
        "📊 Enter Your Years of Experience",
        min_value=0.0,
        max_value=50.0,
        step=0.5,
        format="%.1f",
        key="years_input"
    )

    expected_salary = st.text_input(
        "💰 Enter Your Expected Annual Salary (Optional)",
        key="expected_salary_input",
        disabled=st.session_state.show_result
    )
    
    valid_expected = True
    if expected_salary.strip() != "":
        if not re.fullmatch(r'\d+(\.\d{1,2})?', expected_salary.strip()):
            st.error("🚫 Please enter numbers only (no letters or special characters)")
            valid_expected = False

    button_label = "🔄 Reset" if st.session_state.show_result else "🔮 Predict Salary"

    if st.button(button_label, use_container_width=True):
        if not st.session_state.show_result:
            if valid_expected:
                st.session_state.show_result = True
                st.rerun()
        else:
            st.session_state.show_result = False
            for key in ["years_input", "role_input", "expected_salary_input"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

# -------- AUTO DISAPPEAR --------
if (
    years != st.session_state.last_years or
    expected_salary != st.session_state.last_expected
):
    st.session_state.show_result = False

st.session_state.last_years = years
st.session_state.last_expected = expected_salary
        


# -------- PREDICTION --------
if st.session_state.show_result:
    try:
        annual_salary = model.predict([[years]]).item()
        

        st.markdown(f'<div class="salary-box">💰 Predicted Annual Salary: ₹ {annual_salary:,.0f}</div>', unsafe_allow_html=True)

        if annual_salary < 500000:
            st.info("🟢 Entry Level Salary")
        elif annual_salary < 1500000:
            st.success("🔵 Mid Level Salary")
        else:
            st.warning("🟣 Senior Level Salary")

        if expected_salary.strip() != "":
            expected_value = float(expected_salary)
            lower = annual_salary * 0.9
            upper = annual_salary * 1.1

            if expected_value < lower:
                st.warning("⚠️ Your expectation is lower than predicted range")
            elif expected_value > upper:
                st.error("❌ Your expectation exceeds predicted range")
            else:
                st.success("✅ Your expectation is within acceptable range")
    except Exception as e:
        st.error(f"🚨 Prediction failed: {e}")
                    