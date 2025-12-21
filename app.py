import streamlit as st
import google.generativeai as genai
import pandas as pd

# --- ۱. تنظیمات صفحه ---
st.set_page_config(page_title="سامانه هوشمند سیاست‌گذاری", page_icon="🏛️", layout="centered")

# --- ۲. تنظیمات گرافیکی (یکپارچه با سایر صفحات - Dark Mode) ---
st.markdown("""
<style>
    /* فراخوانی فونت فارسی وزیر */
    @import url('https://cdn.jsdelivr.net/gh/rastikerdar/vazir-font@v30.1.0/dist/font-face.css');
    
    /* تنظیمات کلی صفحه و فونت */
    html, body, [class*="css"] {
        font-family: 'Vazir', sans-serif !important;
        direction: rtl;
    }
    
    /* ۱. پس‌زمینه اصلی (تیره و یکدست) */
    .stApp {
        background-color: #0e1117 !important;
        color: #ffffff !important;
    }
    
    /* ۲. تیترها (سفید یخی) */
    h1, h2, h3 {
        color: #f0f6fc !important;
        text-align: center;
        font-weight: bold;
        padding-bottom: 20px;
        border-bottom: 2px solid #30363d !important;
        margin-bottom: 30px;
    }
    
    /* ۳. متن‌های معمولی */
    p, label, .stMarkdown {
        color: #e6edf3 !important;
    }

    /* ۴. استایل دکمه‌ها (سبز پررنگ و مشخص) */
    div.stButton > button {
        width: 100%;
        background-color: #238636 !important;
        color: white !important;
        border-radius: 8px;
        padding: 10px;
        font-size: 18px;
        border: 1px solid #2ea043 !important;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #2ea043 !important;
        box-shadow: 0 0 10px rgba(46, 160, 67, 0.5);
        transform: translateY(-2px);
    }
    
    /* ۵. کادر متن (تیره با حاشیه روشن) */
    .stTextArea textarea {
        background-color: #161b22 !important;
        color: #ffffff !important;
        border: 1px solid #7d8590 !important;
        border-radius: 10px;
    }
    .stTextArea textarea:focus {
        border-color: #238636 !important;
        box-shadow: 0 0 0 1px #238636 !important;
    }
    
    /* ۶. کادر پاسخ و پیام‌ها (Success/Error) */
    .stSuccess, .stInfo, .stWarning, .stError {
        background-color: #161b22 !important;
        color: #ffffff !important;
        border-radius: 10px;
        padding: 15px;
        border: 1px solid #30363d !important;
    }
    /* خط رنگی کنار کادر ساکسس */
    .stSuccess {
        border-right: 5px solid #238636 !important;
    }
    
    /* ۷. استایل جداول (History) */
    div[data-testid="stTable"] {
        color: white !important;
    }
    th {
        background-color: #21262d !important;
        color: white !important;
    }
    td {
        background-color: #0e1117 !important;
        color: #e6edf3 !important;
    }

</style>
""", unsafe_allow_html=True)

# --- ۳. تنظیمات هوش مصنوعی ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-flash-latest')
except Exception as e:
    st.error("⚠️ خطای اتصال به سرویس گوگل. لطفاً کلید API را بررسی کنید.")

# --- ۴. بدنه اصلی برنامه ---
st.title("🏛️ سامانه هوشمند سیاست‌گذاری جهرمی")
st.write("لطفاً چالش یا مسئله مورد نظر را وارد کنید تا راهکار هوشمند دریافت نمایید:")

# حافظه موقت
if "history" not in st.session_state:
    st.session_state.history = []

# فرم ورودی
desc = st.text_area("شرح مسئله:", height=150, placeholder="مثال: کمبود بودجه در بخش حمل و نقل عمومی...")

if st.button("🔍 تحلیل و ارائه راهکار"):
    if desc:
        try:
            with st.spinner('در حال پردازش و تدوین سیاست‌های پیشنهادی...'):
                # پرامپت حرفه‌ای و رسمی
                # دقت کنید: اینجا با سه گیومه شروع می‌شود
                prompt = f"""
                به عنوان یک مشاور ارشد سیاست‌گذاری عمومی، لطفاً مسئله زیر را تحلیل کنید.
                
                مسئله: {desc}
                
                لطفاً پاسخ را در قالب ساختار زیر ارائه دهید:
                ۱. 🎯 **تحلیل ریشه‌ای:** (کوتاه و دقیق)
                ۲. 💡 **راهکارهای کوتاه‌مدت:** (اجرایی و فوری)
                ۳. 💎 **راهکارهای بلندمدت:** (استراتژیک)
                
                لحن پاسخ: رسمی، مدیریتی و دلسوزانه.
                """ 
                # دقت کنید: اینجا حتماً باید با سه گیومه بسته شود
                
                response = model.generate_content(prompt)
                
                st.markdown("### 📋 گزارش تحلیل هوشمند")
                st.success(response.text)
                
                # ذخیره در تاریخچه
                st.session_state.history.append({"مسئله": desc, "زمان": "جدید"})
        except Exception as e:
            st.error(f"خطا در دریافت پاسخ: {e}")
    else:
        st.warning("لطفاً ابتدا شرح مسئله را وارد نمایید.")

# نمایش تاریخچه ساده
if st.session_state.history:
    st.divider()
    with st.expander("📂 مشاهده سوابق جستجوهای این نشست"):
        df = pd.DataFrame(st.session_state.history)
        st.table(df)
