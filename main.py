from dotenv import load_dotenv

load_dotenv()

from src.constants import EMBEDDING_MODEL_NAME
from src.embedding_model import get_embeddings
from src.llm import get_llm
from src.prompt import get_prompt
from src.rag_chain import get_rag_chain
from src.vector_db import get_docs_search, get_retriever

embedding = get_embeddings(model_name=EMBEDDING_MODEL_NAME)
docs_search = get_docs_search(embedding=embedding)
retriever = get_retriever(docs_search=docs_search, k=3)

llm = get_llm()
prompt = get_prompt()


rag_chain = get_rag_chain(retriever=retriever, llm=llm, prompt=prompt)


print(rag_chain.invoke({"input": "What do you know about ACNE?"}))
