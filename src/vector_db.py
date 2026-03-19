from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec

from src.constants import PINECONE_API_KEY, VECTOR_DB_NAME


def get_vector_db():
    pc = Pinecone(api_key=PINECONE_API_KEY)
    index_name = VECTOR_DB_NAME
    if not pc.has_index(index_name):
        pc.create_index(
            name=index_name,
            dimension=384,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )
    index = pc.Index(index_name)
    return index


def get_docs_search(embedding, index_name=VECTOR_DB_NAME):
    docs_search = PineconeVectorStore.from_existing_index(
        embedding=embedding, index_name=index_name
    )
    return docs_search


def get_retriever(docs_search, k=3):
    retriever = docs_search.as_retriever(
        search_type="similarity", search_kwargs={"k": k}
    )
    return retriever