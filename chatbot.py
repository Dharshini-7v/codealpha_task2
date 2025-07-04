import json
import nltk

nltk.data.path.append("C:/Users/Dharshini/AppData/Roaming/nltk_data")

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Make sure these are downloaded once
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def preprocess(text):
    tokens = word_tokenize(text.lower())
    cleaned = [lemmatizer.lemmatize(word) for word in tokens if word.isalnum() and word not in stop_words]
    return " ".join(cleaned)

def load_faqs():
    with open("faq_data.json", "r") as f:
        data = json.load(f)
    return data["faqs"]

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
    best_score = similarities[0, best_match_index]

    if best_score > 0.3:
        return answers[best_match_index]
    else:
        return "Sorry, I couldn't find a matching answer. Try rephrasing your question."
