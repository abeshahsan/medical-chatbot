from pathlib import Path

from dotenv import load_dotenv
from from_root import from_root

from src.constants import EMBEDDING_MODEL_NAME, VECTOR_DB_NAME
from src.doc_helper import filter_minimal_docs, load_pdf_files, split_and_chunk
from src.embedding_model import get_embeddings
from src.vector_db import get_docs_search, get_vector_db


def main() -> None:
    load_dotenv()

    data_dir = Path(from_root()) / "data"
    docs = load_pdf_files(str(data_dir))
    docs = filter_minimal_docs(docs)
    chunks = split_and_chunk(docs)

    if not chunks:
        print("No documents found to ingest.")
        return

    embedding = get_embeddings(model_name=EMBEDDING_MODEL_NAME)
    get_vector_db()  # Ensures index exists before connecting the vector store.
    docs_search = get_docs_search(embedding=embedding, index_name=VECTOR_DB_NAME)
    docs_search.add_documents(chunks)

    print(f"Ingested {len(chunks)} chunks into Pinecone index '{VECTOR_DB_NAME}'.")


if __name__ == "__main__":
    main()
