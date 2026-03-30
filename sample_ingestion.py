import os
import time
import getpass
from dotenv import load_dotenv

# import pinecone
from pinecone import Pinecone, ServerlessSpec

#Import pdf manipulation library
import PyPDF2

# import langchain
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document

load_dotenv() 

pineC = Pinecone(api_key=os.environ.get("PINECONE_KEY"))
if not os.getenv("GOOGLE_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google API key: ")

# initialize pinecone database
index_name = "sample-simpleragbot-index"

# check whether index exists, and create if not
existing_indexes = [index_info["name"] for index_info in pineC.list_indexes()]

if index_name not in existing_indexes:
    pineC.create_index(
        name=index_name,
        dimension=3072,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )
    while not pineC.describe_index(index_name).status["ready"]:
        time.sleep(1)

index = pineC.Index(index_name)

# initialize embeddings model + vector store
embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2-preview")

vector_store = PineconeVectorStore(index=index, embedding=embeddings)

# Iterate through all pdf files in the "data" folder and add them to the vector store
i = 0
for file in os.listdir("data"):
    if file.endswith(".pdf"):
        with open(os.path.join("data", file), "rb") as f:
            pdf_reader = PyPDF2.PdfReader(f)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                if not text.strip():
                    continue  # salta páginas vazias
                i += 1
                doc = Document(
                    page_content=text,
                    metadata={"source": file, "page": page_num + 1}
                )
                vector_store.add_documents(documents=[doc], ids=[f"id{i}"])

