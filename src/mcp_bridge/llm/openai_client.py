"""OpenAI-compatible local LLM client wrappers.

Provides:
- chat_completion: low-level request with optional tools
- simple_chat: convenience single-turn helper
- conversational_chat: multi-turn helper maintaining history
"""

from __future__ import annotations

import requests
from typing import List, Dict, Optional, Any

LLM_API_URL = "http://localhost:1234/v1/chat/completions"
DEFAULT_MODEL = "qwen/qwen3-4b-2507"


def chat_completion(
    messages: List[Dict[str, str]],
    model: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = -1,
    stream: bool = False,
    tools: Optional[List[Dict[str, Any]]] = None,
    tool_choice: Optional[Any] = None,
    return_raw: bool = False,
) -> Any:
    """Send a chat completion request to the local LLM server."""
    if not isinstance(messages, list) or len(messages) == 0:
        raise ValueError("messages must be a non-empty list")

    for i, msg in enumerate(messages):
        if not isinstance(msg, dict):
            raise ValueError(f"Message at index {i} must be a dictionary")
        if "role" not in msg or "content" not in msg:
            raise ValueError(
                f"Message at index {i} must have 'role' and 'content' keys"
            )
        if msg["role"] not in ["system", "user", "assistant"]:
            raise ValueError(f"Invalid role '{msg['role']}' at index {i}")

    payload: Dict[str, Any] = {
        "model": model or DEFAULT_MODEL,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": stream,
    }
    if tools is not None:
        payload["tools"] = tools
    if tool_choice is not None:
        payload["tool_choice"] = tool_choice

    print(f"LLM: Chat completion request to {LLM_API_URL}")
    print(f"LLM: Model: {payload['model']}, Messages: {len(messages)}")

    try:
        response = requests.post(
            LLM_API_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=60,
        )
        response.raise_for_status()
        result = response.json()
        if return_raw:
            return result
        if "choices" in result and len(result["choices"]) > 0:
            assistant = result["choices"][0].get("message", {})
            content = assistant.get("content")
            if isinstance(content, str):
                print(f"LLM: Response received ({len(content)} chars)")
                return content
            return ""  # tool_calls case
        raise ValueError("Unexpected response format from LLM API")
    except requests.RequestException as e:  # noqa: BLE001
        print(f"LLM: Error communicating with LLM: {e}")
        raise


def simple_chat(prompt: str, system_message: Optional[str] = None) -> str:
    messages: List[Dict[str, str]] = []
    if system_message:
        messages.append({"role": "system", "content": system_message})
    messages.append({"role": "user", "content": prompt})
    print(f"LLM: Simple chat request: '{prompt[:50]}...'")
    return chat_completion(messages)


def conversational_chat(
    conversation_history: List[Dict[str, str]], new_message: str
) -> Dict[str, Any]:
    messages = conversation_history + [{"role": "user", "content": new_message}]
    print(
        f"LLM: Conversational chat with {len(conversation_history)} previous messages"
    )
    response = chat_completion(messages)
    updated_history = messages + [{"role": "assistant", "content": response}]
    return {"response": response, "updated_history": updated_history}


__all__ = [
    "chat_completion",
    "simple_chat",
    "conversational_chat",
    "DEFAULT_MODEL",
    "LLM_API_URL",
]
