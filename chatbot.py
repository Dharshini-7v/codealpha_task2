import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

# Download necessary NLTK data (run this once
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')


# --- Text Preprocessing Functions ---
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    text = text.lower() # Convert to lowercase
    text = re.sub(r'[^a-z0-9\s]', '', text) # Remove punctuation and special characters
    tokens = nltk.word_tokenize(text) # Tokenize
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words] # Remove stopwords and lemmatize
    return ' '.join(tokens)

# --- Load and Preprocess FAQs ---
def load_faqs(filepath='data/faqs.csv'):
    try:
        df = pd.read_csv(filepath)
        df['processed_question'] = df['question'].apply(preprocess_text)
        return df
    except FileNotFoundError:
        print(f"Error: FAQ file not found at {filepath}")
        return None

# --- Chatbot Logic ---
class FAQChatbot:
    def __init__(self, faqs_df):
        self.faqs_df = faqs_df
        self.vectorizer = TfidfVectorizer()
        self.faq_vectors = self.vectorizer.fit_transform(faqs_df['processed_question'])

    def get_best_match(self, user_question):
        processed_user_question = preprocess_text(user_question)
        if not processed_user_question.strip(): # Handle empty processed question
            return "I'm sorry, I couldn't understand your question. Could you please rephrase it?"

        user_question_vector = self.vectorizer.transform([processed_user_question])

        # Calculate cosine similarity
        similarities = cosine_similarity(user_question_vector, self.faq_vectors).flatten()

        # Get the index of the most similar question
        best_match_index = similarities.argmax()
        
        # You can set a similarity threshold to avoid answering irrelevant questions
        similarity_threshold = 0.5 # Adjust as needed
        
        if similarities[best_match_index] > similarity_threshold:
            return self.faqs_df.loc[best_match_index, 'answer']
        else:
            return "I'm sorry, I don't have an answer to that question. Please try rephrasing or ask a different question."

# --- Main Interaction ---
if __name__ == "__main__":
    print("Initializing chatbot...")
    faqs_df = load_faqs()

    if faqs_df is not None:
        chatbot = FAQChatbot(faqs_df)
        print("Chatbot is ready! Type 'quit' to exit.")

        while True:
            user_input = input("You: ")
            if user_input.lower() == 'quit':
                print("Chatbot: Goodbye!")
                break
            
            response = chatbot.get_best_match(user_input)
            print(f"Chatbot: {response}")
    else:
        print("Chatbot could not be initialized. Please check your data/faqs.csv file.")
