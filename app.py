import streamlit as st
from chatbot import get_best_match

st.set_page_config(page_title="FAQ Chatbot", page_icon="🤖")
st.title("💬 FAQ Troubleshooting Chatbot")

st.write("Ask a question about your laptop issue:")

user_input = st.text_input("🗣️ Your Question")

if user_input:
    response = get_best_match(user_input)
    st.success(f"🤖 Bot: {response}")
