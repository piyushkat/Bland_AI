import numpy as np
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings
from .config import OPENAI_API_KEY
from .document_processor import collection

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
llm = ChatOpenAI(model="gpt-4o", api_key=OPENAI_API_KEY, temperature=0.7)

def query_documents(user_query: str, metadata) -> str:
    if not metadata:
        return "No documents available. Please upload a document first."

    try:
        query_embedding = embedding_model.embed_query(user_query)
        results = collection.query(query_embeddings=[query_embedding], n_results=1)

        if results["documents"] and results["documents"][0]:
            relevant_text = results["documents"][0][0]
            relevant_metadata = results["metadatas"][0][0]

            prompt = f"""
            You are an AI assistant trained to extract information from documents. Answer the user's query based solely on the document below:

            **Document Title:** {relevant_metadata['file_name']}
            **Document Content (Excerpt):**
            {relevant_text[:2000]}

            **User Query:**
            {user_query}

            **Instructions:**
            - Provide an accurate answer based only on the document content.
            - If the document does not contain relevant information, respond with: "The document does not contain relevant information for this query."
            - Keep the response short, clear, and precise.
            - Do not use external knowledge beyond the document.
            """
            
            response = llm.invoke(prompt).content
            if "The document does not contain relevant information" not in response:
                return f"From document '{relevant_metadata['file_name']}': {response}"
            
            prompt_general = f"""
            You are an AI assistant with general knowledge. Answer the user's query:

            **User Query:**
            {user_query}

            **Instructions:**
            - Provide an accurate and concise answer based on general knowledge.
            - Do not reference any specific document.
            """
            return f"From general knowledge: {llm.invoke(prompt_general).content}"
        else:
            prompt_general = f"""
            You are an AI assistant with general knowledge. Answer the user's query:

            **User Query:**
            {user_query}

            **Instructions:**
            - Provide an accurate and concise answer based on general knowledge.
            - Do not reference any specific document.
            """
            return f"From general knowledge: {llm.invoke(prompt_general).content}"
    except Exception as e:
        return f"Error processing query: {e}"