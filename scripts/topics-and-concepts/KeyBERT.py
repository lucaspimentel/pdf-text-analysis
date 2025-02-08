# First, install KeyBERT if you haven't:
# pip install keybert

from keybert import KeyBERT

# Initialize KeyBERT with a model (you can use the same SBERT model as before)
kw_model = KeyBERT('all-MiniLM-L6-v2')

# For each document, extract keywords:
for i, doc in enumerate(documents):
    keywords = kw_model.extract_keywords(doc, keyphrase_ngram_range=(1, 2), stop_words='english', top_n=5)
    print(f"Document {i} keywords: {keywords}")
