import streamlit as st
import google.generativeai as genai
import pandas as pd

# --- ۱. تنظیمات صفحه ---
st.set_page_config(page_title="طراحی آمیخته سیاستی", page_icon="📊", layout="wide")

# --- ۲. تنظیمات گرافیکی (تم تاریک و یکپارچه) ---
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
    
    /* ۲. تیترها */
    h1, h2, h3 {
        color: #f0f6fc !important;
        text-align: center;
        border-bottom: 2px solid #30363d !important;
        padding-bottom: 10px;
        margin-bottom: 30px;
    }
    
    /* ۳. متن‌های معمولی */
    p, label, .stMarkdown {
        color: #e6edf3 !important;
    }

    /* ۴. استایل دکمه‌ها (سبز - هماهنگ با سایر صفحات) */
    div.stButton > button {
        width: 100%;
        background-color: #238636 !important;
        color: white !important;
        border-radius: 8px;
        padding: 10px;
        font-size: 16px;
        border: 1px solid #2ea043 !important;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #2ea043 !important;
        box-shadow: 0 0 10px rgba(46, 160, 67, 0.5);
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

    /* ۶. پیام‌های اطلاعاتی (Info Box) */
    .stInfo {
        background-color: #161b22 !important;
        color: #e6edf3 !important;
        border: 1px solid #30363d !important;
    }
    
    /* ۷. تنظیم تصویر (کمی فاصله و سایه) */
    img {
        margin-top: 10px;
        filter: drop-shadow(0 0 5px rgba(255,255,255,0.1));
    }
</style>
""", unsafe_allow_html=True)

# --- ۳. اتصال به گوگل ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-flash-latest')
except Exception as e:
    st.error("⚠️ کلید API یافت نشد یا ارتباط برقرار نیست.")

# --- ۴. بدنه اصلی برنامه ---
st.title("📊 مولد هوشمند آمیخته سیاستی (Policy Mix)")
st.info("این ابزار راهکارها را بر اساس دسته‌بندی استاندارد ابزارهای خط‌مشی عمومی (NATO) تفکیک می‌کند.")

# --- ورودی ---
col1, col2 = st.columns([1, 4]) # نسبت ستون‌ها را اصلاح کردم تا فضا بهتر استفاده شود

with col1:
    # تصویر تزیینی
    st.image("https://cdn-icons-png.flaticon.com/512/2620/2620542.png", width=120)

with col2:
    problem = st.text_area("شرح دقیق مسئله عمومی:", height=130, placeholder="مثال: نرخ بالای مصرف بنزین در ناوگان حمل و نقل...")

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
                
                دسته‌بندی‌ها (مدل NATO):
                1. **ابزارهای قانونی و تنظیمی (Nodality/Regulatory):** (بایدها، نبایدها، استانداردها، جریمه‌ها)
                2. **ابزارهای اقتصادی و انگیزشی (Treasure/Economic):** (یارانه‌ها، مالیات‌ها، مشوق‌های بازار)
                3. **ابزارهای اطلاعاتی و فرهنگی (Information/Sermon):** (آگاهی‌بخشی، کمپین‌ها، شفافیت)
                4. **ابزارهای ساختاری و اجرایی (Organization):** (تغییر فرایندها، دولت الکترونیک، زیرساخت)
                
                در پایان، یک پاراگراف کوتاه درباره «هم‌افزایی» (Synergy) بین این ابزارها بنویسید.
                """
                
                response = model.generate_content(prompt)
                
                st.markdown("### 📋 نتایج طراحی آمیخته سیاستی")
                # نمایش نتیجه در کادر مخصوص برای خوانایی بهتر در تم تاریک
                st.markdown(f"""
                <div style="background-color: #161b22; padding: 20px; border-radius: 10px; border: 1px solid #30363d;">
                    {response.text}
                </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"خطا: {e}")
    else:
        st.warning("لطفاً ابتدا شرح مسئله را وارد کنید.")
