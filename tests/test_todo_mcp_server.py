"""Tests for the To-Do MCP Server (Phase 1 - Create capability).

Verifies that create_todo tool:
- Returns a resource URI with incrementing IDs.
- Rejects empty titles.
"""

import asyncio
import logging
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.shared.exceptions import McpError
import json

logging.getLogger("mcp").setLevel(logging.WARNING)


def test_create_todo_tool():
    async def _run():
        server_params = StdioServerParameters(
            command="python",
            args=["-m", "mcp_bridge.servers.todo_server"],
            env=os.environ.copy(),
        )

        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()

                # First create
                r1 = await session.call_tool("create_todo", {"title": "Buy milk"})
                assert not r1.isError
                uri1 = r1.content[0].text
                assert uri1 == "resource://todos/1"

                # Second create
                r2 = await session.call_tool("create_todo", {"title": "Write docs"})
                assert not r2.isError
                uri2 = r2.content[0].text
                assert uri2 == "resource://todos/2"

                # Validate distinct
                assert uri1 != uri2

                # Error: empty title
                r_err = await session.call_tool("create_todo", {"title": "   "})
                assert r_err.isError, "Expected error for empty title"

                # List resource should show two items
                list_result = await session.read_resource("resource://todos")
                text_payload = list_result.contents[0].text
                assert "Buy milk" in text_payload and "Write docs" in text_payload

                # Read single item
                one = await session.read_resource("resource://todos/1")
                item_json = one.contents[0].text
                data = json.loads(item_json)
                assert data["title"] == "Buy milk"
                assert data["completed"] is False

                # Read non-existent should raise
                try:
                    await session.read_resource("resource://todos/999")
                    assert False, "Expected McpError for missing resource"
                except McpError:
                    pass

                # Update item 1: title and completed
                up = await session.call_tool(
                    "update_todo",
                    {"item_id": 1, "title": "Buy oat milk", "completed": True},
                )
                assert not up.isError
                up_data = json.loads(up.content[0].text)
                assert up_data["title"] == "Buy oat milk"
                assert up_data["completed"] is True

                # Confirm via resource read
                one_after = await session.read_resource("resource://todos/1")
                after_json = json.loads(one_after.contents[0].text)
                assert after_json["title"] == "Buy oat milk"
                assert after_json["completed"] is True

                # Delete item 2
                del_res = await session.call_tool("delete_todo", {"item_id": 2})
                assert not del_res.isError
                del_data = json.loads(del_res.content[0].text)
                assert del_data["title"] == "Write docs"

                # Reading item 2 should now fail
                try:
                    await session.read_resource("resource://todos/2")
                    assert False, "Expected McpError after deletion"
                except McpError:
                    pass

    asyncio.run(_run())


async def main():
    await test_create_todo_tool()


if __name__ == "__main__":
    asyncio.run(main())
