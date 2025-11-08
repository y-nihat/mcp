"""
LLM Service Module

Provides utility functions to interact with a local LLM server.
The LLM is expected to be running at http://localhost:1234
"""

import requests
from typing import List, Dict, Optional, Any

# LLM API configuration
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
    """
    Send a chat completion request to the local LLM server.

    Args:
        messages: List of message dictionaries with 'role' and 'content' keys.
                 Example: [{"role": "user", "content": "Hello"}]
        model: The model to use (defaults to qwen/qwen3-4b-2507)
        temperature: Controls randomness (0.0 to 1.0)
        max_tokens: Maximum tokens to generate (-1 for unlimited)
        stream: Whether to stream the response

    Returns:
        The assistant's response content

    Raises:
        ValueError: If messages is empty or malformed
        requests.RequestException: If the API request fails
    """
    # Validate messages
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

    # Prepare request payload
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

        # Extract the assistant's message from the response
        if "choices" in result and len(result["choices"]) > 0:
            assistant = result["choices"][0].get("message", {})
            content = assistant.get("content")
            if isinstance(content, str):
                print(f"LLM: Response received ({len(content)} chars)")
                return content
            # If no content (e.g., tool_calls present), return empty string for backward compat
            # Callers needing structured data should pass return_raw=True.
            return ""
        else:
            raise ValueError("Unexpected response format from LLM API")

    except requests.RequestException as e:
        print(f"LLM: Error communicating with LLM: {e}")
        raise


def simple_chat(prompt: str, system_message: Optional[str] = None) -> str:
    """
    Simple chat interface that sends a single user prompt to the LLM.

    Args:
        prompt: The user's message/question
        system_message: Optional system message to set context or behavior

    Returns:
        The assistant's response
    """
    messages = []

    if system_message:
        messages.append({"role": "system", "content": system_message})

    messages.append({"role": "user", "content": prompt})

    print(f"LLM: Simple chat request: '{prompt[:50]}...'")
    return chat_completion(messages)


def conversational_chat(
    conversation_history: List[Dict[str, str]], new_message: str
) -> Dict[str, Any]:
    """
    Continue a conversation with the LLM by adding a new user message.

    Args:
        conversation_history: Previous messages in the conversation
        new_message: New user message to add

    Returns:
        Dictionary with 'response' and 'updated_history'
    """
    # Append new user message
    messages = conversation_history + [{"role": "user", "content": new_message}]

    print(
        f"LLM: Conversational chat with {len(conversation_history)} previous messages"
    )

    # Get response
    response = chat_completion(messages)

    # Add assistant response to history
    updated_history = messages + [{"role": "assistant", "content": response}]

    return {"response": response, "updated_history": updated_history}


if __name__ == "__main__":
    # Example usage
    print("Testing LLM service functions...\n")

    # Test simple_chat
    try:
        response = simple_chat(
            prompt="What day is it today?",
            system_message="Always answer in rhymes. Today is Thursday",
        )
        print(f"\nResponse: {response}\n")
    except Exception as e:
        print(f"Error: {e}")
