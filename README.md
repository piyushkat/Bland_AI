# Bland_AI
# Document & Call Assistant

This is a Streamlit-based application that allows users to upload documents (PDF, DOCX, TXT), query them using natural language, and make AI-powered phone calls using Bland AI to discuss document content.

## Features
1. **Document Processing**: Upload and process documents into chunks stored in ChromaDB.
2. **Query Handling**: Ask questions about documents with answers prioritized from the document content, falling back to general knowledge if needed.
3. **AI Phone Calls**: Initiate calls with Bland AI to discuss document content, with live transcript display.

## Folder Structure
DocumentCallAssistant/
├── src/                    # Source code
│   ├── init.py         # Package marker
│   ├── config.py          # Configuration and API keys
│   ├── document_processor.py # Document processing logic
│   ├── query_handler.py    # Query handling logic
│   ├── call_manager.py     # Call and transcript management
│   └── app.py             # Main Streamlit app
├── .env                    # Environment variables (not tracked)
├── .gitignore             # Git ignore file
├── README.md              # This file
└── requirements.txt       # Dependencies


## Setup
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/piyushkat/Bland_AI.git
   cd DocumentCallAssistant
Install Dependencies:

pip install -r requirements.txt

Set Environment Variables: Create a .env file in the root directory with:

OPENAI_API_KEY=your_openai_api_key
BLAND_AI_API_KEY=your_bland_ai_api_key

#### `requirements.txt`
streamlit
pdfplumber
python-docx
langchain
langchain-openai
langchain-huggingface
chromadb
requests
torch
numpy
python-dotenv

### Instructions to Use
1. **Create the Folder Structure**: Manually create the directories and files as outlined above, copying each code block into the respective file.
2. **Install Dependencies**: Run `pip install -r requirements.txt` after creating `requirements.txt`.
3. **Set Up `.env`**: Add your API keys to a `.env` file.
4. **Run the App**: Use `streamlit run src/app.py` from the `DocumentCallAssistant` directory.
