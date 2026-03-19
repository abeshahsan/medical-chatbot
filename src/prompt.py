from langchain.prompts import ChatPromptTemplate


def get_system_prompt():
    system_prompt = (
        "You are an Medical assistant for question-answering tasks. "
        "Use the following pieces of retrieved context to answer "
        "the question. If you don't know the answer, say that you "
        "don't know. Keep the "
        "answer concise."
        "\n\n"
        "{context}"
    )
    return system_prompt


def get_prompt():
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", get_system_prompt()),
            ("human", "{input}"),
        ]
    )
    return prompt
