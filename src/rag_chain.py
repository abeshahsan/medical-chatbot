from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain


def get_combine_documents_chain(llm, prompt):
    combine_documents_chain = create_stuff_documents_chain(llm=llm, prompt=prompt)
    return combine_documents_chain


def get_rag_chain(retriever, llm, prompt):
    combine_documents_chain = get_combine_documents_chain(llm=llm, prompt=prompt)
    rag_chain = create_retrieval_chain(
        retriever=retriever,
        combine_docs_chain=combine_documents_chain,
    )
    return rag_chain
