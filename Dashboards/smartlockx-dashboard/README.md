# 🔐 SmartLockX – Real-Time IoT Unlock Event Analytics Platform

SmartLockX is a real-time data engineering project that simulates Amazon Key–style smart lock unlock events and processes them end-to-end using AWS services and Python. It features a full data pipeline from IoT event simulation to a live Streamlit dashboard with analytics on unlock success, delivery behavior, and location-based trends.

---

## Project Overview

Amazon Key’s mission is to provide seamless, secure access to customer doors during deliveries. SmartLockX emulates that by:

- Simulating **real-time smart lock events** using Python and Faker  
- Streaming events to **Amazon Kinesis**  
- Processing events with **AWS Lambda**  
- Storing events in **Amazon S3** (partitioned by date)  
- Querying data via **Amazon Athena**  
- Visualizing insights through an interactive **Streamlit dashboard**

---

## Tech Stack

- **Language**: Python (Faker, Boto3, Streamlit, Plotly, Pandas)
- **AWS Services**:
  - Amazon Kinesis (event ingestion)
  - AWS Lambda (event processing)
  - Amazon S3 (data lake)
  - Amazon Athena (SQL analysis)
  - AWS Glue (optional for cataloging)
- **Visualization**: Streamlit + Plotly

---

## Dashboard Features

- Unlock status distribution (success/failure/timeout)
- Delivery type breakdown
- Top cities by unlocks
- Daily and hourly unlock volume
- Smart filters (city, status, delivery type)

---

## How It Works

1. **Run the simulator**:
   python unlock_event_simulator.py

2. **Lambda reads from Kinesis** and stores each event to:
   s3://smartlockx-unlock-events-raw/dt=YYYY-MM-DD/event_*.json

3. **Query the data with Athena** (via Glue table):
   SELECT * FROM smartlockx_db.unlock_events LIMIT 10;

4. **Visualize in Streamlit**:
   streamlit run smartlock_dashboard.py
---

## Folder Structure

```
├── unlock_event_simulator.py
├── lambda_kinesis_to_s3.py
├── smartlock_dashboard.py
├── README.md
```

---

## Why It Matters

This project mirrors how Amazon Key might collect and analyze unlock activity at scale. It showcases:

- Real-time IoT simulation
- Serverless event-driven architecture
- Fully interactive analytics pipeline
- AWS-native, cost-effective, and Free Tier–friendly solution

---

## 🧠 Next Phase (Coming Up)

> 🔐 **KeyGuard** – Add ML-based unlock trust scoring and anomaly detection (fraud flagging, timeout clusters, agent behavior)
