from dotenv import load_dotenv

load_dotenv()


from flask import Flask, jsonify, render_template, request

from src.constants import EMBEDDING_MODEL_NAME, PROJECT_ROOT
from src.embedding_model import get_embeddings
from src.llm import get_llm
from src.prompt import get_prompt
from src.rag_chain import get_rag_chain
from src.vector_db import get_docs_search, get_retriever

app = Flask(
    __name__,
    static_folder=str(PROJECT_ROOT / "frontend/static"),
    template_folder=str(PROJECT_ROOT / "frontend"),
)

embedding = get_embeddings(model_name=EMBEDDING_MODEL_NAME)
docs_search = get_docs_search(embedding=embedding)
retriever = get_retriever(docs_search=docs_search, k=3)

llm = get_llm()
prompt = get_prompt()


rag_chain = get_rag_chain(retriever=retriever, llm=llm, prompt=prompt)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    payload = request.get_json(silent=True) or {}
    user_input = str(payload.get("message", "")).strip()
    if not user_input:
        return jsonify({"msg": "Please enter a question."}), 400

    llm_response = rag_chain.invoke({"input": user_input})

    bot_message = f"{llm_response['answer']}"
    return jsonify({"msg": bot_message})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
