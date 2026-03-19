from dotenv import load_dotenv

load_dotenv()


from flask import Flask, jsonify, render_template, request

from src.constants import PROJECT_ROOT

app = Flask(
    __name__,
    static_folder=str(PROJECT_ROOT / "frontend/static"),
    template_folder=str(PROJECT_ROOT / "frontend"),
)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    payload = request.get_json(silent=True) or {}
    user_input = str(payload.get("message", "")).strip()
    if not user_input:
        return jsonify({"msg": "Please enter a question."}), 400

    bot_message = f"You entered: {user_input}"
    return jsonify({"msg": bot_message})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
