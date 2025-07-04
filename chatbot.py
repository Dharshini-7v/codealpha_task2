import json
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def load_faqs():
    with open("faq_data.json", "r") as f:
        data = json.load(f)
    return data["faqs"]

def preprocess(text):
    doc = nlp(text.lower())
    tokens = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
    return " ".join(tokens)

def get_best_match(user_input):
    faqs = load_faqs()
    questions = [faq["question"] for faq in faqs]
    answers = [faq["answer"] for faq in faqs]

    processed_questions = [preprocess(q) for q in questions]
    processed_input = preprocess(user_input)

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(processed_questions + [processed_input])

    similarities = cosine_similarity(vectors[-1], vectors[:-1])
    best_match_index = similarities.argmax()
    score = similarities[0, best_match_index]

    if score > 0.3:
        return answers[best_match_index]
    else:
        return "Sorry, I couldn’t find a match. Try rephrasing your question."

