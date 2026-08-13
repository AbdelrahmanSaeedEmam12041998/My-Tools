import streamlit as st
import pandas as pd
import re
from PIL import Image
import os
import io

# Page Configuration
st.set_page_config(
    page_title="Dispute Unit Tools",
    page_icon="damen_logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
        .main { background-color: #f8fafc; }
        [data-testid="stSidebar"] { background-color: #0f172a; direction: ltr; text-align: center; }
        [data-testid="stSidebar"] span, [data-testid="stSidebar"] p, [data-testid="stSidebar"] div { color: #ffffff !important; font-weight: 600 !important; }
        .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; height: 48px; background-color: #f97316; color: white; border: none; }
        div.stMetric { background-color: #ffffff; padding: 20px; border-radius: 12px; border-left: 6px solid #f97316; direction: rtl; text-align: right; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); }
        h1, h2, h3 { color: #1e293b; direction: rtl; text-align: right; }
    </style>
""", unsafe_allow_html=True)

# ==================== USERS DATABASE ====================
USERS = {
    "a.mahmoud@Damen.com.eg": {"password": "+#8bD;,Z8zf0dY4", "name": "أحمد محمود", "img": "a.mahmoud@Damen.com.eg.png"},
    "a.elkhodary@Damen.com.eg": {"password": "Nw1la9.B)|N[7WK", "name": "أحمد الخضري", "img": "a.elkhodary@Damen.com.eg.png"},
    "h.shouman@Damen.com.eg": {"password": "0ud0L7V'`:5PhKM", "name": "حسام شوتمان", "img": "h.shouman@Damen.com.eg.png"},
    "ahmed.kamal@Damen.com.eg": {"password": "7[s-2l6L@7YE%j7", "name": "أحمد كمال", "img": "ahmed.kamal@Damen.com.eg.png"},
    "barsom.naeem@Damen.com.eg": {"password": "Xhu\\25A0x6(#~C'", "name": "برسوم نعيم", "img": "barsom.naeem@Damen.com.eg.png"},
    "abdelrahman.saeed@Damen.com.eg": {"password": "<E;;W3ky39h=du/", "name": "عبد الرحمن سعيد", "img": "abdelrahman.saeed@Damen.com.eg.png"},
    "mohamed.yahia@Damen.com.eg": {"password": "%'Pnw[15T[8\"1", "name": "محمد يحيى", "img": "mohamed.yahia@Damen.com.eg.png"}
}

if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "username" not in st.session_state: st.session_state.username = ""

if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("<h2 style='text-align: center;'>🛡️ تسجيل الدخول</h2>", unsafe_allow_html=True)
        login_user = st.text_input("البريد الإلكتروني")
        login_pass = st.text_input("كلمة المرور", type="password")
        if st.button("دخول"):
            if login_user in USERS and USERS[login_user]["password"] == login_pass:
                st.session_state.logged_in = True
                st.session_state.username = login_user
                st.rerun()
            else: st.error("بيانات الدخول غير صحيحة")
    st.stop()

current_user = USERS[st.session_state.username]
with st.sidebar:
    st.markdown(f"<p style='text-align: center; color: #38bdf8; font-size: 16px; margin-top: 10px;'>{current_user['name']}</p>", unsafe_allow_html=True)
    if st.button("تسجيل الخروج"):
        st.session_state.logged_in = False
        st.rerun()
    st.markdown("---")
    selected_tool = st.radio("الأدوات:", ["📊 Balance Review", "🔍 Etisalat Checker", "⚡ Dispute Extractor"], label_visibility="collapsed")

if selected_tool == "📊 Balance Review":
    st.title("📊 مراجعة أرصدة التجار")
    col_input, col_results = st.columns([1, 1], gap="large")
    with col_input:
        input_text = st.text_area("ألصق نص التقرير هنا:", height=300)
        calculate_btn = st.button("حساب ومراجعة الرصيد الآن", type="primary")
    with col_results:
        if calculate_btn:
            def parse_report_data(text):
                mapping = {"الرصيد الافتتاحي": "C5", "اضافة رصيد": "C6", "استرجاع رصيد": "C7", "استرحاع رصيد": "C7", 
                           "اضافة عمولات": "C8", "تصحيح بالاضافة": "C9", "تصحيح بالخصم": "C10", "مدفوعات العملاء": "C11",
                           "الرصيد الختامي": "C12", "مبالغ تحت التسوية": "C13", "مدفوعات كارت الائتمان": "C14", 
                           "اضافة جوائز": "C15", "غرامات عدم التحقيق": "C16", "مصاريف صيانة": "C17", 
                           "ايداع اسمارت": "C18", "سحب علي المكشوف": "C19"}
                results = {v: 0.0 for v in mapping.values()}
                for arabic_label, key in mapping.items():
                    match = re.search(re.escape(str(arabic_label)) + r"\s*:\s*\n?\s*(-?[\d\.]+)", text)
                    if match: results[key] = float(match.group(1))
                return results

            data = parse_report_data(input_text)
            expected = round(data['C5'] + data['C6'] + data['C8'] + data['C9'] + data['C7'] + data['C15'] + data['C13'] - data['C10'] - data['C11'] + data['C19'] + data['C17'], 2)
            closing = round(data['C12'], 2)
            variance = round(closing - expected, 2)
            overdraft = round(data['C19'], 2)

            st.metric("الرصيد المتوقع", f"{expected:,.2f}")
            st.metric("الرصيد الختامي", f"{closing:,.2f}")
            st.metric("الفرق النهائي", f"{variance:,.2f}")

            if variance == 0:
                st.success("✅ المطابقة صحيحة تماماً!")
            elif abs(variance) > 0 and overdraft > 0 and abs(variance) == abs(overdraft):
                st.success(f"✅ مفيش فرق حقيقي! بسبب سحب على المكشوف ({overdraft:,.2f}).")
            else:
                st.warning("⚠️ توجد فروق تتطلب المراجعة.")

elif selected_tool == "⚡ Dispute Extractor":
    st.title("⚡ Dispute Extractor")
    uploaded_file = st.file_uploader("اختر ملف الـ Excel:", type=["xlsx", "xls"])
    extraction_type = st.radio("النوع:", ["Complaint", "Reconciliation"], horizontal=True)

    if uploaded_file and st.button("بدء المعالجة", type="primary"):
        df_dump = pd.read_excel(uploaded_file, sheet_name=0)
        processed_data = []
        for _, row in df_dump.iterrows():
            service_name = str(row.get("اسم_الخدمة", "")).strip()
            base_provider = str(row.get("مزود_الخدمة_الاساسي", "")).strip()
            
            # Logic for amount
            if "ADSL" in service_name.upper() and base_provider == "Bee Payment":
                amount = row.get("القيمه_الاساسية", 0)
            else:
                amount = row.get("القيمه_الكليه", 0)

            row_dict = {
                "operation number": row.get("رقم_العملية"),
                "Extra Info": row.get("معلومات_اضافيه"),
                "TRX date": row.get("تاريخ_الانشاء"),
                "Amount": amount,
                "service name": service_name,
                "Provider": row.get("مزود_الخدمة"),
                "Merchant Name": row.get("اسم_التاجر"),
                "Status": "فاشلة" if row.get("حالة_العملية") in [4, "4"] else "ناجحة"
            }
            processed_data.append(row_dict)

        result_df = pd.DataFrame(processed_data)
        st.dataframe(result_df)
        
        # Download & Copy
        output = io.BytesIO()
        result_df.to_excel(output, index=False)
        st.download_button("📥 تحميل التقرير", output.getvalue(), f"{extraction_type}_Report.xlsx")
        
        # Copy logic (excluding Status)
        cols_to_copy = [c for c in result_df.columns if c != "Status"]
        st.code(result_df[cols_to_copy].to_csv(sep='\t', index=False, header=False), language="text")
