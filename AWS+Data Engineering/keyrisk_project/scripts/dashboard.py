import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="KeySentinel Dashboard", layout="wide")
st.title("🔐 KeyRisk Project – Predictive Access Risk Intelligence")

# Load data
df = pd.read_csv("data/smartlock_access_logs.csv")
df["timestamp"] = pd.to_datetime(df["timestamp"])
df["hour"] = df["timestamp"].dt.hour
df["date"] = df["timestamp"].dt.date

# Sidebar Filters
with st.sidebar:
    st.header("🔎 Filter Options")
    regions = st.multiselect("Select Region(s)", options=sorted(df["region"].unique()), default=df["region"].unique())
    drivers = st.multiselect("Select Driver(s)", options=sorted(df["driver_id"].unique()), default=df["driver_id"].unique())
    access_types = st.multiselect("Select Access Type(s)", options=sorted(df["access_type"].unique()), default=df["access_type"].unique())
    time_range = st.slider("Select Hour Range", 0, 23, (0, 23))

# Apply filters
filtered_df = df[
    (df["region"].isin(regions)) &
    (df["driver_id"].isin(drivers)) &
    (df["access_type"].isin(access_types)) &
    (df["hour"].between(time_range[0], time_range[1]))
]

# Layout
col1, col2 = st.columns(2)
with col1:
    st.metric("🔐 Total Unlocks", len(filtered_df))
    st.metric("❌ Failed Attempts", len(filtered_df[filtered_df["status"] == "fail"]))
with col2:
    st.metric("🕒 Avg. Hour of Access", round(filtered_df["hour"].mean(), 2))
    st.metric("📍 Regions Active", filtered_df["region"].nunique())

# Charts
st.subheader("📊 Unlocks by Region")
fig_region = px.bar(filtered_df["region"].value_counts().reset_index(),
                    x="index", y="region", labels={"index": "Region", "region": "Unlock Count"},
                    color="index", title="Unlocks by Region")
st.plotly_chart(fig_region, use_container_width=True)

st.subheader("⏰ Unlocks by Hour of Day")
hour_data = filtered_df["hour"].value_counts().sort_index().reset_index()
hour_data.columns = ["Hour", "Unlock Count"]
fig_hour = px.line(hour_data, x="Hour", y="Unlock Count", markers=True, title="Hourly Unlock Trend")
st.plotly_chart(fig_hour, use_container_width=True)

st.subheader("❗ Failed Unlocks per Driver")
fail_df = filtered_df[filtered_df["status"] == "fail"]
fail_chart = fail_df["driver_id"].value_counts().reset_index()
fail_chart.columns = ["Driver ID", "Failed Attempts"]
fig_fail = px.bar(fail_chart, x="Driver ID", y="Failed Attempts", title="Failed Unlock Attempts by Driver")
st.plotly_chart(fig_fail, use_container_width=True)

st.subheader("🔁 Access Type Distribution")
access_counts = filtered_df.groupby(["driver_id", "access_type"]).size().unstack(fill_value=0)
st.dataframe(access_counts)

st.markdown("📥 *Data queried from Amazon S3 using Athena and visualized here in real-time via Streamlit.*")
