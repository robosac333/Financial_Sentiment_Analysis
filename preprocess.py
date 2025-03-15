import re
import nltk
import string

# Imported NLTK modules for text preprocessing
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Downloaded the required NLTK data sets if they were not already downloaded
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('punkt')

# Initialized the stopwords set and lemmatizer used for preprocessing text
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    """
    Preprocessed the input text by:
    - Converting it to lowercase.
    - Removing URLs.
    - Removing punctuation.
    - Tokenizing the text.
    - Removing stopwords.
    - Lemmatizing tokens.
    Returned the processed text as a single string.
    """
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", "", text)  # Removed URLs
    text = text.translate(str.maketrans("", "", string.punctuation))  # Removed punctuation
    tokens = word_tokenize(text)
    filtered_tokens = [word for word in tokens if word not in stop_words]
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]
    return " ".join(lemmatized_tokens)
