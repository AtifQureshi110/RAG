# ingestion.py
from pypdf import PdfReader

def load_pdf(file_path):
    """Load a PDF and return its full text as a single string."""
    try:
        reader = PdfReader(file_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"PDF file not found: {file_path}")
    except Exception as e:
        raise Exception(f"Failed to read PDF: {e}")

    text_chunks = []
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text_chunks.append(page_text.strip())

    return "\n".join(text_chunks)

# ================== 🔽 TESTING BLOCK ==================
# if __name__ == "__main__":
#     from pathlib import Path

#     # 🔹 Define project root dynamically
#     project_root = Path(__file__).parent.parent  # adjusts relative to this file
#     data_folder = project_root / "data"          # data folder path
#     # 🔹 PDF file path
#     pdf_file = data_folder / "kamran_taj.pdf"

#     # Load PDF text
#     try:
#         text = load_pdf(pdf_file)
#         print(f"📄 Loaded text length: {len(text)}")
#         print(f"📝 Preview:\n{text[:500]}")  # preview first 500 characters
#     except Exception as e:
#         print(f"❌ Error: {e}")