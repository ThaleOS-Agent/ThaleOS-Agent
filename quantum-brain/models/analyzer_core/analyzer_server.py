`from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)
analyzer = pipeline("sentiment-analysis")

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    messages = data.get("messages", [])
    results = analyzer(messages)
    return jsonify(results)

if __name__ == "__main__":
    app.run(port=5005)
