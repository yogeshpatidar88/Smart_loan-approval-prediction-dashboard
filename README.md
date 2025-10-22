# Loan Approval Prediction Dashboard

[![Python](https://img.shields.io/badge/Python-3.12-blue)](https://www.python.org/) 
[![Streamlit](https://img.shields.io/badge/Streamlit-v1.30-orange)](https://streamlit.io/) 
[![Plotly](https://img.shields.io/badge/Plotly-v5.18-purple)](https://plotly.com/python/)

---

## 🚀 Project Overview

The **Loan Approval Prediction Dashboard** is a web-based interactive application that predicts whether a loan application will be approved using a Machine Learning model. The dashboard provides a **comprehensive financial overview**, visual insights, and actionable suggestions for improving loan approval chances.

It is designed for **financial institutions, credit analysts, and users** to understand the factors impacting loan eligibility in a clear and interactive way.

---

## 🛠️ Features

- **Loan Approval Prediction**: Predicts approval based on applicant details like income, CIBIL score, loan amount, and assets.
- **Approval Probability Gauge**: Displays the likelihood of loan approval using a dynamic gauge.
- **Financial Overview**: Interactive bar chart summarizing income, loan amount, tenure, CIBIL score, and assets.
- **Dependents Overview**: Pie chart showing the applicant’s family/dependents structure.
- **Loan Term Impact (EMI)**: Line chart visualizing monthly EMI across the loan tenure.
- **CIBIL Score Visualization**: Gauge chart showing credit score status (Very Poor → Excellent).
- **Actionable Suggestions**: Personalized tips to improve loan approval chances.
- **Dark Theme UI**: Modern, clean, and professional interface using Streamlit and Plotly.

---

## 📊 Tech Stack

- **Python 3.12**
- **Streamlit**: Web application framework for interactive dashboards
- **Pandas**: Data manipulation and preparation
- **Pickle**: Saving/loading the trained ML model and scaler
- **Plotly**: Interactive data visualization (bar charts, pie charts, gauges)
- **Machine Learning Model**: Pre-trained classifier for loan approval

---

## 📝 Input Parameters

The dashboard requires the following inputs from users:

| Parameter              | Input Type |
|------------------------|------------|
| Number of Dependents   | Slider     |
| Education              | SelectBox  |
| Self Employed          | SelectBox  |
| Annual Income (₹)      | Slider     |
| Loan Amount (₹)        | Slider     |
| Loan Duration (Years)  | Slider     |
| CIBIL Score            | Slider     |
| Assets (₹)             | Slider     |

Additional financial and personal details like marital status, employment type, co-applicant income, existing loans, property area, age, and gender are used for better user insight and visualization.

---

## 💻 Installation

1. **Clone the repository**

```bash
git clone https://github.com/your-username/loan-approval-prediction-dashboard.git
cd loan-approval-prediction-dashboard
