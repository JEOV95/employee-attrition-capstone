# Model Card: Employee Attrition Prediction Model

## Model Details
- **Model Type:** Random Forest Classifier
- **Version:** 1.0
- **Training Framework:** scikit-learn 1.9.0
- **Parameters:** n_estimators=500, max_depth=10, min_samples_split=5, min_samples_leaf=2, class_weight='balanced'
- **Classification Threshold:** 0.45 (optimized for F1 score)
- **Date Trained:** September 2026
- **Developer:** Juliane Valentin, Western Governors University Capstone Project

## Intended Use
This model is intended to predict the likelihood that an employee will voluntarily leave an organization, based on demographic and job-related features. It is designed as a proof-of-concept HR analytics tool to demonstrate how machine learning can support proactive employee retention strategies.

**Intended users:** HR analysts and managers seeking to identify at-risk employees before they resign.

**Out-of-scope uses:** This model should NOT be used to make hiring, firing, promotion, or compensation decisions about real individuals. It was trained on synthetic data and must be retrained on real organizational data before any production use.

## Training Data
- **Dataset:** IBM HR Analytics Employee Attrition and Performance dataset
- **Source:** Kaggle (https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset)
- **Size:** 1,470 records, 35 features
- **Nature:** Synthetic dataset created by IBM for educational purposes
- **Train/Test Split:** 80% training (1,176 records), 20% test (294 records)
- **Preprocessing:** Removed zero-variance features (EmployeeCount, StandardHours, Over18); one-hot encoded categorical variables

## Evaluation Data
The model was evaluated on a stratified 20% hold-out test set of 294 records, maintaining the same 16% attrition rate as the full dataset.

## Performance Metrics
| Metric | Score |
|--------|-------|
| Precision | 0.47 |
| Recall | 0.60 |
| F1 Score | 0.52 |
| ROC-AUC | 0.79 |

**Note:** The F1 score of 0.52 reflects the challenge of predicting a minority class (16.1% attrition rate). The ROC-AUC of 0.79 indicates strong discriminative ability across all classification thresholds.

## Key Findings
- **Top predictors:** MonthlyIncome (#1), Age (#2), TotalWorkingYears (#3), OverTime (#8)
- **WorkLifeBalance rank:** #21 (importance: 0.0195)
- **JobSatisfaction rank:** #18 (importance: 0.0248)
- **Hypothesis result:** Partially supported — employees with High Satisfaction but Low WLB (18.5% attrition) leave at nearly the same rate as Low Satisfaction employees with High WLB (19.0%), suggesting work-life balance operates as an independent attrition driver

## Slice Performance
| Subgroup | F1 Score |
|----------|----------|
| Sales Department | 0.67 |
| R&D Department | 0.44 |
| Male | 0.58 |
| Female | 0.44 |
| Single | 0.64 |
| Married | 0.43 |
| Sales Executive | 0.78 |
| Research Scientist | 0.54 |

**Note:** The model performs better for male employees (F1: 0.58) than female employees (F1: 0.44). This disparity should be investigated before any real-world deployment.

## Ethical Considerations
- The dataset includes sensitive demographic features (Gender, Age, MaritalStatus) that could introduce bias
- The model must not be used to make employment decisions that could violate anti-discrimination laws including Title VII of the Civil Rights Act and the Age Discrimination in Employment Act
- A comprehensive fairness audit should be conducted before any production deployment
- Because this model was trained on synthetic data, predictions should not be applied to real employees without retraining on real organizational data

## Limitations
- Trained on synthetic data — may not reflect real-world attrition patterns
- F1 score of 0.52 means approximately half of at-risk employees are missed
- Model performs noticeably worse for female employees and divorced employees
- Dataset is from the 1990s and may not reflect current workforce trends

## Recommendations
- Retrain on real organizational data before production use
- Conduct a fairness audit across all protected demographic groups
- Use predictions as one input among many, not as the sole basis for retention decisions
- Monitor model performance over time and retrain regularly as workforce patterns change

## Citation
IBM. (2017). IBM HR Analytics Employee Attrition & Performance [Dataset]. Kaggle.
https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset