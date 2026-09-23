import random
import re
from pathlib import Path

import joblib
import streamlit as st


st.set_page_config(page_title="QueryGlide", page_icon="Q", layout="wide")
PROJECT_ROOT = Path(__file__).resolve().parent
MODEL_DIR = PROJECT_ROOT / "models"


def clean_text(text):
    """Match the text preparation used during model training."""
    return re.sub(r"[^\w\s]", "", text.lower().strip())


@st.cache_resource
def load_assets():
    """Load the support classifier and answers once per app session."""
    return (
        joblib.load(MODEL_DIR / "queryglide_model.pkl"),
        joblib.load(MODEL_DIR / "responses_map.pkl"),
    )


try:
    bot_pipeline, responses = load_assets()
except FileNotFoundError:
    st.error("Missing model files. Add the two model files beside app.py.")
    st.stop()


st.markdown(
    """
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Playfair+Display:ital,wght@0,600;0,700;1,600&display=swap');
      :root { --ink:#17152a; --paper:#fffdf9; --mist:#f1effa; --plum:#5136ad; --coral:#ff6d57; --line:#ded9eb; }
      .stApp { background:radial-gradient(circle at 84% 8%,#f9d8ce 0,transparent 20%),radial-gradient(circle at 24% 85%,#d9d2ff 0,transparent 27%),#f7f5fb; color:var(--ink); font-family:Manrope,sans-serif; }
      #MainMenu, footer, header { visibility:hidden; }
      [data-testid="stSidebar"] { background:#17152a; border-right:1px solid rgba(255,255,255,.08); }
      [data-testid="stSidebar"] > div:first-child { padding:1.8rem 1.25rem; }
      [data-testid="stSidebar"] * { color:#f9f7ff !important; }
      [data-testid="stSidebar"] [data-baseweb="slider"] div { color:#ff8b78 !important; }
      [data-testid="stSidebar"] button { background:transparent !important; border:1px solid rgba(255,255,255,.3) !important; border-radius:0 !important; font-size:.82rem !important; letter-spacing:.04em; }
      .block-container { max-width:1110px; padding-top:2.1rem; padding-bottom:7.5rem; }
      .wordmark { font-family:'Playfair Display',serif; font-size:1.8rem; line-height:1; letter-spacing:-.07em; }
      .wordmark i { color:#ff8975 !important; font-weight:600; }
      .side-note { color:#b9b5ce !important; font-size:.82rem; line-height:1.65; margin:1rem 0 2.2rem; max-width:190px; }
      .side-rule { height:1px; background:linear-gradient(90deg,#ff7d69 0 22%,rgba(255,255,255,.18) 22%); margin:1.4rem 0; }
      .side-label { color:#aaa5c7 !important; font-size:.67rem; font-weight:800; text-transform:uppercase; letter-spacing:.16em; }
      .block-container h1 { font-family:'Playfair Display',serif; font-size:clamp(2.7rem,5.4vw,5.2rem) !important; font-weight:600; letter-spacing:-.075em; line-height:.93; max-width:780px; margin:.55rem 0 1.1rem !important; }
      .eyebrow { color:#5136ad; font-size:.7rem; font-weight:800; letter-spacing:.17em; text-transform:uppercase; }
      .hero-sub { color:#686377; font-size:1.04rem; line-height:1.7; max-width:540px; }
      .orbital-mark { width:68px; height:68px; margin-top:.5rem; margin-left:auto; position:relative; border:1px solid #5136ad; border-radius:50%; }
      .orbital-mark:before { content:""; position:absolute; width:17px; height:17px; background:#ff735d; border-radius:50%; top:8px; right:7px; }
      .orbital-mark:after { content:""; position:absolute; width:32px; height:32px; border:1px solid #5136ad; border-radius:50%; left:9px; bottom:7px; }
      .greeting { margin-top:3rem; padding:1.55rem 1.7rem 1.35rem; background:#fffdf9; border:1px solid var(--line); border-radius:3px 24px 3px 24px; box-shadow:12px 12px 0 #e3dcfa; }
      .greeting h3 { font-family:'Playfair Display',serif; font-size:1.55rem; letter-spacing:-.04em; margin:0 0 .25rem; }
      .greeting p { color:#767084; margin:0; font-size:.9rem; }
      .stButton > button { min-height:58px; border:1px solid #cfc7e5; background:rgba(255,253,249,.72); border-radius:0 15px 0 15px; color:#2b2545; font-family:Manrope,sans-serif; font-size:.82rem; font-weight:700; letter-spacing:.015em; transition:.2s ease; }
      .stButton > button:hover { transform:translateY(-3px); background:#5136ad; color:#fff !important; border-color:#5136ad; box-shadow:5px 6px 0 #ff9d8c; }
      [data-testid="stChatMessage"] { background:transparent; padding:.5rem 0; }
      [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] { padding:1rem 1.15rem; border-radius:3px 16px 16px 16px; line-height:1.6; }
      [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) [data-testid="stMarkdownContainer"] { background:#e4ddff; color:#2e2169; }
      [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) [data-testid="stMarkdownContainer"] { background:#fffdf9; border:1px solid var(--line); box-shadow:4px 5px 0 rgba(81,54,173,.08); }
      [data-testid="stChatInput"] { background:#fffdf9; border:1px solid #cfc7e5 !important; border-radius:0 17px 0 17px !important; box-shadow:8px 9px 0 #ded7f4; padding:.35rem .55rem; }
      [data-testid="stChatInput"]:focus-within { border-color:#5136ad !important; box-shadow:8px 9px 0 #ded7f4,0 0 0 3px rgba(81,54,173,.12); }
      .signal { display:inline-block; margin-top:.55rem; color:#807a90; font-size:.68rem; font-weight:700; letter-spacing:.08em; text-transform:uppercase; }
      @media (max-width:700px) { .block-container { padding:1.4rem 1rem 6.5rem; } .orbital-mark { display:none; } .greeting { margin-top:2rem; } }
    </style>
    """,
    unsafe_allow_html=True,
)

st.sidebar.markdown('<div class="wordmark">query<i>glide</i></div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="side-note">Your calm corner for questions, updates, and useful next steps.</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="side-rule"></div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="side-label">Answer sensitivity</div>', unsafe_allow_html=True)
confidence_threshold = st.sidebar.slider(
    "Confidence threshold", 0.0, 1.0, 0.45, 0.05,
    help="Higher values only show answers the model is more certain about.",
)
st.sidebar.caption("Move gently toward focus or flexibility.")
st.sidebar.markdown('<div class="side-rule"></div>', unsafe_allow_html=True)
if st.sidebar.button("NEW CONVERSATION", use_container_width=True):
    st.session_state.messages = []
    st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

left, right = st.columns([5, 1])
with left:
    st.markdown('<div class="eyebrow">The support studio / always open</div>', unsafe_allow_html=True)
    st.title("A small question can change the whole day.")
    st.markdown('<div class="hero-sub">Leave the searching behind. Tell QueryGlide what is on your mind and we will find a useful way forward, together.</div>', unsafe_allow_html=True)
with right:
    st.markdown('<div class="orbital-mark"></div>', unsafe_allow_html=True)

selected_prompt = None
if not st.session_state.messages:
    st.markdown('<div class="greeting"><h3>Where should we begin?</h3><p>A few common paths, chosen without the usual clutter.</p></div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("FIND AN ORDER", use_container_width=True):
            selected_prompt = "Where is my order?"
    with c2:
        if st.button("MAKE A RETURN", use_container_width=True):
            selected_prompt = "How do I return an item?"
    with c3:
        if st.button("SORT A PAYMENT", use_container_width=True):
            selected_prompt = "I need help with a payment."

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant" and "meta" in message:
            st.markdown(
                f'<div class="signal">Signal: {message["meta"]["tag"]} / {message["meta"]["confidence"]:.0%} confidence</div>',
                unsafe_allow_html=True,
            )

user_query = selected_prompt or st.chat_input("Write your question here...")
if user_query:
    with st.chat_message("user"):
        st.markdown(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query})

    probabilities = bot_pipeline.predict_proba([clean_text(user_query)])
    max_prob_idx = probabilities.argmax()
    max_probability = float(probabilities[0][max_prob_idx])
    predicted_tag = bot_pipeline.classes_[max_prob_idx]
    if max_probability >= confidence_threshold:
        bot_reply = random.choice(responses[predicted_tag])
    else:
        bot_reply = random.choice(responses.get("fallback", ["I am sorry, I am having trouble understanding that. Could you rephrase it?"]))

    with st.chat_message("assistant"):
        st.markdown(bot_reply)
        st.markdown(
            f'<div class="signal">Signal: {predicted_tag} / {max_probability:.0%} confidence</div>',
            unsafe_allow_html=True,
        )
    st.session_state.messages.append(
        {"role": "assistant", "content": bot_reply, "meta": {"tag": predicted_tag, "confidence": max_probability}}
    )
