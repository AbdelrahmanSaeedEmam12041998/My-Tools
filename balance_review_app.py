import streamlit as st
import pandas as pd
import re
import os
import io
import base64

# Page Configuration
st.set_page_config(
    page_title="Dispute App",
    page_icon="damen_logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
        .main { background-color: #f8fafc; }
        [data-testid="stSidebar"] { 
            background-color: #00205B; 
            border-right: 3px solid #F97316;
            direction: ltr; 
            text-align: center; 
        }
        [data-testid="stSidebar"] span, [data-testid="stSidebar"] p, [data-testid="stSidebar"] div { color: #ffffff !important; font-weight: 600 !important; }
        .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; height: 48px; background-color: #F97316 !important; color: white !important; border: none; }
        .stButton>button:hover { background-color: #ea580c !important; }
        div.stMetric { background-color: #ffffff; padding: 20px; border-radius: 12px; border-left: 6px solid #F97316; direction: rtl; text-align: right; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); }
        h1, h2, h3 { color: #00205B; direction: rtl; text-align: right; }
        .circle-img { 
            border-radius: 50%; 
            border: 3px solid #F97316; 
            width: 90px; 
            height: 90px; 
            object-fit: cover; 
            display: block; 
            margin: 10px auto; 
        }
    </style>
""", unsafe_allow_html=True)

# Users
USERS = {
    "a.mahmoud@Damen.com.eg": {"password": "+#8bD;,Z8zf0dY4", "name": "أحمد محمود", "img": "a.mahmoud@Damen.com.eg.png"},
    "a.elkhodary@Damen.com.eg": {"password": "Nw1la9.B)|N[7WK", "name": "أحمد الخضري", "img": "a.elkhodary@Damen.com.eg.png"},
    "h.shouman@Damen.com.eg": {"password": "0ud0L7V'`:5PhKM", "name": "حسام شوتمان", "img": "h.shouman@Damen.com.eg.png"},
    "ahmed.kamal@Damen.com.eg": {"password": "7[s-2l6L@7YE%j7", "name": "أحمد كمال", "img": "ahmed.kamal@Damen.com.eg.png"},
    "barsom.naeem@Damen.com.eg": {"password": "Xhu\x80x6(#~C'", "name": "برسوم نعيم", "img": "barsom.naeem@Damen.com.eg.png"},
    "abdelrahman.saeed@Damen.com.eg": {"password": "<E;;W3ky39h=du/", "name": "عبد الرحمن سعيد", "img": "abdelrahman.saeed@Damen.com.eg.png"},
    "mohamed.yahia@Damen.com.eg": {"password": "%'Pnw[15T[8\"1", "name": "محمد يحيى", "img": "mohamed.yahia@Damen.com.eg.png"}
}

if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "username" not in st.session_state: st.session_state.username = ""

# Login Page
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        if os.path.exists("damen_logo.png"):
            st.image("damen_logo.png", width=140)
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
            encoded_img = base64.b64encode(img_file.read()).decode()
        st.markdown(f'<img src="data:image/png;base64,{encoded_img}" class="circle-img">', unsafe_allow_html=True)
    
    st.markdown(f"<p style='text-align: center; color: #ffffff; font-size: 16px; margin-top: 5px;'>{current_user['name']}</p>", unsafe_allow_html=True)
    
    if st.button("تسجيل الخروج"):
        st.session_state.logged_in = False
        st.rerun()
        
    st.markdown("---")
    selected_tool = st.radio("الأدوات:", ["📊 Balance Review", "⚡ Dispute Extractor"], label_visibility="collapsed")

# Tools Logic
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
                           "الرصيد الختامي": "C12", "مبالغ تحت التسوية": "C13", "اضافة جوائز": "C15", 
                           "مصاريف صيانة": "C17", "سحب علي المكشوف": "C19"}
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

            if variance == 0: st.success("✅ المطابقة صحيحة تماماً!")
            elif abs(variance) > 0 and overdraft > 0 and abs(variance) == abs(overdraft):
                st.success(f"✅ مفيش فرق حقيقي! بسبب سحب على المكشوف ({overdraft:,.2f}).")
            else: st.warning("⚠️ توجد فروق تتطلب المراجعة.")

elif selected_tool == "⚡ Dispute Extractor":
    st.title("⚡ Dispute Extractor")
    uploaded_file = st.file_uploader("اختر ملف الـ Excel:", type=["xlsx", "xls"])
    extraction_type = st.radio("النوع:", ["Complaint", "Reconciliation"], horizontal=True)

    if uploaded_file and st.button("بدء المعالجة", type="primary"):
        df_dump = pd.read_excel(uploaded_file)
        processed_data = []
        for _, row in df_dump.iterrows():
            service_name = str(row.get("اسم_الخدمة", "")).strip()
            amount = row.get("القيمه_الاساسية", 0) if "ADSL" in service_name.upper() and row.get("مزود_الخدمة_الاساسي") == "Bee Payment" else row.get("القيمه_الكليه", 0)
            
            processed_data.append({
                "operation number": str(row.get("رقم_العملية", "")),
                "Extra Info": str(row.get("معلومات_اضافيه", "")),
                "TRX date": str(row.get("تاريخ_الانشاء", "")),
                "Amount": str(amount),
                "service name": service_name,
                "Provider": str(row.get("مزود_الخدمة", "")),
                "Merchant Name": str(row.get("اسم_التاجر", "")),
                "Status": "فاشلة" if str(row.get("حالة_العملية")) in ["4", "4.0"] else "ناجحة"
            })

        result_df = pd.DataFrame(processed_data)
        st.dataframe(result_df, use_container_width=True)
        
        output = io.BytesIO()
        result_df.to_excel(output, index=False)
        st.download_button("📥 تحميل التقرير", output.getvalue(), f"{extraction_type}_Report.xlsx")
        st.code(result_df.drop(columns=["Status"]).to_csv(sep='\t', index=False, header=False), language="text")
