import streamlit as st
import google.generativeai as genai
import csv
import os
from datetime import datetime
import pandas as pd
import bcrypt # <-- नया

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="fly2laksh AI", page_icon="🚀", layout="wide")

# API KEY SETUP
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    # Testing key (Update with real key if needed locally)
    GEMINI_API_KEY = "AIzaSyDJyB6s935yO0XFyUoNGzjT7fYRZPk4M3I"

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

# Files
LEADS_FILE = 'web_leads.csv'
RESUME_FILE = 'Business Plan.pdf' 
BANNER_IMAGE = 'banner.jpg'
USERS_FILE = 'user_data.csv' # <-- नया

# Session State for Authentication Status
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_email' not in st.session_state:
    st.session_state.user_email = ""


# --- 2. SIDEBAR NAVIGATION ---
# Navigation केवल तभी दिखेगी जब यूज़र लॉग इन होगा
if st.session_state.logged_in:
    with st.sidebar:
        st.title("fly2laksh")
        st.write("Data Analytics & Automation Solutions")
        st.markdown("---")
        menu = st.radio("Navigation", 
            ["🏠 Home (AI Chat)", 
             "🛠 Services", 
             "📂 Portfolio", 
             "📞 Contact", 
             "🔐 Admin Panel"]
        )
        st.markdown("---")
        if st.button("🗑️ Clear Chat Memory"):
            st.session_state.chat_session = None
            st.session_state.messages = []
            st.rerun()
        if st.button("🔓 Logout"): # लॉगआउट बटन
            st.session_state.logged_in = False
            st.session_state.user_email = ""
            st.rerun()
else:
    # जब लॉग इन नहीं होता, तब साइडबार में केवल खाली जगह
    with st.sidebar:
        st.title("🔐 Portal Access")
        st.write("Please log in to continue.")
        menu = None # मेनू को None पर सेट करें


# --- 3. FUNCTIONS ---

def save_web_lead(name, contact, query):
    file_exists = os.path.isfile(LEADS_FILE)
    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LEADS_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['Date', 'Name', 'Contact', 'Query'])
        writer.writerow([date_time, name, contact, query])

# ----------------------------------------------------
# **नया फ़ंक्शन 1: यूज़र को रजिस्टर करने के लिए**
# ----------------------------------------------------
def register_user(email, password):
    file_exists = os.path.isfile(USERS_FILE)
    
    # पासवर्ड को हैश करें (सुरक्षा के लिए)
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    with open(USERS_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['email', 'hashed_password'])
        writer.writerow([email, hashed_password])
    return True

# ----------------------------------------------------
# **नया फ़ंक्शन 2: यूज़र को वेरिफाई करने के लिए**
# ----------------------------------------------------
def verify_user(email, password):
    if not os.path.exists(USERS_FILE):
        return False
    
    try:
        df = pd.read_csv(USERS_FILE)
    except pd.errors.EmptyDataError:
        return False 

    user_row = df[df['email'] == email]
    
    if not user_row.empty:
        stored_hash = user_row.iloc[0]['hashed_password'].encode('utf-8')
        return bcrypt.checkpw(password.encode('utf-8'), stored_hash)
    return False


# --- 4. PAGE CONTENT (LOGIN/APP LOGIC) ---

if st.session_state.logged_in:
    # ----------------------------------------------------
    # **अगर यूज़र LOGGED IN है, तो ही आपका मुख्य ऐप दिखेगा**
    # ----------------------------------------------------
        
    # === 🏠 HOME (CHAT WITH MEMORY) ===
    if menu == "🏠 Home (AI Chat)":
        st.title("fly2laksh")
        st.write(f"Welcome back, {st.session_state.user_email}! Ask me anything.") 

        # A. Session State Initialize (Memory Box)
        if "chat_session" not in st.session_state:
            st.session_state.chat_session = model.start_chat(history=[
                {
                    "role": "user",
                    "parts": ["You are the AI assistant for 'fly2laksh'. Answer professionally, concisely, and keep context in mind."]
                },
                {
                    "role": "model",
                    "parts": ["Understood. I am ready to assist as fly2laksh AI."]
                }
            ])
        
        # B. Display Message History (Screen par dikhana)
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # C. User Input & Logic
        if prompt := st.chat_input("Ex: What is Power BI?"):
            # 1. User ka message dikhao
            with st.chat_message("user"):
                st.markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})

            # 2. Gemini se jawab mango (With Memory)
            try:
                response = st.session_state.chat_session.send_message(prompt)
                ai_text = response.text
            except Exception as e:
                ai_text = "⚠️ Error: Please check API Key or Internet."

            # 3. AI ka message dikhao
            with st.chat_message("assistant"):
                st.markdown(ai_text)
            st.session_state.messages.append({"role": "assistant", "content": ai_text})

    # === 🛠 SERVICES ===
    elif menu == "🛠 Services":
        st.title("📊 Our Services")
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

    # === 📂 PORTFOLIO ===
    elif menu == "📂 Portfolio":
        st.title("📂 Work Portfolio")
        if os.path.exists(RESUME_FILE):
            with open(RESUME_FILE, "rb") as pdf_file:
                st.download_button(
                    label="📥 Download Resume / Portfolio (PDF)",
                    data=pdf_file,
                    file_name="fly2laksh_Portfolio.pdf",
                    mime="application/pdf"
                )
            st.success("Click above to download our latest work profile.")
        else:
            st.warning("⚠️ Portfolio file not found. Please upload 'Business Plan.pdf' to GitHub.")

    # === 📞 CONTACT ===
    elif menu == "📞 Contact":
        st.title("📞 Get in Touch")
        st.markdown("""
        <div style="display: flex; gap: 10px; flex-wrap: wrap;">
            <a href="https://wa.me/918802355381" target="_blank">
                <button style="background-color:#25D366;color:white;border:none;padding:10px 20px;border-radius:5px;">💬 WhatsApp</button>
            </a>
            <a href="https://www.linkedin.com/company/fly2laksh" target="_blank">
                <button style="background-color:#0077b5;color:white;border:none;padding:10px 20px;border-radius:5px;">🤝 LinkedIn</button>
            </a>
            <a href="mailto:fly2laksh@gmail.com">
                <button style="background-color:#EA4335;color:white;border:none;padding:10px 20px;border-radius:5px;">📧 Email</button>
            </a>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.subheader("📩 Send us a Query")
        with st.form("contact_form"):
            name = st.text_input("Name")
            contact = st.text_input("Email / Phone")
            msg = st.text_area("Message")
            btn = st.form_submit_button("🚀 Submit")
            if btn:
                if name and contact:
                    save_web_lead(name, contact, msg)
                    st.success("Thanks! We will contact you soon.")
                else:
                    st.error("Please fill details.")

    # === 🔐 ADMIN ===
    elif menu == "🔐 Admin Panel":
        st.title("🔐 Admin Login")
        # यहां आपको Admin पासवर्ड को भी bcrypt से चेक करना चाहिए, 
        # लेकिन simplicity के लिए इसे अभी के लिए ऐसे ही छोड़ देते हैं।
        pwd = st.text_input("Password", type="password")
        if pwd == "laksh123":
            st.success("Access Granted")
            if os.path.exists(LEADS_FILE):
                df = pd.read_csv(LEADS_FILE)
                st.dataframe(df)
                with open(LEADS_FILE, "rb") as f:
                    st.download_button("📥 Download Leads CSV", f, file_name="web_leads.csv")
            else:
                st.info("No leads yet.")
        else:
            st.warning("Incorrect Password.")
        
else:
    # ----------------------------------------------------
    # **अगर यूज़र LOGGED IN नहीं है, तो लॉगिन/रजिस्ट्रेशन फॉर्म दिखेगा**
    # ----------------------------------------------------
    st.title("🔐 Welcome to fly2laksh AI Portal")
    st.info("Please Login or Register to access the bot and services.")
    
    col_log, col_reg = st.columns(2)
    
    # 1. LOGIN FORM
    with col_log:
        st.subheader("Existing User Login")
        with st.form("login_form"):
            login_email = st.text_input("Email", key="l_email")
            login_pwd = st.text_input("Password", type="password", key="l_pwd")
            login_btn = st.form_submit_button("🔑 Login")
            
            if login_btn:
                if verify_user(login_email, login_pwd):
                    st.session_state.logged_in = True
                    st.session_state.user_email = login_email
                    st.success("Login Successful!")
                    st.rerun()
                else:
                    st.error("Invalid Email or Password.")

    # 2. REGISTRATION FORM
    with col_reg:
        st.subheader("New User Registration")
        with st.form("register_form"):
            reg_email = st.text_input("Email (Required)", key="r_email")
            reg_pwd = st.text_input("Password (Required)", type="password", key="r_pwd")
            reg_pwd_confirm = st.text_input("Confirm Password", type="password", key="r_pwd_c")
            reg_btn = st.form_submit_button("📝 Register")
            
            if reg_btn:
                if not reg_email or not reg_pwd or not reg_pwd_confirm:
                    st.error("Please fill all fields.")
                elif reg_pwd != reg_pwd_confirm:
                    st.error("Passwords do not match.")
                elif os.path.exists(USERS_FILE):
                    df_users = pd.read_csv(USERS_FILE)
                    if reg_email in df_users['email'].values:
                        st.error("This email is already registered. Please login.")
                        st.stop()
                
                register_user(reg_email, reg_pwd)
                st.success("Registration successful! Please login now.")
