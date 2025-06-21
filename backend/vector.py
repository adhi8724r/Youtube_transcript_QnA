from langchain_chroma import Chroma
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from typing import List
from langchain_core.documents import Document
from dotenv import load_dotenv
vector_store = None

load_dotenv()
embedding = GoogleGenerativeAIEmbeddings(model = 'models/embedding-001')

def create_vectorstore(chunks: List[Document])->FAISS:
    global vector_store
    vector_store = FAISS.from_documents(chunks,embedding)
    return vector_store

def get_vectorstore()->FAISS:
    global vector_store
    return vector_store