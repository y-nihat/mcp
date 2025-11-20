import asyncio
import os
import sys
import json
from pathlib import Path

# Ensure repository root is importable
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

            # Read the static health resource
            resp = await session.read_resource("resource://health")
            blocks = getattr(resp, "contents", None) or getattr(resp, "content", [])
            if blocks:
                first = blocks[0]
                text = getattr(first, "text", None) or str(first)
                print(f"Health resource returned: {text}")
            else:
                print("(no content returned from health resource)")

            # Call greet
            greet_resp = await session.call_tool("greet", {"name": "CSStudent"})
            gblocks = getattr(greet_resp, "contents", None) or getattr(greet_resp, "content", None) or []
            if gblocks:
                gtext = getattr(gblocks[0], "text", None) or str(gblocks[0])
                print(f"Output from greet tool: {gtext}")
            else:
                print(f"Output from greet tool: {getattr(greet_resp, 'text', str(greet_resp))}")

            # Call math add
            add_resp = await session.call_tool("math", {"a": 3, "b": 4, "operation": "add"})
            add_val = None
            ablocks = getattr(add_resp, "contents", None) or getattr(add_resp, "content", None) or []
            if ablocks:
                atext = getattr(ablocks[0], "text", None) or str(ablocks[0])
                try:
                    parsed = json.loads(atext)
                    add_val = parsed.get("result") if isinstance(parsed, dict) else parsed
                except Exception:
                    try:
                        obj = eval(atext)
                        add_val = obj.get("result") if isinstance(obj, dict) else obj
                    except Exception:
                        add_val = atext
            else:
                add_val = getattr(add_resp, "text", None) or str(add_resp)

            print(f"Output from math add: 3 + 4 = {add_val}")

            # Call math multiply
            mul_resp = await session.call_tool("math", {"a": 6, "b": 7, "operation": "multiply"})
            mul_val = None
            mblocks = getattr(mul_resp, "contents", None) or getattr(mul_resp, "content", None) or []
            if mblocks:
                mtext = getattr(mblocks[0], "text", None) or str(mblocks[0])
                try:
                    parsed = json.loads(mtext)
                    mul_val = parsed.get("result") if isinstance(parsed, dict) else parsed
                except Exception:
                    try:
                        obj = eval(mtext)
                        mul_val = obj.get("result") if isinstance(obj, dict) else obj
                    except Exception:
                        mul_val = mtext
            else:
                mul_val = getattr(mul_resp, "text", None) or str(mul_resp)

            print(f"Output from math multiply: 6 * 7 = {mul_val}")

            # Call llm_prompt (this tool calls the local LM Studio HTTP API by default)
            # You can override the model/URL via environment variables:
            # LMSTUDIO_URL, LMSTUDIO_MODEL, LMSTUDIO_SYSTEM_MESSAGE
            llm_resp = await session.call_tool("llm_prompt", {"prompt": "Write a short greeting to CSStudent in 1 sentence."})
            llm_val = None
            lblocks = getattr(llm_resp, "contents", None) or getattr(llm_resp, "content", None) or []
            if lblocks:
                ltext = getattr(lblocks[0], "text", None) or str(lblocks[0])
                try:
                    parsed = json.loads(ltext)
                    llm_val = parsed.get("result") if isinstance(parsed, dict) else parsed
                except Exception:
                    # Not JSON — use raw text
                    llm_val = ltext
            else:
                llm_val = getattr(llm_resp, "text", None) or str(llm_resp)

            print(f"Output from llm_prompt tool: {llm_val}")


if __name__ == "__main__":
    asyncio.run(main())
