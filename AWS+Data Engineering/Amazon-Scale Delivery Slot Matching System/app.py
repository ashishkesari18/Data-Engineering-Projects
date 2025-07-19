import streamlit as st
import requests
import json

st.set_page_config(page_title="Amazon Delivery Slot Checker", page_icon="🚚")
st.title("📦 Amazon-Scale Delivery Slot Checker")

st.markdown("""
Use this tool to validate delivery slot availability for selected product IDs in real-time.
""")

# Input fields
product_ids_input = st.text_input("Enter Product IDs (comma-separated):", "P123,P234")
slot_time = st.text_input("Enter Delivery Slot (e.g., 2025-07-25T10:00-12:00):", "2025-07-25T10:00-12:00")

if st.button("🔍 Check Slot Availability"):
    # Parse product_ids
    product_ids = [pid.strip() for pid in product_ids_input.split(",")]

    # Your API Gateway endpoint here (update this!)
    API_URL = "https://54or0jzv20.execute-api.us-east-1.amazonaws.com/prod/search-and-validate"

    payload = {
        "product_ids": product_ids,
        "slot": slot_time
    }

    with st.spinner("Checking availability..."):
        try:
            response = requests.post(API_URL, json=payload)
            if response.status_code == 200:
                results = json.loads(response.json()["body"])
                if results:
                    st.success("Slot results loaded successfully!")
                    for r in results:
                        st.write(f"**Product ID:** `{r['product_id']}`")
                        st.write(f"**Delivery Slot:** `{r['delivery_slot']}`")
                        if r["status"] == "available":
                            st.success("✅ Slot Available")
                        else:
                            st.error("❌ Slot Not Available")
                        st.markdown("---")
                else:
                    st.warning("No slot results found.")
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"Request failed: {e}")
