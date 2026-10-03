import os
import sys
import glob
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

# Set stdout to utf-8 to avoid UnicodeEncodeError on Windows
if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Load API key từ .env
load_dotenv()

DATA_DIR = "./data"
CHROMA_PATH = "./chroma_db"

def run_ingestion():
    print("--- 1. Quét và đọc các file PDF ---")
    pdf_files = glob.glob(os.path.join(DATA_DIR, "*.pdf"))
    if not pdf_files:
        print("Không tìm thấy file PDF nào trong thư mục ./data!")
        return

    all_docs = []
    for pdf_path in pdf_files:
        print(f"Đang đọc: {os.path.basename(pdf_path)}")
        loader = PyPDFLoader(pdf_path)
        docs = loader.load()
        # Đảm bảo metadata chứa tên file chuẩn hóa và số trang
        for doc in docs:
            doc.metadata["source"] = os.path.basename(pdf_path)
            doc.metadata["page"] = doc.metadata.get("page", 0) + 1  # Trang bắt đầu từ 1
        all_docs.extend(docs)

    print(f"\nTổng cộng đọc được {len(all_docs)} trang tài liệu.")

    print("\n--- 2. Chia nhỏ văn bản (Chunking) ---")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = text_splitter.split_documents(all_docs)
    print(f"Tạo thành {len(chunks)} đoạn văn bản (chunks).")

    print("\n--- 3. Khởi tạo Embeddings & Lưu vào ChromaDB ---")
    embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2")
    
    # Tạo hoặc cập nhật Chroma vectorstore
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH
    )
    print(f"Hoàn tất nạp dữ liệu vào Vector Store tại '{CHROMA_PATH}'!")

if __name__ == "__main__":
    run_ingestion()