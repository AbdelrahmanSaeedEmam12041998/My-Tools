import streamlit as st
import pandas as pd
import re
from PIL import Image, ImageOps
import os
import io

# Page Configuration
st.set_page_config(page_title="Dispute App", page_icon="damen_logo.png", layout="wide")

# Custom CSS for "Damen" Theme & Circular Images
st.markdown("""
    <style>
        [data-testid="stSidebar"] { 
            background-color: #00205B; 
            border-right: 2px solid #F97316;
        }
        .css-1544g2n { padding-top: 1rem; }
        .stButton>button { width: 100%; border-radius: 20px; font-weight: bold; background-color: #F97316; color: white; border: none; }
        h1, h2 { color: #00205B; text-align: center; }
        .circle-img { border-radius: 50%; border: 3px solid #F97316; display: block; margin: auto; width: 120px; height: 120px; object-fit: cover; }
    </style>
""", unsafe_allow_html=True)

# Users
USERS = {
    "abdelrahman.saeed@Damen.com.eg": {"password": "<E;;W3ky39h=du/", "name": "عبد الرحمن سعيد", "img": "abdelrahman.saeed@Damen.com.eg.png"}
}

if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "username" not in st.session_state: st.session_state.username = ""

# Login Page
if not st.session_state.logged_in:
    # عرض لوجو ضامن في صفحة الدخول
    if os.path.exists("damen_logo.png"):
        st.image("damen_logo.png", width=150)
    st.markdown("<h1 style='color: #F97316;'>Dispute App</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
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
    # صورة دائرية
    img_path = current_user["img"] if os.path.exists(current_user["img"]) else "damen_logo.png"
    image = Image.open(img_path)
    # تعديل الصورة لتكون دائرية
    st.image(image, width=120, output_format="PNG", caption=None, use_container_width=False)
    st.markdown(f"<p style='text-align: center; color: white; font-weight: bold;'>{current_user['name']}</p>", unsafe_allow_html=True)
    
    if st.button("تسجيل الخروج"):
        st.session_state.logged_in = False
        st.rerun()
    st.markdown("---")
    selected_tool = st.radio("الأدوات:", ["📊 Balance Review", "🔍 Etisalat Checker", "⚡ Dispute Extractor"], label_visibility="collapsed")

# Tools (Same logic as before)
if selected_tool == "📊 Balance Review":
    st.title("📊 مراجعة أرصدة التجار")
    col1, col2 = st.columns([1, 1])
    with col1:
        input_text = st.text_area("ألصق نص التقرير:", height=300)
        if st.button("حساب ومراجعة"):
            # ... (باقي منطق الحساب كما هو) ...
            st.success("تمت العملية!")

elif selected_tool == "⚡ Dispute Extractor":
    st.title("⚡ Dispute Extractor")
    # ... (باقي كود الـ Extractor) ...
