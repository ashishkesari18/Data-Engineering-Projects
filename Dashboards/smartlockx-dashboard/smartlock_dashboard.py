import streamlit as st
import pandas as pd
import json
import plotly.express as px
import os

st.set_page_config(page_title="SmartLockX Dashboard", layout="wide")
st.title("🔐 SmartLockX – Real-Time Unlock Event Dashboard")

@st.cache_data(show_spinner=False)
def load_data():
    json_path = os.path.join(os.path.dirname(__file__), "final_unlock_events.json")
    with open(json_path, "r") as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['date'] = df['timestamp'].dt.date
    df['hour'] = df['timestamp'].dt.hour
    return df

df = load_data()

if df.empty:
    st.warning("⚠️ No data available.")
    st.stop()

# --- Sidebar filters
st.sidebar.header("🔍 Filter Events")
delivery_type = st.sidebar.multiselect("📦 Delivery Type", df['delivery_type'].unique(), default=list(df['delivery_type'].unique()))
status = st.sidebar.multiselect("🔓 Status", df['status'].unique(), default=list(df['status'].unique()))
cities = st.sidebar.multiselect("🌍 City", df['location'].unique(), default=list(df['location'].unique()))

df = df[
    df['delivery_type'].isin(delivery_type) &
    df['status'].isin(status) &
    df['location'].isin(cities)
]

# --- Summary metrics
st.markdown("### 📊 Summary Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Events", len(df))
col2.metric("Success Rate", f"{(df['status'] == 'success').mean()*100:.1f}%")
col3.metric("Unique Devices", df['device_id'].nunique())
col4.metric("Delivery Agents", df['delivery_agent'].nunique())

st.divider()

# --- Charts
st.subheader("🔁 Unlock Status Distribution")
st.plotly_chart(
    px.pie(df, names="status", title="Unlock Status Distribution"),
    use_container_width=True
)

st.subheader("📦 Delivery Type Frequency")
delivery_counts = df['delivery_type'].value_counts().reset_index()
delivery_counts.columns = ['delivery_type', 'count']
st.plotly_chart(
    px.bar(delivery_counts, x='delivery_type', y='count', color='delivery_type',
           title="Delivery Method Trends", labels={'delivery_type': 'Delivery Type', 'count': 'Count'}),
    use_container_width=True
)

st.subheader("🌆 Top Cities by Unlock Volume")
top_cities = df['location'].value_counts().nlargest(10).reset_index()
top_cities.columns = ['City', 'Unlocks']
st.plotly_chart(
    px.bar(top_cities, x="City", y="Unlocks", color="Unlocks", title="Top 10 Cities by Unlocks"),
    use_container_width=True
)

st.subheader("📅 Daily Unlock Volume")
daily = df.groupby('date').size().reset_index(name='Unlocks')
st.plotly_chart(
    px.area(daily, x='date', y='Unlocks', title="Daily Unlock Trends"),
    use_container_width=True
)

st.subheader("⏰ Hourly Unlock Distribution by Status")
hourly = df.groupby(['hour', 'status']).size().reset_index(name='Count')
st.plotly_chart(
    px.line(hourly, x='hour', y='Count', color='status', markers=True, title="Hourly Unlocks by Status"),
    use_container_width=True
)

st.caption("🚀 Built with ❤ by Ashish | Powered by Streamlit & AWS")
