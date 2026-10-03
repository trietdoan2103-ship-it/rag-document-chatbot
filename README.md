# 💬 RAG QA Document Chatbot

An internal enterprise document Question & Answering assistant built on modern **RAG (Retrieval-Augmented Generation)** architecture using **LangChain (LCEL)**, **ChromaDB**, **Google Gemini LLM**, and **Streamlit**.

---

## 📌 Project Overview
The system enables users to ask natural language questions regarding internal organization documents (such as labor regulations, employee handbooks, leave policies, IT security, and travel expense guidelines). It retrieves the most relevant context and synthesizes precise, hallucination-resistant answers with exact document citations (file name and page number).

---

## 🚀 Key Features
- **Automated PDF Parsing & Indexing**: Reads PDF files, performs semantic chunking via `RecursiveCharacterTextSplitter`, and preserves metadata (`source`, `page`).
- **Local Vector Search**: Stores embeddings in a local **ChromaDB** vector store powered by high-performance embedding models (`gemini-embedding-2` / `text-embedding-004`).
- **LangChain Expression Language (LCEL)**: Modern, modular pipeline leveraging `RunnablePassthrough` and `RunnableParallel` for optimal streaming and document retrieval.
- **Accurate Document Citations**: Cites exclusively the source document and page number utilized to construct the answer, avoiding citation clutter.
- **Interactive UI**: Built with Streamlit, featuring an interactive chat interface and a sidebar displaying active indexed documents.

---

## 🛠️ Tech Stack
- **Language**: Python 3.10+
- **LLM**: Google Gemini (`gemini-3.5-flash` / `gemini-1.5-pro`)
- **Embeddings**: `gemini-embedding-2` / `text-embedding-004`
- **Orchestration**: LangChain (LCEL)
- **Vector Database**: ChromaDB
- **User Interface**: Streamlit
- **PDF Generation & Loading**: ReportLab, PyPDF

---

## 📂 Project Structure
```text
new_chatbot_rag/
├── data/                   # Source directory for internal PDF documents
├── chroma_db/              # Local persistent Chroma vector store (auto-generated)
├── .env                    # Environment variables (GOOGLE_API_KEY)
├── .gitignore              # Excludes secrets, cache, and vector store files
├── requirements.txt        # Python dependency specifications
├── generate_samples.py     # Script to generate sample standard company policies
├── ingest.py               # Document loader, text chunking, and embedding pipeline
├── app.py                  # Streamlit web application with RAG retrieval chain
├── SPEC.md                 # System architecture and engineering specification
└── README.md               # Project documentation and user guide

##⚙️ Installation & Quick Start
1. Clone the Repository
git clone https://github.com/trietdoan2103-ship-it/rag-document-chatbot
cd rag-document-chatbot

2. Set Up a Virtual Environment
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate

3. Install Dependencies
pip install -r requirements.txt

4. Configure Environment Variables
Create a .env file in the project root directory:
GOOGLE_API_KEY=your_gemini_api_key_here
Obtain your API key from Google AI Studio

5. Generate Sample Documents (Optional)
If you do not have documents in the ./data folder yet, generate 5 sample internal PDF policies:
python generate_samples.py

6. Ingest & Index Documents
python ingest.py

7. Launch the Application
streamlit run app.py
The application will automatically open in your browser at: http://localhost:8501.

##📖 User Guide
How to Use the Application
Verify Loaded Documents: Check the left sidebar under "Dữ liệu tài liệu" to ensure all target PDF files in ./data/ are recognized.

Submit a Query: Type your question into the chat input bar at the bottom of the screen and press Enter.

Review Answers & Source Citations: The assistant will stream or display the answer derived strictly from the contextual chunks, followed by a citation block (e.g., [Nguồn: Quy_dinh_nghi_phep_va_phuc_loi.pdf - Trang 1]).

Adding New Documents:

Place your new .pdf files into the ./data/ directory.

Run python ingest.py in your terminal to re-index the database.

Refresh the Streamlit page (F5 or Rerun).