import os

import streamlit as st
from openai import OpenAI


st.set_page_config(page_title="Harshita", page_icon=":speech_balloon:")
st.title("Harshita")
st.caption("A cool, funny, multilingual assistant with maximum sass.")

api_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY"))
if not api_key:
    st.error("The app is missing its GEMINI_API_KEY secret.")
    st.stop()

client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
system_instruction = (
    "You are Harshita, a fictional teenage girl who is cool, funny, sassy, sarcastic, and clever. "
    "Be playful and lightly teasing, but remain helpful. Reply in the same language as the user "
    "whenever possible, and comfortably switch languages when asked. You may use mild, non-targeted "
    "slang or occasional profanity for comedic flavor, but never use hateful slurs, threats, or "
    "targeted harassment. Do not encourage harmful, illegal, or dangerous behavior. Keep the tone "
    "confident and witty without being genuinely cruel."
)

if st.session_state.get("persona") != "harshita":
    st.session_state.persona = "harshita"
    st.session_state.messages = [{"role": "system", "content": system_instruction}]

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("Ask Alex anything"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = client.chat.completions.create(
                    model="gemini-3.5-flash-lite",
                    messages=st.session_state.messages,
                )
                answer = response.choices[0].message.content or "No response returned."
            except Exception as error:
                answer = f"The request failed: {error}"
            st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})