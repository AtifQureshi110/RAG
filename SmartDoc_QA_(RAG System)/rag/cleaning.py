# cleaning.py
import re

def clean_text(text, lower=True):
    """
    Clean text by removing extra whitespace and optionally converting to lowercase.
    """
    text = re.sub(r"\s+", " ", text)  # collapse whitespace
    text = text.strip()
    if lower:
        text = text.lower()
    return text

# ================== 🔽 TESTING BLOCK ==================
# if __name__ == "__main__":
#     from ingestion import load_pdf
#     from pathlib import Path
#     # 🔹 Define project root dynamically
#     project_root = Path(__file__).parent.parent
#     data_folder = project_root / "data"
#     # 🔹 PDF file path
#     pdf_file = data_folder / "refference letter_Atif_DR. ARIFA BHUTTO, PHD.pdf"

#     # Load and clean text
#     try:
#         raw_text = load_pdf(pdf_file)
#         cleaned = clean_text(raw_text)
#         print(f"📄 Raw text length: {len(raw_text)}")
#         print(f"📄 Cleaned text length: {len(cleaned)}")
#         print(f"📝 Preview:\n{cleaned[:500]}")  # show first 500 chars
#     except Exception as e:
#         print(f"❌ Error: {e}")