# 🤖 PDFGPT –Tiny LLM for Your PDFs

An AI-powered chatbot that lets users upload multiple PDF files and communicate with them in natural language. Developed using Retrieval-Augmented Generation (RAG) and a local LLM.
---

## 🚀 Features

* Multiple PDFs per chat (independent knowledge per chat)
* Semantic search using FAISS
* Local LLM (Mistral(OLLAMA))
* Context-aware follow-up questions (query rewriting)
* Clean UI with active chat highlighting

---

## 🧠 How It Works (Architecture)

```text
User Query
   ↓
Query Rewriting (context-aware)
   ↓
FAISS Vector Search
   ↓
Relevant Chunks Retrieved
   ↓
LLM (Mistral via Ollama)
   ↓
Final Answer (streamed)
```

---

## 🛠️ Tech Stack

| Component  | Technology            |
| ---------- | --------------------- |
| UI         | Streamlit             |
| LLM        | Mistral (via Ollama)  |
| Framework  | LangChain             |
| Vector DB  | FAISS                 |
| Embeddings | Sentence Transformers |
| Language   | Python                |

---

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/RahulBharadwaj90/PDFGPT.git
cd PDFGPT
```

---

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Install Ollama

Download: https://ollama.com

Run model:

```bash
ollama run mistral
```

---

## ▶️ Run the App

```bash
python -m streamlit run app.py
```

---

## 📌 Usage

1. Click ➕ New Chat
2. Upload one or multiple PDFs
3. Ask questions about your documents
4. Switch between chats
5. Each chat maintains its own PDFs and history

---

## ⚠️ Limitations

* Runs on CPU → slower response time
* Small models may hallucinate
* No persistent storage (resets on refresh)
* No source citation (yet)
* Depends heavily on retrieval quality

---

## 🚀 Future Improvements

* Show source (PDF + page number)
* Save chats and PDFs (database)
* Deploy online (Streamlit Cloud / Render)
* Improve accuracy with better models
* Add document-level filtering

---

## 🧠 Key Concepts Implemented

* Retrieval-Augmented Generation (RAG)
* Vector Databases (FAISS)
* HuggingFace(Embeddings)
* Query Rewriting (Context Awareness)
* Local LLM Integration

---

## 📸 Screenshots

<img width="1911" height="824" alt="image" src="https://github.com/user-attachments/assets/5e034c6f-7452-4d74-8299-b1602eb96e79" />

<img width="1919" height="815" alt="image" src="https://github.com/user-attachments/assets/86766d7e-14a4-42f0-bc76-a8e7b7d04fc7" />

<img width="1917" height="810" alt="image" src="https://github.com/user-attachments/assets/dbc60882-e852-4c1a-881f-bd3218017b7d" />

