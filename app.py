import streamlit as st
from chatbot import FAQChatbot, load_faqs

st.set_page_config(page_title="Laptop FAQ Chatbot", page_icon="💻")
st.title("💬 Laptop Troubleshooting FAQ Chatbot")

# Load data
faqs_df = load_faqs("faqs.csv")
chatbot = FAQChatbot(faqs_df)

# Chat input
user_question = st.text_input("Ask me a laptop troubleshooting question:")

if user_question:
    response = chatbot.get_best_match(user_question)
    st.markdown(f"**Chatbot:** {response}")
