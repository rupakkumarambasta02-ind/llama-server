from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "codellama:7b"

@app.route("/openai/v1/chat/completions", methods=["POST"])
def chat_completions():
    data = request.json

    # Extract OpenAI-style fields
    messages = data.get("messages", [])
    model = data.get("model", OLLAMA_MODEL)
    temperature = data.get("temperature", 0.7)
    max_tokens = data.get("max_tokens", 512)
    print(model, temperature)

    # Forward to Ollama
    ollama_payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=ollama_payload)
        response.raise_for_status()
        result = response.json()

        # Wrap Ollama response in OpenAI-style format
        return jsonify({
            "id": "chatcmpl-local",
            "object": "chat.completion",
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": result["message"]["content"]
                },
                "finish_reason": "stop"
            }],
            "model": model
        })

    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=8000)
