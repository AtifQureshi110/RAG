# from pinecone import Pinecone
# from rag.embedding import get_embedding
# import os
# from dotenv import load_dotenv

# # 🔴 CONTROL FLAG
# UPLOAD = False  # ❗ Change to True ONLY when adding NEW data

# load_dotenv()

# # Initialize Pinecone
# pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
# index = pc.Index("rag-recommandation-letter-project")

# # expected_dim = 3072  # ✅ Pinecone index dimension
# def upload_chunks(chunks):
#     if not UPLOAD:
#         print("⚠️ Upload skipped (UPLOAD = False)")
#         return

#     chunks = [c for c in chunks if c.strip()]
#     vectors = []

#     for i, chunk in enumerate(chunks):
#         emb = get_embedding(chunk)

#         if emb is None:
#             print(f"❌ Skipping chunk {i}, embedding is None")
#             continue

#         print(f"✅ Chunk {i} embedding length: {len(emb)}")

#         vectors.append({
#             "id": str(i),
#             "values": emb,
#             "metadata": {"text": chunk}
#         })

#     print(f"\n📦 Total valid vectors: {len(vectors)}")

#     if vectors:
#         index.upsert(vectors=vectors)
#         print("✅ Uploaded to Pinecone SUCCESSFULLY 🚀")
#     else:
#         print("⚠️ No valid vectors to upload")


# indexing.py
from pinecone import Pinecone
from rag.embedding import get_embedding
import os
from dotenv import load_dotenv
import uuid

load_dotenv()

# Initialize Pinecone
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("rag-recommandation-letter-project")


def upload_chunks(chunks, document_name="unknown_doc"):
    """
    Upload chunks to Pinecone with embeddings.
    """

    # Clean chunks
    chunks = [c for c in chunks if c.strip()]
    vectors = []

    for i, chunk in enumerate(chunks):
        emb = get_embedding(chunk)

        if emb is None:
            print(f"❌ Skipping chunk {i}")
            continue

        safe_doc_name = document_name.replace(" ", "_").lower()
        vector_id = f"{safe_doc_name}_{i}"

        vectors.append({
            "id": vector_id,
            "values": emb,
            "metadata": {
                "text": chunk,
                "source": document_name
            }
        })

        print(f"✅ Chunk {i} embedded")

    print(f"\n📦 Total valid vectors: {len(vectors)}")

    # 🔹 Batch upload (safe for large data)
    batch_size = 50
    for i in range(0, len(vectors), batch_size):
        batch = vectors[i:i + batch_size]
        index.upsert(vectors=batch)

    print("✅ Uploaded to Pinecone SUCCESSFULLY 🚀")


# ================== 🔽 TESTING BLOCK ==================
# if __name__ == "__main__":
#     from ingestion import load_pdf
#     from cleaning import clean_text
#     from chunking import chunk_text
#     from pathlib import Path

#     # 🔹 Smart path
#     project_root = Path(__file__).parent.parent
#     pdf_file = project_root / "data" / "kamran_taj.pdf"

#     # 🔹 Load pipeline
#     text = load_pdf(pdf_file)
#     cleaned = clean_text(text)
#     chunks = chunk_text(cleaned)

#     print(f"📄 Total chunks: {len(chunks)}")

#     # 🔹 Upload to Pinecone
#     upload_chunks(chunks, document_name="kamran_taj.pdf")