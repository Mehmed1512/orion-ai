import os
import json
import datetime
import requests
import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(
    page_title="أوريون الشام Enterprise",
    page_icon="⚜️",
    layout="wide",
    initial_sidebar_state="expanded"
)

GOLD_MAIN = "#b9a779"
GOLD_HOVER = "#cbb98b"
BG_DARK = "#0d0f12"
CARD_BG = "#151821"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Cairo:wght@300;400;600;700;900&display=swap');
    
    html, body, [class*="css"], .stApp {{
        font-family: 'Cairo', 'Amiri', sans-serif !important;
        background-color: {BG_DARK} !important;
        color: #e2e8f0 !important;
        direction: rtl;
    }}
    
    header[data-testid="stHeader"] {{
        background: transparent !important;
    }}

    section[data-testid="stSidebar"] {{
        background-color: #11131a !important;
        border-left: 1px solid rgba(185, 167, 121, 0.2) !important;
    }}

    .stButton>button {{
        background: linear-gradient(135deg, {GOLD_MAIN} 0%, #9e8d63 100%) !important;
        color: #0d0f12 !important;
        font-weight: 700 !important;
        border-radius: 10px !important;
        border: 1px solid {GOLD_HOVER} !important;
        padding: 0.65rem 1.25rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 15px rgba(185, 167, 121, 0.18) !important;
        width: 100%;
        font-family: 'Cairo', sans-serif !important;
    }}

    .stButton>button:hover {{
        background: linear-gradient(135deg, {GOLD_HOVER} 0%, {GOLD_MAIN} 100%) !important;
        box-shadow: 0 6px 22px rgba(185, 167, 121, 0.4) !important;
        transform: translateY(-2px);
    }}

    div[data-testid="stChatMessage"] {{
        background-color: {CARD_BG} !important;
        border-radius: 16px !important;
        padding: 1.35rem !important;
        margin-bottom: 1.1rem !important;
        border: 1px solid rgba(185, 167, 121, 0.15) !important;
        box-shadow: 0 4px 25px rgba(0, 0, 0, 0.3) !important;
    }}

    .stChatInputContainer textarea {{
        background-color: {CARD_BG} !important;
        color: #ffffff !important;
        border: 1px solid rgba(185, 167, 121, 0.35) !important;
        border-radius: 14px !important;
        font-family: 'Cairo', sans-serif !important;
    }}

    .stChatInputContainer textarea:focus {{
        border-color: {GOLD_MAIN} !important;
        box-shadow: 0 0 14px rgba(185, 167, 121, 0.35) !important;
    }}

    .gold-header {{
        color: {GOLD_MAIN} !important;
        font-weight: 800 !important;
        font-family: 'Amiri', serif !important;
        letter-spacing: 0px;
    }}

    .status-badge {{
        background: rgba(185, 167, 121, 0.12);
        color: {GOLD_MAIN};
        padding: 6px 16px;
        border-radius: 25px;
        border: 1px solid rgba(185, 167, 121, 0.3);
        font-size: 0.88rem;
        display: inline-block;
        margin-bottom: 1rem;
        font-weight: 600;
    }}

    code {{
        background-color: #1a1d27 !important;
        color: #e5c07b !important;
        border-radius: 6px !important;
        padding: 2px 6px !important;
        font-family: 'Courier New', monospace !important;
    }}

    pre {{
        border: 1px solid rgba(185, 167, 121, 0.25) !important;
        border-radius: 12px !important;
        background-color: #12141d !important;
    }}
</style>
""", unsafe_allow_html=True)

deepseek_key = st.secrets.get("DEEPSEEK_API_KEY") or os.environ.get("DEEPSEEK_API_KEY")
gemini_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

if not deepseek_key:
    st.error("يرجى إضافة DEEPSEEK_API_KEY في Streamlit Secrets للبدء.")
    st.stop()

def query_deepseek(messages_list):
    headers = {
        "Authorization": f"Bearer {deepseek_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek-chat",
        "messages": messages_list,
        "temperature": 0.7
    }
    response = requests.post("https://api.deepseek.com/v1/chat/completions", headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        raise Exception(f"خطأ المزود ({response.status_code}): {response.text}")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "api_history" not in st.session_state:
    st.session_state.api_history = [
        {
            "role": "system",
            "content": "أنت مساعد ذكي متطور ومستقل (أوريون الشام Enterprise). تتسم بالحكمة، الدقة، والأصالة الشامية. تبرع في البرمجة النظيفة، كتابة الأكواد، التفكير المنطقي، وتحليل النصوص بأسلوب راقٍ ومتقن باللغة العربية."
        }
    ]

with st.sidebar:
    st.markdown("<h2 class='gold-header'>🏛️ أوريون الشام</h2>", unsafe_allow_html=True)
    st.markdown("<div class='status-badge'>⚜️ محرك DeepSeek المطور v3.0</div>", unsafe_allow_html=True)
    
    st.divider()

    st.markdown("<h4 class='gold-header'>🖼️ توليد الصور الفنية</h4>", unsafe_allow_html=True)
    image_prompt = st.text_input("وصف اللوحة البصرية:", placeholder="اكتب وصف الصورة...")
    if st.button("توليد اللوحة البصرية"):
        if image_prompt and gemini_key:
            with st.spinner("جاري الرسم والتوليد..."):
                try:
                    g_client = genai.Client(api_key=gemini_key)
                    result = g_client.models.generate_images(
                        model='imagen-3.0-generate-002',
                        prompt=image_prompt,
                        config=types.GenerateImagesConfig(
                            number_of_images=1,
                            output_mime_type="image/jpeg",
                            aspect_ratio="1:1"
                        )
                    )
                    for generated_image in result.generated_images:
                        st.image(generated_image.image.image_bytes, caption=image_prompt, use_container_width=True)
                except Exception as e:
                    st.error(f"خطأ في توليد الصورة: {e}")
        elif not gemini_key:
            st.warning("يتطلب توليد الصور وجود GEMINI_API_KEY في Secrets.")
        else:
            st.warning("يرجى كتابة وصف الصورة أولاً.")

    st.divider()

    st.markdown("<h4 class='gold-header'>📄 إدارة الملفات والمرفقات</h4>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "ارفق ملف كود أو مستند نصي:",
        type=["txt", "py", "js", "html", "css", "json", "md"]
    )

    st.divider()

    st.markdown("<h4 class='gold-header'>⚙️ إدارة الجلسة</h4>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("جلسة جديدة"):
            st.session_state.messages = []
            st.session_state.api_history = [
                {
                    "role": "system",
                    "content": "أنت مساعد ذكي متطور ومستقل (أوريون الشام Enterprise). تتسم بالحكمة، الدقة، والأصالة الشامية. تبرع في البرمجة النظيفة، كتابة الأكواد، التفكير المنطقي، وتحليل النصوص بأسلوب راقٍ ومتقن باللغة العربية."
                }
            ]
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

st.markdown("<h1 class='gold-header'>⚜️ المساعد الذكي الفائق — أوريون الشام</h1>", unsafe_allow_html=True)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("أدخل استفسارك، أمرك البرمجي، أو مسألتك هنا...")

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
    st.session_state.api_history.append({"role": "user", "content": full_user_content})

    with st.chat_message("assistant"):
        with st.spinner("جاري المعالجة والتفكير بالذكاء الشامي..."):
            try:
                bot_response = query_deepseek(st.session_state.api_history)
                st.write(bot_response)
                st.session_state.messages.append({"role": "assistant", "content": bot_response})
                st.session_state.api_history.append({"role": "assistant", "content": bot_response})
            except Exception as e:
                st.error(f"حدث خطأ أثناء المعالجة: {e}")
