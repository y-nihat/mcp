"""Persistence tests for To-Do MCP Server with SQLite backend.

Uses a temporary sqlite file to verify data persists across new sessions.
"""

import asyncio
import logging
import os
import tempfile
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.shared.exceptions import McpError

logging.getLogger("mcp").setLevel(logging.WARNING)


def test_todo_persistence_sqlite():
    async def _run(db_path: str):
        env = os.environ.copy()
        env["MCP_TODO_DB"] = db_path
        server_params = StdioServerParameters(
            command="python",
            args=["-m", "mcp_bridge.servers.todo_server"],
            env=env,
        )

        # First session: create items
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                c1 = await session.call_tool("create_todo", {"title": "Persist A"})
                assert not c1.isError
                c2 = await session.call_tool("create_todo", {"title": "Persist B"})
                assert not c2.isError

        # Second session: verify persistence and mutate
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                all_res = await session.read_resource("resource://todos")
                payload = all_res.contents[0].text
                assert "Persist A" in payload and "Persist B" in payload

                # Update one, delete the other
                up = await session.call_tool(
                    "update_todo", {"item_id": 1, "completed": True}
                )
                assert not up.isError
                dl = await session.call_tool("delete_todo", {"item_id": 2})
                assert not dl.isError

        # Third session: confirm changes persisted
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                one = await session.read_resource("resource://todos/1")
                data = json.loads(one.contents[0].text)
                assert data["completed"] is True
                # Item 2 should be gone
                try:
                    await session.read_resource("resource://todos/2")
                    assert False, "Expected McpError for deleted item"
                except McpError:
                    pass

    with tempfile.TemporaryDirectory() as td:
        db_path = os.path.join(td, "todos.db")
        asyncio.run(_run(db_path))
