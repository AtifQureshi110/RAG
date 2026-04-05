# 🔹 4. Chunking
# Use semantic-aware chunking (better)
# def chunk_text(text, chunk_size=500, overlap=100):
#     sentences = text.split(". ")

#     chunks = []
#     current_chunk = ""

#     for sentence in sentences:
#         if len(current_chunk) + len(sentence) < chunk_size:
#             current_chunk += sentence + ". "
#         else:
#             chunks.append(current_chunk.strip())
#             current_chunk = sentence + ". "

#     if current_chunk:
#         chunks.append(current_chunk.strip())

#     return chunks

# from Clean_text_2 import clean_text
# from ingestion_1 import load_pdf

# # Load data
# text = load_pdf(r"E:\RAG Projects\SmartDoc_QA_(RAG System)\data\refference letter_Atif_DR. ARIFA BHUTTO, PHD.pdf")

# cleaned_text = clean_text(text)

# def chunk_text(text, chunk_size=500, overlap=100):
#     chunks = []
#     start = 0

#     while start < len(text):
#         end = start + chunk_size
#         chunks.append(text[start:end])
#         start += chunk_size - overlap

#     return chunks

# chunking.py
from nltk.tokenize import sent_tokenize

def chunk_text(text, chunk_size=500, overlap=100):
    """Split text into chunks based on sentences with optional overlap."""
    sentences = sent_tokenize(text)
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue

        # Add sentence to current chunk if it fits
        if len(current_chunk) + len(sentence) <= chunk_size:
            if current_chunk:
                current_chunk += " " + sentence
            else:
                current_chunk = sentence
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence

    # Add last chunk
    if current_chunk:
        chunks.append(current_chunk.strip())

    # Apply overlap if needed
    if overlap > 0 and len(chunks) > 1:
        overlapped_chunks = []
        for i in range(len(chunks)):
            if i == 0:
                overlapped_chunks.append(chunks[i])
            else:
                overlap_text = chunks[i-1][-overlap:]
                overlapped_chunks.append(overlap_text + " " + chunks[i])
        chunks = overlapped_chunks

    return chunks

# ================== 🔽 TESTING BLOCK ==================
# if __name__ == "__main__":

#     from ingestion import load_pdf
#     from cleaning import clean_text
#     from pathlib import Path

#     # 🔹 Define project root dynamically
#     project_root = Path(__file__).parent.parent  # Smart relative path

#     # 🔹 PDF file (relative to project root)
#     data_folder = project_root / "data"
#     pdf_file = data_folder / "refference letter_Atif_DR. ARIFA BHUTTO, PHD.pdf"

#     # Load & clean text
#     text = load_pdf(pdf_file)
#     cleaned_text = clean_text(text)

#     # Debug: check text loaded
#     print(f"📄 Loaded text length: {len(cleaned_text)}")
#     print(f"📝 Text preview:\n{cleaned_text[:300]}\n")

#     # Chunk the text
#     chunks = chunk_text(cleaned_text)
#     print(f"📦 Total chunks: {len(chunks)}")
#     if chunks:
#         print(f"🧩 First chunk preview:\n'{chunks[0][:200]}'")  # First 200 chars preview