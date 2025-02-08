import os
import subprocess


def pdf_to_text(input_file):
    pdftotext_path = os.path.join(
        os.path.expanduser("~"),
        "Downloads",
        "xpdf-tools-win-4.05",
        "bin64",
        "pdftotext.exe",
    )
    if not os.path.exists(pdftotext_path):
        raise FileNotFoundError(f"pdftotext.exe not found at {pdftotext_path}")

    output_file = input_file.replace(".pdf", ".txt")
    subprocess.run(
        [pdftotext_path, "-nopgbrk", "-raw", "-enc", "UTF-8", input_file, output_file],
        check=True,
    )

    with open(output_file, "r", encoding="utf-8") as f:
        return f.read()


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
OUTPUT_DIRECTORY = "D:\\source\\lucaspimentel\\pdf-text-analysis\\output\\xpdf"
process_pdfs_in_directory(INPUT_DIRECTORY, OUTPUT_DIRECTORY)
