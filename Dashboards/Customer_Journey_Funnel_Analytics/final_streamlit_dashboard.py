
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title="Customer Funnel Dashboard", layout="wide")
st.title("📊 Final Customer Journey Funnel Dashboard")
st.markdown("This dashboard visualizes the complete customer funnel journey with full segment and campaign context.")
st.image("architecture.png", caption="📐 Customer Journey Funnel – AWS Architecture", use_column_width=True)

# --- Load Final Data ---
df = pd.read_csv("customer_journey_events.csv", parse_dates=["timestamp"])

# --- Sidebar Filters ---
with st.sidebar:
    st.header("🎛️ Filter Options")
    selected_sources = st.multiselect("Source", sorted(df["source"].unique()), default=list(df["source"].unique()))
    selected_devices = st.multiselect("Device", sorted(df["device"].unique()), default=list(df["device"].unique()))
    selected_segments = st.multiselect("User Segment", sorted(df["user_segment"].unique()), default=list(df["user_segment"].unique()))
    selected_utm = st.multiselect("UTM Medium", sorted(df["utm_medium"].unique()), default=list(df["utm_medium"].unique()))
    selected_campaigns = st.multiselect("Campaign", sorted(df["campaign"].unique()), default=list(df["campaign"].unique()))

# --- Filter Data ---
df_filtered = df[
    df["source"].isin(selected_sources) &
    df["device"].isin(selected_devices) &
    df["user_segment"].isin(selected_segments) &
    df["utm_medium"].isin(selected_utm) &
    df["campaign"].isin(selected_campaigns)
]

# --- Funnel Summary ---
funnel_order = ["ad_click", "product_view", "cart_add", "checkout"]
funnel_counts = (
    df_filtered.groupby("event_type")["user_id"]
    .nunique()
    .reindex(funnel_order)
    .reset_index()
    .rename(columns={"user_id": "users"})
)
base_users = funnel_counts.loc[funnel_counts["event_type"] == "ad_click", "users"].values[0]
funnel_counts["conversion_rate_percent"] = (funnel_counts["users"] / base_users * 100).round(2)

# --- Layout ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("📉 Funnel Drop-off")
    fig1, ax = plt.subplots()
    ax.bar(funnel_counts["event_type"], funnel_counts["users"], color="teal")
    ax.set_title("User Count at Each Funnel Stage")
    ax.set_ylabel("Users")
    ax.set_xlabel("Funnel Stage")
    st.pyplot(fig1)

with col2:
    st.subheader("🔻 Interactive Funnel")
    fig2 = px.funnel(funnel_counts, x='users', y='event_type', color='event_type',
                     title="Interactive Conversion Funnel")
    st.plotly_chart(fig2, use_container_width=True)

# --- Segment Insight ---
st.subheader("📊 Conversion Rate by User Segment")
segment_df = df_filtered[df_filtered["event_type"].isin(["ad_click", "checkout"])]
segment_summary = (
    segment_df.drop_duplicates(["user_id", "event_type", "user_segment"])
    .pivot_table(index="user_segment", columns="event_type", values="user_id", aggfunc="nunique")
    .fillna(0)
)
segment_summary["conversion_rate"] = (segment_summary["checkout"] / segment_summary["ad_click"] * 100).round(2)
segment_summary = segment_summary.reset_index()

fig3 = px.bar(segment_summary, x="user_segment", y="conversion_rate", color="user_segment",
              title="Checkout Conversion Rate by Segment", labels={"conversion_rate": "Conversion Rate (%)"})
st.plotly_chart(fig3, use_container_width=True)

# --- UTM Campaign Insight ---
st.subheader("📈 Campaign Conversion Trends")
campaign_df = df_filtered[df_filtered["event_type"].isin(["ad_click", "checkout"])]
campaign_summary = (
    campaign_df.drop_duplicates(["user_id", "event_type", "campaign"])
    .pivot_table(index="campaign", columns="event_type", values="user_id", aggfunc="nunique")
    .fillna(0)
)
campaign_summary["conversion_rate"] = (campaign_summary["checkout"] / campaign_summary["ad_click"] * 100).round(2)
campaign_summary = campaign_summary.reset_index()

fig4 = px.bar(campaign_summary, x="campaign", y="conversion_rate", color="campaign",
              title="Conversion Rate by Campaign", labels={"conversion_rate": "Conversion Rate (%)"})
st.plotly_chart(fig4, use_container_width=True)

# --- Final Table ---
st.subheader("📋 Funnel Metrics Table")
st.dataframe(funnel_counts.rename(columns={"event_type": "Stage"}), use_container_width=True)
