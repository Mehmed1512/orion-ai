import os
import json
import datetime
import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(
    page_title="Orion AI Enterprise",
    page_icon="⚜️",
    layout="wide",
    initial_sidebar_state="expanded"
)

GOLD_MAIN = "#b9a779"
GOLD_HOVER = "#cbb98b"
BG_DARK = "#0b0c10"
CARD_BG = "#13151c"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;900&display=swap');
    
    html, body, [class*="css"], .stApp {{
        font-family: 'Cairo', sans-serif !important;
        background-color: {BG_DARK} !important;
        color: #e0e6ed !important;
    }}
    
    header[data-testid="stHeader"] {{
        background: transparent !important;
    }}

    section[data-testid="stSidebar"] {{
        background-color: #0f1117 !important;
        border-right: 1px solid rgba(185, 167, 121, 0.15) !important;
    }}

    .stButton>button {{
        background: linear-gradient(135deg, {GOLD_MAIN} 0%, #a39266 100%) !important;
        color: #0a0b0e !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 0.6rem 1.2rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 14px rgba(185, 167, 121, 0.15) !important;
        width: 100%;
    }}

    .stButton>button:hover {{
        background: linear-gradient(135deg, {GOLD_HOVER} 0%, {GOLD_MAIN} 100%) !important;
        box-shadow: 0 6px 20px rgba(185, 167, 121, 0.35) !important;
        transform: translateY(-2px);
    }}

    div[data-testid="stChatMessage"] {{
        background-color: {CARD_BG} !important;
        border-radius: 14px !important;
        padding: 1.25rem !important;
        margin-bottom: 1rem !important;
        border: 1px solid rgba(185, 167, 121, 0.12) !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25) !important;
    }}

    .stChatInputContainer textarea {{
        background-color: {CARD_BG} !important;
        color: #ffffff !important;
        border: 1px solid rgba(185, 167, 121, 0.3) !important;
        border-radius: 12px !important;
        font-family: 'Cairo', sans-serif !important;
    }}

    .stChatInputContainer textarea:focus {{
        border-color: {GOLD_MAIN} !important;
        box-shadow: 0 0 12px rgba(185, 167, 121, 0.3) !important;
    }}

    .gold-header {{
        color: {GOLD_MAIN} !important;
        font-weight: 800 !important;
        letter-spacing: -0.5px;
    }}

    .status-badge {{
        background: rgba(185, 167, 121, 0.1);
        color: {GOLD_MAIN};
        padding: 4px 12px;
        border-radius: 20px;
        border: 1px solid rgba(185, 167, 121, 0.2);
        font-size: 0.85rem;
        display: inline-block;
        margin-bottom: 1rem;
    }}

    code {{
        background-color: #1a1d26 !important;
        color: #e5c07b !important;
        border-radius: 6px !important;
        padding: 2px 6px !important;
    }}

    pre {{
        border: 1px solid rgba(185, 167, 121, 0.2) !important;
        border-radius: 10px !important;
        background-color: #161822 !important;
    }}
</style>
""", unsafe_allow_html=True)

api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("المفتاح غير معرّف في النظام.")
    st.stop()

client = genai.Client(api_key=api_key)

def get_current_time() -> str:
    now = datetime.datetime.now()
    return f"الوقت والتاريخ الحالي: {now.strftime('%Y-%m-%d %H:%M:%S')}"

def create_and_save_file(file_name: str, text_content: str) -> str:
    try:
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(text_content)
        return f"تم حفظ الملف بنجاح باسم: {file_name}"
    except Exception as e:
        return f"حدث خطأ أثناء حفظ الملف: {str(e)}"

my_tools = [get_current_time, create_and_save_file]

system_instruction = """
أنت نظام ذكاء اصطناعي متطور جداً (Orion AI Enterprise).
تتميز بالدقة الفائقة في تحليل الأكواد البرمجية، الكتابة العالية الجودة، ومعالجة المستندات والصور.
قم بتقديم إجابات موثوقة، أنيقة، ومنسقة بأعلى المعايير المهنية باللغة العربية.
"""

MODEL_NAME = "gemini-3.6-flash"

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat" not in st.session_state:
    st.session_state.chat = client.chats.create(
        model=MODEL_NAME,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            tools=my_tools,
        )
    )

with st.sidebar:
    st.markdown("<h2 class='gold-header'>⚜️ Orion AI</h2>", unsafe_allow_html=True)
    st.markdown("<div class='status-badge'>النظام الذكي المطور v2.0</div>", unsafe_allow_html=True)
    
    st.divider()

    st.markdown("<h4 class='gold-header'>🎨 توليد الصور الفنية</h4>", unsafe_allow_html=True)
    image_prompt = st.text_input("الوصف البصري:", placeholder="اكتب وصف الصورة...")
    if st.button("توليد الصورة"):
        if image_prompt:
            with st.spinner("جاري معالجة الطلب..."):
                try:
                    result = client.models.generate_images(
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
                    st.error(f"خطأ: {e}")

    st.divider()

    st.markdown("<h4 class='gold-header'>📁 إدارة المرفقات</h4>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "رفع مستند أو صورة:",
        type=["png", "jpg", "jpeg", "txt", "py", "js", "html", "css", "json"]
    )

    st.divider()

    st.markdown("<h4 class='gold-header'>⚙️ الجلسة</h4>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("جلسة جديدة"):
            st.session_state.messages = []
            st.session_state.chat = client.chats.create(
                model=MODEL_NAME,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    tools=my_tools,
                )
            )
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

st.markdown("<h1 class='gold-header'>المساعد الذكي الفائق</h1>", unsafe_allow_html=True)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("أدخل استفسارك أو أمرك البرمجي هنا...")

if user_input:
    display_text = user_input
    contents_to_send = [user_input]

    if uploaded_file is not None:
        file_bytes = uploaded_file.read()
        file_type = uploaded_file.type
        
        if "image" in file_type:
            contents_to_send.append(
                types.Part.from_bytes(data=file_bytes, mime_type=file_type)
            )
            display_text += f"\n\n*[صورة مرفقة: {uploaded_file.name}]*"
        else:
            text_content = file_bytes.decode("utf-8", errors="ignore")
            contents_to_send.append(f"\nمحتوى الملف المرفق ({uploaded_file.name}):\n{text_content}")
            display_text += f"\n\n*[ملف مرفق: {uploaded_file.name}]*"

    st.session_state.messages.append({"role": "user", "content": display_text})
    with st.chat_message("user"):
        st.write(display_text)

    with st.chat_message("assistant"):
        with st.spinner("جاري التحليل والتنفيد..."):
            try:
                response = st.session_state.chat.send_message(contents_to_send)
                st.write(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"خطأ في التنفيذ: {e}")
