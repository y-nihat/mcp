"""MCP↔LLM & To-Do Server Demo

This script now supports two demo modes:

1. (default) LLM tool-call bridge with the math MCP server
2. (--todo) Direct scripted interaction with the to-do MCP server showcasing
   the full CRUD lifecycle (create, list, get, update, delete) with terminal output.

Math Bridge Requirements:
    - Local OpenAI-compatible LLM at http://localhost:1234
    - `mcp_bridge.servers.math_server` importable (editable install of this repo)

To-Do Demo Requirements:
    - `mcp_bridge.servers.todo_server` (in this repo)
    - Optional: set MCP_TODO_DB=/path/to/todos.db to persist between runs

Usage:
    python bridge_demo.py                  # math LLM bridge demo
    python bridge_demo.py --stub           # (deprecated) stub mode
    python bridge_demo.py --todo           # to-do CRUD demo (no LLM needed)
"""

from __future__ import annotations

import asyncio
import json
import sys
from typing import List, Optional

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from pathlib import Path
import os

# With the package installed editable (pip install -e .), we no longer need
# manual sys.path or PYTHONPATH injections. We invoke the math server via
# its module path using -m. This keeps the demo minimal and mirrors real usage.

from mcp_bridge.bridge.client import MCPLLMBridge, BridgeConfig


async def run_math_demo(use_stub: bool = False) -> int:
    """Run the math LLM bridge demo (backward compatible with original interface)."""

    if use_stub:
        print("Warning: --stub mode is deprecated. Using live mode instead.")
        print("For test scenarios, use: python test_llm_mcp_bridge_scenarios.py")
        print()

    # Start MCP math server over stdio by module name (editable install handles path)
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "mcp_bridge.servers.math_server"],
        env=os.environ.copy(),
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("✓ Connected to Math MCP Server")

            # Create bridge with default config
            bridge = MCPLLMBridge(session, config=BridgeConfig())

            # Run conversation
            result = await bridge.run_conversation(
                user_prompt="Compute (3 + 5) * 4 using available tools and explain briefly.",
            )

            print("\n" + "=" * 70)
            print("FINAL RESPONSE:")
            print(result["final_response"])
            print("=" * 70)
            print(
                f"Stats: {result['tool_calls_made']} tool calls, {result['rounds']} rounds"
            )

    return 0


async def run_todo_demo(db_path: Optional[str] = None) -> int:
    """Run a linear scripted demo against the to-do MCP server.

    Steps:
        1. create_todo
        2. read all todos (resource://todos)
        3. read the single created todo
        4. update_todo (change title + set completed=True)
        5. read the updated item
        6. delete_todo
        7. final list of todos (should not contain deleted id)
    """

    env = os.environ.copy()
    if db_path:
        env["MCP_TODO_DB"] = db_path

    server_params = StdioServerParameters(
        command="python",
        args=["-m", "mcp_bridge.servers.todo_server"],
        env=env,
    )

    print("Starting to-do MCP server...\n")
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("✓ Connected to To-Do MCP Server")

            # Discover tools for transparency
            tools_resp = await session.list_tools()
            tool_names = [t.name for t in getattr(tools_resp, "tools", [])]
            print("Tools available:", ", ".join(tool_names) or "(none)")
            print()

            # 1. Create
            print("[1] create_todo(title='Write docs')")
            create_res = await session.call_tool("create_todo", {"title": "Write docs"})
            if getattr(create_res, "isError", False):
                print(
                    "  -> ERROR:",
                    getattr(create_res.content[0], "text", "unknown error"),
                )
                return 1
            created_uri = getattr(create_res.content[0], "text", "").strip()
            print("  -> Created URI:", created_uri)

            # Extract numeric id (resource://todos/{id})
            try:
                todo_id = int(created_uri.rsplit("/", 1)[-1])
            except Exception:  # noqa: BLE001
                print("Failed to parse created id from URI")
                return 1

            # 2. List all
            print("\n[2] read_resource('resource://todos') -> list all")
            list_all = await session.read_resource("resource://todos")
            print("  -> Items:")
            blocks = getattr(list_all, "contents", None) or getattr(
                list_all, "content", []
            )
            for block in blocks:
                text = getattr(block, "text", None)
                if text:
                    try:
                        obj = json.loads(text)
                        print(json.dumps(obj, indent=2))
                    except Exception:  # noqa: BLE001
                        print(text)
                else:
                    print(repr(block))

            # 3. Get single
            print(f"\n[3] read_resource('{created_uri}') -> single item")
            single = await session.read_resource(created_uri)
            blocks = getattr(single, "contents", None) or getattr(single, "content", [])
            if blocks:
                block = blocks[0]
                text = getattr(block, "text", "")
                try:
                    obj = json.loads(text)
                    print("  -> Item:")
                    print(json.dumps(obj, indent=2))
                except Exception:  # noqa: BLE001
                    print("  -> Item:", text)
            else:
                print("  -> Item: (no content returned)")

            # 4. Update
            print(
                "\n[4] update_todo(item_id, title='Write detailed docs', completed=True)"
            )
            update_res = await session.call_tool(
                "update_todo",
                {"item_id": todo_id, "title": "Write detailed docs", "completed": True},
            )
            if getattr(update_res, "isError", False):
                print(
                    "  -> ERROR:",
                    getattr(update_res.content[0], "text", "unknown error"),
                )
                return 1
            updated_text = (
                getattr(update_res.content[0], "text", "")
                if getattr(update_res, "content", None)
                else ""
            )
            print("  -> Updated:", updated_text)

            # 5. Read updated single
            print(f"\n[5] read_resource('{created_uri}') -> updated item")
            updated_single = await session.read_resource(created_uri)
            blocks = getattr(updated_single, "contents", None) or getattr(
                updated_single, "content", []
            )
            if blocks:
                block = blocks[0]
                text = getattr(block, "text", "")
                try:
                    obj = json.loads(text)
                    print("  -> Item:")
                    print(json.dumps(obj, indent=2))
                except Exception:  # noqa: BLE001
                    print("  -> Item:", text)
            else:
                print("  -> Item: (no content returned)")

            # 6. Delete
            print("\n[6] delete_todo(item_id)")
            del_res = await session.call_tool("delete_todo", {"item_id": todo_id})
            if getattr(del_res, "isError", False):
                print(
                    "  -> ERROR:", getattr(del_res.content[0], "text", "unknown error")
                )
                return 1
            deleted_text = (
                getattr(del_res.content[0], "text", "")
                if getattr(del_res, "content", None)
                else ""
            )
            print("  -> Deleted:", deleted_text)

            # 7. Final list
            print("\n[7] Final read_resource('resource://todos')")
            final_list = await session.read_resource("resource://todos")
            blocks = getattr(final_list, "contents", None) or getattr(
                final_list, "content", []
            )
            if blocks:
                print("  -> Items:")
                for block in blocks:
                    text = getattr(block, "text", None)
                    if text:
                        try:
                            obj = json.loads(text)
                            print(json.dumps(obj, indent=2))
                        except Exception:  # noqa: BLE001
                            print(text)
                    else:
                        print(repr(block))
            else:
                print("  -> Items: {}")

    print("\nTo-Do demo complete.")
    return 0


def main(argv: List[str]) -> int:
    use_stub = "--stub" in argv
    if "--todo" in argv:
        # Optional --db=<path> for persistence
        db_path = None
        for arg in argv:
            if arg.startswith("--db="):
                db_path = arg.split("=", 1)[1]
        return asyncio.run(run_todo_demo(db_path=db_path))
    return asyncio.run(run_math_demo(use_stub=use_stub))


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
