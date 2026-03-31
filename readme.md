# MediChat RAG 🏥

A Retrieval-Augmented Generation (RAG) chatbot built around a fictional Portuguese clinic. Powered by LangChain, Google Gemini Embeddings, Pinecone, and Groq (Llama 3).

---

## Tech Stack

| Component        | Technology                        |
|------------------|-----------------------------------|
| Embeddings       | Google Gemini (`embedding-2`)     |
| Vector Store     | Pinecone                          |
| LLM              | Groq API (Llama 3)                |
| RAG Framework    | LangChain                         |
| PDF Processing   | PyPDF                             |

---

## Requirements

- **Python 3.12.10** (strictly required — see setup notes below)
- Pinecone account (free tier)
- Google AI Studio API key (free tier)
- Groq API key (free tier)

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/franciscoamador13/medichat-rag.git
cd medichat-rag
```

### 2. Create a virtual environment

> ⚠️ **Important:** This project requires **Python 3.12.10** specifically.
> Binary installers for Python 3.12 are only available up to version 3.12.10.
> Versions 3.12.11+ and Python 3.13+ do not provide Windows binary installers for all dependencies.
> Python 3.14 is **not compatible** with several dependencies (e.g. NumPy, ChromaDB).
>
> Download Python 3.12.10 here: https://www.python.org/downloads/release/python-31210/

```bash
# Make sure you're using Python 3.12
py -3.12 -m venv venv_medichat

# Activate (Windows CMD — recommended over PowerShell)
venv_medichat\Scripts\activate.bat

# Activate (Mac/Linux)
source venv_medichat/bin/activate

# Confirm the correct version
python --version  # Should print Python 3.12.10
```

> 💡 **Windows PowerShell users:** If you get a script execution error, either use CMD instead,
> or run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` in PowerShell first.

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> ⚠️ **Pinecone compatibility note:** `pinecone-client` was renamed to `pinecone`. Do **not** install `pinecone-client`.
> `langchain-pinecone 0.2.x` requires `pinecone>=6.0.0,<8.0.0` — installing `pinecone 8.x` will cause an `ImportError`.

### 4. Configure environment variables

Create a `.env` file in the root of the project:

```env
GOOGLE_API_KEY=your_google_api_key
PINECONE_API_KEY=your_pinecone_api_key
claude_API_KEY=your_claude_api_key
```

---

## Project Structure

```
medichat-rag/
├── data/               # PDF documents (fictional clinic)
├── venv_medichat/      # Virtual environment (not committed)
├── .env                # API keys (not committed)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Roadmap

- [ ] Phase 1 — PDF ingestion & embedding pipeline
- [ ] Phase 2 — RAG chain with Groq (Llama 3)
- [ ] Phase 3 — FastAPI backend
- [ ] Phase 4 — Streamlit frontend

---

## Notes

- The clinic and all documents used in this project are entirely fictional and for demonstration purposes only.
- This project was developed as part of a personal portfolio toward a career in AI/ML Engineering.