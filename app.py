import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go


st.set_page_config(page_title="GlobalMech Forecasting", layout="wide")


df = pd.read_csv("data/raw/globalmech_data.csv", parse_dates=["Date"], index_col="Date")
model = joblib.load("model.pkl")

targets = ["Dom_Cap", "Dom_Spares", "Exp_Cap", "Exp_Spares"]


def create_features(df):
    df_fe = df.copy()

    for col in targets:
        df_fe[f"{col}_lag1"] = df_fe[col].shift(1)
        df_fe[f"{col}_lag3"] = df_fe[col].shift(3)

    for col in ["Dom_Cap", "Dom_Spares"]:
        df_fe[f"{col}_roll3"] = df_fe[col].rolling(3).mean()

    df_fe["month"] = df_fe.index.month
    df_fe["quarter"] = df_fe.index.quarter

    df_fe.dropna(inplace=True)
    return df_fe

df_fe = create_features(df)

X = df_fe.drop(columns=targets)


st.sidebar.title("🎛️ Scenario Controls")

usd_change = st.sidebar.slider("USD Change", -10, 10, 0)
install_change = st.sidebar.slider("Install Base Change", -100, 100, 0)
shipping_change = st.sidebar.slider("Shipping Index Change", -20, 20, 0)


latest_X = X.tail(1).copy()

latest_X["USD_INR"] += usd_change
latest_X["Install_Base"] += install_change
latest_X["Shipping_Index"] += shipping_change

baseline = model.predict(X.tail(1))
scenario = model.predict(latest_X)


st.title("🚀 GlobalMech Revenue Forecasting Dashboard")


st.subheader("📊 Revenue Impact Summary")

cols = st.columns(4)

for i, col in enumerate(targets):
    change = scenario[0][i] - baseline[0][i]
    cols[i].metric(
        label=col,
        value=f"{scenario[0][i]:.0f}",
        delta=f"{change:.0f}"
    )


st.subheader("📈 Revenue Trends")

for col in targets:
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df_fe.index,
        y=df_fe[col],
        mode='lines',
        name='Historical'
    ))
    
    fig.add_trace(go.Scatter(
        x=[df_fe.index[-1]],
        y=[scenario[0][targets.index(col)]],
        mode='markers',
        name='Scenario Prediction',
        marker=dict(size=10)
    ))
    
    fig.update_layout(title=col, height=300)
    
    st.plotly_chart(fig, use_container_width=True)


st.subheader("🧠 Key Insights")

if usd_change > 0:
    st.write("📈 Increase in USD is boosting export revenues.")

if install_change > 0:
    st.write("🏭 Higher install base is driving spares demand.")

if shipping_change > 0:
    st.write("🚢 Shipping delays may negatively impact export capital.")

if usd_change == 0 and install_change == 0 and shipping_change == 0:
    st.write("📊 No scenario applied. Showing baseline forecast.")