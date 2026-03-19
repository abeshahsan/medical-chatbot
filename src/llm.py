import os

from langchain_openai import ChatOpenAI

from src.constants import OPENROUTER_BASE_URL, OPENROUTER_API_KEY

# Use OpenRouter through the OpenAI-compatible client.


# llm = ChatOpenAI(
#     model="gpt-4o",
#     api_key=OPENROUTER_API_KEY,  # type: ignore
#     base_url=OPENROUTER_BASEURL,
#     max_completion_tokens=512,
# )


def get_llm():
    llm = ChatOpenAI(
        model="gpt-4o",
        api_key=OPENROUTER_API_KEY,  # type: ignore
        base_url=OPENROUTER_BASE_URL,
        max_completion_tokens=512,
    )
    return llm
