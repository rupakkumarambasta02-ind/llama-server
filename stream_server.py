from flask import Flask, request, Response
import requests
import json

app = Flask(__name__)
OLLAMA_URL = "http://localhost:11434/api/chat"

@app.route("/openai/v1/chat/completions", methods=["POST"])
def chat_completions():
    data = request.json
    messages = data.get("messages", [])
    model = data.get("model", "codellama:7b")
    temperature = data.get("temperature", 0.7)
    stream = data.get("stream", False)

    ollama_payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "stream": stream
    }

    if stream:
        def generate():
            with requests.post(OLLAMA_URL, json=ollama_payload, stream=True) as r:
                for line in r.iter_lines():
                    if line:
                        chunk = json.loads(line.decode())
                        content = chunk.get("message", {}).get("content", "")
                        if content:
                            yield f'data: {json.dumps({"choices": [{"delta": {"content": content}}]})}\n\n'
            yield 'data: [DONE]\n\n'

        return Response(generate(), content_type='text/event-stream')

    else:
        r = requests.post(OLLAMA_URL, json=ollama_payload)
        r.raise_for_status()
        result = r.json()
        return {
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
        }

if __name__ == "__main__":
    app.run(port=8000)
