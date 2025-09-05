# Local LLM API with CodeLlama 7B via Ollama

This project wraps the open-source CodeLlama 7B model (running locally via Ollama) in an OpenAI-compatible REST API. It supports both standard and streaming chat completions.

🚀 Features
✅ Local inference using CodeLlama 7B

✅ OpenAI-style /v1/chat/completions endpoint

✅ Streaming and non-streaming support

✅ LangChain-compatible prompt templates

✅ Easy integration with existing OpenAI clients

🛠️ Installation
1. Install Ollama
Download and install Ollama from https://ollama.com/download

Verify installation:

ollama --version

2. Pull CodeLlama 7B Model

ollama pull codellama:7b


🧪 Run the Model
Start the model server:

ollama run codellama:7b

This exposes a local endpoint at:

http://localhost:11434/api/chat

🧰 Non-Streaming Setup
▶️ Start the Non-Streaming Server

python server.py

This exposes:
POST http://localhost:8000/openai/v1/chat/completions

💬 Run the Non-Streaming Client
python client.py

The client sends OpenAI-style requests and prints the full response after completion.

🌊 Streaming Setup

▶️ Start the Streaming Server
python server_stream.py

This exposes:
POST http://localhost:8000/openai/v1/chat/completions

with stream: true support.

💬 Run the Streaming Client
python client_stream.py

The client sends a streaming request and prints tokens as they arrive.

📄 Example Payload
{
  "model": "codellama:7b",
  "messages": [
    { "role": "user", "content": "Write a Python function to reverse a string." }
  ],
  "temperature": 0.7,
  "max_tokens": 500,
  "stream": true
}

🧩 Notes
Ollama auto-detects GPU (e.g., RTX 3060) and uses it if available.

Streaming responses follow OpenAI’s SSE format (data: {...}\n\n).

You can integrate this with LangChain using ChatOpenAI and base_url="http://localhost:8000/openai/v1".