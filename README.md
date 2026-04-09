# 🚀 GlobalMech Revenue Forecasting & Scenario Simulation System

## 📌 Overview

This project is an end-to-end data science solution developed for **GlobalMech Industries**, focusing on forecasting revenue across multiple business streams and enabling scenario-based decision-making.

The system uses multivariate time series data, machine learning models, and an interactive dashboard to provide insights into business performance under different conditions.

---

## 🏭 Business Context

GlobalMech operates across four key revenue streams:

* Domestic Capital Equipment
* Domestic Spares / After-Sales
* Export Capital Equipment
* Export Spares / After-Sales

Each stream behaves differently and is influenced by various internal and external factors such as install base, currency exchange rates, and shipping conditions.

---

## 🎯 Objectives

* Forecast revenue for all four business streams
* Incorporate multiple influencing variables (multivariate modeling)
* Enable **scenario-based analysis (what-if simulation)**
* Build an interactive dashboard for business users

---

## 🧠 Key Features

* 📊 Multivariate Forecasting
* 🔄 Multi-output Machine Learning Model (Random Forest)
* 📈 Time Series Modeling (SARIMAX)
* 🎛️ Scenario Simulation Engine
* 🌐 Interactive Streamlit Dashboard
* 📉 Model Evaluation & Visualization

---

## 📂 Project Structure

```
globalmech_forecasting/
│
├── app.py                      # Streamlit dashboard
├── model.pkl                  # Trained model
├── requirements.txt
│
├── data/
│   └── raw/globalmech_data.csv
│
├── notebooks/
│   ├── 01_data_generation.ipynb
│   ├── 02_eda.ipynb
│   ├── 03_feature_engineering.ipynb
│   ├── 04_modeling.ipynb
│
├── src/                       
└── README.md
```

---

## ⚙️ Tech Stack

* Python
* Pandas, NumPy
* Matplotlib, Seaborn, Plotly
* Scikit-learn (Random Forest)
* Statsmodels (SARIMAX)
* Streamlit

---

## 🔍 Methodology

1. Data Generation (Synthetic but realistic business data)
2. Exploratory Data Analysis (EDA)
3. Feature Engineering (lags, rolling mean, time features)
4. Model Training (Random Forest + SARIMAX)
5. Model Evaluation (MAE, visualization)
6. Scenario Simulation Engine
7. Deployment using Streamlit

---

## 📊 Model Performance

The model achieved an average error range of approximately **8–12%**, which is considered acceptable for business forecasting applications.

---

## 🎛️ Scenario Simulation

A key highlight of this project is the ability to simulate business scenarios:

* Change USD exchange rate
* Modify install base
* Adjust shipping conditions

👉 The system dynamically updates revenue predictions based on these changes.

---

## 🌐 Live Demo

👉 *https://globalmech-forecasting-ofng7vq2erjxx4qucdxopg.streamlit.app/*

---

## 🧠 Business Insights

* Export revenue is sensitive to currency fluctuations
* Spare parts revenue is strongly driven by install base
* Shipping delays negatively impact export performance
* Different revenue streams require separate modeling strategies

---

## 🚀 How to Run Locally

```bash
git clone https://github.com/your-username/globalmech-forecasting.git
cd globalmech-forecasting

pip install -r requirements.txt

python -m streamlit run app.py
```

---

## 🔮 Future Improvements

* Integration with real-world datasets
* Advanced models (XGBoost, LSTM)
* API-based deployment
* Enhanced dashboard UI

---

## 👨‍💻 Author

**Ashmeet Singh**
Data Science Aspirant/Intern

---

## ⭐ Acknowledgment

This project demonstrates the application of data science techniques to solve real-world business problems and support data-driven decision-making.
