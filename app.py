import os
import json
import datetime
import requests
import streamlit as st

# إعدادات الصفحة
st.set_page_config(
    page_title="أوريون الشام Enterprise",
    page_icon="⚜️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# الألوان والتنسيق
GOLD_MAIN = "#b9a779"
GOLD_HOVER = "#cbb98b"
BG_DARK = "#0d0f12"
CARD_BG = "#151821"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&display=swap');
    
    html, body, [class*="css"], .stApp {{
        font-family: 'Cairo', sans-serif !important;
        background-color: {BG_DARK} !important;
        color: #e2e8f0 !important;
    }}
    
    header[data-testid="stHeader"] {{
        background: transparent !important;
    }}

    section[data-testid="stSidebar"] {{
        background-color: #11131a !important;
        border-left: 1px solid rgba(185, 167, 121, 0.2) !important;
        min-width: 280px !important;
        max-width: 100vw !important;
    }}

    .stButton>button {{
        background: linear-gradient(135deg, {GOLD_MAIN} 0%, #9e8d63 100%) !important;
        color: #0d0f12 !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
        border: 1px solid {GOLD_HOVER} !important;
        padding: 0.5rem 1rem !important;
        transition: all 0.2s ease !important;
        width: 100%;
        font-family: 'Cairo', sans-serif !important;
    }}

    .stButton>button:hover {{
        background: linear-gradient(135deg, {GOLD_HOVER} 0%, {GOLD_MAIN} 100%) !important;
        box-shadow: 0 4px 15px rgba(185, 167, 121, 0.3) !important;
    }}

    div[data-testid="stChatMessage"] {{
        background-color: {CARD_BG} !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        margin-bottom: 0.8rem !important;
        border: 1px solid rgba(185, 167, 121, 0.15) !important;
    }}

    .stChatInputContainer textarea {{
        background-color: {CARD_BG} !important;
        color: #ffffff !important;
        border: 1px solid rgba(185, 167, 121, 0.35) !important;
        border-radius: 10px !important;
        font-family: 'Cairo', sans-serif !important;
    }}

    .gold-header {{
        color: {GOLD_MAIN} !important;
        font-weight: 800 !important;
        font-family: 'Cairo', sans-serif !important;
        word-break: break-word;
        line-height: 1.4 !important;
        margin-bottom: 0.5rem !important;
    }}

    .status-badge {{
        background: rgba(185, 167, 121, 0.12);
        color: {GOLD_MAIN};
        padding: 4px 12px;
        border-radius: 20px;
        border: 1px solid rgba(185, 167, 121, 0.3);
        font-size: 0.8rem;
        display: inline-block;
        margin-bottom: 1rem;
        font-weight: 600;
    }}

    @media (max-width: 768px) {{
        h1.gold-header {{ font-size: 1.4rem !important; }}
        h2.gold-header {{ font-size: 1.2rem !important; }}
        h4.gold-header {{ font-size: 1rem !important; }}
        div[data-testid="stChatMessage"] {{ padding: 0.75rem !important; }}
    }}

    code {{
        background-color: #1a1d27 !important;
        color: #e5c07b !important;
        border-radius: 6px !important;
        padding: 2px 6px !important;
    }}

    pre {{
        border: 1px solid rgba(185, 167, 121, 0.25) !important;
        border-radius: 10px !important;
        background-color: #12141d !important;
        overflow-x: auto !important;
    }}
</style>
""", unsafe_allow_html=True)

# جلب المفتاح
gemini_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

if not gemini_key:
    st.error("يرجى إضافة GEMINI_API_KEY في Streamlit Secrets للبدء.")
    st.stop()

# دالة الاستدعاء المباشر الذكية مع التراجع التلقائي
def call_gemini_api(prompt_text):
    headers = {'Content-Type': 'application/json'}
    payload = {
        "system_instruction": {
            "parts": [{
                "text": "أنت مساعد ذكي متطور ومستقل (أوريون الشام Enterprise). تتسم بالحكمة والدقة. تبرع في البرمجة النظيفة، كتابة الأكواد، والتفكير المنطقي باللغة العربية."
            }]
        },
        "contents": [{
            "parts": [{"text": prompt_text}]
        }]
    }

    # المحاولة الأولى: gemini-2.5-flash
    url_primary = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={gemini_key}"
    res = requests.post(url_primary, headers=headers, json=payload)
    
    if res.status_code == 200:
        return res.json()['candidates'][0]['content']['parts'][0]['text']

    # المحاولة الثانية في حال التعثر: gemini-1.5-flash عبر v1beta
    url_fallback = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}"
    res_fb = requests.post(url_fallback, headers=headers, json=payload)

    if res_fb.status_code == 200:
        return res_fb.json()['candidates'][0]['content']['parts'][0]['text']

    # إذا فشل كلاهما إظهار الخطأ المباشر
    raise Exception(f"خطأ ({res.status_code}): {res.text}")

if "messages" not in st.session_state:
    st.session_state.messages = []

# القائمة الجانبية
with st.sidebar:
    st.markdown("<h2 class='gold-header'>🏛️ أوريون الشام</h2>", unsafe_allow_html=True)
    st.markdown("<div class='status-badge'>⚜️ محرك Gemini المباشر المجاني</div>", unsafe_allow_html=True)
    
    st.divider()

    st.markdown("<h4 class='gold-header'>📄 إدارة المرفقات</h4>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "رفع ملف:",
        type=["txt", "py", "js", "html", "css", "json", "md"]
    )

    st.divider()

    st.markdown("<h4 class='gold-header'>⚙️ الجلسة</h4>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("جديد"):
            st.session_state.messages = []
            st.rerun()
            
    with col2:
        if st.session_state.messages:
            chat_text = "\n\n".join([f"{m['role'].upper()}: {m['content']}" for m in st.session_state.messages])
            st.download_button(
                label="تصدير",
                data=chat_text,
                file_name=f"export_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain"
            )

# واجهة الشات الرئيسية
st.markdown("<h1 class='gold-header'>⚜️ أوريون الشام Enterprise</h1>", unsafe_allow_html=True)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("أدخل استفسارك أو أمرك البرمجي هنا...")

if user_input:
    display_text = user_input
    file_context = ""

    if uploaded_file is not None:
        text_content = uploaded_file.read().decode("utf-8", errors="ignore")
        file_context = f"\n\n[محتوى الملف المرفق {uploaded_file.name}]:\n{text_content}"
        display_text += f"\n\n*[ملف مرفق: {uploaded_file.name}]*"

    st.session_state.messages.append({"role": "user", "content": display_text})
    with st.chat_message("user"):
        st.write(display_text)

    full_user_content = user_input + file_context

    with st.chat_message("assistant"):
        with st.spinner("جاري التفكير والمعالجة..."):
            try:
                bot_response = call_gemini_api(full_user_content)
                st.write(bot_response)
                st.session_state.messages.append({"role": "assistant", "content": bot_response})
            except Exception as e:
                st.error(f"حدث خطأ أثناء المعالجة: {e}")
