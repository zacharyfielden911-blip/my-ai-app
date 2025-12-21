import streamlit as st
import google.generativeai as genai
import pandas as pd

# --- ۱. تنظیمات صفحه ---
st.set_page_config(page_title="سامانه هوشمند سیاست‌گذاری", page_icon="🏛️", layout="centered")

# --- ۲. تنظیمات گرافیکی (CSS) ---
st.markdown("""
<style>
    /* فراخوانی فونت فارسی وزیر */
    @import url('https://cdn.jsdelivr.net/gh/rastikerdar/vazir-font@v30.1.0/dist/font-face.css');
    
    html, body, [class*="css"] {
        font-family: 'Vazir', sans-serif !important;
        direction: rtl;
    }
    
    /* رنگ پس‌زمینه */
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* تنظیمات تیترها */
    h1 {
        color: #1e3a8a; /* آبی نفتی */
        text-align: center;
        font-weight: bold;
        padding-bottom: 20px;
        border-bottom: 2px solid #e5e7eb;
        margin-bottom: 30px;
    }
    
    /* استایل دکمه */
    div.stButton > button {
        width: 100%;
        background-color: #2563eb;
        color: white;
        border-radius: 10px;
        padding: 10px;
        font-size: 18px;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #1d4ed8;
        transform: translateY(-2px);
    }
    
    /* کادر متن */
    .stTextArea textarea {
        border-radius: 10px;
        border: 1px solid #d1d5db;
        background-color: white;
    }
    
    /* کادر پاسخ */
    .stSuccess {
        background-color: #dcfce7;
        border-radius: 10px;
        padding: 15px;
        border-right: 5px solid #22c55e;
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
st.title("🏛️ یسامانه هوشمند سیاست‌گذاری جهرمی")
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
                prompt = f"""
                به عنوان یک مشاور ارشد سیاست‌گذاری عمومی، لطفاً مسئله زیر را تحلیل کنید.
                
                مسئله: {desc}
                
                لطفاً پاسخ را در قالب ساختار زیر ارائه دهید:
                ۱. 🎯 **تحلیل ریشه‌ای:** (کوتاه و دقیق)
                ۲. 💡 **راهکارهای کوتاه‌مدت:** (اجرایی و فوری)
                ۳. 💎 **راهکارهای بلندمدت:** (استراتژیک)
                
                لحن پاسخ: رسمی، مدیریتی و دلسوزانه.
                """
                
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

