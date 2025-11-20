from typing import Any
import os
import requests
from mcp.server.fastmcp import FastMCP

# Create FastMCP server instance
mcp = FastMCP("level3-server")


@mcp.resource(
    "resource://health",
    name="health",
    title="Health",
    description="Server health status",
)
def health() -> str:
    """Return a short health status string for Level 3."""
    return "ok"


@mcp.tool()
def greet(name: str) -> str:
    """Return a greeting message for the provided name."""
    if not isinstance(name, str):
        raise ValueError("name must be a string")
    return f"Hello, {name}! Welcome to MCP."


@mcp.tool()
def math(a: float, b: float, operation: str) -> dict:
    if operation == "add":
        return {"result": a + b}
    if operation == "multiply":
        return {"result": a * b}
    raise ValueError(f"invalid operation: {operation}. expected 'add' or 'multiply'")


@mcp.tool()
def llm_prompt(prompt: str) -> dict[str, Any]:
    """Send a prompt to an LM Studio model and return its output as JSON.

    This function attempts to use the `lm_studio.Client` API. If the package
    or model is not available it will return a deterministic fallback string
    so the demo remains runnable in environments without LM Studio.
    """
    # Use the local LM Studio HTTP API by default. Allow configuring URL
    # and an optional system message via environment variables.
    lm_url = os.environ.get("LMSTUDIO_URL", "http://localhost:1234/v1/chat/completions")
    model = os.environ.get("LMSTUDIO_MODEL", "qwen/qwen3-4b-2507")
    system_msg = os.environ.get("LMSTUDIO_SYSTEM_MESSAGE")

    messages = []
    if system_msg:
        messages.append({"role": "system", "content": system_msg})
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": model,
        "messages": messages,
        "temperature": float(os.environ.get("LMSTUDIO_TEMPERATURE", 0.7)),
        "max_tokens": int(os.environ.get("LMSTUDIO_MAX_TOKENS", -1)),
        "stream": False,
    }

    try:
        resp = requests.post(lm_url, json=payload, timeout=15)
        resp.raise_for_status()
    except Exception as exc:
        return {"result": f"[error] LM Studio request failed: {exc}. Prompt: {prompt}"}

    try:
        data = resp.json()
    except Exception as exc:
        return {"result": f"[error] invalid JSON response from LM Studio: {exc}. Raw: {resp.text}"}

    # Typical chat-completions responses include choices[*].message.content
    try:
        choice = data.get("choices", [None])[0]
        if choice is None:
            raise KeyError("no choices")
        # new-style: choice["message"]["content"]
        if isinstance(choice.get("message"), dict) and "content" in choice["message"]:
            text = choice["message"]["content"]
        elif "text" in choice:
            text = choice["text"]
        else:
            text = str(choice)
    except Exception:
        # Fallback: try common top-level fields
        text = data.get("result") or data.get("text") or str(data)

    return {"result": text}


if __name__ == "__main__":
    import logging

    logging.getLogger("mcp").setLevel(logging.WARNING)
    mcp.run(transport="stdio")
