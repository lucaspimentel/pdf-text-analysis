import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from nltk.corpus import stopwords

# Ensure you have downloaded stopwords (if not already)
# import nltk
# nltk.download('stopwords')
stop_words = stopwords.words('english')

def preprocess(text):
    # Tokenize, lower, and remove stopwords
    return [token for token in simple_preprocess(text) if token not in stop_words]

# Suppose 'documents' is a list of your document texts
processed_docs = [preprocess(doc) for doc in documents]

# Create a dictionary and corpus needed for LDA
dictionary = corpora.Dictionary(processed_docs)
corpus = [dictionary.doc2bow(doc) for doc in processed_docs]

# Train an LDA model on the whole corpus
num_topics = 5  # adjust as needed
lda_model = gensim.models.LdaModel(corpus=corpus,
                                   id2word=dictionary,
                                   num_topics=num_topics,
                                   random_state=42,
                                   update_every=1,
                                   chunksize=100,
                                   passes=10,
                                   alpha='auto')

# For each document, you can now print out the topic distribution:
for i, bow in enumerate(corpus):
    topics = lda_model.get_document_topics(bow)
    print(f"Document {i} topics: {topics}")
