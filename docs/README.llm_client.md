# LLM Client Usage

Provides utility functions for interacting with a local OpenAI-compatible LLM server (chat completions, single-prompt chat, multi-turn conversations).

## Prerequisites

- Local LLM server running at `http://localhost:1234` (e.g., LM Studio, LocalAI, Ollama)
- Python 3.9+
- Install dependencies: `pip install -e .[dev]`

## Basic Usage

```python
from mcp_bridge.llm.openai_client import simple_chat, chat_completion, conversational_chat

# Simple single-prompt chat
response = simple_chat(
    prompt="What is Python?",
    system_message="You are a helpful programming tutor."
)
print(response)

# Full control with chat_completion
response = chat_completion(
    messages=[
        {"role": "system", "content": "Always answer in rhymes."},
        {"role": "user", "content": "What day is it today?"}
    ],
    temperature=0.7,
)
print(response)

# Multi-turn conversation
conv = conversational_chat()
conv.send_user("Tell me a joke.")
conv.send_user("Make it about Python.")
print(conv.get_history())
```

## Features

- OpenAI-compatible API
- System prompt, temperature, max tokens, streaming
- Error handling for invalid inputs

See `src/mcp_bridge/llm/openai_client.py` for details.
