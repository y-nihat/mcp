import asyncio
import os
import sys
import json
from pathlib import Path

# Ensure the repository root is on sys.path so the local `mcp` package is importable
repo_root = Path(__file__).resolve().parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


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
            print("Client connected.")

            # Read the static resource
            resp = await session.read_resource("resource://info")
            blocks = getattr(resp, "contents", None) or getattr(resp, "content", [])
            if blocks:
                first = blocks[0]
                text = getattr(first, "text", None) or str(first)
                print(text)
            else:
                print("(no content returned)")

            # Call the greet tool
            tool_resp = await session.call_tool("greet", {"name": "CSStudent"})

            # Extract returned text safely
            greeting = None
            # Many responses expose `content` or `contents` as a list of blocks
            blocks = getattr(tool_resp, "contents", None) or getattr(tool_resp, "content", None) or []
            if blocks:
                first = blocks[0]
                greeting = getattr(first, "text", None) or str(first)
            else:
                # Fallbacks
                greeting = getattr(tool_resp, "text", None) or str(tool_resp)

            # Print the result as JSON (a JSON string containing the greeting)
            print(json.dumps(greeting))


if __name__ == "__main__":
    asyncio.run(main())
