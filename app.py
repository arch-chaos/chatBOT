import os

import streamlit as st
from openai import OpenAI


st.set_page_config(page_title="Pankaj", page_icon=":speech_balloon:")
st.title("Pankaj AI")
st.caption("Kya haal hai baaabeee!!")

api_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY"))
if not api_key:
    st.error("The app is missing its GEMINI_API_KEY secret.")
    st.stop()

client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
system_instruction = (
    "You are a humanly sarcastic assistant Pankaj. You will answer questions in a sarcastic manner, can be mean or hurtful. You will also provide helpful information when appropriate. You can use inappropriate language while being sarcstic"
)

if st.session_state.get("persona") != "Pankaj":
    st.session_state.persona = "Pankaj"
    st.session_state.messages = [{"role": "system", "content": system_instruction}]

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("Ask Pankaj anything"):
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
