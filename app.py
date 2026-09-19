import os
import json
import datetime
import streamlit as st
from google import genai
from google.genai import types

# ---------------------------------------------------------
# 1. إعداد الصفحة والتصميم الهيكلي
# ---------------------------------------------------------
st.set_page_config(
    page_title="المساعد الذكي الفاخر",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# 2. تطبيق الهوية البصرية بالألوان المطلوبة (#b9a779)
# ---------------------------------------------------------
GOLD_ACCENT = "#b9a779"

custom_css = f"""
<style>
    /* خلفية الصفحة والعناصر العامة */
    .stApp {{
        background-color: #0f1117;
        color: #e0e0e0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}
    
    /* القائمة الجانبية */
    section[data-testid="stSidebar"] {{
        background-color: #161922 !important;
        border-left: 1px solid rgba(185, 167, 121, 0.2);
    }}

    /* الأزرار الرئيسية باللون الذهبي */
    .stButton>button {{
        background-color: {GOLD_ACCENT} !important;
        color: #111111 !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        border: none !important;
        transition: all 0.3s ease !important;
    }}
    
    .stButton>button:hover {{
        background-color: #cbb98b !important;
        box-shadow: 0 4px 12px rgba(185, 167, 121, 0.3) !important;
        transform: translateY(-1px);
    }}

    /* إدخال المحادثة */
    .stChatInputContainer textarea {{
        border: 1px solid {GOLD_ACCENT} !important;
        background-color: #1a1d26 !important;
        color: #ffffff !important;
        border-radius: 10px !important;
    }}

    /* فقاعات المحادثة */
    div[data-testid="stChatMessage"] {{
        background-color: #1a1d27;
        border-radius: 12px;
        padding: 12px 16px;
        margin-bottom: 10px;
        border: 1px solid rgba(185, 167, 121, 0.15);
    }}

    /* عناوين اللوحات */
    h1, h2, h3, .gold-text {{
        color: {GOLD_ACCENT} !important;
    }}

    /* محرر الأكواد */
    pre code {{
        border-radius: 8px !important;
        border: 1px solid rgba(185, 167, 121, 0.3) !important;
    }}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. إعداد الاتصال بـ Gemini API
# ---------------------------------------------------------
api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("لم يتم العثور على API Key! يرجى إضافته في Streamlit Secrets باسم GEMINI_API_KEY.")
    st.stop()

client = genai.Client(api_key=api_key)

# ---------------------------------------------------------
# 4. الأدوات الجانبية وإدارة الجلسات
# ---------------------------------------------------------
def get_current_time() -> str:
    """ترجع الوقت والتاريخ الحاليين بدقة."""
    now = datetime.datetime.now()
    return f"الوقت والتاريخ الحالي: {now.strftime('%Y-%m-%d %H:%M:%S')}"

def create_and_save_file(file_name: str, text_content: str) -> str:
    """تنشئ ملفاً نصياً جديداً وتحفظ فيه المحتوى المقدم."""
    try:
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(text_content)
        return f"تم حفظ الملف بنجاح باسم: {file_name}"
    except Exception as e:
        return f"حدث خطأ أثناء حفظ الملف: {str(e)}"

my_tools = [get_current_time, create_and_save_file]

system_instruction = """
أنت مساعد ذكاء اصطناعي محترف ومتقدم جداً.
الميزات الأساسية التي تقدمها:
1. البرمجة المتقدمة: عند كتابة أي كود برمجي، قدم خوارزميات نظيفة (Clean Code)، موثقة بتعليقات، واستخدم أفضل الممارسات البرمجية.
2. معالجة الصور والتوليد: لديك القدرة على قراءة وتحليل الصور بدقة، واقتراح تحسينات عليها.
3. التفاعل الاحترافي باللغة العربية بأسلوب فخم ومنسق.
4. حفظ واستخراج البيانات والملفات حسب طلب المستخدم.
"""

MODEL_NAME = "gemini-3.6-flash"

# إدارة جلسات السجل (History)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

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

# ---------------------------------------------------------
# 5. القائمة الجانبية (Sidebar & Controls)
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("<h2 class='gold-text'>👑 المساعد الذكي</h2>", unsafe_allow_html=True)
    st.caption("نظام المحادثات المتطور وتوليد الصور")
    
    st.divider()

    # خيار توليد الصور
    st.markdown("<h4 class='gold-text'>🎨 توليد وتحسين الصور</h4>", unsafe_allow_html=True)
    image_prompt = st.text_input("وصف الصورة المراد توليدها:")
    if st.button("✨ توليد الصورة"):
        if image_prompt:
            with st.spinner("جاري رسم وتوليد الصورة..."):
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
                    st.error(f"حدث خطأ أثناء توليد الصورة: {e}")
        else:
            st.warning("يرجى كتابة وصف للصورة أولاً.")

    st.divider()

    # مرفقات الصور والملفات
    st.markdown("<h4 class='gold-text'>📂 المرفقات وتحليل الأكواد</h4>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "رفع صورة أو ملف برمجي/نصي:",
        type=["png", "jpg", "jpeg", "txt", "py", "js", "html", "css", "json"]
    )

    st.divider()

    # إدارة المحادثات والذاكرة
    st.markdown("<h4 class='gold-text'>💾 إدارة المحادثة</h4>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ محادثة جديدة"):
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
        # تصدير المحادثة الحالية
        if st.session_state.messages:
            chat_text = "\n\n".join([f"{m['role'].upper()}: {m['content']}" for m in st.session_state.messages])
            st.download_button(
                label="📥 تصدير",
                data=chat_text,
                file_name=f"chat_history_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain"
            )

# ---------------------------------------------------------
# 6. الواجهة الرئيسية واستعراض المحادثة
# ---------------------------------------------------------
st.markdown("<h1 class='gold-text'>✨ المساعد البرمجي والشخصي</h1>", unsafe_allow_html=True)

# عرض الرسائل السابقة
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# مدخل الرسالة الرئيسية
user_input = st.chat_input("اكتب سؤالك، كودك البرمجي، أو طلبك هنا...")

if user_input:
    display_text = user_input
    contents_to_send = [user_input]

    # لمعالجة المرفق إن وجد
    if uploaded_file is not None:
        file_bytes = uploaded_file.read()
        file_type = uploaded_file.type
        
        if "image" in file_type:
            contents_to_send.append(
                types.Part.from_bytes(data=file_bytes, mime_type=file_type)
            )
            display_text += f"\n\n*[مرفق صورة: {uploaded_file.name}]*"
        else:
            text_content = file_bytes.decode("utf-8", errors="ignore")
            contents_to_send.append(f"\nمحتوى الملف المرفق ({uploaded_file.name}):\n{text_content}")
            display_text += f"\n\n*[مرفق ملف: {uploaded_file.name}]*"

    st.session_state.messages.append({"role": "user", "content": display_text})
    with st.chat_message("user"):
        st.write(display_text)

    with st.chat_message("assistant"):
        with st.spinner("جاري التفكير ومعالجة الطلب..."):
            try:
                response = st.session_state.chat.send_message(contents_to_send)
                st.write(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"حدث خطأ أثناء معالجة الطلب: {e}")
