# To-Do MCP Server

Implements a CRUD to-do list server using FastMCP. Supports in-memory and SQLite storage (set `MCP_TODO_DB` env var for persistence).

## Usage

Run server:

```bash
python src/mcp_bridge/servers/todo_server.py
```

Call tools programmatically:

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

server_params = StdioServerParameters(
    command="python",
    args=["src/mcp_bridge/servers/todo_server.py"],
    env=None,
)

async with stdio_client(server_params) as (read, write):
    async with ClientSession(read, write) as session:
        await session.initialize()
        uri = await session.call_tool("create_todo", {"title": "Write docs"})
        print(uri.content[0].text)  # resource://todos/1
```

## Features

- Create, update, delete, list, and get to-do items
- SQLite persistence for robust testing
- Demo: `python examples/bridge_demo.py --todo`
