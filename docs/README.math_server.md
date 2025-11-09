# Math MCP Server

Implements addition and multiplication tools using FastMCP. Validates input for type, emptiness, numeric values, NaN, and infinity. See `src/mcp_bridge/servers/math_server.py`.

## Usage

Run server:

```bash
python src/mcp_bridge/servers/math_server.py
```

Call tools programmatically:

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

server_params = StdioServerParameters(
    command="python",
    args=["src/mcp_bridge/servers/math_server.py"],
    env=None,
)

async with stdio_client(server_params) as (read, write):
    async with ClientSession(read, write) as session:
        await session.initialize()
        result = await session.call_tool("add", {"numbers": [10, 20, 30]})
        print(result.content[0].text)  # 60.0
```

## Error Handling

- Empty list, non-numeric, NaN, infinity: returns error
- See test suite for examples
