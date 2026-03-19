import os

from from_root import from_root

PROJECT_ROOT = from_root()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL")

VECTOR_DB_NAME = "medical-chatbot"


EMBEDDING_MODEL_NAME = "BAAI/bge-small-en-v1.5"