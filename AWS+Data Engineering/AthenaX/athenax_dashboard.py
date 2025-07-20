import streamlit as st
import pandas as pd
import boto3
from io import StringIO
import plotly.express as px

st.set_page_config(page_title="AthenaX Leadership Dashboard", layout="wide")
st.title("📊 AthenaX – Leadership & Mentorship Insights")

# AWS S3 Config
BUCKET_NAME = "athenax-bronze-layer"
KEY = "gold/"  # Gold folder path

# S3 Client
s3 = boto3.client("s3")

# List and fetch the latest CSV files in gold/
files = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=KEY)
csv_files = [f["Key"] for f in files.get("Contents", []) if f["Key"].endswith(".csv")]
csv_files.sort()

if not csv_files:
    st.error("No CSV files found in the gold layer.")
else:
    df_list = []
    for file in csv_files:
        obj = s3.get_object(Bucket=BUCKET_NAME, Key=file)
        body = obj["Body"].read().decode("utf-8")
        df = pd.read_csv(StringIO(body))
        df_list.append(df)
    data = pd.concat(df_list, ignore_index=True)

    # KPIs
    st.markdown("### 📌 Key Metrics")
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("👥 Total Employees", f"{data.shape[0]:,}")
    kpi2.metric("⭐ Avg. Leadership Score", f"{data['avg_leadership_score'].mean():.2f}")
    kpi3.metric("🎓 Avg. Mentorships Completed", f"{data['completed_mentorships'].mean():.2f}")

    st.markdown("---")

    # Leadership Score Distribution
    st.subheader("📈 Leadership Score Distribution")
    fig1 = px.histogram(data, x='avg_leadership_score', nbins=30, title='Leadership Score Distribution', color_discrete_sequence=['#1f77b4'])
    st.plotly_chart(fig1, use_container_width=True)

    # Mentorships vs Leadership
    st.subheader("📊 Mentorships vs Leadership Score")
    fig2 = px.scatter(data, x="completed_mentorships", y="avg_leadership_score",
                      color="last_promotion_status",
                      title="Mentorships Completed vs Leadership Score",
                      labels={"completed_mentorships": "Mentorships", "avg_leadership_score": "Leadership Score"})
    st.plotly_chart(fig2, use_container_width=True)

    # Promotion Status Breakdown
    st.subheader("📌 Promotion Status Breakdown")
    promotion_counts = data['last_promotion_status'].value_counts().reset_index()
    promotion_counts.columns = ['Promotion Status', 'Count']
    fig3 = px.pie(promotion_counts, names='Promotion Status', values='Count', title="Promotion Status Distribution")
    st.plotly_chart(fig3, use_container_width=True)

    # Top Leadership Scores Without Promotion
    st.subheader("🏆 Top Leadership Scores Without Promotions")
    top_no_promo = data[data['last_promotion_status'] == 'not_promoted'] \
                    .sort_values(by='avg_leadership_score', ascending=False).head(10)
    st.dataframe(top_no_promo)

    # Most Mentorships but No Promotion
    st.subheader("🎓 Most Mentorships Without Promotion")
    top_mentors = data[(data['last_promotion_status'] == 'not_promoted') &
                      (data['completed_mentorships'] > 0)] \
                  .sort_values(by='completed_mentorships', ascending=False).head(10)
    st.dataframe(top_mentors)

    # Promotion Readiness vs High Potential Matrix
    st.subheader("🧠 Promotion Readiness vs High Potential Matrix")
    if 'high_potential_flag' in data.columns and 'promotion_ready_flag' in data.columns:
        flag_df = data.groupby(['high_potential_flag', 'promotion_ready_flag'])['employee_id'].count().reset_index()
        flag_df.columns = ['High Potential', 'Promotion Ready', 'Count']
        fig4 = px.sunburst(flag_df, path=['High Potential', 'Promotion Ready'], values='Count',
                           color='Count', title='Promotion Readiness vs High Potential')
        st.plotly_chart(fig4, use_container_width=True)
    else:
        st.info("🚫 Required columns ('high_potential_flag', 'promotion_ready_flag') not found in dataset.")

    st.markdown("---")
    st.markdown("⬇️ Download full Gold Layer dataset")
    st.download_button("Download CSV", data.to_csv(index=False), file_name="athenax_gold_layer.csv")
