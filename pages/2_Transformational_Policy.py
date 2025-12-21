import streamlit as st
import google.generativeai as genai
import pandas as pd

# --- ۱. تنظیمات صفحه ---
st.set_page_config(page_title="طراحی سیاست نوآوری تحول‌آفرین", page_icon="🧬", layout="wide")

# --- ۲. تنظیمات گرافیکی (هماهنگ با سایر صفحات) ---
st.markdown("""
<style>
    @import url('https://cdn.jsdelivr.net/gh/rastikerdar/vazir-font@v30.1.0/dist/font-face.css');
    
    html, body, [class*="css"] {
        font-family: 'Vazir', sans-serif !important;
        direction: rtl;
    }
    
    .stApp {
        background-color: #f8fafc;
    }
    
    h1, h2, h3 {
        color: #334155;
        border-bottom: 2px solid #e2e8f0;
        padding-bottom: 10px;
    }

    /* استایل مراحل */
    .step-container {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        border: 1px solid #e2e8f0;
    }

    div.stButton > button {
        background-color: #4f46e5; /* رنگ متفاوت برای تمایز */
        color: white;
        border-radius: 8px;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #4338ca;
    }
</style>
""", unsafe_allow_html=True)

# --- ۳. اتصال به هوش مصنوعی (Google Gemini) ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    # استفاده از همان مدل پروژه شما
    model = genai.GenerativeModel('gemini-flash-latest')
except Exception as e:
    st.error("⚠️ خطای اتصال به سرویس گوگل. لطفاً کلید API را بررسی کنید.")

# --- مدیریت وضعیت (Session State) برای مراحل ---
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = ""
if 'final_mix' not in st.session_state:
    st.session_state.final_mix = ""

# --- ۴. بدنه اصلی برنامه ---
st.title("🧬 دستیار سیاست‌گذاری نوآوری تحول‌آفرین")
st.markdown("مبتنی بر چارچوب **Weber & Rohracher (2012)** و **شکست‌های سیستمی**")

# --- مرحله ۱: دریافت ورودی‌ها ---
if st.session_state.step == 1:
    with st.container():
        st.markdown("### گام اول: تشریح مسئله و بستر نهادی")
        
        col1, col2 = st.columns(2)
        with col1:
            problem = st.text_area("الف) مسئله یا چالش اصلی:", height=150, placeholder="مثال: آلودگی هوای کلان‌شهرها و عدم موفقیت خودروهای برقی...")
        with col2:
            goals = st.text_area("ب) اهداف سیاستی مورد انتظار:", height=150, placeholder="مثال: کاهش ۳۰ درصدی کربن تا سال ۱۴۰۵...")
            
        context = st.text_area("ج) زمینه نهادی (قوانین موجود، بازیگران، قدرت چانه‌زنی):", height=100, placeholder="مثال: بودجه دولتی محدود است اما بخش خصوصی توانمند است...")

        if st.button("🔍 تحلیل شکست‌ها و پیشنهاد اولیه"):
            if problem and goals and context:
                with st.spinner('در حال تحلیل شکست‌های بازار، سیستمی و تحولی...'):
                    try:
                        # پرامپت تخصصی مرحله اول
                        prompt_analysis = f"""
                        شما یک متخصص ارشد سیاست‌گذاری علم و فناوری (STI Policy) هستید.
                        
                        ورودی‌ها:
                        - مسئله: {problem}
                        - اهداف: {goals}
                        - زمینه نهادی: {context}

                        وظیفه: تحلیل وضعیت بر اساس چارچوب "شکست‌های تحولی" (Weber & Rohracher) و "سیستم‌های نوآوری".
                        
                        خروجی را دقیقاً با ساختار زیر تولید کن:
                        1. **شناسایی شکست‌ها (Failures Identification):**
                           - **شکست بازار:** (مثل پیامدهای خارجی، اطلاعات نامتقارن)
                           - **شکست سیستمی:** (زیرساختی، نهادی، شبکه‌ای، قابلیت)
                           - **شکست تحولی:** (جهت‌گیری، هماهنگی سیاستی، شکل‌دهی تقاضا، بازتابندگی)
                        
                        2. **ابزارهای پیشنهادی اولیه:**
                           برای هر دسته شکست، ابزار متناسب (مقرراتی، اقتصادی، نرم) پیشنهاد بده.
                        
                        لحن: کاملاً آکادمیک و تخصصی.
                        """
                        
                        response = model.generate_content(prompt_analysis)
                        st.session_state.analysis_result = response.text
                        st.session_state.step = 2
                        st.rerun() # رفرش صفحه برای رفتن به مرحله بعد
                    except Exception as e:
                        st.error(f"خطا: {e}")
            else:
                st.warning("لطفاً تمام فیلدها را پر کنید.")

# --- مرحله ۲: نمایش تحلیل و دریافت بازخورد ---
elif st.session_state.step == 2:
    st.markdown("### گام دوم: تحلیل هوشمند و دریافت قیود")
    
    with st.expander("📄 مشاهده گزارش تحلیل شکست‌ها", expanded=True):
        st.markdown(st.session_state.analysis_result)
    
    st.info("با توجه به تحلیل بالا، آیا ملاحظات خاصی (بودجه، محدودیت سیاسی، ترجیحات ابزاری) دارید که باید در نسخه نهایی اعمال شود؟")
    
    feedback = st.text_area("بازخورد و قیود اجرایی شما:", height=100, placeholder="مثال: امکان وضع مالیات جدید وجود ندارد، روی ابزارهای تشویقی تمرکز کنید...")
    
    col_back, col_next = st.columns([1, 4])
    with col_back:
        if st.button("بازگشت"):
            st.session_state.step = 1
            st.rerun()
    with col_next:
        if st.button("💎 تدوین آمیخته سیاستی نهایی"):
            with st.spinner('در حال ترکیب ابزارها و رفع تضادهای سیاستی...'):
                try:
                    # پرامپت تخصصی مرحله دوم
                    prompt_final = f"""
                    شما مسئول تدوین "آمیخته سیاستی" (Policy Mix) نهایی هستید.
                    
                    تحلیل اولیه سیستم:
                    {st.session_state.analysis_result}
                    
                    قیود و بازخورد جدید کاربر:
                    {feedback}
                    
                    وظیفه: یک بسته سیاستی نهایی و سازگار تدوین کنید.
                    خروجی باید شامل:
                    1. **جدول آمیخته سیاستی:** (شامل هدف، ابزار، نوع ابزار)
                    2. **تحلیل هم‌افزایی و تضاد:** (آیا ابزارها همدیگر را خنثی می‌کنند یا تقویت؟)
                    3. **توصیه اجرایی:** گام اول اجرا چیست؟
                    """
                    
                    response_final = model.generate_content(prompt_final)
                    st.session_state.final_mix = response_final.text
                    st.session_state.step = 3
                    st.rerun()
                except Exception as e:
                    st.error(f"خطا: {e}")

# --- مرحله ۳: خروجی نهایی ---
elif st.session_state.step == 3:
    st.success("✅ سند آمیخته سیاستی با موفقیت تدوین شد.")
    
    st.markdown("### سند نهایی آمیخته سیاستی (Final Policy Mix)")
    st.markdown(st.session_state.final_mix)
    
    if st.button("🔄 شروع پروژه جدید"):
        st.session_state.step = 1
        st.session_state.analysis_result = ""
        st.session_state.final_mix = ""
        st.rerun()
