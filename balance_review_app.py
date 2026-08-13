import streamlit as st
import pandas as pd
import re
import os
import io
import base64

# Page Configuration
st.set_page_config(
    page_title="Dispute App",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - ثيم فاتح احترافي
st.markdown("""
    <style>
        .stApp { background-color: #F8FAFC; color: #1E293B; }
        [data-testid="stSidebar"] { 
            background-color: #0A192F; 
            border-right: 4px solid #FF7700;
            direction: ltr; 
            text-align: center; 
        }
        [data-testid="stSidebar"] span, [data-testid="stSidebar"] p, [data-testid="stSidebar"] div { color: #FFFFFF !important; font-weight: 600 !important; }
        .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; height: 48px; background-color: #FF7700 !important; color: white !important; border: none; }
        .stButton>button:hover { background-color: #e56b00 !important; }
        div.stMetric { background-color: #FFFFFF; padding: 20px; border-radius: 12px; border: 1px solid #E2E8F0; border-right: 6px solid #FF7700; direction: rtl; text-align: right; }
        div.stMetric label { color: #64748B !important; }
        div.stMetric div[data-testid="stMetricValue"] { color: #0F172A !important; }
        h1, h2, h3, label { color: #0F172A !important; direction: rtl; text-align: right; font-family: 'Segoe UI', sans-serif; }
        .circle-img { border-radius: 50%; border: 3px solid #FF7700; width: 90px; height: 90px; object-fit: cover; display: block; margin: 10px auto; }
        .stTextArea textarea, .stTextInput input { background-color: #FFFFFF !important; color: #0F172A !important; border: 1px solid #CBD5E1 !important; border-radius: 8px !important; }
        /* شكل الرموز التعبيرية */
        .payment-icons { font-size: 50px; text-align: center; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# Users
USERS = {
    "a.mahmoud@Damen.com.eg": {"password": "+#8bD;,Z8zf0dY4", "name": "أحمد محمود", "img": "a.mahmoud@Damen.com.eg.png"},
    "abdelrahman.saeed@Damen.com.eg": {"password": "<E;;W3ky39h=du/", "name": "عبد الرحمن سعيد", "img": "abdelrahman.saeed@Damen.com.eg.png"},
    "mohamed.yahia@Damen.com.eg": {"password": "%'Pnw[15T[8\"1", "name": "محمد يحيى", "img": "mohamed.yahia@Damen.com.eg.png"}
}

if "logged_in" not in st.session_state: st.session_state.logged_in = False

# Login Page - بدون صورة، استبدالها بأيقونات مدفوعات
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown("<div style='height: 60px;'></div>", unsafe_allow_html=True)
        # رموز المدفوعات كـ تصميم
        st.markdown("<div class='payment-icons'>💳 💸 📱 🔐</div>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; color: #0F172A;'>Dispute App</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #64748B;'>نظام إدارة وتسوية المدفوعات الإلكترونية</p>", unsafe_allow_html=True)
        
        login_user = st.text_input("البريد الإلكتروني")
        login_pass = st.text_input("كلمة المرور", type="password")
        if st.button("دخول"):
            if login_user in USERS and USERS[login_user]["password"] == login_pass:
                st.session_state.logged_in = True
                st.session_state.username = login_user
                st.rerun()
            else: st.error("بيانات الدخول غير صحيحة")
    st.stop()

# (باقي منطق الأدوات كما هو في كودك الأخير)
