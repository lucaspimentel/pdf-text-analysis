import os
import pdfplumber


def pdf_to_text(input_file):
    full_text = ""
    found_line = False

    with pdfplumber.open(input_file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            full_text += text

    return full_text


def process_pdfs_in_directory(input_directory, output_directory):
    os.makedirs(output_directory, exist_ok=True)

    for filename in os.listdir(input_directory):
        if filename.endswith(".pdf"):
            base_name = os.path.splitext(os.path.basename(filename))[0]
            input_file = os.path.join(input_directory, filename)
            output_file = os.path.join(output_directory, f"{base_name}.txt")

            print(f"Processing {input_file}...")
            text = pdf_to_text(input_file)

            with open(output_file, "w", encoding="utf-8") as f:
                f.write(text)


INPUT_DIRECTORY = "INPUT_PATH"
OUTPUT_DIRECTORY = "OUTPUT_PATH\\pdfplumber"
process_pdfs_in_directory(INPUT_DIRECTORY, OUTPUT_DIRECTORY)
