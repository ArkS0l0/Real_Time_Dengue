import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import requests
import os
import textwrap
import html
import streamlit.components.v1 as components 

# ============== CONFIGURATION ==============
import telebot
from ultralytics import YOLO
from PIL import Image
import os
import csv
from datetime import datetime
import io

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
tab_dashboard, tab_scanner, tab_newsletter, tab_map, tab_FAQprevent, tab_symptom = st.tabs(
    ["📊 Dashboard", "📷 Environment Scanner", "📰 Newsletter", "🗺️ Hotspot Map", "❓ Prevention Tips", "🩺 Symptom Triage"]
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
# TAB 2 — ENVIRONMENT SCANNER
# -------------------------------
with tab_scanner:
    st.header("📷 Environment Scanner")
    st.markdown("**Scan your environment for potential mosquito breeding sites using AI**")
    
    st.markdown("---")
    
    # Info section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🤖 How It Works")
        st.markdown("""
        Our AI-powered Telegram bot uses **YOLOv8** computer vision to detect potential 
        dengue mosquito breeding sites in photos of your environment.
        
        **What it detects:**
        - 🍾 **Bottles** - Discarded bottles holding water
        - 🛞 **Tires** - Old tires collecting rainwater
        - 🌸 **Vases** - Flower pots and vases with stagnant water
        - 🕳️ **Drain Inlets** - Clogged or open drains
        - 🥥 **Coconut Shells** - Coconut husks holding water
        
        **How to use:**
        1. Click the button below to open the Telegram bot
        2. Send a photo of your surroundings
        3. Get instant risk assessment and recommendations!
        """)
        
        st.markdown("---")
        
        # Telegram bot button
        st.subheader("🚀 Start Scanning")
        telegram_url = "https://t.me/dengueENV_bot"
        st.link_button("📱 Open Environment Scanner Bot", telegram_url, use_container_width=True)
        
        st.info("💡 **Tip:** For best results, take clear photos in good lighting and include areas where water might collect.")
    
    with col2:
        st.subheader("📊 Risk Levels")
        
        # Risk level indicators
        st.markdown("**🟢 LOW RISK** (Score < 2)")
        st.caption("No immediate action needed")
        
        st.markdown("**🟡 MEDIUM RISK** (Score 2-5)")
        st.caption("Remove detected items")
        
        st.markdown("**🔴 HIGH RISK** (Score > 5)")
        st.caption("Immediate action required")
    
    st.markdown("---")
    
    # Scan History Table
    st.subheader("📋 Recent Scan History")
    
    if os.path.exists('environment_scans.csv'):
        try:
            # Read CSV with proper column names
            scans_df = pd.read_csv('environment_scans.csv', 
                                   names=['timestamp', 'user_id', 'username', 'detections', 'risk_score', 'risk_level'],
                                   header=None)
            if len(scans_df) > 0:
                # Show last 10 scans (newest first)
                display_df = scans_df.tail(10).iloc[::-1]
                display_df = display_df[['timestamp', 'detections', 'risk_score', 'risk_level']]
                display_df.columns = ['Time', 'Detections', 'Score', 'Risk Level']
                st.dataframe(display_df, use_container_width=True, hide_index=True)
                
                # Show scanned images
                st.subheader("🖼️ Scanned Images")
                if os.path.exists('detections/scan'):
                    image_files = [f for f in os.listdir('detections/scan') if f.endswith(('.jpg', '.png', '.jpeg'))]
                    if image_files:
                        # Show last 6 images in grid
                        image_files = image_files[-6:]
                        cols = st.columns(3)
                        for idx, img_file in enumerate(image_files):
                            with cols[idx % 3]:
                                img_path = os.path.join('detections/scan', img_file)
                                st.image(img_path, use_container_width=True)
                    else:
                        st.info("No scanned images yet.")
                else:
                    st.info("No scanned images yet.")
            else:
                st.info("No scans recorded yet. Use the Telegram bot to start scanning!")
        except Exception as e:
            st.error(f"Error loading scan history: {e}")
    else:
        st.info("No scans recorded yet. Use the Telegram bot to start scanning!")
    
    # Refresh button
    if st.button("🔄 Refresh Scan History"):
        st.rerun()

# -------------------------------
# AI AGENT FUNCTIONS FOR NEWS AGGREGATION
# -------------------------------

# Default NewsAPI key (users can provide their own to override)
DEFAULT_NEWSAPI_KEY = "bbdae050b85b4eee92ca92e0427db557"

def extract_location_from_title(title: str) -> str:
    """
    Extract location name from news title.
    Looks for area names after keywords like 'in', 'at', or 'near'.
    """
    title_lower = title.lower()
    # Common Singapore locations
    locations = ['woodlands', 'tampines', 'ang mo kio', 'bedok', 'clementi', 'geylang', 
                 'jurong', 'bukit merah', 'bukit panjang', 'bukit timah', 'changi', 'choa chu kang',
                 'kallang', 'marine parade', 'newton', 'novena', 'orchard', 'outram', 'pasir ris',
                 'punggol', 'queenstown', 'sengkang', 'serangoon', 'tanjong pagar', 'toa payoh',
                 'ubi', 'west coast', 'western', 'eastern', 'central']
    
    for location in locations:
        if location in title_lower:
            return location
    
    # Fallback: extract words after 'in', 'at', 'near'
    words = title_lower.split()
    for i, word in enumerate(words):
        if word in ['in', 'at', 'near'] and i + 1 < len(words):
            return words[i + 1]
    
    return "singapore"

def extract_unique_key(title: str) -> str:
    """
    Extract a unique identifier from news title to detect duplicates.
    Uses location as the primary deduplication key.
    """
    location = extract_location_from_title(title)
    return location.lower()[:30]

def fetch_singapore_dengue_news(days_back=30):
    """
    Fetch Singapore dengue-related news from multiple sources using NewsAPI.
    Returns deduplicated news with summaries.
    
    Args:
        days_back: Number of days to search back (default 30 for free tier limit)
    """
    try:
        # Using NewsAPI (free tier available)
        # Use default API key or user-provided key from session state
        api_key = st.session_state.get('news_api_key', DEFAULT_NEWSAPI_KEY)
        
        if not api_key:
            return None, "No NewsAPI key available. Please check configuration."
        
        # Search for Singapore dengue news
        search_query = "dengue Singapore"
        url = f"https://newsapi.org/v2/everything"
        
        # Calculate from_date (NewsAPI free tier: max 30 days back)
        from_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
        
        params = {
            'q': search_query,
            'sortBy': 'publishedAt',
            'language': 'en',
            'apiKey': api_key,
            'pageSize': 100,  # Max page size to get more results
            'from': from_date
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        articles = response.json().get('articles', [])
        
        if not articles:
            return None, "No dengue news found for Singapore"
        
        # Filter for Singapore-only articles
        singapore_articles = []
        for article in articles:
            content = f"{article.get('title', '')} {article.get('description', '')}".lower()
            # Check if article mentions Singapore specifically
            if 'singapore' in content:
                singapore_articles.append(article)
        
        if not singapore_articles:
            return None, "No Singapore-specific dengue news found"
        
        return singapore_articles, None
        
    except requests.exceptions.Timeout:
        return None, "Request timeout. Please try again."
    except requests.exceptions.ConnectionError:
        return None, "Connection error. Check your internet connection."
    except Exception as e:
        return None, f"Error fetching news: {str(e)}"

def deduplicate_news(articles: list) -> dict:
    """
    Deduplicate news articles by identifying same cases covered by different sources.
    Groups articles by unique case and returns source tracking.
    """
    if not articles:
        return {}
    
    # Dictionary to group articles by unique case
    cases = {}
    
    for article in articles:
        title = article.get('title', '')
        source = article.get('source', {}).get('name', 'Unknown Source')
        url = article.get('url', '')
        description = article.get('description', '')
        published_at = article.get('publishedAt', '')
        
        # Create unique key for case
        unique_key = extract_unique_key(title)
        
        if unique_key not in cases:
            cases[unique_key] = {
                'title': title,
                'case_id': unique_key,
                'description': description,
                'sources': [],
                'published_at': published_at
            }
        
        # Add source to this case
        if source not in [s['name'] for s in cases[unique_key]['sources']]:
            cases[unique_key]['sources'].append({
                'name': source,
                'url': url
            })
    
    return cases

def generate_simple_summary(article_title: str, description: str) -> str:
    """
    Generate a simple summary from article title and description.
    """
    if not description:
        return article_title
    
    # Use first 150 characters of description if available
    summary = description[:150].strip()
    if len(description) > 150:
        summary += "..."
    
    return summary

def display_singapore_dengue_news():
    """
    Main function to display Singapore dengue news with deduplication.
    """
    st.subheader("📰 Singapore Dengue News Feed")
    st.caption("🇸🇬 **Singapore-only dengue news** | Deduplicated by case | Multiple sources shown")
    
    # Show NewsAPI Coverage Information
    with st.expander("ℹ️ **About NewsAPI Coverage**", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            📌 **Free Tier: Shows articles from ~last 30 days**
            - Up to 100 articles per request
            - 1 request per 12 seconds
            - Good for recent news only
            """)
        with col2:
            st.markdown("""
            💳 **Paid Tier: Access to full historical data (5 years)**
            - Unlimited historical searches
            - Higher request limits
            - Better for research and analysis
            
            🔑 **Get your own API key at [newsapi.org](https://newsapi.org) for extended history**
            """)
    
    st.markdown("---")
    
    # Get API key from user (optional override)
    col1, col2 = st.columns([3, 1])
    with col1:
        api_key_input = st.text_input(
            "📌 NewsAPI Key (Optional - press Enter or leave blank to use default)",
            type="password",
            key="news_api_key_input",
            placeholder="Leave blank to use default key"
        )
    
    with col2:
        fetch_button = st.button("🔍 Fetch News", key="fetch_news_btn")
    
    if fetch_button:
        # Use provided key or fall back to default
        api_key = api_key_input if api_key_input else DEFAULT_NEWSAPI_KEY
        
        # Store API key in session state
        st.session_state['news_api_key'] = api_key
        
        with st.spinner("Fetching Singapore dengue news from last 30 days..."):
            articles, error = fetch_singapore_dengue_news(days_back=30)
        
        if error:
            st.warning(f"⚠️ {error}")
            return
        
        if not articles:
            st.info("No articles found")
            return
        
        # Deduplicate news
        unique_cases = deduplicate_news(articles)
        
        if not unique_cases:
            st.info("No unique dengue cases found in news")
            return
        
        # Display results
        st.success(f"Found **{len(unique_cases)}** unique dengue case(s) from **{sum(len(case['sources']) for case in unique_cases.values())}** source article(s)")
        
        st.info("💡 **Tip:** Showing articles from last 30 days (free tier limit). Get a paid API key at newsapi.org to search 30+ years of historical news!")
        
        st.markdown("---")
        
        # Display each unique case
        for idx, (case_id, case_data) in enumerate(unique_cases.items(), 1):
            with st.container(border=True):
                # Case number and title
                st.markdown(f"### Case #{idx}")
                st.markdown(f"**{case_data['title']}**")
                
                # Summary
                summary = generate_simple_summary(case_data['title'], case_data['description'])
                st.markdown(f"📝 **Summary:** {summary}")
                
                # Published date
                if case_data['published_at']:
                    pub_date = case_data['published_at'][:10]  # Extract date only
                    st.caption(f"📅 Published: {pub_date}")
                
                # Sources reporting this case
                st.markdown("**📰 Sources reporting this case:**")
                sources_text = ""
                for source in case_data['sources']:
                    sources_text += f"- [{source['name']}]({source['url']})\n"
                st.markdown(sources_text)
                
                # Divider
                st.markdown("---")
    
    # Show cached news if available
    if 'cached_news' in st.session_state:
        st.info("💾 Showing cached news from last fetch")

# -------------------------------
# TAB 3 — NEWSLETTER
# -------------------------------
with tab_newsletter:
    st.header("📰 Community Newsletter")

    # Create two sub-sections
    col_news, col_manual = st.columns(2)
    
    with col_news:
        st.subheader("🔗 Singapore Dengue News Aggregator")
        st.write("Fetch latest Singapore dengue news from multiple sources.")
        display_singapore_dengue_news()
    
    st.markdown("---") 
    
    with col_manual:
        st.subheader("✍️ Manual Newsletter Creator")
        st.write("Create and save dengue updates for residents and stakeholders.")

        newsletter_text = st.text_area("Newsletter content", height=250)

        if st.button("Save Newsletter"):
            with open("newsletter.txt", "a", encoding="utf-8") as f:
                f.write(f"\n\n=== {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")
                f.write(newsletter_text)

            st.success("Newsletter saved to newsletter.txt")

# -------------------------------
# TAB 4 — HOTSPOT MAP
# -------------------------------
with tab_map:
    st.header("🗺️ Dengue Hotspot Map")

    st.write("This map shows hotspot locations based on reported clusters or uploaded data.")

    # Existing map logic
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

    st.markdown("---")

    # 🔹 Botpress Chat Section
    st.subheader("💬 Dengue Hotspot Assistant")
    st.caption("Ask about clusters, risk levels, or what actions to take in hotspot areas.")

    bot_url = "https://cdn.botpress.cloud/webchat/v3.5/shareable.html?configUrl=https://files.bpcontent.cloud/2026/01/15/11/20260115113719-WNAZ8CYZ.json"

    components.iframe(
        bot_url,
        height=600,
        scrolling=True
    )


# Footer
st.markdown("---")
st.markdown("""
**🦟 Dengue Risk Prediction System**

This tool is for public health planning purposes. Always consult official health authorities for guidance.

**Data Sources:**
- Weather: OpenWeatherMap API
- Dengue cases: Local CSV or manual entry
- Environment scans: AI-powered Telegram bot (@dengueENV_bot)
- Prevention tips: NEA Singapore, Clean and Green Singapore, gov.sg 

**License:** MIT (Open Source)
""")

# -------------------------------
# TAB 5 — FAQ & Prevention Tips
# -------------------------------

with tab_FAQprevent:
    st.header("❓ Dengue FAQ & Prevention Tips")
    st.markdown("Ask our helpful AI assistant about how to prevent you and your family from dengue. (BLOCK steps, SAW steps, how to protect yourself at home and more.)")
    st.caption("Scroll up or down to see your previous messages. Chat history is not saved if you refresh the page.")
   
    # Add CSS for scrollable chat container
    st.markdown(
        """
        <style>
        .chat-scroll {
            height: 500px;
            overflow-y: auto;
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            padding: 15px;
            background-color: #f9f9f9;
            margin-bottom: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Initialize Session State
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Flag to trigger AI generation after a rerun
    if "generate_response" not in st.session_state:
        st.session_state.generate_response = False

    # Create scrollable chat container
    with st.container(border=False, height=400):
        # Display chat messages using Streamlit's built-in chat_message
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    # Handle AI Response (If triggered)
    # This block runs AFTER the page reloads with the user's new message visible
    if st.session_state.generate_response:
        with st.spinner("Consulting knowledge base..."):
            try:
                # Use the last message (which is the user's) as the prompt
                last_user_msg = st.session_state.messages[-1]["content"]
                
                n8n_webhook_url = "https://n8ngc.codeblazar.org/webhook/dengue-chatbot"
                
                response = requests.post(
                    n8n_webhook_url,
                    json={"question": last_user_msg},
                    timeout=30
                )
                response.raise_for_status()
                
                response_data = response.json()
                ai_reply = response_data.get("answer", 
                           response_data.get("output", 
                           response_data.get("text", "Sorry, I couldn't generate a response.")))
                
                if isinstance(ai_reply, dict):
                    ai_reply = str(ai_reply)

            except Exception as e:
                ai_reply = f"⚠️ Error contacting AI service: {e}"

            # Append AI reply
            st.session_state.messages.append({"role": "assistant", "content": ai_reply})
            
            # Turn off the flag
            st.session_state.generate_response = False
            
            # Rerun one last time to show the AI message in the list
            st.rerun()

    # Input Area - using chat input for better UX
    user_input = st.chat_input("Ask a question about dengue prevention...")
    
    # Submission Logic
    if user_input:
        # 1. Append User Message
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # 2. Set flag to generate response on next run
        st.session_state.generate_response = True
        
        # 3. Rerun immediately to update the chat window with user's message
        st.rerun()

# -------------------------------
# TAB 6 — SYMPTOM TRIAGE ASSISTANT
# -------------------------------

with tab_symptom:
    st.header("🩺 Symptom Triage Assistant")
    st.markdown("Use this AI assistant to check your symptoms and receive guidance.")
    
    # Use your verified Botpress shareable link
    bot_url = "https://cdn.botpress.cloud/webchat/v3.5/shareable.html?configUrl=https://files.bpcontent.cloud/2026/01/13/05/20260113053805-C6LOWMH2.json"
    
    # This renders the full Botpress window (logo and all) inside your tab
    components.iframe(bot_url, height=650, scrolling=True)

    st.warning("⚠️ **Medical Disclaimer:** This AI assistant is for triage guidance only.")




