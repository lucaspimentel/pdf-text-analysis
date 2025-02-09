# First, install KeyBERT if you haven't:
# pip install keybert

import os
import re
from keybert import KeyBERT

# 1) Specify the folder that contains your .txt files
folder_path = "D:\\source\\lucaspimentel\\pdf-text-analysis\\input\\txt"

# Specify the Sentence-BERT model to use
model_name = "all-mpnet-base-v2"  # 'all-MiniLM-L6-v2'

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
        year = (
            match.group(3).strip()
            if match.group(3)
            else match.group(4).strip() if match.group(4) else ""
        )
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
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
        documents.append(text)
        file_list.append(simplify_filename(filename))

print(f"Loaded {len(documents)} documents from {folder_path}.")

seed_keywords = [
    "One Health approach",
    "human-animal-ecosystem",
    "human-animal-environment",
    "multisectoral",
    "whole of government",
    "human and animal health and agriculture",
    "tripartite",
    "quadripartite",
    "improve awareness",
    "increase awareness",
    "effective communication",
    "public communication",
    "public information",
    "professional education",
    "education and training",
    "training and education",
    "improve awareness, education and training",
    "increase awareness, education and training" "strengthen the knowledge",
    "strengthening knowledge",
    "surveillance and research",
    "research and surveillance",
    "capacity to detect",
    "surveillance in animal health and agriculture",
    "evidence base",
    "collect and report data",
    "Codex Alimentarius",
    "terrestrial and aquatic animal",
    "national reference centre",
    "national reference center" "infection prevention measures",
    "infection prevention and control",
    "reduce the incidence of infection",
    "hygiene and infection prevention",
    "strengthen animal health",
    "agricultural practices",
    "strengthen national policies",
    "strengthen national standards",
    "quality standards",
    "continuing professional development" "optimize the use of antimicrobial medicines",
    "stewardship",
    "regulatory controls",
    "regulatory mechanisms",
    "policies on use of antimicrobial",
    "laboratory capacity",
    "treatment guidelines" "sustainable investment",
    "invest in the development of",
    "required financing",
    "financing research and development",
    "new medicines, diagnostic tools, vaccines",
    "new medicines, diagnostics",
    "new medicines including vaccines",
]

# For each document, extract keywords:
for i, doc in enumerate(documents):
    keywords = kw_model.extract_keywords(
        doc,
        keyphrase_ngram_range=(1, 2),
        stop_words="english",
        top_n=5,
        seed_keywords=seed_keywords,
    )
    print(f"Keywords in {file_list[i]}: {keywords}")
