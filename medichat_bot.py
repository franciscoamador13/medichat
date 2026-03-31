from typing import List
from getpass import getpass

import os
import streamlit as st
import anthropic
from dotenv import load_dotenv
from pinecone import Pinecone
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

# ── Config ────────────────────────────────────────────────────────────────────

load_dotenv()

SYSTEM_PROMPT = """You are an assistant for question-answering tasks.
Use the following pieces of retrieved context to answer the question.
If you don't know the answer, or it is not in the context, just say that you don't know.
Use three sentences maximum and keep the answer concise.
Do not use Markdown formatting in your response.
Context: {context}"""

# ── Initialization (cached) ────────────────────────────────────────────────────

@st.cache_resource #This prevents the vector store and llm from being reloaded on every interaction, which would be inefficient.
def load_vector_store() -> PineconeVectorStore:
    if not os.getenv("GOOGLE_API_KEY"):
        os.environ["GOOGLE_API_KEY"] = getpass("Enter your Google API key: ")

    index = Pinecone(api_key=os.environ["PINECONE_KEY"]).Index(os.environ["PINECONE_INDEX_NAME"])
    embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2-preview")
    return PineconeVectorStore(index=index, embedding=embeddings)

@st.cache_resource
def load_llm() -> ChatAnthropic:
    return ChatAnthropic(model="claude-haiku-4-5", max_tokens=1000, temperature=1)

# ── App ───────────────────────────────────────────────────────────────────────

st.title("MediChat - A RAG Bot for Medical Question-Answering")

vector_store = load_vector_store()
llm = load_llm()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Messages history
for message in st.session_state.messages:
    role = "user" if isinstance(message, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.markdown(message.content)

# User inputs
if prompt := st.chat_input("Ask a question about the functioning of the company"):
    st.session_state.messages.append(HumanMessage(prompt))
    with st.chat_message("user"):
        st.write(prompt)

    # Retrieval + response
    with st.spinner("Thinking..."):
        retriever = vector_store.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={"k": 3, "score_threshold": 0.5},
        )
        docs = retriever.invoke(prompt)
        context = "".join(doc.page_content for doc in docs)

        messages_to_send = [
            SystemMessage(SYSTEM_PROMPT.format(context=context)),
            *st.session_state.messages,
        ]

        try:
            result = llm.invoke(messages_to_send).content
        except anthropic._exceptions.OverloadedError:
            result = "Sorry, the model is currently overloaded. Please try again in a bit."
        except Exception:
            result = "Sorry, something went wrong. Please try again in a bit."

    st.session_state.messages.append(AIMessage(result))
    with st.chat_message("assistant"):
        st.write(result)