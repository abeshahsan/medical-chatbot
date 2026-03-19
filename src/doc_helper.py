from typing import List

from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter


def load_pdf_files(path):
    loader = PyPDFDirectoryLoader(path=path, recursive=True)
    docs = loader.load()
    return docs


def filter_minimal_docs(docs: List[Document]):
    minimal_docs: List[Document] = []

    for doc in docs:
        minimal_docs.append(
            Document(
                page_content=doc.page_content,
                metadata={"source": doc.metadata["source"]},
            )
        )
    return minimal_docs


def split_and_chunk(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=200)
    splitted_text_chunks = text_splitter.split_documents(documents)
    return splitted_text_chunks
