import asyncio
import os
import sys
from pathlib import Path

# Make the repository root importable when running this script directly so the
# locally-checked-out `mcp` package can be imported without an editable install.
repo_root = Path(__file__).resolve().parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main() -> None:
    # Launch the server script in the same directory as this client
    server_script = Path(__file__).resolve().parent / "mcp_server.py"

    server_params = StdioServerParameters(
        command=sys.executable,
        args=[str(server_script)],
        env=os.environ.copy(),
    )

    # Connect to the server over stdio transport (stdio_client launches the subprocess)
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("Client connected.")

            # Read the static health resource
            resp = await session.read_resource("resource://health")
            # Response may expose `contents` or `content` depending on transport wrapper
            blocks = getattr(resp, "contents", None) or getattr(resp, "content", [])

            if not blocks:
                print("(no content returned from health resource)")
                return

            first = blocks[0]
            text = getattr(first, "text", None) or str(first)
            print(text)


if __name__ == "__main__":
    asyncio.run(main())
