import streamlit as st
import google.generativeai as genai
import pandas as pd

# --- تنظیمات صفحه ---
st.set_page_config(page_title="طراحی آمیخته سیاستی", page_icon="📊", layout="wide")

# --- استایل (مشابه صفحه اصلی) ---
st.markdown("""
<style>
    @import url('https://cdn.jsdelivr.net/gh/rastikerdar/vazir-font@v30.1.0/dist/font-face.css');
    html, body, [class*="css"] { font-family: 'Vazir', sans-serif !important; direction: rtl; }
    .stApp { background-color: #f0f2f6; }
    h1 { color: #0f172a; text-align: center; border-bottom: 2px solid #334155; padding-bottom: 10px; }
    div.stButton > button { background-color: #0f766e; color: white; width: 100%; }
    div.stButton > button:hover { background-color: #0d9488; }
</style>
""", unsafe_allow_html=True)

# --- اتصال به گوگل ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-flash-latest')
except:
    st.error("کلید API یافت نشد.")

# --- عنوان ---
st.title("📊 مولد هوشمند آمیخته سیاستی (Policy Mix)")
st.info("این ابزار راهکارها را بر اساس دسته‌بندی استاندارد ابزارهای خط‌مشی عمومی تفکیک می‌کند.")

# --- ورودی ---
col1, col2 = st.columns([1, 2])
with col1:
    # استفاده از تصویر آنلاین برای زیبایی
    st.image("https://cdn-icons-png.flaticon.com/512/2620/2620542.png", width=100)
with col2:
    problem = st.text_area("شرح دقیق مسئله عمومی:", height=100, placeholder="مثال: نرخ بالای مصرف بنزین در ناوگان حمل و نقل...")

if st.button("🛠️ تدوین بسته سیاستی"):
    if problem:
        with st.spinner('در حال طراحی ابزارهای سیاستی...'):
            try:
                # پرامپت آکادمیک برای آمیخته سیاستی
                prompt = f"""
                به عنوان یک متخصص ارشد خط‌مشی‌گذاری عمومی، برای حل مسئله زیر، یک «آمیخته سیاستی» (Policy Mix) جامع تدوین کنید.
                مسئله: {problem}
                
                لطفاً پاسخ را دقیقاً در قالب جدول زیر و با ترمینولوژی آکادمیک ارائه دهید. 
                برای هر دسته، حداقل ۲ ابزار مشخص و اجرایی بنویسید.
                
                دسته‌بندی‌ها:
                1. **ابزارهای قانونی و تنظیمی (Regulatory/Stick):** (بایدها، نبایدها، استانداردها، جریمه‌ها)
                2. **ابزارهای اقتصادی و انگیزشی (Economic/Carrot):** (یارانه‌ها، مالیات‌ها، مشوق‌های بازار)
                3. **ابزارهای اطلاعاتی و فرهنگی (Information/Sermon):** (آگاهی‌بخشی، کمپین‌ها، شفافیت)
                4. **ابزارهای ساختاری و اجرایی (Organizational):** (تغییر فرایندها، دولت الکترونیک، زیرساخت)
                
                در پایان، یک پاراگراف کوتاه درباره «هم‌افزایی» (Synergy) بین این ابزارها بنویسید.
                """
                
                response = model.generate_content(prompt)
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"خطا: {e}")
    else:
        st.warning("لطفاً صورت مسئله را وارد کنید.")
