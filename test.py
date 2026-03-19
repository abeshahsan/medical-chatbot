from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

# Use OpenRouter through the OpenAI-compatible client.
llm = ChatOpenAI(
    model="gpt-4o",
    api_key=os.getenv("OPENAI_API_KEY"), # type: ignore
    base_url=os.getenv("BASE_URL"),
    max_completion_tokens=512
)

# Example usage
response = llm.invoke("What do you know about ACNE?")
print(response.content)

