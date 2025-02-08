# First, install KeyBERT if you haven't:
# pip install keybert

import os
import re
from keybert import KeyBERT

# 1) Specify the folder that contains your .txt files
folder_path = "D:\\source\\lucaspimentel\\pdf-text-analysis\\output\\xpdf"

# Specify the Sentence-BERT model to use
model_name = 'all-mpnet-base-v2' # 'all-MiniLM-L6-v2'

# Initialize KeyBERT with a model (you can use the same SBERT model as before)
kw_model = KeyBERT(model_name)

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

# seed_keywords = ["antimicrobial", "national action plan", "AMR", "NAP", "antibiotic", "surveillance", "resistance"]

# For each document, extract keywords:
for i, doc in enumerate(documents):
    keywords = kw_model.extract_keywords(doc, keyphrase_ngram_range=(1, 2), stop_words='english', top_n=5)
    print(f"Keywords in {file_list[i]}: {keywords}")
