# from google import genai
# import os
# from dotenv import load_dotenv
# from pinecone import Pinecone
# from embedding import get_embedding

# # 🔴 CONTROL FLAG

# load_dotenv()

# api_key = os.getenv("GOOGLE_API_KEY")
# client = genai.Client(api_key=api_key)

# def generate_answer(context, query):
#     # 🔹 Prompt
#     prompt = f"""
#     You are an AI assistant.

#     Answer from the context as accurately as possible.
#     If the answer is partially available, try to extract it.
#     Only say "Not available in document" if absolutely no information exists.

#     Context:
#     {context}

#     Question:
#     {query}
#     """

#     response = client.models.generate_content(
#         model="models/gemini-2.5-flash",
#         contents=prompt
#     )

#     return response.text.strip()


# if __name__ == "__main__":
#     from embedding import get_embedding
#     from retriever import search

#     query = input("Enter your question: ")

#     # 🔹 Step 1: get query embedding
#     query_emb = get_embedding(query)

#     # 🔹 Step 2: retrieve from Pinecone
#     results = search(query_emb, top_k=3)

#     # 🔹 Step 3: build context from Pinecone
#     context = "\n\n".join([m["metadata"]["text"] for m in results["matches"]])

#     # 🔹 Step 4: generate answer
#     answer = generate_answer(context, query)

#     print("\n💡 Final Answer:\n", answer)


# generator.py
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise ValueError("❌ GOOGLE_API_KEY not found")

client = genai.Client(api_key=API_KEY)


def generate_answer(context, query):
    """
    Generate answer using retrieved context.
    """

    if not context.strip():
        return "Sorry, I could not find relevant information in the document."

    prompt = f"""
You are a helpful AI assistant.

Answer the question based ONLY on the provided context.
If the answer is partially available, try to infer carefully.
If no relevant information exists, say: "Not available in document".

Context:
{context}

Question:
{query}

Answer in a clear and human-friendly way:
"""

    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=prompt
    )

    return response.text.strip()


# ================== 🔽 TESTING BLOCK ==================
# if __name__ == "__main__":
#     from embedding import get_embedding
#     from retriever import search

#     query = input("Enter your question: ")

#     # 🔹 Step 1: Embedding
#     query_emb = get_embedding(query)

#     if query_emb is None:
#         print("❌ Failed to generate embedding")
#         exit()

#     # 🔹 Step 2: Retrieve from Pinecone
#     results = search(query_emb, top_k=3)

#     matches = results.get("matches", [])

#     if not matches:
#         print("⚠️ No relevant data found in Pinecone")
#         context = ""
#     else:
#         # 🔹 Step 3: Build context
#         context = "\n\n".join([m["metadata"]["text"] for m in matches])

#         print("\n🔍 Retrieved Context:\n")
#         for i, m in enumerate(matches):
#             print(f"Chunk {i} (Score: {m['score']:.4f})")
#             print(m["metadata"]["text"])
#             print("-" * 50)

#     # 🔹 Step 4: Generate Answer
#     answer = generate_answer(context, query)

#     print("\n💡 Final Answer:\n", answer)