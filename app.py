import streamlit as st
import time
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import Ollama


# PAGE CONFIG
st.set_page_config(page_title="AI Chat Assistant", layout="wide")
st.title("🤖 PDFGPT ")

if "chats" not in st.session_state:
    st.session_state.chats = {"Chat 1": []}

if "current_chat" not in st.session_state:
    st.session_state.current_chat = "Chat 1"
current_chat = st.session_state.current_chat

st.markdown(
    f"""
    <div style='padding:10px; border-radius:10px; background:#1e293b; color:white; margin-bottom:10px;'>
        🟢 <b>Active Chat:</b> {current_chat}
    </div>
    """,
    unsafe_allow_html=True
)



st.sidebar.title("💬 Chats")

if st.sidebar.button("➕ New Chat"):
    new_chat_name = f"Chat {len(st.session_state.chats) + 1}"
    st.session_state.chats[new_chat_name] = []
    st.session_state.current_chat = new_chat_name

for chat_name in st.session_state.chats.keys():
    if chat_name == st.session_state.current_chat:
        st.sidebar.markdown(
            f"""
            <div style="
                padding:8px;
                border-radius:8px;
                background-color:#374151;
                color:white;
                font-weight:bold;
                margin-bottom:5px;
            ">
                💬 {chat_name}
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        if st.sidebar.button(chat_name, key=f"btn_{chat_name}"):
            st.session_state.current_chat = chat_name
            st.rerun()

# LOAD MODEL
llm = Ollama(model="mistral")

# SESSION STATE
messages = st.session_state.chats[st.session_state.current_chat]

if "vectorstores" not in st.session_state:
    st.session_state.vectorstores = {}

# DISPLAY CHAT HISTORY
for msg in messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# FILE UPLOAD
uploaded_files = st.file_uploader(
    f"Upload PDFs for {st.session_state.current_chat}",
    type="pdf",
    accept_multiple_files=True,
    key=f"uploader_{st.session_state.current_chat}"
)

if uploaded_files:
    st.write("📂 Uploaded PDFs:")
    for file in uploaded_files:
        st.write(f"• {file.name}")

if uploaded_files and st.session_state.current_chat not in st.session_state.vectorstores:

    all_docs = []

    for uploaded_file in uploaded_files:
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.read())

        loader = PyPDFLoader("temp.pdf")
        documents = loader.load()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=100
        )

        docs = splitter.split_documents(documents)
        all_docs.extend(docs)

    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    vectorstore = FAISS.from_documents(all_docs, embeddings)

    st.session_state.vectorstores[st.session_state.current_chat] = vectorstore

    st.success(f"✅ {len(uploaded_files)} PDFs processed!")



# CHAT INPUT
query = st.chat_input("Ask something...")

vectorstore = st.session_state.vectorstores.get(st.session_state.current_chat)

if query:
    messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    if vectorstore is None:
        with st.chat_message("assistant"):
            st.markdown("⚠️ Please upload a PDF first.")
    else:
        chat_history = "\n".join(
            [f"{m['role']}: {m['content']}" for m in messages[-4:]]
        )

        rewrite_prompt = f"""
        Given the conversation below, rewrite the latest question to be fully self-contained.

        Conversation:
        {chat_history}

        Latest question:
        {query}

        Rewritten question:
        """

        rewritten_query = llm.invoke(rewrite_prompt)

        results = vectorstore.similarity_search(rewritten_query, k=4)

        cleaned_chunks = []
        for doc in results:
            text = doc.page_content.replace("\n", " ").strip()
            cleaned_chunks.append(text)

        context = " ".join(cleaned_chunks)
        context = context[:1000]

        prompt = f"""
        You are a very helpful AI assistant.

        Answer clearly and concisely based only on the context given.

        Context:
        {context}

        Question: {query}

        Answer:
        """

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = llm.invoke(prompt)

                def stream_text(text):
                    for word in text.split():
                        yield word + " "
                        time.sleep(0.02)

                st.write_stream(stream_text(response))

        messages.append({
            "role": "assistant",
            "content": response
        })