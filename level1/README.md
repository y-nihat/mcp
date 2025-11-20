# Level 1 — Add a Tool

This level extends Level 0 by introducing a Tool in addition to the static Resource.

What is a Tool?

- A Tool is a callable operation exposed by an MCP server. Tools accept parameters and return results. They are intended for actions (e.g., computations, state changes) while Resources are read-only endpoints.

How Level 1 extends Level 0

- Level 0 demonstrated a minimal MCP handshake and a static Resource (`resource://info`).
- Level 1 keeps that Resource and adds one Tool named `greet` which accepts a `name` string and returns a greeting message.

How the client calls a Tool via MCP

- The client establishes a session with the MCP server (over stdio in this example) using `stdio_client` and `ClientSession`.
- To invoke a tool, the client uses `session.call_tool(tool_name, params_dict)`.
- The server executes the tool and returns a response payload; the client inspects the response and prints or processes the result.

Files

- `mcp_server.py` — FastMCP server exposing `resource://info` and the `greet` tool. Runs over stdio.
- `mcp_client.py` — asyncio client that launches the server subprocess, reads the resource, calls the `greet` tool with `{"name": "CSStudent"}`, and prints the returned greeting as JSON.

Expected output

When run from the repository root or from the `level1/` directory with the `mcp` conda env active:

```bash
conda activate mcp
python level1/mcp_client.py
```

You should see:

```
Client connected.
This is a static resource from my MCP server.
"Hello, CSStudent! Welcome to MCP."
```
