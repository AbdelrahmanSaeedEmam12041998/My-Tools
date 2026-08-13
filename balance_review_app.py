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

# Session State
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "username" not in st.session_state: st.session_state.username = ""

# ==================== LOGIN ====================
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

# ==================== SIDEBAR ====================
current_user = USERS[st.session_state.username]
with st.sidebar:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        img_to_show = current_user["img"] if os.path.exists(current_user["img"]) else "damen_logo.png"
        try:
            image = Image.open(img_to_show)
            st.image(image, use_container_width=True)
        except:
            st.write("👤")
            
    st.markdown(f"<p style='text-align: center; color: #38bdf8; font-size: 16px; margin-top: 10px;'>{current_user['name']}</p>", unsafe_allow_html=True)
    
    if st.button("تسجيل الخروج"):
        st.session_state.logged_in = False
        st.rerun()
        
    st.markdown("---")
    selected_tool = st.radio("الأدوات:", ["📊 Balance Review", "🔍 Etisalat Checker", "⚡ Dispute Extractor"], label_visibility="collapsed")

# ==================== TOOLS (Logic) ====================
if selected_tool == "📊 Balance Review":
    st.title("📊 مراجعة أرصدة التجار (Balance Review)")
    st.markdown("<p style='direction: rtl; text-align: right; color: #64748b;'>أداة متطورة لمطابقة تقارير الحسابات اليومية واستخراج الـ Variance بدقة متناهية.</p>", unsafe_allow_html=True)
    st.markdown("---")

    col_input, col_results = st.columns([1, 1], gap="large")

    with col_input:
        st.markdown("<h3 style='direction: rtl; text-align: right;'>📥 مدخلات التقرير</h3>", unsafe_allow_html=True)
        input_text = st.text_area("ألصق نص التقرير هنا (Paste Report):", height=300, placeholder="قم بنسخ بيانات التقرير من النظام وألصقها هنا مباشرة...")
        calculate_btn = st.button("حساب ومراجعة الرصيد الآن", type="primary")

    with col_results:
        st.markdown("<h3 style='direction: rtl; text-align: right;'>📈 النتائج والتحليل المالي</h3>", unsafe_allow_html=True)
        
        if calculate_btn:
            if not input_text.strip():
                st.warning("⚠️ من فضلك ألصق التقرير في المربع المخصص أولاً.")
            else:
                def parse_report_data(text):
                    mapping = {
                        "الرصيد الافتتاحي": ("C5", "الرصيد الافتتاحي"),
                        "اضافة رصيد": ("C6", "إضافة رصيد"),
                        "استرجاع رصيد": ("C7", "استرجاع رصيد"),
                        "استرحاع رصيد": ("C7", "استرجاع رصيد"),
                        "اضافة عمولات": ("C8", "إضافة عمولات"),
                        "تصحيح بالاضافة": ("C9", "تصحيح بالإضافة"),
                        "تصحيح بالخصم": ("C10", "تصحيح بالخصم"),
                        "مدفوعات العملاء": ("C11", "مدفوعات العملاء"),
                        "الرصيد الختامي": ("C12", "الرصيد الختامي"),
                        "مبالغ تحت التسوية": ("C13", "مبالغ تحت التسوية"),
                        "مدفوعات كارت الائتمان": ("C14", "مدفوعات كارت الائتمان"),
                        "اضافة جوائز": ("C15", "إضافة جوائز"),
                        "غرامات عدم التحقيق": ("C16", "غرامات عدم التحقيق"),
                        "مصاريف صيانة": ("C17", "مصاريف صيانة"),
                        "ايداع اسمارت": ("C18", "إيداع اسمارت"),
                        "سحب علي المكشوف": ("C19", "سحب على المكشوف")
                    }
                    results = {}
                    raw_data = {}
                    for arabic_label, (key, label_name) in mapping.items():
                        pattern = re.escape(str(arabic_label)) + r"\s*:\s*\n?\s*(-?[\d\.]+)"
                        match = re.search(pattern, text)
                        if match:
                            try:
                                val = float(match.group(1))
                                results[key] = val
                                raw_data[label_name] = val
                            except ValueError:
                                pass
                        if key not in results:
                            results[key] = 0.0
                    return results, raw_data

                data, raw_data = parse_report_data(input_text)
                
                expected = (
                    data.get('C5', 0) + data.get('C6', 0) + data.get('C8', 0) + data.get('C9', 0) + 
                    data.get('C7', 0) + data.get('C15', 0) + data.get('C13', 0) - data.get('C10', 0) - 
                    data.get('C11', 0) + data.get('C19', 0) + data.get('C17', 0)
                )
                closing = data.get('C12', 0)
                variance = closing - expected
                overdraft = data.get('C19', 0)

                st.metric("الرصيد المتوقع (Expected Balance)", f"{expected:,.2f}")
                st.metric("الرصيد الختامي (Closing Balance)", f"{closing:,.2f}")
                st.metric("الفرق النهائي (Variance)", f"{variance:,.2f}")

                if abs(variance) > 0 and overdraft > 0 and abs(round(variance, 2)) == abs(round(overdraft, 2)):
                    st.success(f"✅ مفيش فرق حقيقي! الفرق ده بسبب إن التاجر سحب على المكشوف بقيمة ({overdraft:,.2f}) وهوا نفس مبلغ الفرق بالضبط.")
                elif abs(variance) == 0:
                    st.success("✅ المطابقة صحيحة تماماً ومفيش أي فروق!")
                else:
                    st.warning("⚠️ توجد فروق تتطلب المراجعة الفنية.")

                with st.expander("🔍 عرض تفاصيل بنود التقرير المستخرجة"):
                    for label, val in raw_data.items():
                        st.text(f"• {label} : {val}")
        else:
            st.info("👈 قم بلصق التقرير في المربع الجانبي ثم اضغط على زر الحساب لعرض النتائج هنا.")

elif selected_tool == "🔍 Etisalat Checker":
    st.title("🔍 Etisalat Transaction Checker")
    st.info("أداة مخصصة لفحص ومطابقة معاملات اتصالات قريباً...")

elif selected_tool == "⚡ Dispute Extractor":
    st.title("⚡ Dispute Extractor")
    st.markdown("<p style='direction: rtl; text-align: right; color: #64748b;'>أداة معالجة واستخراج تقارير الشكاوى (Complaint) والمطابقات (Reconciliation) تلقائياً.</p>", unsafe_allow_html=True)
    st.markdown("---")

    uploaded_file = st.file_uploader("اختر ملف الـ Excel:", type=["xlsx", "xls"])
    
    extraction_type = st.radio("اختر نوع التقرير المطلوب استخراجه:", ["Complaint", "Reconciliation"], horizontal=True)

    if uploaded_file is not None:
        try:
            df_dump = pd.read_excel(uploaded_file, sheet_name=0)
            
            if st.button("بدء المعالجة والاستخراج", type="primary"):
                processed_data = []
                
                for idx, row in df_dump.iterrows():
                    def get_val(col_name):
                        if col_name in df_dump.columns:
                            val = row[col_name]
                            return "" if pd.isna(val) else str(val).strip()
                        return ""

                    extra_info = get_val("معلومات_اضافيه")
                    ref_num = get_val("الرقم_المرجعي")
                    trx_date = get_val("تاريخ_الانشاء")
                    service_name = get_val("اسم_الخدمة")
                    op_num = get_val("رقم_العملية")
                    merchant_code = get_val("كود_التاجر")
                    merchant_name = get_val("اسم_التاجر")
                    gov_name = get_val("اسم_المحافظه")
                    status_val = get_val("حالة_العملية")
                    provider_name = get_val("مزود_الخدمة")
                    
                    # المنطق المحدث للـ Amount
                    base_provider = get_val("مزود_الخدمة_الاساسي")
                    val_basic = row["القيمه_الاساسية"] if "القيمه_الاساسية" in df_dump.columns and not pd.isna(row["القيمه_الاساسية"]) else 0
                    val_total = row["القيمه_الكليه"] if "القيمه_الكليه" in df_dump.columns and not pd.isna(row["القيمه_الكليه"]) else 0
                    
                    if "ADSL" in service_name.upper() and base_provider == "Bee Payment":
                        amount = val_basic
                    else:
                        amount = val_total

                    status_str = "فاشلة" if status_val in ["4", "4.0"] else ("ناجحة" if status_val in ["1", "1.0"] else "")

                    if extraction_type == "Complaint":
                        op_num_formatted = f"Damen{op_num}" if op_num else ""
                        row_dict = {
                            "Extra Info": extra_info,
                            "provider operation numb": ref_num,
                            "TRX date": trx_date,
                            "Amount": amount,
                            "operation number": op_num_formatted,
                            "service name": service_name,
                            "Merchant Code": merchant_code,
                            "Merchant Name": merchant_name,
                            "Gov": gov_name,
                            "Status": status_str
                        }
                    else:
                        ref_reco = ref_num if ref_num and ref_num.lower() != "empty" else extra_info
                        row_dict = {
                            "operation number": op_num,
                            "Extra Info": ref_reco,
                            "TRX date": trx_date,
                            "Amount": amount,
                            "service name": service_name,
                            "Provider": provider_name,
                            "Merchant Name": merchant_name,
                            "Status": status_str
                        }
                    
                    processed_data.append(row_dict)

                result_df = pd.DataFrame(processed_data)
                
                st.success(f"✅ تم معالجة واستخراج بيانات الـ {extraction_type} بنجاح!")
                st.dataframe(result_df, use_container_width=True)

                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    result_df.to_excel(writer, index=False, sheet_name=extraction_type)
                processed_excel = output.getvalue()

                # تقسيم الشاشة لأزرار التحميل والنسخ
                col_dl, col_cp = st.columns([1, 1])
                
                with col_dl:
                    st.download_button(
                        label=f"📥 تحميل ملف الـ {extraction_type} جاهز",
                        data=processed_excel,
                        file_name=f"{extraction_type}_Report.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )

                with col_cp:
                    cols_to_copy = [c for c in result_df.columns if c != "Status"]
                    text_to_copy = result_df[cols_to_copy].to_csv(sep='\t', index=False, header=False)
                    st.code(text_to_copy, language="text")
                    st.caption("👆 يمكنك الضغط على زر النسخ في أعلى المربع أعلاه لنسخ البيانات لحد قبل الـ Status مباشرة.")

        except Exception as e:
            st.error(f"حدث خطأ أثناء قراءة الملف: {e}")