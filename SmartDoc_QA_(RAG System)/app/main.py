# # main.py
# import streamlit as st

# import sys
# import os

# ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# sys.path.insert(0, ROOT_DIR)

# from rag.ingestion import load_pdf
# from rag.cleaning  import clean_text
# from rag.chunking  import chunk_text
# from rag.indexing  import upload_chunks
# from rag.retriever import search
# from rag.generator import generate_answer
# from rag.embedding import get_embedding


# st.set_page_config(page_title="SmartDoc RAG QA", layout="wide")
# # ---------- HEADER ----------
# st.title("📄 SmartDoc QA")
# st.markdown("Ask questions from your documents. Human-like answers, powered by AI & RAG system.")

# # ---------- ADMIN PANEL (hidden by default) ----------
# with st.expander("⚙️ Admin Panel (Upload New Documents)", expanded=False):
#     admin_key = st.text_input("Enter Admin Key to Upload Documents", type="password")
#     if admin_key == "admin123":  # Change to your own secure key
#         uploaded_files = st.file_uploader(
#         "Upload PDF(s) for indexing", type=["pdf"], accept_multiple_files=True
#         )
#         if uploaded_files:
#             st.info("Processing files...")
#             for file in uploaded_files:
#                 text = load_pdf(file)
#                 cleaned_text = clean_text(text)
#                 chunks = chunk_text(cleaned_text)
#                 upload_chunks(chunks)
#             st.success("✅ Upload complete!")
#     elif admin_key:
#         st.error("❌ Invalid Admin Key!")
# # ---------- USER QUERY PANEL ----------
# st.header("💡 Ask a Question")
# query = st.text_input("Type your question here:")

# if st.button("Ask"):
#     if not query.strip():
#         st.warning("Please enter a question.")
#     else:
#         # -------- Retrieve context ----------
#         # 1. Get embeddings for the query (simulate embedding like chunks)
#         # 2. Search Pinecone
#         # This is a placeholder; replace with your retrieval logic
#         try:
#             query_emb = generate_answer("dummy context", query)  # optional: dummy embedding
#             results = search(query_emb, top_k=5)
#             context = "\n".join([res["metadata"]["text"] for res in results["matches"]]) if results.get("matches") else "Not available in document"
#         except Exception as e:
#             context = "Not available in document"

#         # -------- Generate answer ----------
#         answer = generate_answer(context, query)

#         # -------- Display ----------
#         st.subheader("📝 Answer")
#         st.write(answer)

#         # Optional: show retrieved context
#         with st.expander("🔍 Retrieved Context"):
#             st.write(context)

#         # Feedback buttons
#         col1, col2 = st.columns(2)
#         with col1:
#             if st.button("👍 Helpful"):
#                 st.success("Thanks for your feedback!")
#         with col2:
#             if st.button("👎 Not Helpful"):
#                 st.info("Thanks! We will try to improve.")



# main.py
import streamlit as st
import sys
import os

# ----------------- Project Path Setup -----------------
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT_DIR)

from rag.ingestion import load_pdf
from rag.cleaning import clean_text
from rag.chunking import chunk_text
from rag.indexing import upload_chunks
from rag.retriever import search
from rag.generator import generate_answer
from rag.embedding import get_embedding

# ----------------- Streamlit Page Config -----------------
st.set_page_config(page_title="SmartDoc RAG QA", layout="wide")

st.title("SmartDoc Assistant")

st.markdown("""
Ask questions from your documents and get accurate, context-based answers.

**How it works:**
- Upload your PDF documents (admin access required)
- Ask questions in plain English
- The system retrieves relevant information and generates answers

**Note:**  
If the requested information is not found in the document, the system will clearly indicate it.
""")

st.info("Answers are generated only from the uploaded documents.")

# ---------- ADMIN PANEL ----------
with st.expander("Document Upload (Admin Only)", expanded=False):
    admin_key = st.text_input("Enter Admin Key to Upload Documents", type="password")
    if admin_key == "admin123":  # Change to your secure key
        uploaded_files = st.file_uploader(
            "Upload PDF(s) for indexing", type=["pdf"], accept_multiple_files=True
        )
        if uploaded_files:
            st.info("Processing files...")
            for file in uploaded_files:
                # Load and clean text
                text = load_pdf(file)
                cleaned_text = clean_text(text)
                # Chunk the text
                chunks = chunk_text(cleaned_text)
                # Upload chunks to Pinecone with document metadata
                upload_chunks(chunks, document_name=file.name)
            st.success("✅ Upload complete!")
    elif admin_key:
        st.error("❌ Invalid Admin Key!")

# ---------- USER QUERY PANEL ----------
st.header("Ask Questions from Your Documents")

query = st.text_input(
    "Enter your question (e.g., student details, recommendation, dates, etc.):"
)

if st.button("Get Answer"):
    if not query.strip():
        st.warning("Please enter a question related to the uploaded documents.")
    else:
        # ---------------- Retrieve Context ----------------
        try:
            # 1. Generate query embedding
            query_emb = get_embedding(query)

            # 2. Search Pinecone
            results = search(query_emb, top_k=5)

            # 3. Build context from Pinecone results
            if results and results.matches:
                context = "\n".join([m.metadata.get("text", "") for m in results.matches])
                answer = generate_answer(context, query)
            else:
                answer = "The requested information is not available in the uploaded documents. Please try rephrasing your question."

        except Exception as e:
            # Fallback context for user-friendly message
            context = "The requested information could not be retrieved from the uploaded documents. Please refine your query or try again."
            
            # Log technical details for debugging without exposing to end users
            st.error(f"Retrieval encountered an error. Please contact support if the issue persists.")
            print(f"[ERROR] Retrieval failed: {e}")  # For developer logs
        # ---------------- Generate Answer ----------------
        try:
            answer = generate_answer(context, query)

        except Exception as e:
            # Fallback message for the user
            answer = "The system was unable to generate an answer at this time. Please try again or rephrase your question."
            
            # Friendly, professional notification in the UI
            st.error("An error occurred while generating the answer. Please contact support if the issue persists.")
            
            # Developer log for debugging
            print(f"[ERROR] Answer generation failed: {e}")

        # # ---------------- Display Answer ----------------
        # st.subheader("Answer")
        # st.write(answer)

        # # Optional: show retrieved context
        # with st.expander("Retrieved Context"):
        #     st.write(context)

        # # ---------------- Feedback Buttons ----------------
        # col1, col2 = st.columns(2)
        # with col1:
        #     if st.button("👍 Helpful"):
        #         st.success("Thanks for your feedback!")
        # with col2:
        #     if st.button("👎 Not Helpful"):
        #         st.info("Thanks! We will try to improve.")

        # ---------------- Display Answer ----------------
        st.subheader("Answer")
        st.write(answer)

        # ---------------- Optional: Show Retrieved Context ----------------
        with st.expander("Source Document Context"):
            st.write(context)

        # ---------------- Feedback Section ----------------
        st.markdown("### Feedback")
        col1, col2 = st.columns(2)

        with col1:
            if st.button("Helpful"):
                st.success("Thank you for your feedback!")

        with col2:
            if st.button("Not Helpful"):
                st.info("Thanks! Your feedback will help improve the system.")