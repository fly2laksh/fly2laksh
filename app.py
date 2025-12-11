import streamlit as st
import google.generativeai as genai
import os
import sys

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="fly2laksh AI Assistant", layout="wide")

# API Key Loading (Secure method for Streamlit Cloud)
try:
    # Key Streamlit Cloud secrets se load hogi
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except KeyError:
    # Agar key nahi mili to app ko rok dein
    st.error("Error: Gemini API Key not found in Secrets. Please set 'GEMINI_API_KEY' in Streamlit Cloud settings.")
    st.stop()

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am your AI Business Assistant. How can I help you today?"}
    ]
    
# --- 2. STREAMLIT UI ---
st.title("Fly2laksh Simple AI Assistant")
st.caption("Ask me anything about Excel, Data, or Business Logic.")

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 3. INPUT AND AI RESPONSE LOGIC ---
if prompt := st.chat_input("Say something..."):
    # 1. User message display aur history me add karna
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. AI Response generate karna
    with st.spinner("Thinking..."):
        try:
            # History ko Gemini format me taiyar karna
            history = [{"role": msg["role"], "parts": [msg["content"]]} for msg in st.session_state.messages]
            
            # Response generate karna
            response = model.generate_content(history)
            ai_response = response.text
            
        except Exception as e:
            ai_response = "Sorry, I ran into an error. Please try again. (API issue)"
            
    # 3. AI response ko history me add karna aur display karna
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
    with st.chat_message("assistant"):
        st.markdown(ai_response)
