import os
from pdfminer.high_level import extract_text


def pdf_to_text(input_file):
    return extract_text(input_file)


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


INPUT_DIRECTORY = "D:\\source\\lucaspimentel\\pdf-text-analysis\\input"
OUTPUT_DIRECTORY = "D:\\source\\lucaspimentel\\pdf-text-analysis\\output\\pdfminer"
process_pdfs_in_directory(INPUT_DIRECTORY, OUTPUT_DIRECTORY)
