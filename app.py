import os
import streamlit as st
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

CHROMA_PATH = "./chroma_db"

st.set_page_config(page_title="RAG Chatbot - Hỏi đáp tài liệu", layout="wide")

# Sidebar
with st.sidebar:
    st.title("📚 Dữ liệu tài liệu")
    if os.path.exists("./data"):
        files = os.listdir("./data")
        st.write("Các tài liệu hiện có:")
        for f in files:
            if f.endswith(".pdf"):
                st.markdown(f"- 📄 `{f}`")
    st.markdown("---")
    st.caption("LLM: gemini-3.5-flash | Embeddings: gemini-embedding-2")

st.title("💬 Chatbot Hỏi Đáp Tài Liệu Nội Bộ")

# Kiểm tra dữ liệu vector store
if not os.path.exists(CHROMA_PATH):
    st.error("Chưa tìm thấy cơ sở dữ liệu ChromaDB. Vui lòng chạy `python ingest.py` trước!")
    st.stop()

# Khởi tạo RAG Chain (cache để không load lại nhiều lần)
@st.cache_resource
def get_rag_chain():
    embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2")
    vectorstore = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
    retriever = vectorstore.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={"k": 3, "score_threshold": 0.4}
    )
    
    llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash", temperature=0.2)

    system_prompt = (
        "Bạn là trợ lý AI trả lời câu hỏi dựa trên các tài liệu nội bộ được cung cấp bên dưới.\n"
        "Chỉ trả lời dựa trên ngữ cảnh (context). Nếu thông tin không có trong tài liệu, hãy trả lời trung thực là không tìm thấy thông tin.\n"
        "Bắt buộc: Ở cuối câu trả lời, hãy trích dẫn nguồn tham khảo theo định dạng [Nguồn: tên_file - Trang X] của CHÍNH XÁC tài liệu mà bạn đã dùng để lấy thông tin. Tuyệt đối không liệt kê các tài liệu không liên quan.\n\n"
        "Ngữ cảnh:\n{context}"
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])

    def format_docs(docs):
        return "\n\n".join(
            f"[Nguồn: {doc.metadata.get('source', 'Unknown')} - Trang {doc.metadata.get('page', 1)}]\n{doc.page_content}" 
            for doc in docs
        )

    rag_chain_from_docs = (
        RunnablePassthrough.assign(context=(lambda x: format_docs(x["context"])))
        | prompt
        | llm
        | StrOutputParser()
    )

    rag_chain_with_source = RunnableParallel(
        {"context": retriever, "input": RunnablePassthrough()}
    ).assign(answer=rag_chain_from_docs)

    return rag_chain_with_source

rag_chain = get_rag_chain()

# Quản lý lịch sử chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Xử lý câu hỏi người dùng
if prompt := st.chat_input("Hỏi điều gì đó về nội quy, sổ tay, phúc lợi..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Đang tìm kiếm thông tin và tạo câu trả lời..."):
            response = rag_chain.invoke(prompt)
            answer = response["answer"]
            
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})