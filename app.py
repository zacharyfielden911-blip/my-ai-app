import streamlit as st
import google.generativeai as genai
import pandas as pd

# --- تنظیمات صفحه ---
st.set_page_config(page_title="دستیار هوشمند", direction="rtl")

# --- تنظیمات کلید (مخصوص فضای ابری) ---
# به جای نوشتن مستقیم کلید، آن را از بخش مخفی (Secrets) می‌خوانیم
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("کلید API پیدا نشد! لطفاً در تنظیمات Streamlit Cloud وارد کنید.")

# --- انتخاب مدل ---
# سرورهای خارجی به همه مدل‌ها دسترسی دارند، اما ما از نسخه مطمئن استفاده می‌کنیم
model = genai.GenerativeModel('gemini-1.5-flash')

# --- استایل راست‌چین ---
st.markdown("""
<style>
    .stApp {
        direction: rtl;
        text-align: right;
    }
    .stTextArea textarea {
        font-family: 'Tahoma', sans-serif;
        direction: rtl;
    }
</style>
""", unsafe_allow_html=True)

st.title("🌍 دستیار هوشمند (نسخه آنلاین)")

# --- حافظه ---
if "problems" not in st.session_state:
    st.session_state.problems = []

# --- ورودی ---
desc = st.text_area("مشکل خود را بنویسید:", height=150)

if st.button("دریافت راهکار"):
    if desc:
        try:
            with st.spinner('در حال تفکر...'):
                response = model.generate_content(f"به عنوان مشاور دانا، ۳ راهکار کوتاه و کاربردی برای این مشکل بده: {desc}")
                st.success("پاسخ:")
                st.write(response.text)
                st.session_state.problems.append(desc)
        except Exception as e:
            st.error(f"خطا: {e}")

# --- تاریخچه ---
if st.session_state.problems:
    st.divider()
    st.write("تاریخچه:")
    st.dataframe(pd.DataFrame(st.session_state.problems), use_container_width=True)