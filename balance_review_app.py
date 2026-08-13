import streamlit as st
import pandas as pd
import re
import os
import io
import base64

# Page Configuration
st.set_page_config(page_title="Dispute App", page_icon="damen_logo.png", layout="wide")

# Custom CSS - ثيم ضامن (أزرق وبرتقالي) مع خلفية داكنة مريحة
st.markdown("""
    <style>
        .stApp { background-color: #001233; } /* خلفية داكنة احترافية */
        [data-testid="stSidebar"] { background-color: #001D3D; border-right: 4px solid #F97316; }
        .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; height: 45px; background-color: #F97316 !important; color: white !important; border: none; }
        .stButton>button:hover { background-color: #ea580c !important; }
        
        /* ضبط الخطوط والألوان داخل التطبيق */
        h1, h2, h3, p, label, div { color: #FFFFFF !important; font-family: sans-serif; }
        .stMetric { background-color: #003566 !important; padding: 15px; border-radius: 10px; border-bottom: 3px solid #F97316; }
        
        /* الصورة الشخصية */
        .circle-img { border-radius: 50%; border: 3px solid #F97316; width: 100px; height: 100px; object-fit: cover; display: block; margin: 0 auto 10px auto; }
        
        /* تنسيق المدخلات */
        .stTextArea textarea { background-color: #001D3D !important; color: #FFD60A !important; border: 1px solid #F97316 !important; }
    </style>
""", unsafe_allow_html=True)

# Users (كما هي)
USERS = {
    "abdelrahman.saeed@Damen.com.eg": {"password": "<E;;W3ky39h=du/", "name": "عبد الرحمن سعيد", "img": "abdelrahman.saeed@Damen.com.eg.png"}
}

if "logged_in" not in st.session_state: st.session_state.logged_in = False

# Login Page
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        # لوجو مستطيل
        if os.path.exists("damen_logo.png"):
            st.image("damen_logo.png", width=350) # حجم أكبر ومستطيل
        st.markdown("<h1 style='text-align: center; color: #F97316;'>Dispute App</h1>", unsafe_allow_html=True)
        
        login_user = st.text_input("البريد الإلكتروني")
        login_pass = st.text_input("كلمة المرور", type="password")
        if st.button("دخول"):
            if login_user in USERS and USERS[login_user]["password"] == login_pass:
                st.session_state.logged_in = True
                st.session_state.username = login_user
                st.rerun()
            else: st.error("بيانات الدخول غير صحيحة")
    st.stop()

# Sidebar
current_user = USERS[st.session_state.username]
with st.sidebar:
    img_path = current_user["img"]
    if os.path.exists(img_path):
        with open(img_path, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode()
            st.markdown(f'<img src="data:image/png;base64,{encoded}" class="circle-img">', unsafe_allow_html=True)
    
    st.markdown(f"<h3 style='text-align: center;'>{current_user['name']}</h3>", unsafe_allow_html=True)
    if st.button("تسجيل الخروج"):
        st.session_state.logged_in = False
        st.rerun()
    st.markdown("---")
    selected_tool = st.radio("الأدوات:", ["📊 Balance Review", "⚡ Dispute Extractor"])

# Tools Logic (باقي الكود كما هو)
if selected_tool == "📊 Balance Review":
    st.title("📊 مراجعة أرصدة التجار")
    # ... (باقي المنطق كما هو)
elif selected_tool == "⚡ Dispute Extractor":
    st.title("⚡ Dispute Extractor")
    # ... (باقي المنطق كما هو)
