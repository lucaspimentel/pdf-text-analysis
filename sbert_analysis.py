import os
import re
from sentence_transformers import SentenceTransformer, util
import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

# 1) Specify the folder that contains your .txt files
folder_path = "<PATH>"

# Specify the Sentence-BERT model to use
model_name = 'all-mpnet-base-v2' # 'all-MiniLM-L6-v2'

# 2) Function to simplify filenames
def simplify_filename(filename: str) -> str:
    """
    Extracts just the country name and the year range (or single year) from a filename.
    
    Examples:
      "Afghanistan AMR NAP (2017-2021).txt" => "Afghanistan 2017-2021"
      "Algeria AMR NAP (2024-2028) English Translation.txt" => "Algeria 2024-2028"
      "Argentina AMR NAP [2015] English Translation.txt" => "Argentina 2015"
      "Cambodia AMR NAP (2019-2023) English Translation (WOAH version).txt" => "Cambodia 2019-2023"
      "Cook Islands AMR NAP (2016-2020).txt" => "Cook Islands 2016-2020"
    """

    # Extract the country name and year range (or single year) from the filename
    match = re.match(r"(.+) AMR NAP (\((\d{4}-\d{4})\)|\[(\d{4})\])?.+", filename)
    if match:
        country = match.group(1).strip()
        year = match.group(3).strip() if match.group(3) else match.group(4).strip() if match.group(4) else ""
    else:
        country = filename.strip()
        year = ""

    # output the simplified filename
    return f"{country} {year}".strip()


# 3) Read all .txt files and store their contents and simplified filenames
documents = []
file_list = []  # will store simplified filenames for output

for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        documents.append(text)
        file_list.append(simplify_filename(filename))

print(f"Loaded {len(documents)} documents from {folder_path}.")

# 4) Load a Sentence-BERT model
model = SentenceTransformer(model_name)

# 5) Convert documents to SBERT embeddings
embeddings = model.encode(documents, convert_to_tensor=True)

# 6) Compute pairwise cosine similarity
similarity_matrix = util.cos_sim(embeddings, embeddings).cpu().numpy()
# similarity_matrix[i, j] represents similarity between document i and j

# 7) Identify the most similar document for each file (using simplified filenames)
num_docs = len(documents)
for i in range(num_docs):
    row = similarity_matrix[i].copy()
    row[i] = -1  # ignore self-similarity
    best_match_idx = np.argmax(row)
    print(f"'{file_list[i]}' is most similar to '{file_list[best_match_idx]}' with score {row[best_match_idx]:.4f}")

# 8) t-SNE for visualization
tsne = TSNE(n_components=2, random_state=42)
reduced_embeddings = tsne.fit_transform(embeddings.cpu())

plt.figure(figsize=(20, 15))
plt.scatter(reduced_embeddings[:, 0], reduced_embeddings[:, 1], alpha=0.6)
for i, fname in enumerate(file_list):
    plt.annotate(fname, (reduced_embeddings[i, 0], reduced_embeddings[i, 1]))
plt.title("SBERT Document Embeddings (t-SNE Visualization)")
plt.show()
