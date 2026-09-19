import os
import json
import datetime
import requests
import streamlit as st

# ============================================================
#  إعدادات الصفحة
# ============================================================
st.set_page_config(
    page_title="أوريون الشام Enterprise",
    page_icon="⚜️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
#  نظام الألوان والهوية البصرية
# ============================================================
GOLD_MAIN   = "#c9b37e"
GOLD_HOVER  = "#e0cc96"
GOLD_SOFT   = "#d8c79a"
BG_DARK     = "#0b0d11"
CARD_BG     = "#151924"
CARD_BG_2   = "#1b2130"
BORDER_GOLD = "rgba(201, 179, 126, 0.22)"
TEXT_MAIN   = "#e8eaf0"
TEXT_MUTED  = "#9aa3b2"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700;800;900&display=swap');

    /* ---------- الخط الأساسي (بدون تحديد شامل مفرط) ---------- */
    html, body, .stApp {{
        font-family: 'Cairo', 'Segoe UI', Tahoma, sans-serif !important;
        line-height: 1.7 !important;
    }}
    .stApp p, .stApp span, .stApp li, .stApp label,
    .stApp input, .stApp textarea, .stApp button,
    .stApp [data-testid="stMarkdownContainer"] {{
        font-family: 'Cairo', 'Segoe UI', Tahoma, sans-serif !important;
    }}

    .stApp {{
        background:
            radial-gradient(1200px 600px at 85% -10%, rgba(201,179,126,0.07), transparent 60%),
            radial-gradient(900px 500px at -10% 110%, rgba(201,179,126,0.05), transparent 55%),
            {BG_DARK} !important;
        color: {TEXT_MAIN} !important;
    }}

    header[data-testid="stHeader"] {{
        background: transparent !important;
    }}

    /* ---------- الشريط الجانبي ---------- */
    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #10131b 0%, #0d1017 100%) !important;
        border-left: 1px solid {BORDER_GOLD} !important;
    }}

    /* ---------- العناوين (لون ذهبي صلب بدون قص الخلفية) ---------- */
    .gold-header {{
        color: {GOLD_MAIN} !important;
        font-weight: 800 !important;
        line-height: 1.6 !important;
        margin: 0 0 0.5rem 0 !important;
        display: block !important;
        letter-spacing: 0.2px;
    }}
    h1.gold-header {{ font-size: 1.8rem !important; }}
    h2.gold-header {{ font-size: 1.4rem !important; }}
    h4.gold-header {{ font-size: 1.05rem !important; }}

    .status-badge {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(74, 222, 128, 0.08);
        color: #4ade80;
        border: 1px solid rgba(74, 222, 128, 0.25);
        padding: 4px 14px;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 600;
        line-height: 1.5;
    }}
    .status-badge::before {{
        content: "";
        width: 7px; height: 7px;
        border-radius: 50%;
        background: #4ade80;
        box-shadow: 0 0 8px #4ade80;
        animation: pulse-dot 2s infinite;
        flex-shrink: 0;
    }}
    @keyframes pulse-dot {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.35; }}
    }}

    /* ---------- الأزرار ---------- */
    .stButton>button {{
        background: linear-gradient(135deg, {GOLD_MAIN} 0%, #a08c5e 100%) !important;
        color: #0d0f12 !important;
        font-weight: 700 !important;
        border-radius: 10px !important;
        border: 1px solid {GOLD_HOVER} !important;
        transition: all 0.18s ease !important;
        width: 100%;
        line-height: 1.5 !important;
        white-space: normal !important;
        height: auto !important;
        min-height: 2.5rem;
    }}
    .stButton>button:hover {{
        background: linear-gradient(135deg, {GOLD_HOVER} 0%, {GOLD_MAIN} 100%) !important;
        box-shadow: 0 4px 18px rgba(201, 179, 126, 0.35) !important;
    }}

    .stDownloadButton>button {{
        background: transparent !important;
        color: {GOLD_MAIN} !important;
        border: 1px solid {BORDER_GOLD} !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        width: 100%;
        line-height: 1.5 !important;
        white-space: normal !important;
        height: auto !important;
        min-height: 2.5rem;
    }}
    .stDownloadButton>button:hover {{
        background: rgba(201, 179, 126, 0.1) !important;
    }}

    /* ---------- فاصل أنيق (محصور بكلاس لن يكسر عناصر أخرى) ---------- */
    .stApp hr {{
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent, {BORDER_GOLD}, transparent) !important;
        margin: 1rem 0 !important;
    }}

    /* ---------- رسائل المحادثة ---------- */
    div[data-testid="stChatMessage"] {{
        background: {CARD_BG} !important;
        border-radius: 14px !important;
        padding: 0.9rem 1.1rem !important;
        margin-bottom: 0.7rem !important;
        border: 1px solid rgba(255,255,255,0.06) !important;
        overflow-wrap: break-word !important;
    }}
    div[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p {{
        line-height: 1.8 !important;
        margin-bottom: 0.6rem !important;
    }}

    /* ---------- حقل الإدخال ---------- */
    .stChatInputContainer textarea {{
        background: {CARD_BG_2} !important;
        color: {TEXT_MAIN} !important;
        border: 1px solid {BORDER_GOLD} !important;
        border-radius: 14px !important;
        caret-color: {GOLD_MAIN} !important;
        line-height: 1.7 !important;
    }}
    .stChatInputContainer textarea:focus {{
        border-color: {GOLD_MAIN} !important;
        box-shadow: 0 0 0 3px rgba(201,179,126,0.12) !important;
    }}

    /* ---------- السلايدرز والقوائم ---------- */
    div[data-testid="stSlider"] [data-baseweb="slider"] div[role="slider"] {{
        background-color: {GOLD_MAIN} !important;
        border-color: {GOLD_HOVER} !important;
    }}
    div[data-testid="stSlider"] [data-baseweb="slider"] > div > div:first-child {{
        background: linear-gradient(90deg, #8f7d52, {GOLD_MAIN}) !important;
    }}

    section[data-testid="stFileUploaderDropzone"] {{
        background-color: {CARD_BG_2} !important;
        border: 1px dashed {BORDER_GOLD} !important;
        border-radius: 12px !important;
    }}

    /* ---------- الأكواد ---------- */
    code {{
        background-color: #1c2233 !important;
        color: #e8c47c !important;
        border-radius: 6px !important;
        padding: 2px 7px !important;
        font-size: 0.88em;
    }}
    pre {{
        border: 1px solid {BORDER_GOLD} !important;
        border-radius: 12px !important;
        background-color: #101421 !important;
        overflow-x: auto !important;
    }}

    /* ---------- Expander ---------- */
    .stApp details {{
        background: {CARD_BG} !important;
        border: 1px solid rgba(255,255,255,0.07) !important;
        border-radius: 12px !important;
    }}
    .stApp details summary {{
        font-weight: 700 !important;
        color: {GOLD_MAIN} !important;
        line-height: 1.6 !important;
    }}

    /* ============================================================
       التجاوب مع الشاشات
       ============================================================ */
    .block-container {{
        max-width: 960px !important;
        padding-top: 1.5rem !important;
        padding-bottom: 5rem !important;
    }}

    @media (max-width: 1024px) {{
        .block-container {{ max-width: 100% !important; }}
    }}

    @media (max-width: 768px) {{
        section[data-testid="stSidebar"] {{
            min-width: 0 !important;
            width: 84vw !important;
        }}
        .block-container {{
            padding-left: 0.9rem !important;
            padding-right: 0.9rem !important;
        }}
        h1.gold-header {{ font-size: 1.35rem !important; }}
        div[data-testid="stChatMessage"] {{
            padding: 0.7rem 0.8rem !important;
        }}
    }}

    /* شريط تمرير أنيق */
    ::-webkit-scrollbar {{ width: 8px; height: 8px; }}
    ::-webkit-scrollbar-track {{ background: transparent; }}
    ::-webkit-scrollbar-thumb {{
        background: rgba(201,179,126,0.25);
        border-radius: 10px;
    }}
    ::-webkit-scrollbar-thumb:hover {{
        background: rgba(201,179,126,0.45);
    }}
</style>
""", unsafe_allow_html=True)

# ============================================================
#  جلب المفتاح (لم يُمسّ)
# ============================================================
gemini_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

if not gemini_key:
    st.error("⚠️ يرجى إضافة GEMINI_API_KEY في Streamlit Secrets للبدء.")
    st.stop()

# ============================================================
#  دالة الاستدعاء المباشرة المتقدمة (اتصال السيرفر كما هو)
# ============================================================
def call_gemini_api(prompt_text, system_instruction_text, temperature, max_tokens, top_p=None):
    headers = {'Content-Type': 'application/json'}

    generation_config = {
        "temperature": temperature,
        "maxOutputTokens": max_tokens
    }
    if top_p is not None:
        generation_config["topP"] = top_p

    payload = {
        "system_instruction": {
            "parts": [{"text": system_instruction_text}]
        },
        "contents": [{
            "parts": [{"text": prompt_text}]
        }],
        "generationConfig": generation_config
    }

    # 1. المحاولة الأولى
    url_primary = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent?key={gemini_key}"
    res = requests.post(url_primary, headers=headers, json=payload)
    if res.status_code == 200:
        return res.json()['candidates'][0]['content']['parts'][0]['text']

    # 2. خطة التراجع الديناميكية
    models_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={gemini_key}"
    try:
        models_res = requests.get(models_url)
        if models_res.status_code == 200:
            models_list = models_res.json().get('models', [])
            for m in models_list:
                m_name = m.get('name', '').replace('models/', '')
                if 'generateContent' in m.get('supportedGenerationMethods', []):
                    fallback_url = f"https://generativelanguage.googleapis.com/v1beta/models/{m_name}:generateContent?key={gemini_key}"
                    fb_res = requests.post(fallback_url, headers=headers, json=payload)
                    if fb_res.status_code == 200:
                        return fb_res.json()['candidates'][0]['content']['parts'][0]['text']
    except Exception:
        pass

    raise Exception(f"خطأ ({res.status_code}): {res.text}")

# ============================================================
#  حالة الجلسة
# ============================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# ============================================================
#  الشريط الجانبي — مركز الإعدادات
# ============================================================
with st.sidebar:
    st.markdown("<h2 class='gold-header'>⚜️ أوريون الشام</h2>", unsafe_allow_html=True)
    st.markdown("<div class='status-badge'>المحرك متصل ومستقر</div>", unsafe_allow_html=True)

    st.divider()

    # ---- قسم تخصيص النموذج ----
    st.markdown("<h4 class='gold-header'>🎯 تخصيص النموذج</h4>", unsafe_allow_html=True)
    mode = st.radio(
        "وضع المساعد:",
        ["💻 مساعد برمجي متقدم", "📊 مُحلل وإداري", "🎨 مبتكر وإبداعي", "⚡ سريع وموجز"],
        index=0
    )
    mode_clean = mode.split(" ", 1)[1]

    system_instructions = {
        "مساعد برمجي متقدم": "أنت مساعد ذكي متطور ومستقل (أوريون الشام Enterprise). تتسم بالحكمة والدقة. تبرع في البرمجة النظيفة، كتابة الأكواد، وتصحيح الأخطاء باللغة العربية.",
        "مُحلل وإداري": "أنت مستشار تقني وإداري خبير. تقدم تحليلات دقيقة، خطط عملية، وإجابات هيكلية واضحة باللغة العربية.",
        "مبتكر وإبداعي": "أنت محرك فكري ومبدع. تقدم أفكاراً غير تقليدية وحلولاً ابتكارية متميزة باللغة العربية.",
        "سريع وموجز": "أنت مساعد سريع يقدّم إجابات مباشرة، مختصرة ومفيدة دون إطالة."
    }
    selected_instruction = system_instructions[mode_clean]

    # ---- معلمات التوليد المتقدمة ----
    with st.expander("⚙️ إعدادات التوليد المتقدمة", expanded=False):
        temperature = st.slider(
            "🌡️ درجة الإبداع (Temperature)",
            min_value=0.0, max_value=1.0, value=0.7, step=0.05,
            help="القيم المنخفضة = إجابات أكثر دقة (مناسبة للبرمجة). العالية = إبداعية."
        )

        top_p = st.slider(
            "🎯 نطاق التنوع (Top-P)",
            min_value=0.1, max_value=1.0, value=0.95, step=0.05,
            help="يتحكم في تنوع الكلمات المختارة."
        )

        max_tokens = st.select_slider(
            "📏 الحد الأقصى للرموز",
            options=[512, 1024, 2048, 4096, 8192],
            value=4096
        )

        use_context = st.toggle("🧠 الذاكرة (سياق المحادثة)", value=True)

        context_depth = st.slider(
            "عمق السياق (عدد الرسائل السابقة)",
            min_value=2, max_value=20, value=8, step=2,
            disabled=not use_context
        )

    st.divider()

    # ---- المرفقات ----
    st.markdown("<h4 class='gold-header'>📄 المرفقات والملفات</h4>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "رفع ملف للمعالجة:",
        type=["txt", "py", "js", "html", "css", "json", "md", "csv", "sql"]
    )
    if uploaded_file is not None:
        st.caption(f"📎 تم تحميل: `{uploaded_file.name}`")

    st.divider()

    # ---- إدارة الجلسة ----
    st.markdown("<h4 class='gold-header'>⚙️ إدارة المحادثة</h4>", unsafe_allow_html=True)
    st.write(f"💬 إجمالي الرسائل: **{len(st.session_state.messages)}**")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 جلسة جديدة", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    with col2:
        if st.session_state.messages:
            chat_text = "\n\n".join([f"[{m['role'].upper()}]\n{m['content']}" for m in st.session_state.messages])
            st.download_button(
                label="⬇️ تصدير السجل",
                data=chat_text,
                file_name=f"orion_chat_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain",
                use_container_width=True
            )

# ============================================================
#  الواجهة الرئيسية
# ============================================================
st.markdown("<h1 class='gold-header'>⚜️ أوريون الشام Enterprise</h1>", unsafe_allow_html=True)

if not st.session_state.messages:
    st.markdown(
        f"<div style='text-align:center; padding:2.5rem 1rem; color:{TEXT_MUTED};"
        f"font-family:Cairo,sans-serif; line-height:2;'>"
        f"<div style='font-size:2.6rem; margin-bottom:0.5rem;'>⚜️</div>"
        f"<p style='font-size:1.05rem; font-weight:700; color:{GOLD_MAIN}; margin:0;'>مرحباً بك في أوريون الشام</p>"
        f"<p style='font-size:0.9rem; margin:0;'>اسألني أي شيء — برمجة، تحليل، إبداع، أو استشارة تقنية.</p>"
        f"</div>",
        unsafe_allow_html=True
    )

for msg in st.session_state.messages:
    avatar = "🧑‍💻" if msg["role"] == "user" else "⚜️"
    with st.chat_message(msg["role"], avatar=avatar):
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
    with st.chat_message("user", avatar="🧑‍💻"):
        st.write(display_text)

    full_user_content = user_input + file_context
    if use_context and len(st.session_state.messages) > 2:
        recent = st.session_state.messages[:-1][-context_depth:]
        history_text = "\n\n".join([f"{m['role']}: {m['content']}" for m in recent])
        full_user_content = (
            f"[سياق المحادثة السابقة]:\n{history_text}\n\n"
            f"[الرسالة الحالية]:\n{full_user_content}"
        )

    with st.chat_message("assistant", avatar="⚜️"):
        with st.spinner("جاري المعالجة بناءً على الإعدادات المحددة..."):
            try:
                bot_response = call_gemini_api(
                    full_user_content,
                    selected_instruction,
                    temperature,
                    max_tokens,
                    top_p
                )
                st.write(bot_response)
                st.session_state.messages.append({"role": "assistant", "content": bot_response})
            except Exception as e:
                st.error(f"حدث خطأ أثناء المعالجة: {e}")
