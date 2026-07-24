import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================
# Page Configuration
# ==========================================

st.set_page_config(
    page_title="US Flight Analysis Dashboard",
    page_icon="✈️",
    layout="wide"
)

st.title("✈️ US Flight Analysis Dashboard")
st.write("Interactive dashboard for analysing US flight operations.")

# ==========================================
# Load Dataset
# ==========================================

df = pd.read_csv("flight_data_2024.csv")

df = df.drop_duplicates()
df = df.dropna()

# ==========================================
# Sidebar Filters
# ==========================================

st.sidebar.header("🎛️ Filters")

selected_state = st.sidebar.selectbox(
    "Select State",
    ["All"] + sorted(df["origin_state_nm"].unique().tolist())
)

selected_month = st.sidebar.selectbox(
    "Select Month",
    ["All"] + sorted(df["month"].unique().tolist())
)

# ==========================================
# Apply Filters
# ==========================================

filtered_df = df.copy()

if selected_state != "All":
    filtered_df = filtered_df[
        filtered_df["origin_state_nm"] == selected_state
    ]

if selected_month != "All":
    filtered_df = filtered_df[
        filtered_df["month"] == selected_month
    ]

# ==========================================
# Dataset Preview
# ==========================================

st.subheader("📋 Dataset Preview")

st.dataframe(filtered_df.head())

# ==========================================
# KPI Cards
# ==========================================

st.markdown("---")

st.subheader("📊 Dashboard Summary")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Flights", len(filtered_df))
col2.metric("States", filtered_df["origin_state_nm"].nunique())
col3.metric("Average Distance", round(filtered_df["distance"].mean(), 2))
col4.metric("Average Air Time", round(filtered_df["air_time"].mean(), 2))

# ==========================================
# First Row
# ==========================================

st.markdown("---")

col1, col2 = st.columns(2)

with col1:

    st.subheader("📈 Flights by State")

    state_chart = (
        filtered_df.groupby("origin_state_nm")
        .size()
        .reset_index(name="Flights")
    )

    fig = px.bar(
        state_chart,
        x="origin_state_nm",
        y="Flights",
        color="Flights",
        color_continuous_scale="Blues"
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:

    st.subheader("🌦 Average Weather Delay by State")

    weather = (
        filtered_df.groupby("origin_state_nm")["weather_delay"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        weather,
        x="origin_state_nm",
        y="weather_delay",
        color="weather_delay",
        color_continuous_scale="Reds"
    )

    st.plotly_chart(fig, use_container_width=True)

# ==========================================
# Second Row
# ==========================================

st.markdown("---")

col3, col4 = st.columns(2)

with col3:

    st.subheader("✈️ Distance vs Air Time")

    fig = px.scatter(
        filtered_df,
        x="distance",
        y="air_time",
        color="weather_delay",
        opacity=0.6,
        title="Distance vs Air Time"
    )

    st.plotly_chart(fig, use_container_width=True)

with col4:

    st.subheader("📊 Flight Distance Distribution")

    fig = px.histogram(
        filtered_df,
        x="distance",
        nbins=40,
        color_discrete_sequence=["steelblue"]
    )

    st.plotly_chart(fig, use_container_width=True)

# ==========================================
# Third Row
# ==========================================

st.markdown("---")

col5, col6 = st.columns(2)

with col5:

    st.subheader("📦 Air Time Distribution")

    top_states = (
        filtered_df["origin_state_nm"]
        .value_counts()
        .head(10)
        .index
    )

    box_df = filtered_df[
        filtered_df["origin_state_nm"].isin(top_states)
    ]

    fig = px.box(
        box_df,
        x="origin_state_nm",
        y="air_time",
        color="origin_state_nm"
    )

    fig.update_layout(showlegend=False)

    st.plotly_chart(fig, use_container_width=True)

with col6:

    st.subheader("🛬 Average Late Aircraft Delay")

    delay = (
        filtered_df.groupby("origin_state_nm")["late_aircraft_delay"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        delay,
        x="origin_state_nm",
        y="late_aircraft_delay",
        color="late_aircraft_delay",
        color_continuous_scale="Purples"
    )

    st.plotly_chart(fig, use_container_width=True)

# ==========================================
# Footer
# ==========================================

st.markdown("---")

st.markdown(
    """
    ### 📌 About

    This dashboard was developed using **Python**, **Pandas**, **Plotly**, and **Streamlit** to analyze US flight data. It provides interactive visualizations to explore flight operations, weather delays, flight distance, air time, and state-level performance.
    """
)