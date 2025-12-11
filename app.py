import streamlit as st
import google.generativeai as genai
import csv
import os
from datetime import datetime
import pandas as pd
import bcrypt 

# --- 1. CONFIGURATION ---
# ध्यान दें: page_title और layout के बीच में comma (,) जरूरी है
st.set_page_config(page_title="fly2laksh", layout="wide")

# API KEY SETUP
try:
    # पहले secrets से key लेने की कोशिश करें
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    # अगर secrets काम न करे, तो error न आए इसलिए empty रखें या hardcode करें (Not Recommended for production)
    # st.error("Gemini API Key not found in Secrets!")
    GEMINI_API_KEY = "YOUR_FALLBACK_KEY_HERE" 

# अगर Key मिल गई हो तभी configure करें
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.0-flash')

# Files
LEADS_FILE = 'web_leads.csv'
RESUME_FILE = 'Business Plan.pdf' 
BANNER_IMAGE = 'banner.jpg'
USERS_FILE = 'user_data.csv' 

# Session State for Authentication Status
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_email' not in st.session_state:
    st.session_state.user_email = ""

# --- 2. SIDEBAR NAVIGATION ---
# Navigation code starts here...
