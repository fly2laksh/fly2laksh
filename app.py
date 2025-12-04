import streamlit as st
import google.generativeai as genai
import csv
import os
from datetime import datetime
import pandas as pd

# --- 1. SETTINGS & CONFIGURATION ---
st.set_page_config(page_title="fly2laksh AI", page_icon="🚀", layout="wide")

# Apni API Key Yahan Dalein
GEMINI_API_KEY = 'PASTE_YOUR_GOOGLE_API_KEY_HERE'
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

# Files Paths
LEADS_FILE = 'web_leads.csv'
RESUME_FILE = 'my_resume.pdf' # Make sure ye file uploaded ho
BANNER_IMAGE = 'banner.jpg'   # Make sure ye file uploaded ho

# --- 2. SIDEBAR MENU (Navigation) ---
with st.sidebar:
    # Logo/Image display
    if os.path.exists(BANNER_IMAGE):
        st.image(BANNER_IMAGE, use_column_width=True)
    else:
        st.title("🚀 fly2laksh")
    
    st.markdown("### Navigation")
    menu = st.radio("Go to:", ["🏠 Home (AI Chat)", "🛠 Services", "📂 Portfolio", "📞 Contact", "🔐 Admin Panel"])
    
    st.markdown("---")
    st.markdown("### About Us")
    st.info("We provide Data Cleaning, Automation, and Power BI solutions.")

# --- 3. FUNCTIONS (Backend Logic) ---

# Lead Save Karna (Web Form se)
def save_web_lead(name, contact, query):
    file_exists = os.path.isfile(LEADS_FILE)
    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(LEADS_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['Date', 'Name', 'Contact', 'Query'])
        writer.writerow([date_time, name, contact, query])

# AI Response Function
def get_gemini_response(prompt):
    try:
        # System instruction add kar rahe hain
        full_prompt = prompt + " (Answer professionally as fly2laksh AI Assistant. Keep it concise.)"
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return "Network Error. Please try again."

# --- 4. MAIN PAGE LOGIC ---

# === PAGE: HOME (CHAT) ===
if menu == "🏠 Home (AI Chat)":
    st.title("🤖 Chat with fly2laksh AI")
    st.write("Ask me anything about Data Analytics, Excel, or Power BI!")

    # Chat History Initialize (Memory)
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Purani Chat Dikhana
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User Input
    if prompt := st.chat_input("Type your question here..."):
        # 1. User ka message dikhao
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # 2. AI ka jawab lao
        response = get_gemini_response(prompt)

        # 3. AI ka message dikhao
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

# === PAGE: SERVICES ===
elif menu == "🛠 Services":
    st.title("📊 Our Services")
    st.write("We offer professional data solutions for your business.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("✅ Data Cleaning & Automation")
        st.success("✅ Power BI Dashboards")
        st.success("✅ Excel Reconciliation")
        st.success("✅ GST & Finance Data")
    
    with col2:
        st.info("✅ Zoho Setup")
        st.info("✅ Digital Marketing")
        st.info("✅ Data Migration")
        st.info("✅ Budgeting & Forecasting")

# === PAGE: PORTFOLIO ===
elif menu == "📂 Portfolio":
    st.title("📂 Our Work Portfolio")
    st.write("Download our resume and case studies below.")
    
    # Resume Download Button
    if os.path.exists(RESUME_FILE):
        with open(RESUME_FILE, "rb") as pdf_file:
            st.download_button(
                label="📥 Download Portfolio (PDF)",
                data=pdf_file,
                file_name="fly2laksh_Portfolio.pdf",
                mime="application/pdf"
            )
    else:
        st.warning("⚠️ Portfolio file is being uploaded.")

# === PAGE: CONTACT (Lead Form) ===
elif menu == "📞 Contact":
    st.title("📞 Get in Touch")
    
    # Smart Links
    st.markdown("""
    <a href="https://wa.me/918802355381" target="_blank"><button style="background-color:#25D366;color:white;border:none;padding:10px 20px;border-radius:5px;cursor:pointer;">💬 Chat on WhatsApp</button></a>
    &nbsp;
    <a href="https://www.linkedin.com/company/fly2laksh" target="_blank"><button style="background-color:#0077b5;color:white;border:none;padding:10px 20px;border-radius:5px;cursor:pointer;">🤝 LinkedIn</button></a>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("📩 Send us a Message (Lead Form)")
    
    # Form for Lead Collection
    with st.form("lead_form"):
        name = st.text_input("Your Name")
        contact = st.text_input("Email or Phone")
        query = st.text_area("How can we help you?")
        submitted = st.form_submit_button("🚀 Submit Request")
        
        if submitted:
            if name and contact:
                save_web_lead(name, contact, query)
                st.success(f"Thank you {name}! We have received your query.")
            else:
                st.error("Please fill Name and Contact details.")

# === PAGE: ADMIN PANEL (Secret) ===
elif menu == "🔐 Admin Panel":
    st.title("🔐 Admin Dashboard")
    
    # Simple Password Lock
    password = st.text_input("Enter Admin Password", type="password")
    
    if password == "laksh123":  # <--- Yahan apna password set karein
        st.success("Access Granted!")
        
        if os.path.exists(LEADS_FILE):
            st.subheader("📋 Recent Leads")
            # CSV file ko Table ki tarah dikhana
            df = pd.read_csv(LEADS_FILE)
            st.dataframe(df)
            
            # Download Button for CSV
            with open(LEADS_FILE, "rb") as f:
                st.download_button("📥 Download Leads CSV", f, file_name="leads.csv")
        else:
            st.info("No leads yet.")
    elif password:
        st.error("Wrong Password!")
