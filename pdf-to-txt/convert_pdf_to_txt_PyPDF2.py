import os
import PyPDF2


def pdf_to_text(input_file):
    extracted_text = ""

    with open(input_file, "rb") as file:
        reader = PyPDF2.PdfReader(file)

        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            extracted_text += page.extract_text()

    return extracted_text

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
OUTPUT_DIRECTORY = "D:\\source\\lucaspimentel\\pdf-text-analysis\\output\\PyPDF2"
process_pdfs_in_directory(INPUT_DIRECTORY, OUTPUT_DIRECTORY)
