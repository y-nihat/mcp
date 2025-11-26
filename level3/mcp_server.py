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
    """Return a greeting message using LLM."""
    if not isinstance(name, str):
        raise ValueError("name must be a string")
    
    lm_url = os.environ.get("LMSTUDIO_URL", "http://localhost:1234/v1/chat/completions")
    model = os.environ.get("LMSTUDIO_MODEL", "qwen/qwen3-4b-2507")
    
    prompt = f"Generate a friendly greeting for {name}. Mention MCP. One sentence."
    messages = [
        {"role": "system", "content": "You are a friendly assistant."},
        {"role": "user", "content": prompt}
    ]
    
    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": int(os.environ.get("LMSTUDIO_MAX_TOKENS", 100)),
        "stream": False,
    }
    
    try:
        resp = requests.post(lm_url, json=payload, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        
        choice = data.get("choices", [None])[0]
        if choice is None:
            raise KeyError("no choices")
        
        if isinstance(choice.get("message"), dict) and "content" in choice["message"]:
            text = choice["message"]["content"].strip()
        elif "text" in choice:
            text = choice["text"].strip()
        else:
            text = str(choice).strip()
        
        return text
        
    except Exception as exc:
        return f"[error] LLM greeting failed: {exc}. Fallback: Hello, {name}!"


@mcp.tool()
def math(a: float, b: float, operation: str) -> dict:
    """Perform math operations using LLM."""
    lm_url = os.environ.get("LMSTUDIO_URL", "http://localhost:1234/v1/chat/completions")
    model = os.environ.get("LMSTUDIO_MODEL", "qwen/qwen3-4b-2507")
    
    prompt = f"Calculate {a} {operation} {b}. Return only the number."
    messages = [
        {"role": "system", "content": "You are a calculator. Return only the numeric result."},
        {"role": "user", "content": prompt}
    ]
    
    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.0,
        "max_tokens": int(os.environ.get("LMSTUDIO_MAX_TOKENS", 50)),
        "stream": False,
    }
    
    try:
        resp = requests.post(lm_url, json=payload, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        
        choice = data.get("choices", [None])[0]
        if choice is None:
            raise KeyError("no choices")
        
        if isinstance(choice.get("message"), dict) and "content" in choice["message"]:
            text = choice["message"]["content"].strip()
        elif "text" in choice:
            text = choice["text"].strip()
        else:
            text = str(choice).strip()
        
        try:
            result = float(text)
        except ValueError:
            import re
            numbers = re.findall(r'-?\d+\.?\d*', text)
            if numbers:
                result = float(numbers[0])
            else:
                result = text
        
        return {"result": result}
        
    except Exception as exc:
        return {"result": f"[error] LLM calculation failed: {exc}"}


@mcp.tool()
def llm_prompt(prompt: str) -> dict[str, Any]:
    """Send a prompt to LLM and return response."""
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
        data = resp.json()
        
        choice = data.get("choices", [None])[0]
        if choice is None:
            raise KeyError("no choices")
        
        if isinstance(choice.get("message"), dict) and "content" in choice["message"]:
            text = choice["message"]["content"]
        elif "text" in choice:
            text = choice["text"]
        else:
            text = str(choice)
        
        return {"result": text}
        
    except Exception as exc:
        return {"result": f"[error] LLM request failed: {exc}"}


if __name__ == "__main__":
    import logging

    logging.getLogger("mcp").setLevel(logging.WARNING)
    mcp.run(transport="stdio")
