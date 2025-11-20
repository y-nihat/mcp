# Level 2 — Math Tool

This level builds on Level 1 and demonstrates how MCP tools can accept multiple parameters and return structured results.

What this level adds

- Level 1 had a static Resource (`resource://info`) and a `greet` Tool.
- Level 2 keeps those and adds a `math` Tool that accepts two numeric parameters and an operation string.

How MCP tools accept multiple parameters

- Tools are just Python functions decorated with `@mcp.tool()`.
- Parameters are passed as a JSON object by the client (e.g., `{"a": 3, "b": 4, "operation": "add"}`) and mapped to the tool function's arguments.
- Tools can return structured data (e.g., a dict) which the client can parse.

The `math` tool

- Signature: `math(a: number, b: number, operation: str)`
- Behavior:
  - If `operation == "add"` returns `{"result": a + b}`
  - If `operation == "multiply"` returns `{"result": a * b}`
  - Otherwise raises a clear error

How the client calls the tool

- The client calls `await session.call_tool("math", {"a": 3, "b": 4, "operation": "add"})`.
- The response typically contains content blocks; the client inspects the text and parses JSON to extract the `result`.

Expected output

Running from repo root with the `mcp` env active:

```bash
conda activate mcp
python level2/mcp_client.py
```

Example output:

```
Client connected.
This is a static resource from my MCP server.
Output from greet tool: Hello, CSStudent! Welcome to MCP.
Output from math add: 3 + 4 = 7
Output from math multiply: 6 * 7 = 42
```
