import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pickle

# Load model, threshold, and feature names
with open('model/model.pkl', 'rb') as f:
    model = pickle.load(f)
with open('model/threshold.pkl', 'rb') as f:
    threshold = pickle.load(f)
with open('model/feature_names.pkl', 'rb') as f:
    feature_names = pickle.load(f)

# Load data
df = pd.read_csv('data/WA_Fn-UseC_-HR-Employee-Attrition.csv')

# Page config
st.set_page_config(page_title="Employee Attrition Dashboard",
                   page_icon="📊", layout="wide")

st.title("📊 Employee Attrition Prediction Dashboard")
st.markdown("**Machine Learning-Based HR Analytics Tool**")
st.markdown("---")

# Sidebar navigation
page = st.sidebar.selectbox("Navigate", [
    "Overview",
    "Feature Analysis",
    "Model Performance",
    "Prediction Tool"
])

# ── PAGE 1: OVERVIEW ──────────────────────────────────────────────────────────
if page == "Overview":
    st.header("Overview")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Employees", "1,470")
    col2.metric("Attrition Rate", "16.1%")
    col3.metric("Employees at Risk", "237")

    st.subheader("Attrition by Department")
    dept_attr = df.groupby('Department')['Attrition'].apply(
        lambda x: (x == 'Yes').sum() / len(x) * 100).sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(8, 4))
    dept_attr.plot(kind='bar', ax=ax, color='salmon', edgecolor='black')
    ax.set_ylabel('Attrition Rate (%)')
    ax.set_title('Attrition Rate by Department')
    ax.tick_params(axis='x', rotation=0)
    plt.tight_layout()
    st.pyplot(fig)

    st.subheader("Attrition by OverTime")
    ot_attr = df.groupby('OverTime')['Attrition'].apply(
        lambda x: (x == 'Yes').sum() / len(x) * 100)
    fig2, ax2 = plt.subplots(figsize=(5, 4))
    ot_attr.plot(kind='bar', ax=ax2, color='steelblue', edgecolor='black')
    ax2.set_ylabel('Attrition Rate (%)')
    ax2.set_title('Attrition Rate by OverTime')
    ax2.tick_params(axis='x', rotation=0)
    plt.tight_layout()
    st.pyplot(fig2)

    st.subheader("Hypothesis: Work-Life Balance vs Job Satisfaction")
    df['SatisfactionGroup'] = df['JobSatisfaction'].apply(
        lambda x: 'High Satisfaction' if x >= 3 else 'Low Satisfaction')
    df['WLBGroup'] = df['WorkLifeBalance'].apply(
        lambda x: 'Low WLB' if x <= 2 else 'High WLB')
    pivot = df.pivot_table(values='Attrition', index='SatisfactionGroup',
                           columns='WLBGroup',
                           aggfunc=lambda x: (x == 'Yes').sum() / len(x) * 100)
    fig3, ax3 = plt.subplots(figsize=(8, 4))
    pivot.plot(kind='bar', ax=ax3, color=['salmon', 'steelblue'], edgecolor='black')
    ax3.set_ylabel('Attrition Rate (%)')
    ax3.set_title('Attrition Rate by Job Satisfaction and Work-Life Balance')
    ax3.tick_params(axis='x', rotation=0)
    ax3.legend(title='Work-Life Balance')
    plt.tight_layout()
    st.pyplot(fig3)
    st.info("**Finding:** Employees with High Satisfaction but Low WLB (18.5%) leave at nearly the same rate as Low Satisfaction employees with High WLB (19.0%), suggesting work-life balance is an independent attrition driver.")

# ── PAGE 2: FEATURE ANALYSIS ──────────────────────────────────────────────────
elif page == "Feature Analysis":
    st.header("Feature Analysis")

    importances = model.feature_importances_
    feat_imp = pd.DataFrame({
        'Feature': feature_names,
        'Importance': importances
    }).sort_values('Importance', ascending=False).head(20)

    st.subheader("Top 20 Feature Importances")
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.barplot(data=feat_imp, x='Importance', y='Feature',
                hue='Feature', palette='coolwarm', legend=False, ax=ax)
    ax.set_title('Top 20 Feature Importances - Random Forest')
    ax.set_xlabel('Importance Score')
    plt.tight_layout()
    st.pyplot(fig)

    st.subheader("Key Findings")
    st.markdown("""
    - **MonthlyIncome** is the strongest predictor of attrition
    - **Age** and **TotalWorkingYears** rank #2 and #3
    - **OverTime** is a strong predictor (combined Yes/No)
    - **WorkLifeBalance** ranks #21 and **JobSatisfaction** ranks #18
    - Both satisfaction variables have similar importance scores, supporting the hypothesis
    """)

# ── PAGE 3: MODEL PERFORMANCE ─────────────────────────────────────────────────
elif page == "Model Performance":
    st.header("Model Performance")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Precision", "0.47")
    col2.metric("Recall", "0.60")
    col3.metric("F1 Score", "0.52")
    col4.metric("ROC-AUC", "0.79")

    st.subheader("Confusion Matrix")
    st.image('screenshots/confusion_matrix.png')

    st.subheader("ROC Curve")
    st.image('screenshots/roc_curve.png')

    st.subheader("Slice Performance Summary")
    slice_data = {
        'Group': ['Sales Dept', 'R&D Dept', 'Male', 'Female',
                  'Single', 'Married', 'Sales Executive', 'Research Scientist'],
        'F1 Score': [0.67, 0.44, 0.58, 0.44, 0.64, 0.43, 0.78, 0.54]
    }
    st.dataframe(pd.DataFrame(slice_data))

# ── PAGE 4: PREDICTION TOOL ───────────────────────────────────────────────────
elif page == "Prediction Tool":
    st.header("Attrition Risk Prediction Tool")
    st.markdown("Enter employee details to predict attrition risk.")

    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.slider("Age", 18, 60, 35)
        monthly_income = st.number_input("Monthly Income ($)", 1000, 20000, 5000)
        total_working_years = st.slider("Total Working Years", 0, 40, 10)
        years_at_company = st.slider("Years at Company", 0, 40, 5)
        distance_from_home = st.slider("Distance from Home (miles)", 1, 30, 10)

    with col2:
        overtime = st.selectbox("OverTime", ["Yes", "No"])
        job_satisfaction = st.slider("Job Satisfaction (1-4)", 1, 4, 3)
        work_life_balance = st.slider("Work-Life Balance (1-4)", 1, 4, 3)
        environment_satisfaction = st.slider("Environment Satisfaction (1-4)", 1, 4, 3)
        num_companies = st.slider("Number of Companies Worked", 0, 9, 2)

    with col3:
        department = st.selectbox("Department",
                                   ["Sales", "Research & Development", "Human Resources"])
        job_role = st.selectbox("Job Role",
                                 ["Sales Executive", "Research Scientist",
                                  "Laboratory Technician", "Manufacturing Director",
                                  "Healthcare Representative", "Sales Representative",
                                  "Research Director", "Human Resources", "Manager"])
        marital_status = st.selectbox("Marital Status", ["Single", "Married", "Divorced"])
        business_travel = st.selectbox("Business Travel",
                                        ["Travel_Rarely", "Travel_Frequently", "Non-Travel"])
        stock_option = st.slider("Stock Option Level (0-3)", 0, 3, 1)

    if st.button("Predict Attrition Risk", type="primary"):
        # Build input row matching training features
        input_data = pd.DataFrame(0, index=[0], columns=feature_names)

        # Set numerical features
        num_map = {
            'Age': age, 'MonthlyIncome': monthly_income,
            'TotalWorkingYears': total_working_years,
            'YearsAtCompany': years_at_company,
            'DistanceFromHome': distance_from_home,
            'JobSatisfaction': job_satisfaction,
            'WorkLifeBalance': work_life_balance,
            'EnvironmentSatisfaction': environment_satisfaction,
            'NumCompaniesWorked': num_companies,
            'StockOptionLevel': stock_option,
        }
        for feat, val in num_map.items():
            if feat in input_data.columns:
                input_data[feat] = val

        # Set categorical dummies
        cat_map = {
            f'OverTime_{overtime}': 1,
            f'Department_{department}': 1,
            f'JobRole_{job_role}': 1,
            f'MaritalStatus_{marital_status}': 1,
            f'BusinessTravel_{business_travel}': 1,
        }
        for feat, val in cat_map.items():
            if feat in input_data.columns:
                input_data[feat] = val

        prob = model.predict_proba(input_data)[0][1]
        risk_pct = round(prob * 100, 1)

        st.markdown("---")
        if prob >= threshold:
            st.error(f"⚠️ **High Attrition Risk: {risk_pct}%**")
            st.markdown("This employee is predicted to be **at risk of leaving**.")
        else:
            st.success(f"✅ **Low Attrition Risk: {risk_pct}%**")
            st.markdown("This employee is predicted to **stay**.")

        st.progress(int(risk_pct))
        st.caption(f"Threshold: {round(threshold*100)}% | Model: Random Forest")