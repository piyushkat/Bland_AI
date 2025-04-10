import os
import pdfplumber
from docx import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
import chromadb
from chromadb.config import Settings
import streamlit as st
from .config import DATA_DIR, CHROMA_PERSIST_DIR

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
chroma_client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIR, settings=Settings(anonymized_telemetry=False))
collection = chroma_client.get_or_create_collection(name="document_embeddings")

def extract_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    try:
        if ext == ".pdf":
            with pdfplumber.open(file_path) as pdf:
                return "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
        elif ext == ".docx":
            doc = Document(file_path)
            return "\n".join([p.text for p in doc.paragraphs])
        elif ext == ".txt":
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
    except Exception as e:
        st.error(f"Error extracting text: {e}")
    return ""

def add_document(file):
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    file_path = os.path.join(DATA_DIR, file.name)
    with open(file_path, "wb") as f:
        f.write(file.getbuffer())

    text = extract_text(file_path)
    if not text:
        st.error("No extractable text found.")
        return

    splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=150)
    chunks = splitter.split_text(text)
    
    if not chunks:
        st.error("Failed to split document into chunks.")
        return
    
    try:
        embeddings = embedding_model.embed_documents(chunks)
        ids = [f"{file.name}_{i}" for i in range(len(chunks))]
        metadatas = [{"file_name": file.name, "chunk_index": i} for i in range(len(chunks))]

        collection.add(embeddings=embeddings, documents=chunks, metadatas=metadatas, ids=ids)

        metadata = load_metadata()
        metadata.append({"file_name": file.name, "chunks": len(chunks)})
        with open(os.path.join(DATA_DIR, "metadata.json"), "w") as f:
            json.dump(metadata, f, indent=4)

        st.success(f"📄 {file.name} uploaded & processed successfully!")
    except Exception as e:
        st.error(f"Error processing document: {e}")

def load_metadata():
    metadata_file = os.path.join(DATA_DIR, "metadata.json")
    if os.path.exists(metadata_file):
        try:
            with open(metadata_file, "r") as f:
                content = f.read().strip()
                if not content:
                    return []
                return json.loads(content)
        except json.JSONDecodeError:
            st.error("❌ Error: metadata.json is corrupted. Resetting...")
            os.remove(metadata_file)
            return []
    return []