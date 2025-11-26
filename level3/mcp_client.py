import asyncio
import os
import sys
import json
import requests
from pathlib import Path
from typing import cast, Optional
from pydantic import AnyUrl

# Ensure repository root is importable
repo_root = Path(__file__).resolve().parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


def call_llm(prompt: str, system_message: Optional[str] = None, temperature: float = 0.7) -> str:
    """Call LLM directly without tool abstraction."""
    lm_url = os.environ.get("LMSTUDIO_URL", "http://localhost:1234/v1/chat/completions")
    model = os.environ.get("LMSTUDIO_MODEL", "qwen/qwen3-4b-2507")
    
    messages = []
    if system_message:
        messages.append({"role": "system", "content": system_message})
    messages.append({"role": "user", "content": prompt})
    
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": int(os.environ.get("LMSTUDIO_MAX_TOKENS", 200)),
        "stream": False,
    }
    
    try:
        resp = requests.post(lm_url, json=payload, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        
        choice = data.get("choices", [None])[0]
        if choice and isinstance(choice.get("message"), dict):
            result = choice["message"]["content"].strip()
        elif choice and "text" in choice:
            result = choice["text"].strip()
        else:
            result = str(choice).strip()
        
        return result
        
    except Exception as exc:
        return f"[error] LLM call failed: {exc}"


async def main() -> None:
    server_script = Path(__file__).resolve().parent / "mcp_server.py"

    server_params = StdioServerParameters(
        command=sys.executable,
        args=[str(server_script)],
        env=os.environ.copy(),
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            # Health check
            resp = await session.read_resource(cast(AnyUrl, "resource://health"))
            blocks = getattr(resp, "contents", None) or getattr(resp, "content", [])
            resp = await session.read_resource(cast(AnyUrl, "resource://health"))
            blocks = getattr(resp, "contents", None) or getattr(resp, "content", [])
            if blocks:
                first = blocks[0]
                text = getattr(first, "text", None) or str(first)
                print(f"Health: {text}")

            # Greet using LLM
            name = "CSStudent"
            greet_result = call_llm(
                prompt=f"Generate a friendly greeting for {name}. Mention MCP. One sentence.",
                system_message="You are a friendly assistant.",
                temperature=0.7
            )
            print(f"Greet: {greet_result}")

            # Math addition using LLM
            a, b = 3, 4
            add_result = call_llm(
                prompt=f"Calculate {a} + {b}. Return only the number.",
                system_message="You are a calculator.",
                temperature=0.0
            )
            print(f"Math: {a} + {b} = {add_result}")

            # Math multiplication using LLM
            a, b = 6, 7
            mul_result = call_llm(
                prompt=f"Calculate {a} * {b}. Return only the number.",
                system_message="You are a calculator.",
                temperature=0.0
            )
            print(f"Math: {a} * {b} = {mul_result}")

            # Custom prompt using LLM
            custom_result = call_llm(
                prompt="Write a short greeting to CSStudent in 1 sentence.",
                temperature=0.7
            )
            print(f"Custom: {custom_result}")


if __name__ == "__main__":
    asyncio.run(main())
