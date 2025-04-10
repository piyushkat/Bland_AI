import streamlit as st
from .config import OPENAI_API_KEY, COUNTRY_CODES
from .document_processor import add_document, load_metadata
from .query_handler import query_documents
from .call_manager import make_call, get_transcript

st.set_page_config(layout="wide", page_title="Document & Call Assistant")

st.title("📚 Document & Call Assistant")
st.markdown("""
This app allows you to:
1. Upload and process documents (PDF, DOCX, TXT)
2. Query the documents using natural language
3. Make AI-powered phone calls about the document content
""")

api_status = "✅ Connected" if OPENAI_API_KEY else "❌ Not connected"
st.sidebar.header("🔑 API Status")
st.sidebar.info(f"OpenAI API: {api_status}")

st.sidebar.header("📂 Document Upload")
file = st.sidebar.file_uploader("Upload Document (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])
if file and st.sidebar.button("Process File"):
    add_document(file)

metadata = load_metadata()
if metadata:
    st.sidebar.header("📚 Processed Documents")
    for doc in metadata:
        st.sidebar.markdown(f"- {doc['file_name']} ({doc['chunks']} chunks)")

st.header("🔍 Document Query")
user_query = st.text_input("Ask a question about your documents or any general query:")
if st.button("Submit Query"):
    if user_query:
        with st.spinner("Processing query..."):
            response = query_documents(user_query, metadata)
            st.markdown("### Answer:")
            st.markdown(response)
    else:
        st.warning("Please enter a query.")

st.sidebar.header("📞 Bland AI Call")
selected_country = st.sidebar.selectbox("Select Country", list(COUNTRY_CODES.keys()))
country_code = COUNTRY_CODES[selected_country]
phone_number = st.sidebar.text_input("Enter Phone Number", placeholder="9876543210")

if st.sidebar.button("📲 Make Call"):
    if phone_number:
        with st.spinner("Initiating call..."):
            full_number = f"{country_code}{phone_number}"
            call_id = make_call(full_number)
            if call_id:
                get_transcript(call_id)
    else:
        st.sidebar.error("❌ Enter a valid phone number.")

st.sidebar.markdown("---")
st.sidebar.markdown("### Model Information")
st.sidebar.info("Using OpenAI GPT-4o for document queries and classification")