import streamlit as st
import requests
import json
import folium
import random
from streamlit_folium import folium_static

from geopy.distance import geodesic
BACKEND_URL = "http://127.0.0.1:8000/get_aisle"
GEMINI_API_KEY = "GEMINI_API_KEY"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateText?key={GEMINI_API_KEY}"
MAPBOX_ACCESS_TOKEN = "MAPBOX_ACCESS_TOKEN"
MAPBOX_DIRECTIONS_URL = "https://api.mapbox.com/directions/v5/mapbox/walking/"

st.title("🛒 Walmart AR Navigation")
product = st.text_input("🔍 Enter product name:")
store_id = st.text_input("🏬 Enter store ID:")

# 📍 User Location Input (or Auto-Generate Random Nearby)
use_my_location = st.checkbox("📍 Use My Location")
if use_my_location:
    user_lat = random.uniform(37.7740, 37.7755)  # Simulated latitude
    user_lon = random.uniform(-122.4190, -122.4205)  # Simulated longitude
else:
    user_lat = st.number_input("📍 Enter Your Latitude", value=37.7749, format="%.6f")
    user_lon = st.number_input("📍 Enter Your Longitude", value=-122.4194, format="%.6f")

if st.button("Find Aisle"):
    if not product or not store_id:
        st.warning("⚠️ Please enter both product name and store ID.")
    else:
        try:
            #Step 1: Fetch Aisle Info from FastAPI Backend
            response = requests.get(BACKEND_URL, params={"product": product, "store_id": store_id})
            if response.status_code == 200:
                data = response.json()
                aisle = data.get("aisle", "Unknown")
                st.success(f" Product '{product}' is in Aisle: {aisle}")

                # 🔮 Step 2: Query Google Gemini API for Aisle Location
                gemini_prompt = {
                    "contents": [{
                        "role": "user",
                        "parts": [{
                            "text": f"Provide ONLY the latitude and longitude of aisle {aisle} inside Walmart store {store_id}. "
                                    f"Return only JSON like: {{'latitude': 37.7749, 'longitude': -122.4194}}"
                        }]
                    }]
                }
                gemini_response = requests.post(GEMINI_URL, json=gemini_prompt)

                #Handle Gemini Response
                aisle_lat, aisle_lon = None, None
                if gemini_response.status_code == 200:
                    try:
                        gemini_data = gemini_response.json()
                        gemini_text = gemini_data.get("candidates", [{}])[0].get("output", "{}")
                        gemini_json = json.loads(gemini_text)
                        aisle_lat = float(gemini_json.get("latitude", 0))
                        aisle_lon = float(gemini_json.get("longitude", 0))
                    except Exception:
                        st.warning("Failed to parse aisle location from Gemini.")

                #Fallback if coordinates are missing
                if not aisle_lat or not aisle_lon:
                    aisle_lat, aisle_lon = user_lat + 0.0005, user_lon + 0.0005 
                
                st.success(f"📍 Aisle {aisle} is located at: ({aisle_lat}, {aisle_lon})")

                # 🚶 Step 3: Generate Route using Mapbox API
                route_url = f"{MAPBOX_DIRECTIONS_URL}{user_lon},{user_lat};{aisle_lon},{aisle_lat}?access_token={MAPBOX_ACCESS_TOKEN}&geometries=geojson"
                route_response = requests.get(route_url)

                if route_response.status_code == 200:
                    route_data = route_response.json()
                    if "routes" in route_data and route_data["routes"]:
                        route_coords = route_data["routes"][0]["geometry"]["coordinates"]

                        # 🗺️ Create an improved map
                        map_object = folium.Map(location=[user_lat, user_lon], zoom_start=20, tiles="cartodbpositron")

                        # Add User Location Marker
                        folium.Marker(
                            [user_lat, user_lon], 
                            tooltip="Your Location", 
                            icon=folium.Icon(color="blue", icon="user")
                        ).add_to(map_object)

                        # Add Aisle Location Marker
                        folium.Marker(
                            [aisle_lat, aisle_lon], 
                            tooltip=f"Aisle {aisle}", 
                            icon=folium.Icon(color="red", icon="info-sign")
                        ).add_to(map_object)

                        # Draw the Route
                        route_polyline = [(coord[1], coord[0]) for coord in route_coords]
                        folium.PolyLine(route_polyline, color="green", weight=5, opacity=0.8).add_to(map_object)

                        folium_static(map_object)
                    else:
                        st.warning("Failed to get navigation route from Mapbox.")
                else:
                    st.error("Mapbox API Error. Check credentials or request format.")

            else:
                st.error("Product not found or API error.")

        except requests.exceptions.RequestException:
            st.error("Error connecting to backend.")
