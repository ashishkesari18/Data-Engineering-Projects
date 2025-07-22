
import streamlit as st
import boto3
import pandas as pd
import json
import plotly.express as px

st.set_page_config(page_title="SmartLockX Dashboard", layout="wide")
st.title("🔐 SmartLockX – Real-Time Unlock Event Dashboard")

# S3 config
BUCKET = "smartlockx-unlock-events-raw"
s3 = boto3.client("s3")

@st.cache_data(show_spinner=False)
def load_data():
    objects = s3.list_objects_v2(Bucket=BUCKET)
    if "Contents" not in objects:
        return pd.DataFrame()

    rows = []
    for obj in objects["Contents"]:
        if obj["Key"].endswith(".json"):
            try:
                response = s3.get_object(Bucket=BUCKET, Key=obj["Key"])
                data = json.loads(response["Body"].read().decode("utf-8"))
                rows.append(data)
            except:
                continue

    if not rows:
        return pd.DataFrame()

    df = pd.DataFrame(rows)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['date'] = df['timestamp'].dt.date
    df['hour'] = df['timestamp'].dt.hour
    return df

df = load_data()

if df.empty:
    st.warning("⚠️ No data available. Run your simulator.")
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
    px.histogram(df, x="status", color="status", title="Unlock Status Distribution"),
    use_container_width=True
)

st.subheader("📦 Delivery Type Frequency")
st.plotly_chart(
    px.histogram(df, x="delivery_type", color="delivery_type", title="Delivery Method Trends"),
    use_container_width=True
)

st.subheader("🌆 Top Cities by Unlock Volume")
top_cities = df['location'].value_counts().nlargest(10).reset_index()
top_cities.columns = ['City', 'Unlocks']
st.plotly_chart(
    px.bar(top_cities, x="City", y="Unlocks", color="City", title="Top 10 Cities"),
    use_container_width=True
)

st.subheader("📅 Daily Unlock Volume")
daily = df.groupby('date').size().reset_index(name='Unlocks')
st.plotly_chart(
    px.line(daily, x='date', y='Unlocks', markers=True, title="Daily Unlock Trends"),
    use_container_width=True
)

st.subheader("⏰ Hourly Unlock Distribution by Status")
hourly = df.groupby(['hour', 'status']).size().reset_index(name='Count')
st.plotly_chart(
    px.bar(hourly, x='hour', y='Count', color='status', barmode='group', title="Unlocks by Hour and Status"),
    use_container_width=True
)
