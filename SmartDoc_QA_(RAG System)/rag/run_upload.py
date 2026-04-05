# from ingestion import load_pdf
# from cleaning import clean_text
# from chunking import chunk_text
# from indexing import upload_chunks



# from ingestion import load_pdf
# from cleaning import clean_text
# from chunking import chunk_text
# from indexing import upload_chunks

# # Step 1: just the file path (string)
# file_path = r"E:\RAG Projects\SmartDoc_QA_(RAG System)\data\kamran_taj.pdf"

# # Step 2: extract text
# text = load_pdf(file_path)

# # Step 3: clean text
# cleaned_text = clean_text(text)

# # Step 4: split into chunks
# chunks = chunk_text(cleaned_text)

# print("Total chunks:", len(chunks))
# for i, c in enumerate(chunks[:5]):
#     print(f"Chunk {i}: '{c[:100]}'\n")

# # Step 5: upload to Pinecone
# upload_chunks(chunks)

# # testing purpose 
# # print("Extracted text length:", len(text))

# # cleaned_text = clean_text(text)

# # print("Cleaned text length:", len(cleaned_text))

# # chunks = chunk_text(cleaned_text)

# # print("Total chunks:", len(chunks))

# # for i, c in enumerate(chunks[:3]):
# #     print(f"\nChunk {i}:\n{c[:200]}")