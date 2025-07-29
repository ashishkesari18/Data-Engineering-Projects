# Key Risk Project– Predictive Access Risk Engine for Amazon Smart Deliveries

Amazon Key allows secure in-home, in-garage, and in-business deliveries. But what if a driver’s behavior hints at a potential breach or operational failure?

KeyRisk is a real-time predictive engine that flags risky driver unlock behavior — like repeated failures, late-night access, and suspicious delivery routes.

---

## Features
- Real-time driver risk scoring based on smartlock metadata
- Athena-powered SQL insights on unlock behavior
- Streamlit dashboard for live visualizations and drill-downs
- Filter by region, driver ID, access type, and hour of the day
- Future-ready architecture for AWS Lambda, SNS, and production alerts
---

## How to Use

### 1. Generate Fresh Log Data
python scripts/data_generate.py

### 2. Score Driver Risk
python scripts/risk_engine.py

### 3. Launch the Interactive Dashboard
streamlit run scripts/dashboard.py

## Dashboard Insights (PowerBI-Level Interactivity)
- Unlock attempts by region
- Time-of-day usage trends
- Failed unlocks by driver
- Access type analysis
- Drill-down filters for region, driver, hour

---

## Built With
- Python + Pandas
- Streamlit + Plotly
- AWS Athena (simulated queries)
- Faker (for synthetic log generation)


## Cloud Simulation
> Logs are stored in **Amazon S3**, queried via **Athena**, and visualized live through **Streamlit**. Alerts can be plugged into **SNS** for real-time operational use.

## Business Impact
- Reduces investigation time for delivery anomalies
- Proactively flags risky drivers before incidents occur
- Helps Amazon Key ops team take preventive action