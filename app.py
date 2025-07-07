import streamlit as st
from chatbot import FAQChatbot, load_faqs

# --- Page Config ---
st.set_page_config(
    page_title="💻 Laptop FAQ Chatbot",
    page_icon="🤖",
    layout="centered",
)

# --- Custom Styling ---
st.markdown("""
    <style>
    .stTextInput>div>div>input {
        border: 2px solid #4CAF50;
        border-radius: 10px;
        padding: 0.5rem;
    }
    .stMarkdown {
        font-size: 18px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Load Chatbot ---
faqs_df = load_faqs("faqs.csv")
chatbot = FAQChatbot(faqs_df)

# --- Sidebar Info ---
with st.sidebar:
    st.title("ℹ️ About")
    st.markdown("This chatbot helps answer **laptop troubleshooting** questions.")
    st.markdown("Built by **Dharshini V.** for CodeAlpha Internship 🌟")

# --- Main App ---
st.title("🤖 Laptop Troubleshooting Chatbot")
st.markdown("Ask your laptop issues like: *'Wi-Fi not working'*, *'Laptop overheating'*, *'Screen flickering'*, etc.")

user_input = st.text_input("💬 Your Question")

if user_input:
    response = chatbot.get_best_match(user_input)
    st.markdown(f"**🧠 Chatbot:** {response}")

