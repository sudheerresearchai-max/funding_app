import streamlit as st
import google.generativeai as genai
from datetime import datetime
import os

# --- Page Configuration ---
st.set_page_config(page_title="Startup Funding Aggregator", page_icon="🚀", layout="wide")

# --- 🔑 API KEY SECTION ---
# Your key is hardcoded here so you don't have to type it.
# ⚠️ IMPORTANT: Do NOT upload this specific file to GitHub, or your key will be leaked.
api_key = "AIzaSyD3bMsxHCxHgKDAVGdr7j7DoJyKN6AvAN0"

# --- Sidebar ---
with st.sidebar:
    st.header("⚙️ Settings")
    st.success("✅ API Key Loaded") 
    
    st.divider()
    sector = st.selectbox("Select Sector", ["AI", "Fintech", "SaaS", "Crypto", "Biotech", "General"])
    fetch_btn = st.button("Find Latest Funding 🚀", type="primary")

# --- Main Logic ---
def get_funding_news(api_key, sector):
    try:
        genai.configure(api_key=api_key)
        
        # Enable Google Search Tool (Grounding)
        tools = [
            {"google_search": {}} 
        ]
        model = genai.GenerativeModel('gemini-1.5-flash', tools=tools)
        
        today = datetime.now().strftime("%B %d, %Y")
        prompt = f"""
        Act as a VC Analyst. Search for the latest startup funding rounds in '{sector}' from the last 24 hours (Date: {today}).
        
        Format as a Markdown table: 
        | Startup | Amount | Round | Investor | Description |
        
        Then provide 3 bullet points on market trends.
        If no verified news is found today, write 'NO_NEWS_FOUND'.
        """
        
        with st.spinner(f"Scanning the web for {sector} deals..."):
            return model.generate_content(prompt)
            
    except Exception as e:
        return f"Error: {str(e)}"

# --- UI ---
st.title("🚀 Startup Funding News")
st.caption(f"Tracking real-time deals in: {sector}")

if fetch_btn:
    result = get_funding_news(api_key, sector)
    if isinstance(result, str): # Error caught
        st.error(result)
    else:
        st.markdown(result.text)
