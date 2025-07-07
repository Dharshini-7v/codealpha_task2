import json
import nltk
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('punkt')
nltk.download('stopwords')

# Load JSON data
with open("faqs.json", "r") as f:
    faq_data = json.load(f)

# Extract questions and answers
questions = [item["question"] for item in faq_data]
answers = [item["answer"] for item in faq_data]

# Preprocess function
def preprocess(text):
    tokens = word_tokenize(text.lower())
    tokens = [t for t in tokens if t not in string.punctuation]
    tokens = [t for t in tokens if t not in stopwords.words('english')]
    return ' '.join(tokens)

# Preprocess questions
processed_questions = [preprocess(q) for q in questions]

# TF-IDF Vectorization
vectorizer = TfidfVectorizer()
vectors = vectorizer.fit_transform(processed_questions)

# Response function
def get_answer(user_input):
    user_input_processed = preprocess(user_input)
    user_vector = vectorizer.transform([user_input_processed])
    similarity = cosine_similarity(user_vector, vectors)
    idx = similarity.argmax()
    return answers[idx]

if __name__ == "__main__":
    print("Laptop Troubleshooting FAQ Chatbot (type 'exit' to quit)")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        print("Bot:", get_answer(user_input))
# Add this to the bottom for UI
try:
    import streamlit as st
    st.title("💻 Laptop Troubleshooting Chatbot")
    query = st.text_input("Ask your laptop issue:")
    if query:
        st.write("Bot:", get_answer(query))
except ImportError:
    pass
