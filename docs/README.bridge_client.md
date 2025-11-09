# Bridge Client Usage

The bridge client dynamically discovers MCP server tools and orchestrates multi-round tool calling for LLMs. Converts MCP tool schemas to OpenAI-compatible format and injects tool results into conversations.

## Basic Usage

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp_bridge.bridge.client import MCPLLMBridge, BridgeConfig

server_params = StdioServerParameters(
    command="python",
    args=["-m", "mcp_bridge.servers.math_server"],
    env=None,
)

async with stdio_client(server_params) as (read, write):
    async with ClientSession(read, write) as session:
        await session.initialize()
        bridge = MCPLLMBridge(session, config=BridgeConfig())
        result = await bridge.run_conversation(
            user_prompt="Compute (3 + 5) * 4 using available tools and explain briefly."
        )
        print(result["final_response"])
```

## Features

- Dynamic tool discovery (no hardcoded specs)
- Converts MCP JSON Schemas to OpenAI `tools` format
- Multi-round orchestration with result injection
- Configurable system prompt, max rounds, verbosity

See `src/mcp_bridge/bridge/client.py` for details and advanced options.
