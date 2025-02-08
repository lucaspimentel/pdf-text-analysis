import os
import fitz  # PyMuPDF


def pdf_to_text(input_file):
    pdf_document = fitz.open(input_file)
    pdf_text = ""

    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        pdf_text += page.get_text("text")  # Extract text in plain format

    return pdf_text


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
OUTPUT_DIRECTORY = "OUTPUT_PATH\\PyMuPDF"
process_pdfs_in_directory(INPUT_DIRECTORY, OUTPUT_DIRECTORY)
