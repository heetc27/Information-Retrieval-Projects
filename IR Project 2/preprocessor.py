import collections
from nltk.stem import PorterStemmer
import re
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')

class Preprocessor:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.ps = PorterStemmer()

    def get_doc_id(self, doc):
        """ Splits each line of the document, into doc_id & text.
            Already implemented"""
        arr = doc.split("\t")
        return int(arr[0]), arr[1]

    def tokenizer(self, text):
        # Step 1: Converting document to lowercase
        text_lowercase = text.lower()

        # Step 2: Removing special characters from document
        text_lowercase = re.sub(r"[^a-zA-Z0-9]+", ' ', text_lowercase)

        # Step 3: Removing extra spaces from document
        tokenized_text = re.sub(' +', ' ', text_lowercase)

        # Step 4: Splitting the document into 'tokens'
        tokens_with_stopwords = tokenized_text.split()

        # Step 5: Initializing stopwords
        stop_words = set(stopwords.words('english'))

        #Step 6: Removing stop words from document
        # token is considered if word is not present in stopwords
        tokens = [word for word in tokens_with_stopwords if not word.lower()
                in stop_words]

        # Step 7: Stemming
        stemmer = PorterStemmer()
        final_tokens = [stemmer.stem(w) for w in tokens]
        return final_tokens