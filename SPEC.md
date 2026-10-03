# TECHNICAL SPECIFICATION (SPEC.md)
## Dự án: RAG Document QA Chatbot

---

## 1. Mục tiêu & Phạm vi dự án
Xây dựng một ứng dụng hỏi đáp tài liệu thông minh (Retrieval-Augmented Generation - RAG) có khả năng phân tích, lập chỉ mục và trả lời câu hỏi chính xác dựa trên bộ tài liệu PDF nội bộ (quy mô 5–10 file PDF, tương đương 100–200 trang). Ứng dụng phải trích dẫn nguồn rõ ràng (tên file và số trang tương ứng) cho mỗi câu trả lời.

---

## 2. Ngăn xếp Công nghệ (Tech Stack)

| Thành phần | Công nghệ lựa chọn | Lý do kiến trúc |
| :--- | :--- | :--- |
| **Ngôn ngữ** | Python (>= 3.10) | Hệ sinh thái AI & Data xử lý tốt nhất. |
| **Giao diện (UI)** | Streamlit | Xây dựng giao diện chat trực quan, phản hồi nhanh, dễ triển khai. |
| **LLM** | `gemini-1.5-pro` | Cửa sổ ngữ cảnh (Context Window) lớn, tốc độ sinh kết quả cao, chi phí tối ưu. |
| **Embedding** | `text-embedding-004` | Mô hình nhúng thế hệ mới của Google, hỗ trợ ngữ nghĩa tiếng Việt chính xác. |
| **RAG Framework** | LangChain (`langchain-google-genai`, `langchain-community`) | Đầy đủ abstractions cho Ingestion, Retrieval, Document Loading và Metadata preservation. |
| **Vector DB** | ChromaDB (`chromadb`) | Cực kỳ nhẹ, hỗ trợ lưu trữ Persistent trên đĩa cứng cục bộ, không cần dựng service riêng biệt. |
| **PDF Parser** | `pypdf` | Đọc nhanh nội dung PDF và tự động trích xuất metadata số trang (`page`). |

---

## 3. Kiến trúc Chi tiết & Luồng dữ liệu (Data Pipeline)

### 3.1. Luồng Nạp dữ liệu (Ingestion Pipeline)
1. **Quét dữ liệu:** Quét toàn bộ file `.pdf` trong thư mục `./data`.
2. **Đọc tài liệu (Document Loading):** Sử dụng `PyPDFLoader` để đọc từng trang:
   - Giữ lại `page_content`.
   - Giữ lại `metadata` gồm `source` (tên file) và `page` (chỉ số trang thực tế, convert từ index 0-based sang 1-based: `page + 1`).
3. **Phân mảnh văn bản (Chunking):**
   - Sử dụng `RecursiveCharacterTextSplitter`.
   - `chunk_size`: 1000 ký tự.
   - `chunk_overlap`: 200 ký tự.
   - `separators`: `["\n\n", "\n", " ", ""]`.
4. **Sinh Vector Nhúng (Embedding):**
   - Sử dụng `GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")`.
5. **Lưu trữ (Vector Persistence):**
   - Lưu trữ chunks và embeddings vào thư mục cục bộ `./chroma_db` với collection tên `pdf_rag_collection`.

### 3.2. Luồng Truy vấn & Phản hồi (Retrieval & QA Pipeline)
1. **Nhận câu hỏi:** Người dùng nhập prompt qua `st.chat_input`.
2. **Truy xuất tương đồng (Retrieval):**
   - Tạo vector nhúng cho câu hỏi.
   - Tìm kiếm Top-$k$ ($k=4$) các đoạn văn bản có độ tương đồng cosine cao nhất qua ChromaDB.
3. **Đóng gói Prompt (Prompt Engineering):**
   - Định dạng Prompt kiểm soát chặt chẽ Hallucination:
     ```text
     Bạn là trợ lý thông minh hỗ trợ trả lời câu hỏi dựa trên tài liệu được cung cấp.
     Chỉ sử dụng thông tin trong phần Ngữ cảnh (Context) sau đây để trả lời.
     Nếu trong Ngữ cảnh không có thông tin hoặc không đủ để kết luận, hãy trả lời trung thực: "Tài liệu được cung cấp không có thông tin này."
     
     Ngữ cảnh:
     {context}

     Câu hỏi: {question}

     Trả lời:
     ```
4. **Sinh phản hồi:** Gọi `ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.2)`.
5. **Trích xuất & Định dạng Nguồn (Source Attribution):**
   - Trích xuất danh sách duy nhất các bộ `(source, page)` từ Top-$k$ context chunks.
   - Định dạng output hiển thị kèm metadata.

---

## 4. Đặc tả Giao diện (Streamlit UI Specification)

### 4.1. Thanh bên (Sidebar)
- **Tình trạng CSDL:** Hiển thị số lượng chunks hiện có hoặc trạng thái "Chưa nạp dữ liệu".
- **Danh sách tài liệu:** Liệt kê các file PDF tìm thấy trong `./data`.
- **Nút hành động:** `[Nạp / Cập nhật Dữ liệu]` -> Khi bấm sẽ kích hoạt hàm Ingestion và reload lại database.

### 4.2. Màn hình chính (Chat Interface)
- Sử dụng `st.chat_message("user")` và `st.chat_message("assistant")`.
- Lưu trữ lịch sử đoạn hội thoại trong `st.session_state.messages`.
- **Format phản hồi hiển thị:**
  ```markdown
  [Nội dung trả lời từ mô hình...]

  ---
  **Nguồn tham khảo:**
  - `Tên_File.pdf` - Trang X
  - `Tên_File_Khác.pdf` - Trang Y
  ```

---

## 5. Cấu trúc Thư mục Dự án

```text
rag-chatbot/
│
├── data/                       # Thư mục chứa các file PDF (5-10 files)
│   ├── Noiquy_congty.pdf
│   └── Sotay_nhanvien.pdf
│
├── chroma_db/                  # Thư mục sinh tự động lưu Vector Database
│
├── .env                        # Biến môi trường: GOOGLE_API_KEY=...
├── requirements.txt            # Thư viện phụ thuộc
├── ingest.py                   # Script xử lý Document Ingestion
└── app.py                      # Ứng dụng chính Streamlit
```

---

## 6. Yêu cầu Cài đặt Thư viện (`requirements.txt`)

```text
streamlit>=1.35.0
langchain>=0.2.0
langchain-google-genai>=1.0.6
langchain-community>=0.2.0
chromadb>=0.5.0
pypdf>=4.2.0
python-dotenv>=1.0.1
```

---

## 7. Các Tiêu chí Nghiệm thu (Acceptance Criteria)
1. **Đọc đúng & đủ:** Đọc được đầy đủ nội dung từ 5–10 file PDF trong `./data` mà không lỗi encoding/font tiếng Việt.
2. **Metadata chính xác:** Mỗi chunk khi truy vấn ra phải mang đúng tên file và số trang gốc.
3. **Độ chính xác cao:** Trả lời chính xác câu hỏi dựa trên tài liệu (ví dụ: số ngày phép, quy trình nội bộ), không bịa thông tin khi tài liệu không đề cập.
4. **Trực quan:** Hiển thị rõ nguồn tài liệu trích dẫn theo từng câu trả lời trên giao diện Streamlit.