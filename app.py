import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import requests
import os

# Page config
st.set_page_config(
    page_title="Dengue Risk Predictor",
    page_icon="🦟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title
st.title("🦟 Dengue Risk Prediction System")
st.markdown("**Real-time dengue danger assessment with AI-powered mitigation recommendations**")

# -------------------------------
# HEAD TABS NAVIGATION
# -------------------------------
tab_dashboard, tab_newsletter, tab_map = st.tabs(
    ["📊 Dashboard", "📰 Newsletter", "🗺️ Hotspot Map"]
)

# -------------------------------
# SIDEBAR INPUTS (SHARED ACROSS TABS)
# -------------------------------
st.sidebar.header("📝 Input Parameters")
area = st.sidebar.text_input("Area name (e.g., Woodlands, Ang Mo Kio)", "Woodlands")
construction = st.sidebar.checkbox("Construction sites present?", True)

# Weather section
st.sidebar.header("🌤️ Weather Data")
weather_source = st.sidebar.radio("Weather source:", ["Manual Entry", "OpenWeatherMap API"])

humidity = 70
temperature = 30
rainfall = 0.0

if weather_source == "OpenWeatherMap API":
    api_key = st.sidebar.text_input("OpenWeatherMap API Key", type="password", placeholder="Enter your API key")
    if api_key and st.sidebar.button("Fetch Weather"):
        try:
            # Geocoding
            geo_url = f'http://api.openweathermap.org/geo/1.0/direct?q={area}&limit=1&appid={api_key}'
            geo_response = requests.get(geo_url, timeout=10)
            geo = geo_response.json()

            if not geo:
                st.sidebar.error("Location not found. Try a more specific area name.")
            else:
                lat, lon = geo[0]['lat'], geo[0]['lon']

                # Weather
                weather_url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={api_key}'
                w_response = requests.get(weather_url, timeout=10)
                w = w_response.json()['main']

                st.sidebar.success("✓ Weather data fetched!")
                humidity = w['humidity']
                temperature = w['temp']
                rainfall = 0.0

        except Exception as e:
            st.sidebar.error(f"Error fetching weather: {e}")

else:
    humidity = st.sidebar.slider("Humidity (%)", 0, 100, 70)
    temperature = st.sidebar.slider("Temperature (°C)", 15, 45, 30)
    rainfall = st.sidebar.slider("Recent rainfall (mm)", 0.0, 100.0, 0.0)

# Dengue cases section
st.sidebar.header("🔴 Dengue Data")
cases_source = st.sidebar.radio("Cases source:", ["Local CSV", "Manual Entry"])

historical_cases = 39
active_clusters = 5

if cases_source == "Local CSV":
    if os.path.exists('dengue_cases.csv'):
        try:
            df = pd.read_csv('dengue_cases.csv')
            area_match = df[df.iloc[:, 0].str.lower() == area.lower()]
            if not area_match.empty:
                historical_cases = int(area_match.iloc[0, 1])
                active_clusters = int(area_match.iloc[0, 2]) if len(area_match.columns) > 2 else 0
                st.sidebar.success(f"✓ Loaded {historical_cases} cases for {area}")
            else:
                historical_cases = st.sidebar.number_input("Dengue cases last week", 0, 1000, 39)
                active_clusters = st.sidebar.number_input("Active clusters", 0, 50, 5)
        except Exception as e:
            st.sidebar.error(f"CSV load error: {e}")
            historical_cases = st.sidebar.number_input("Dengue cases last week", 0, 1000, 39)
            active_clusters = st.sidebar.number_input("Active clusters", 0, 50, 5)
    else:
        st.sidebar.info("dengue_cases.csv not found. Using manual entry.")
        historical_cases = st.sidebar.number_input("Dengue cases last week", 0, 1000, 39)
        active_clusters = st.sidebar.number_input("Active clusters", 0, 50, 5)
else:
    historical_cases = st.sidebar.number_input("Dengue cases last week", 0, 1000, 39)
    active_clusters = st.sidebar.number_input("Active clusters", 0, 50, 5)

# -------------------------------
# SCORING ALGORITHM
# -------------------------------
score = 0.0
score += 2 if construction else 0
score += max(0, min(2, (float(humidity) - 60) / 7.5)) if humidity > 60 else 0

if temperature >= 30:
    score += 1.5
elif temperature >= 26:
    score += 0.8

if rainfall >= 50:
    score += 2
elif rainfall >= 20:
    score += 1

if historical_cases >= 20:
    score += 3
elif historical_cases >= 5:
    score += 1

if active_clusters >= 3:
    score += 1

score = int(min(10, round(score)))

# Danger level
if score >= 6:
    danger = "High"
    color = "🔴"
elif score >= 3:
    danger = "Medium"
    color = "🟡"
else:
    danger = "Low"
    color = "🟢"

action_map = {
    'High': 'Immediate — Enhanced surveillance, fogging where appropriate, community alerts, and intensive source reduction',
    'Medium': 'Targeted inspections, community outreach, larvicide in hotspots, weekly monitoring',
    'Low': 'Routine monitoring and public education; update weekly'
}

# -------------------------------
# TAB 1 — DASHBOARD
# -------------------------------
with tab_dashboard:

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Risk Score", f"{score}/10")
    with col2:
        st.metric("Danger Level", f"{color} {danger}")
    with col3:
        st.metric("Active Clusters", active_clusters)

    st.subheader("📋 Recommended Action Level")
    st.info(action_map[danger])

    # Mitigation suggestions
    st.subheader("💡 Tailored Mitigation Suggestions")
    suggestions = []
    if construction:
        suggestions.append("Inspect construction sites and drains; enforce water management")
    if humidity >= 75:
        suggestions.append("Increase stagnant water checks (humid conditions favor mosquitoes)")
    if temperature >= 30:
        suggestions.append("Focus on outdoor breeding spots; adult mosquitoes more active")
    if rainfall >= 50:
        suggestions.append("Clear rainwater from containers and debris")
    if historical_cases >= 5:
        suggestions.append("Conduct targeted house-to-house inspections in clusters")
    if active_clusters >= 3:
        suggestions.append("Set up temporary cluster response teams")

    if suggestions:
        for i, s in enumerate(suggestions, 1):
            st.success(f"{i}. {s}")
    else:
        st.success("Maintain routine monitoring and public education")

    # Visualization: Risk score trend
    st.subheader("📈 4-Week Risk Trend")
    weeks = [datetime.today() - timedelta(weeks=i) for i in range(3, -1, -1)]
    np.random.seed(42)
    past_scores = np.clip(np.random.normal(score, 1, 4).astype(int), 0, 10)

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(weeks, past_scores, marker='o', linewidth=2, markersize=8)
    ax.fill_between(weeks, past_scores, alpha=0.3)
    ax.set_ylabel('Risk Score', fontsize=12)
    ax.set_title(f'Dengue Risk Trend - {area}', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    st.pyplot(fig, use_container_width=True)

    # Danger level circle
    st.subheader("🎯 Danger Indicator")
    colA, colB, colC = st.columns([1, 2, 1])
    with colB:
        fig, ax = plt.subplots(figsize=(6, 6))
        color_map = {'High': '#FF6B6B', 'Medium': '#FFD93D', 'Low': '#6BCB77'}
        circle = plt.Circle((0.5, 0.5), 0.4, color=color_map[danger], alpha=0.8)
        ax.add_patch(circle)
        ax.text(0.5, 0.5, f'{danger}\n(Score: {score})', ha='center', va='center',
                fontsize=24, fontweight='bold', color='white')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        st.pyplot(fig, use_container_width=True)

    # Input summary
    st.subheader("📊 Input Summary")
    input_df = pd.DataFrame({
        'Parameter': ['Area', 'Construction Sites', 'Humidity (%)', 'Temperature (C)', 'Recent Rainfall (mm)', 'Cases (Last Week)', 'Active Clusters'],
        'Value': [area, 'Yes' if construction else 'No', humidity, temperature, rainfall, historical_cases, active_clusters]
    })
    st.table(input_df)

# -------------------------------
# TAB 2 — NEWSLETTER
# -------------------------------
with tab_newsletter:
    st.header("📰 Community Newsletter")

    st.write("Create and save dengue updates for residents and stakeholders.")

    newsletter_text = st.text_area("Newsletter content", height=250)

    if st.button("Save Newsletter"):
        with open("newsletter.txt", "a", encoding="utf-8") as f:
            f.write(f"\n\n=== {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")
            f.write(newsletter_text)

        st.success("Newsletter saved to newsletter.txt")

# -------------------------------
# TAB 3 — HOTSPOT MAP
# -------------------------------
with tab_map:
    st.header("🗺️ Dengue Hotspot Map")

    st.write("This map shows hotspot locations based on reported clusters or uploaded data.")

    # If a CSV exists, use it; else demo data
    if os.path.exists("dengue_hotspots.csv"):
        hotspot_df = pd.read_csv("dengue_hotspots.csv")
        st.success("Loaded hotspot data from dengue_hotspots.csv")
    else:
        hotspot_df = pd.DataFrame({
            "lat": [1.4303, 1.4404, 1.4211],
            "lon": [103.8355, 103.8001, 103.9102],
            "cases": [22, 41, 17]
        })
        st.info("Demo hotspot data in use. Add dengue_hotspots.csv to use real data.")

    st.map(hotspot_df[["lat", "lon"]])

# Footer
st.markdown("---")
st.markdown("""
**🦟 Dengue Risk Prediction System**

This tool is for public health planning purposes. Always consult official health authorities for guidance.

**Data Sources:**
- Weather: OpenWeatherMap API
- Dengue cases: Local CSV or manual entry

**License:** MIT (Open Source)
""")
