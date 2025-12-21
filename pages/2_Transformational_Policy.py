import streamlit as st
import google.generativeai as genai

# --- ۱. تنظیمات صفحه ---
st.set_page_config(page_title="طراحی سیاست نوآوری تحول‌آفرین", page_icon="🧬", layout="wide")

# --- ۲. تنظیمات گرافیکی (High Contrast Dark Mode) ---
st.markdown("""
<style>
    @import url('https://cdn.jsdelivr.net/gh/rastikerdar/vazir-font@v30.1.0/dist/font-face.css');
    
    /* اعمال فونت و راست‌چین کردن کل صفحه */
    html, body, [class*="css"] {
        font-family: 'Vazir', sans-serif !important;
        direction: rtl;
    }
    
    /* ۱. پس‌زمینه اصلی اپلیکیشن (خیلی تیره) */
    .stApp {
        background-color: #0e1117 !important; /* سیاه مایل به سرمه‌ای تیره */
        color: #ffffff !important; /* تمام متون پیش‌فرض سفید */
    }
    
    /* ۲. تیترها */
    h1, h2, h3, h4, h5, h6 {
        color: #f0f6fc !important; /* سفید یخی */
        border-bottom: 2px solid #30363d !important;
        padding-bottom: 10px;
    }
    
    /* ۳. متن‌های معمولی و لیبل‌ها */
    p, label, .stMarkdown {
        color: #e6edf3 !important; /* خاکستری خیلی روشن */
        font-size: 1.1rem !important; /* کمی درشت‌تر برای خوانایی موبایل */
    }

    /* ۴. کادرهای ورودی (TextArea) - اصلاح رنگ برای دیده شدن */
    .stTextArea textarea {
        background-color: #161b22 !important; /* تیره اما متفاوت از پس‌زمینه */
        color: #ffffff !important;
        border: 1px solid #7d8590 !important; /* حاشیه روشن برای دیده شدن مرزها */
        border-radius: 8px;
    }
    
    /* ۵. دکمه‌ها (High Contrast) */
    div.stButton > button {
        background-color: #238636 !important; /* سبز پررنگ و مشخص */
        color: #ffffff !important;
        font-weight: bold;
        border: 1px solid #2ea043 !important;
        border-radius: 8px;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #2ea043 !important;
        box-shadow: 0 0 10px rgba(46, 160, 67, 0.5);
    }

    /* ۶. باکس‌های پیام (Success/Info/Error) */
    .stAlert {
        background-color: #161b22 !important;
        color: #ffffff !important;
        border: 1px solid #30363d;
    }
    
    /* ۷. کادر دور نتایج (Expander) */
    .streamlit-expanderHeader {
        background-color: #21262d !important;
        color: #ffffff !important;
        border-radius: 5px;
    }
    
</style>
""", unsafe_allow_html=True)

# --- ۳. اتصال به هوش مصنوعی ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-flash-latest')
except Exception as e:
    st.error("⚠️ خطای اتصال به سرویس گوگل. لطفاً کلید API را بررسی کنید.")

# --- مدیریت وضعیت ---
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = ""
if 'final_mix' not in st.session_state:
    st.session_state.final_mix = ""

# --- ۴. بدنه اصلی برنامه ---
st.title("🧬 دستیار سیاست‌گذاری جهرمی")
st.markdown("---")

# --- مرحله ۱: دریافت ورودی‌ها ---
if st.session_state.step == 1:
    st.markdown("### 📝 گام اول: تعریف مسئله")
    st.info("لطفاً اطلاعات زیر را با دقت وارد کنید. تمام فیلدها برای تحلیل دقیق ضروری هستند.")
    
    col1, col2 = st.columns(2)
    with col1:
        problem = st.text_area("۱. مسئله یا چالش اصلی:", height=150, placeholder="مثال: آلودگی هوای کلان‌شهرها...")
    with col2:
        goals = st.text_area("۲. اهداف سیاستی:", height=150, placeholder="مثال: کاهش ۳۰ درصدی کربن...")
        
    context = st.text_area("۳. زمینه نهادی (قوانین و بازیگران):", height=100, placeholder="مثال: بودجه دولتی محدود است...")

    if st.button("🔍 تحلیل شکست‌ها و پیشنهاد اولیه"):
        if problem and goals and context:
            with st.spinner('در حال پردازش هوشمند...'):
                try:
                    prompt_analysis = f"""
                    شما متخصص سیاست‌گذاری هستید. بر اساس نظریه وبر و روراچر (Weber & Rohracher):
                    مسئله: {problem}
                    اهداف: {goals}
                    زمینه: {context}
                    
                    خروجی Markdown:
                    1. شناسایی شکست‌ها (بازار، سیستمی، تحولی)
                    2. ابزارهای پیشنهادی متناظر
                    """
                    response = model.generate_content(prompt_analysis)
                    st.session_state.analysis_result = response.text
                    st.session_state.step = 2
                    st.rerun()
                except Exception as e:
                    st.error(f"خطا: {e}")
        else:
            st.warning("لطفاً تمام فیلدها را پر کنید.")

# --- مرحله ۲: نمایش تحلیل و دریافت بازخورد ---
elif st.session_state.step == 2:
    st.markdown("### 📊 گام دوم: نتایج تحلیل اولیه")
    
    with st.expander("برای مشاهده گزارش کامل تحلیل اینجا کلیک کنید", expanded=True):
        st.markdown(st.session_state.analysis_result)
    
    st.markdown("---")
    st.markdown("### 💬 دریافت بازخورد نهایی")
    st.write("آیا محدودیتی (مثل بودجه یا مخالفت سیاسی) وجود دارد که باید در نظر گرفته شود؟")
    
    feedback = st.text_area("قیود و ملاحظات اجرایی:", height=100)
    
    c1, c2 = st.columns([1, 4])
    with c1:
        if st.button("🔙 بازگشت"):
            st.session_state.step = 1
            st.rerun()
    with c2:
        if st.button("💎 تدوین نهایی آمیخته سیاستی"):
            with st.spinner('در حال نهایی‌سازی...'):
                try:
                    prompt_final = f"""
                    بر اساس تحلیل قبلی: {st.session_state.analysis_result}
                    و بازخورد کاربر: {feedback}
                    یک آمیخته سیاستی نهایی تدوین کن.
                    """
                    response_final = model.generate_content(prompt_final)
                    st.session_state.final_mix = response_final.text
                    st.session_state.step = 3
                    st.rerun()
                except Exception as e:
                    st.error(f"خطا: {e}")

# --- مرحله ۳: خروجی نهایی ---
elif st.session_state.step == 3:
    st.success("سند نهایی آماده شد!")
    st.markdown("### 🏁 سند آمیخته سیاستی (Final Policy Mix)")
    
    # نمایش در کادر مجزا برای خوانایی بهتر در حالت دارک
    st.markdown(f"""
    <div style="background-color: #1c2128; padding: 20px; border-radius: 10px; border: 1px solid #444c56;">
        {st.session_state.final_mix}
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔄 شروع مجدد"):
        st.session_state.step = 1
        st.session_state.analysis_result = ""
        st.session_state.final_mix = ""
        st.rerun()
