import streamlit as st
from chatbot import get_best_match

st.set_page_config(page_title="FAQ Bot", page_icon="💻")
st.title("💬 Laptop Troubleshooting Chatbot")

st.write("Ask a question related to your laptop issues:")

user_input = st.text_input("🔍 Your Question")

if user_input:
    response = get_best_match(user_input)
    st.success(f"🤖 {response}")

