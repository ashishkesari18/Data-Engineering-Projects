# 📊 AthenaX – Leadership & Mentorship Insights

**AthenaX** is a real-time serverless dashboard built to deliver powerful insights into employee leadership scores, mentorship completions, and promotion patterns using AWS-native tools. This interactive dashboard is designed to support HR leadership teams in making data-driven talent decisions at Amazon scale.

---

## Project Overview

The AthenaX pipeline processes employee signals (like mentorship completions, leadership scores, and promotions) through a robust ETL workflow. The final, aggregated data is visualized through an elegant and professional Streamlit dashboard.

The dashboard answers key business questions like:
- Who are the top employees with high leadership scores but no promotions?
- Which employees completed mentorships but were overlooked for promotion?
- What does the promotion-readiness matrix look like across the org?

---

## Architecture

![AthenaX Architecture](architecture.png)

### Components Used:
- **AWS S3** – Bronze, Silver, Gold Data Lake layers
- **AWS Glue** – ETL transformation from raw signals to refined features
- **Amazon Athena** – SQL-based exploration & validation
- **Streamlit** – Interactive and beautiful visualization dashboard (hosted publicly)

---

## Features

- Leadership Score Distribution
- Mentorships vs Leadership Scatter Analysis
- Promotion Status Breakdown (Pie + Bar)
- Top 10 Without Promotion (by Leadership / Mentorship)
- Promotion Readiness vs High Potential Matrix
- Full Gold Layer Table Viewer
- One-click Gold Layer Download

---

## Live Dashboard

> 🔗 **[Click here to open the AthenaX Dashboard](https://your-streamlit-link.streamlit.app)**  

## Contributing

This project is part of the **AWS 100 Projects** challenge.  
Pull requests, suggestions, and ideas are welcome!

## Contact

**Author:** Ashish Kesari  
**LinkedIn:** [linkedin.com/in/ashish-kesari](https://www.linkedin.com/in/ashishk18/)  
