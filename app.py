import streamlit as st
import datetime
from google import genai
from google.genai import types

st.set_page_config(
    page_title="المساعد الذكي الشامل",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 المساعد الذكي الشخصي")
st.caption("مساعد متكامل لإدارة المهام، قراءة الصور والملفات، وإنشاء المستندات")

API_KEY = "AQ.Ab8RN6KrNkOzrtovH9kP_7xtQDY0FeZEgtvDvngHuKMTIdSPjw"
client = genai.Client(api_key=API_KEY)

def get_current_time() -> str:
    """ترجع الوقت والتاريخ الحاليين بدقة."""
    now = datetime.datetime.now()
    return f"الوقت والتاريخ الحالي: {now.strftime('%Y-%m-%d %H:%M:%S')}"

def create_and_save_file(file_name: str, text_content: str) -> str:
    """تنشئ ملفاً نصياً جديداً وتحفظ فيه المحتوى المقدم على جهاز المستخدم."""
    try:
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(text_content)
        return f"تم إنشاء الملف وحفظه بنجاح باسم: {file_name}"
    except Exception as e:
        return f"حدث خطأ أثناء حفظ الملف: {str(e)}"

my_tools = [get_current_time, create_and_save_file]

system_instruction = """
أنت مساعد ذكاء اصطناعي شخصي متقدم وقوي جداً.
تتحدث العربية بطلاقة وبأسلوب محترف ومفيد.
لديك أدوات تمكنك من معرفة الوقت الحالي وحفظ الملفات على الجهاز.
إذا طلب منك المستخدم كتابة تقرير أو كود أو نص وحفظه، قم بكتابة المحتوى واستخدم أداة create_and_save_file لحفظه تلقائياً.
يمكنك أيضاً تحليل ورؤية الصور والملفات المرفقة بدقة.
"""

MODEL_NAME = "gemini-3.6-flash"

if "chat" not in st.session_state:
    st.session_state.chat = client.chats.create(
        model=MODEL_NAME,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            tools=my_tools,
        )
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("📂 مرفقات وقدرات المساعد")
    uploaded_file = st.file_uploader(
        "ارفق صورة أو ملف نصي للمساعد:",
        type=["png", "jpg", "jpeg", "txt", "py", "js", "html", "css"]
    )
    if uploaded_file:
        st.success(f"تم تحميل: {uploaded_file.name}")

    if st.button("🗑️ مسح المحادثة وإعادة البدء"):
        st.session_state.messages = []
        st.session_state.chat = client.chats.create(
            model=MODEL_NAME,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                tools=my_tools,
            )
        )
        st.rerun()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("اكتب رسالتك أو أمرك هنا...")

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
            display_text += f"\n\n*[مرفق صورة: {uploaded_file.name}]*"
        else:
            text_content = file_bytes.decode("utf-8", errors="ignore")
            contents_to_send.append(f"\nمحتوى الملف المرفق ({uploaded_file.name}):\n{text_content}")
            display_text += f"\n\n*[مرفق ملف نصي: {uploaded_file.name}]*"

    st.session_state.messages.append({"role": "user", "content": display_text})
    with st.chat_message("user"):
        st.write(display_text)

    with st.chat_message("assistant"):
        with st.spinner("جاري التفكير وتنفيد المهمة..."):
            try:
                response = st.session_state.chat.send_message(contents_to_send)
                st.write(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"حدث خطأ: {e}")
