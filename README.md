# employee-attrition-capstone
const { Document, Packer, Paragraph, TextRun } = require('docx');
const fs = require('fs');

const readme = `# Employee Attrition Prediction — BSDA Capstone Project

**Western Governors University | Juliane Valentin | September 2026**

---

## Project Overview

This capstone project develops a machine learning-based system for predicting employee attrition using the IBM HR Analytics Employee Attrition and Performance dataset. The goal is to help HR departments identify at-risk employees proactively — before they resign — enabling targeted retention interventions.

**Research Question:** Which job-related, demographic, and satisfaction factors are most predictive of employee attrition, and can a machine learning model accurately identify at-risk employees before they choose to leave?

**Hypothesis:** Employees with high job satisfaction but low work-life balance scores are equally likely to leave as employees with low job satisfaction, suggesting that work-life balance is an independent attrition driver rather than a component of overall satisfaction.

---

## Key Findings

- **MonthlyIncome** is the strongest predictor of attrition, followed by Age and TotalWorkingYears
- **OverTime** employees leave at 30.5% — nearly three times the rate of non-overtime workers (10.4%)
- **Hypothesis partially supported:** Employees with High Satisfaction but Low Work-Life Balance (18.5% attrition) leave at nearly the same rate as Low Satisfaction employees with High Work-Life Balance (19.0%)
- **WorkLifeBalance** ranked #21 and **JobSatisfaction** ranked #18 in feature importance — similar scores supporting independent effects

---

## Model Performance

| Metric | Score |
|--------|-------|
| Precision | 0.47 |
| Recall | 0.60 |
| F1 Score | 0.52 |
| ROC-AUC | 0.79 |

- **Model:** Random Forest Classifier (500 estimators, max_depth=10, class_weight='balanced')
- **Classification Threshold:** 0.45 (optimized for F1)
- **Train/Test Split:** 80/20 stratified

---

## Project Structure

\`\`\`
employee-attrition-capstone/
│
├── data/
│   └── WA_Fn-UseC_-HR-Employee-Attrition.csv   # IBM HR Analytics dataset
│
├── model/
│   ├── model.pkl                                 # Trained Random Forest model
│   ├── threshold.pkl                             # Optimized classification threshold
│   └── feature_names.pkl                         # Feature names used in training
│
├── notebooks/
│   └── eda.ipynb                                 # Full analysis notebook
│
├── screenshots/
│   ├── attrition_overview.png
│   ├── attrition_by_category.png
│   ├── hypothesis_comparison.png
│   ├── correlation_heatmap.png
│   ├── confusion_matrix.png
│   ├── roc_curve.png
│   └── feature_importance.png
│
├── app.py                                        # Streamlit dashboard
├── model_card.md                                 # Model documentation
├── slice_output.txt                              # Slice performance analysis results
└── README.md
\`\`\`

---

## How to Run

### 1. Clone the repository
\`\`\`bash
git clone https://github.com/JEOV95/employee-attrition-capstone.git
cd employee-attrition-capstone
\`\`\`

### 2. Create and activate a virtual environment
\`\`\`bash
python -m venv venv
# Windows
venv\\Scripts\\activate
# Mac/Linux
source venv/bin/activate
\`\`\`

### 3. Install dependencies
\`\`\`bash
pip install pandas scikit-learn matplotlib seaborn streamlit notebook
\`\`\`

### 4. Run the Streamlit dashboard
\`\`\`bash
streamlit run app.py
\`\`\`

### 5. Open the analysis notebook
\`\`\`bash
jupyter notebook notebooks/eda.ipynb
\`\`\`

---

## Dashboard Pages

- **Overview** — Attrition rates by department, overtime, and the hypothesis comparison chart
- **Feature Analysis** — Top 20 feature importances from the Random Forest model
- **Model Performance** — Confusion matrix, ROC curve, and slice performance summary
- **Prediction Tool** — Enter employee details to receive an attrition risk prediction

---

## Dataset

**IBM HR Analytics Employee Attrition and Performance**
- Source: [Kaggle](https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset)
- Records: 1,470 employees
- Features: 35
- Target: Attrition (Yes/No)
- Nature: Synthetic dataset created by IBM for educational purposes

---

## Tools and Technologies

| Tool | Purpose |
|------|---------|
| Python 3.13 | Primary programming language |
| pandas | Data loading and manipulation |
| scikit-learn | Model training and evaluation |
| matplotlib / seaborn | Data visualization |
| Streamlit | Interactive dashboard |
| pickle | Model serialization |
| Git / GitHub | Version control |

---

## References

- Alsubaiei, M., Alrashidi, M., & Alrashidi, A. (2022). Predicting employee attrition using machine learning approaches. *Applied Sciences, 12*(13), 6424.
- Fayyazi, M., & Aslani, F. (2015). The impact of work-life balance on employees' job satisfaction and turnover intention. *International Letters of Social and Humanistic Sciences, 51*, 33–41.
- IBM. (2017). *IBM HR Analytics Employee Attrition & Performance* [Dataset]. Kaggle.
- Society for Human Resource Management. (2023). *State of the workplace report 2022–2023*. SHRM.
`;

fs.writeFileSync('/mnt/user-data/outputs/README.md', readme);
console.log('Done');