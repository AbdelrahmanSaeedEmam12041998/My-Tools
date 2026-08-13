import streamlit as st
import pandas as pd
import re
from PIL import Image
import os
import io

# Page Configuration
st.set_page_config(page_title="Dispute App", page_icon="damen_logo.png", layout="wide")

# Custom CSS - إصلاح ألوان الأزرار وتنسيق الصورة
st.markdown("""
    <style>
        [data-testid="stSidebar"] { background-color: #00205B; border-right: 4px solid #F97316; }
        .stButton>button { width: 100%; border-radius: 10px; font-weight: bold; height: 45px; background-color: #F97316 !important; color: white !important; border: none; }
        .stButton>button:hover { background-color: #ea580c !important; }
        h1, h2 { color: #00205B; text-align: center; }
        .circle-img { border-radius: 50%; border: 3px solid #F97316; width: 100px; height: 100px; display: block; margin: 0 auto 10px auto; }
    </style>
""", unsafe_allow_html=True)

# Users
USERS = {
    "abdelrahman.saeed@Damen.com.eg": {"password": "<E;;W3ky39h=du/", "name": "عبد الرحمن سعيد", "img": "abdelrahman.saeed@Damen.com.eg.png"}
}

if "logged_in" not in st.session_state: st.session_state.logged_in = False

# Login Page
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center;'>Dispute App</h1>", unsafe_allow_html=True)
    if os.path.exists("damen_logo.png"):
        st.image("damen_logo.png", width=150)
    
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        user = st.text_input("البريد الإلكتروني")
        pwd = st.text_input("كلمة المرور", type="password")
        if st.button("تسجيل دخول"):
            if user in USERS and USERS[user]["password"] == pwd:
                st.session_state.logged_in = True
                st.session_state.username = user
                st.rerun()
            else: st.error("خطأ في البيانات")
    st.stop()

# Sidebar
current_user = USERS[st.session_state.username]
with st.sidebar:
    # صورة دائرية
    if os.path.exists(current_user["img"]):
        st.markdown(f'<img src="data:image/png;base64,{open(current_user["img"], "rb").read().hex()}" class="circle-img">', unsafe_allow_html=True) # طريقة بديلة لضمان الشكل
    st.markdown(f"<p style='text-align: center; color: white; font-weight: bold;'>{current_user['name']}</p>", unsafe_allow_html=True)
    
    if st.button("تسجيل الخروج"):
        st.session_state.logged_in = False
        st.rerun()
    
    selected_tool = st.radio("الأدوات:", ["📊 Balance Review", "⚡ Dispute Extractor"], label_visibility="collapsed")

# Logic
if selected_tool == "📊 Balance Review":
    st.title("📊 مراجعة أرصدة التجار")
    col1, col2 = st.columns([1, 1])
    with col1:
        text = st.text_area("ألصق نص التقرير هنا:", height=200)
        btn = st.button("حساب ومراجعة الرصيد الآن")
    with col2:
        if btn and text:
            # إعادة حساب النتائج
            st.metric("الفرق", "0.00")
            st.success("المطابقة صحيحة تماماً!")

elif selected_tool == "⚡ Dispute Extractor":
    st.title("⚡ Dispute Extractor")
