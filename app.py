import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go


st.set_page_config(page_title="GlobalMech Forecasting", layout="wide")


mode = st.sidebar.radio(
    "Select Mode",
    ["Data-Driven (Existing Product)", "Cold Start (New Product)"]
)

if mode == "Data-Driven (Existing Product)":

    st.title("🚀 GlobalMech Revenue Forecasting Dashboard")

    # =========================
    # 📂 Load Data & Model
    # =========================
    df = pd.read_csv("data/raw/globalmech_data.csv", parse_dates=["Date"], index_col="Date")
    model = joblib.load("model.pkl")

    targets = ["Dom_Cap", "Dom_Spares", "Exp_Cap", "Exp_Spares"]

    # =========================
    # 🧠 Feature Engineering
    # =========================
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

    # =========================
    # 🎛️ Scenario Controls
    # =========================
    st.sidebar.title("🎛️ Scenario Controls")

    usd_change = st.sidebar.slider("USD Change", -10, 10, 0)
    install_change = st.sidebar.slider("Install Base Change", -100, 100, 0)
    shipping_change = st.sidebar.slider("Shipping Index Change", -20, 20, 0)

    # =========================
    # 🌍 Region Selection
    # =========================
    regions = st.multiselect(
        "Select Regions to Compare",
        ["India", "USA", "Europe"],
        default=["India"]
    )

    COUNTRY_CODES = {
        "India": "IN",
        "USA": "US",
        "Europe": "FR"
    }

    from cold_start.worldbank_api import WorldBankAPI

    # =========================
    # 🔮 Base Feature Setup
    # =========================
    latest_X = X.tail(1).copy()

    latest_X["USD_INR"] += usd_change
    latest_X["Install_Base"] += install_change
    latest_X["Shipping_Index"] += shipping_change

    # =========================
    # 🌍 REGION-WISE PREDICTION
    # =========================
    region_predictions = []

    for region in regions:

        country_code = COUNTRY_CODES[region]

        wb = WorldBankAPI(country_code)
        data = wb.get_country_data()

        gdp = data.get("gdp_per_capita") or 10000
        internet = data.get("internet_penetration") or 50

        # normalize
        import numpy as np

        gdp_factor = np.log1p(gdp) / 10   # log scaling
        gdp_factor = min(max(gdp_factor, 0.5), 3)
        internet_factor = (internet / 100) ** 1.5

        # copy features
        region_X = latest_X.copy()

        # inject geo impact
        region_X["USD_INR"] *= gdp_factor
        region_X["Install_Base"] *= internet_factor

        prediction = model.predict(region_X)

        region_predictions.append({
            "region": region,
            "prediction": prediction[0],
            "data": data
        })

    # =========================
    # 🌍 REGION COMPARISON UI
    # =========================
    st.subheader("🌍 Region-wise Revenue Forecast")

    if len(region_predictions) > 0:

        cols = st.columns(len(region_predictions))

        for i, res in enumerate(region_predictions):

            total_revenue = res["prediction"].sum()

            cols[i].metric(
                label=res["region"],
                value=f"₹ {total_revenue:,.0f}"
            )

            # breakdown
            with cols[i].expander("View Breakdown"):
                st.write({
                    "Dom_Cap": res["prediction"][0],
                    "Dom_Spares": res["prediction"][1],
                    "Exp_Cap": res["prediction"][2],
                    "Exp_Spares": res["prediction"][3],
                })

    else:
        st.warning("⚠️ Please select at least one region")

    # =========================
    # 🌍 ECONOMIC DATA DISPLAY
    # =========================
    for res in region_predictions:
        st.subheader(f"🌍 {res['region']} Economic Data")
        st.json(res["data"])

    # =========================
    # 🏆 BEST REGION
    # =========================
    if len(region_predictions) > 0:
        best_region = max(region_predictions, key=lambda x: x["prediction"].sum())
        st.success(f"🏆 Best Region for Revenue: {best_region['region']}")

elif mode == "Cold Start (New Product)":

    st.title("🚀 Cold Start Product Forecasting")

    # 🎛️ Inputs
    market_size = st.slider("Total Market Size", 100000, 10000000, 1000000)
    capture_rate = st.slider("Market Capture %", 0.01, 0.5, 0.1)
    growth_rate = st.slider("Base Growth Rate", 0.1, 1.0, 0.3)
    price = st.slider("Base Price per User", 100, 5000, 500)
    conversion = st.slider("Base Conversion Rate", 0.01, 0.2, 0.05)

    # 🌍 Region selection
    regions = st.multiselect(
        "Select Regions to Compare",
        ["India", "USA", "Europe"],
        default=["India", "USA"]
    )

    # 🌍 Country codes
    COUNTRY_CODES = {
        "India": "IN",
        "USA": "US",
        "Europe": "FR"
    }

    from cold_start.market_sizing import MarketSizing
    from cold_start.scenario_engine import ScenarioEngine
    from cold_start.worldbank_api import WorldBankAPI

    # 📊 Market Sizing
    market = MarketSizing(
        total_market=market_size,
        target_percentage=0.3,
        capture_rate=capture_rate
    )

    st.subheader("📊 Market Size Analysis")
    st.json(market.calculate())

    K = market.get_max_users()

    # =========================
    # 🌍 MULTI-REGION FORECAST
    # =========================
    st.subheader("🌍 Multi-Region Forecast Comparison")

    fig_multi = go.Figure()
    region_results = []

    for region in regions:

        country_code = COUNTRY_CODES[region]

        # 🌍 Fetch real data
        wb = WorldBankAPI(country_code)
        data = wb.get_country_data()

        gdp = data.get("gdp_per_capita") or 10000
        internet = data.get("internet_penetration") or 50

        # normalize
        gdp_factor = min(max(gdp / 50000, 0.5), 1.5)
        internet_factor = internet / 100

        # adjusted inputs
        adj_growth = growth_rate * internet_factor
        adj_conversion = conversion * internet_factor
        adj_price = price * gdp_factor

        # forecasting
        engine = ScenarioEngine(K)
        scenario = engine.run("Expected", adj_growth, adj_price, adj_conversion)

        fig_multi.add_trace(go.Scatter(
            x=scenario["months"],
            y=scenario["revenue"],
            name=region
        ))

        final_rev = scenario["revenue"][-1]

        region_results.append({
            "region": region,
            "revenue": final_rev,
            "data": data
        })

    st.plotly_chart(fig_multi, use_container_width=True)

    # =========================
    # 💰 REGION COMPARISON
    # =========================
    st.subheader("💰 Region-wise Revenue Comparison")

    if len(region_results) > 0:

        cols = st.columns(len(region_results))

        for i, res in enumerate(region_results):
            cols[i].metric(
                label=res["region"],
                value=f"₹ {int(res['revenue']):,}"
            )

    else:
        st.warning("⚠️ Please select at least one region")

    # =========================
    # 🌍 SHOW ECONOMIC DATA
    # =========================
    for res in region_results:
        st.subheader(f"🌍 {res['region']} Economic Data")
        st.json(res["data"])

    # =========================
    # 🏆 BEST REGION
    # =========================
    if len(region_results) > 0:
        best_region = max(region_results, key=lambda x: x["revenue"])
        st.success(f"🏆 Best Market to Launch: {best_region['region']}")
    # =========================
    # 📈 SCENARIO ENGINE (BASE)
    # =========================
    engine = ScenarioEngine(K)

    scenarios = [
        engine.run("Best Case", growth_rate * 1.5, price * 1.2, conversion * 1.5),
        engine.run("Expected Case", growth_rate, price, conversion),
        engine.run("Worst Case", growth_rate * 0.6, price * 0.8, conversion * 0.5),
    ]

    # =========================
    # 📈 USER GROWTH GRAPH
    # =========================
    st.subheader("📈 User Growth Scenarios")

    fig_users = go.Figure()

    for scenario in scenarios:
        fig_users.add_trace(go.Scatter(
            x=scenario["months"],
            y=scenario["users"],
            name=scenario["name"]
        ))

    st.plotly_chart(fig_users, use_container_width=True)

    # =========================
    # 💰 REVENUE GRAPH
    # =========================
    st.subheader("💰 Revenue Growth Scenarios")

    fig_revenue = go.Figure()

    for scenario in scenarios:
        fig_revenue.add_trace(go.Scatter(
            x=scenario["months"],
            y=scenario["revenue"],
            name=scenario["name"]
        ))

    st.plotly_chart(fig_revenue, use_container_width=True)

    # =========================
    # 💰 FINAL REVENUE
    # =========================
    st.subheader("💰 Final Revenue Projection (At Market Saturation)")

    market_data = market.calculate()
    som = market_data["SOM"]

    final_paying_users = som * conversion
    base_final_revenue = final_paying_users * price

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Users", f"{int(som):,}")
    col2.metric("Paying Users", f"{int(final_paying_users):,}")
    col3.metric("Final Revenue", f"₹ {int(base_final_revenue):,}")

    # =========================
    # 💰 SCENARIO COMPARISON
    # =========================
    st.subheader("💰 Scenario Outcome Comparison")

    scenario_cols = st.columns(3)

    for i, scenario in enumerate(scenarios):
        scenario_final_revenue = scenario["revenue"][-1]

        scenario_cols[i].metric(
            label=scenario["name"],
            value=f"₹ {int(scenario_final_revenue):,}"
        )

    # =========================
    # 📊 PROFIT ESTIMATION
    # =========================
    st.subheader("📊 Region-wise Profit Estimation")

    cost_per_user = st.slider("Cost per User", 50, 1000, 200)
    fixed_cost = st.slider("Fixed Cost", 100000, 10000000, 1000000)

    profit_cols = st.columns(len(region_results))

    for i, res in enumerate(region_results):

        region = res["region"]
        revenue = res["revenue"]

        total_cost = (som * cost_per_user) + fixed_cost
        profit = revenue - total_cost

        profit_cols[i].metric(
            label=f"{region} Profit",
            value=f"₹ {int(profit):,}"
        )