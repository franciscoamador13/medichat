# MediChat RAG 🏥

A Retrieval-Augmented Generation (RAG) chatbot built around a fictional Portuguese clinic.
Powered by LangChain, Google Gemini Embeddings, Pinecone, and Claude (Anthropic).

---

## Tech Stack

| Component      | Technology                                   |
|----------------|----------------------------------------------|
| Embeddings     | Google Gemini (`gemini-embedding-2-preview`) |
| Vector Store   | Pinecone                                     |
| LLM            | Claude Haiku (`claude-haiku-4-5`)            |
| RAG Framework  | LangChain                                    |
| PDF Processing | PyPDF2                                       |
| Frontend       | Streamlit                                    |

---

## Requirements

- **Python 3.12.10** (strictly required — see setup notes below)
- Pinecone account (free tier)
- Google AI Studio API key (free tier)
- Anthropic API key

---

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/franciscoamador13/medichat-rag.git
cd medichat-rag
```

### 2. Create a virtual environment

> ⚠️ **Important:** This project requires **Python 3.12.10** specifically.
> Python 3.14 is **not compatible** with several dependencies.
>
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
> `langchain-pinecone 0.2.x` requires `pinecone>=6.0.0,<8.0.0`.

### 4. Configure environment variables

Use the `.env.example` provided in the root of the project, name it to `.env` and fill it with your information

### 5. Ingest documents

Place your PDF files in the `data/` folder, then run:
```bash
python ingestion.py
```

This only needs to be run once, or whenever you add new documents.

### 6. Run the app
```bash
streamlit run app.py
```

---

## Project Structure
```
medichat-rag/
├── data/               # PDF documents (fictional clinic)
├── venv_medichat/      # Virtual environment (not committed)
├── .env                # API keys (not committed)
├── .gitignore
├── app.py              # Streamlit app (RAG chatbot)
├── ingestion.py        # PDF ingestion & embedding pipeline
├── requirements.txt
└── README.md
```

---

## How It Works

1. **Ingest** (`ingestion.py`) — PDFs are split into chunks, embedded with Google Gemini, and stored in Pinecone.
2. **Retrieve** — On each user question, the top 3 most relevant chunks are fetched from Pinecone.
3. **Generate** — The retrieved context is injected into the prompt and sent to Claude Haiku for a concise answer.

---

## Notes

- The clinic and all documents used in this project are entirely fictional and for demonstration purposes only.
- This project was developed as part of a personal portfolio toward a career in AI/ML Engineering.