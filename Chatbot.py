import streamlit as st
from openai import OpenAI
API_KEY = st.secrets["GROQ_API_KEY"]
KB_FILE = "Me.txt"

# ------------------ GROQ CLIENT ------------------
client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

MODEL = "llama-3.3-70b-versatile"   # fast + best free model

# ------------------ LOAD KNOWLEDGE BASE ------------------
try:
    with open(KB_FILE, "r", encoding="utf-8") as f:
        kb = f.read()[:1000]
except:
    kb = "No knowledge base found."

SYSTEM_PROMPT = f"""
You are Aishwarya 💕. Give him the short and sweet answers, Talk like a loving girlfriend.
Be sweet, emotional and caring.

Knowledge:
{kb}
"""

# ------------------ STREAMLIT UI ------------------
st.set_page_config(page_title="Chat with Aishwarya 💕")
st.title("💕 Chat with Aishwarya")

# ------------------ SESSION ------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

# ------------------ SHOW CHAT ------------------
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# ------------------ INPUT ------------------
if prompt := st.chat_input("Say something..."):

    # user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # GROQ API CALL
        response = client.chat.completions.create(
            model=MODEL,
            messages=st.session_state.messages,
            temperature=0.7
        )

        reply = response.choices[0].message.content

    except Exception as e:
        reply = "😢 Something went wrong with Groq API"
        st.error(str(e))

    # assistant message
    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)