# tell me how it basically work what's basic purpose and here a dummy testing is performing do not like that if i have real data so make it from that 

# from google import genai
# import os
# from dotenv import load_dotenv


# # Load environment variables from .env
# load_dotenv()

# api_key = os.getenv("GOOGLE_API_KEY")
# client = genai.Client(api_key=api_key)


# def get_embedding(text):
#     try:
#         if not text.strip():
#             print("⚠️ Empty text received")
#             return None

#         emb_response = client.models.embed_content(
#             model="models/gemini-embedding-001",
#             contents=text
#         )

#         emb = emb_response.embeddings[0].values

#         print(f"✅ Embedding generated, length: {len(emb)}")  # DEBUG

#         return emb

#     except Exception as e:
#         print("❌ Embedding error:", e)
#         return None
    
# # if __name__ == "__main__":
# #     test_text = "This is a test sentence"
# #     result = get_embedding(test_text)
# #     print("Result:", result[:5] if result else "None")

# embedding.py
from google import genai
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise ValueError("❌ GOOGLE_API_KEY not found in .env")

# Initialize GenAI client
client = genai.Client(api_key=API_KEY)


def get_embedding(text):
    """
    Generate embedding for a single text chunk.

    Args:
        text (str): The text to embed.

    Returns:
        list[float] | None: Embedding vector or None if error.
    """
    try:
        if not text or not text.strip():
            print("⚠️ Empty text received, skipping embedding")
            return None

        response = client.models.embed_content(
            model="models/gemini-embedding-001",
            contents=text
        )

        emb = response.embeddings[0].values
        print(f"✅ Embedding generated, length: {len(emb)}")
        return emb

    except Exception as e:
        print(f"❌ Embedding error: {e}")
        return None


def get_embeddings(chunks):
    """
    Generate embeddings for a list of text chunks.

    Args:
        chunks (list[str]): List of text chunks.

    Returns:
        list[dict]: Each dict contains {"text": chunk, "embedding": emb}
    """
    results = []
    for i, chunk in enumerate(chunks):
        emb = get_embedding(chunk)
        if emb:
            results.append({"text": chunk, "embedding": emb})
        else:
            print(f"⚠️ Skipped chunk {i} due to empty or failed embedding")
    return results

# ================== 🔽 TESTING BLOCK ==================
# if __name__ == "__main__":
#     # Example: run only for testing real document chunks
#     from ingestion import load_pdf
#     from cleaning import clean_text
#     from chunking import chunk_text
#     from pathlib import Path

#     # Project root and data file
#     project_root = Path(__file__).parent.parent
#     pdf_file = project_root / "data" / "kamran_taj.pdf"

#     # Load, clean, and chunk PDF text
#     text = load_pdf(pdf_file)
#     cleaned_text = clean_text(text)
#     chunks = chunk_text(cleaned_text)

#     print(f"📦 Total chunks to embed: {len(chunks)}")

#     # Generate embeddings for all chunks
#     embeddings = get_embeddings(chunks)
#     print(f"✅ Total embeddings generated: {len(embeddings)}")
#     print(f"🧩 Preview first chunk embedding: {embeddings[0]['embedding'][:10]}")