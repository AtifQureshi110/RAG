# from pinecone import Pinecone
# import os
# from dotenv import load_dotenv
# load_dotenv()
# pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))


# index_name = "rag-recommandation-letter-project"
# index = pc.Index(index_name)

# def search(query_embedding, top_k=5):
#     results = index.query(
#         vector=query_embedding,
#         top_k=top_k,
#         include_metadata=True
#     )
#     # return results

#     # 🔍 DEBUG: Show what Pinecone returns
#     # print("\n🔍 Retrieved Chunks from Pinecone:\n")
#     # for i, match in enumerate(results["matches"]):
#     #     print(f"Chunk {i}:")
#     #     print(match["metadata"]["text"])
#     #     print("-" * 50)

#     return results

# if __name__ == "__main__":
#     from embedding import get_embedding   # ⚠️ if inside rag → use: from .embedding import get_embedding

#     query = input("Enter your question: ")

#     query_emb = get_embedding(query)

#     results = search(query_emb)


# retriever.py
import os
from dotenv import load_dotenv
from pinecone import Pinecone

# Load environment variables
load_dotenv()

# Initialize Pinecone
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
INDEX_NAME = "rag-recommandation-letter-project"
index = pc.Index(INDEX_NAME)


def search(query_embedding, top_k=5):
    if query_embedding is None:
        print("⚠️ Invalid query embedding. Skipping search.")
        return None

    try:
        results = index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True
        )
        return results  # This is a Pinecone QueryResult object
    except Exception as e:
        print(f"❌ Pinecone query failed: {e}")
        return None

# ================== 🔽 TESTING BLOCK ==================
# if __name__ == "__main__":
#     from embedding import get_embedding

#     query = input("Enter your question: ").strip()
#     if not query:
#         print("⚠️ Empty query provided. Exiting...")
#         exit(1)

#     query_emb = get_embedding(query)
#     if query_emb is None:
#         print("❌ Failed to generate embedding. Exiting...")
#         exit(1)

#     results = search(query_emb, top_k=3)

#     if not results or not results.matches:
#         print("⚠️ No matching results found in Pinecone.")
#     else:
#         print(f"\n💡 Top {len(results.matches)} results:")
#         for i, match in enumerate(results.matches, start=1):
#             text_preview = match.metadata.get("text", "")[:200].replace("\n", " ")
#             source = match.metadata.get("source", "Unknown")
#             print(f"{i}. [{source}] {text_preview}...\n")