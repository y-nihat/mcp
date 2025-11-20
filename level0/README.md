# Level 0 — Minimal MCP handshake

What is MCP?

- MCP (Model-Callable Protocol) is a minimal RPC-style protocol used to connect LLMs (or other clients) to local servers exposing tools and resources.
- Servers expose Tools (callable functions) and Resources (readable URIs). Clients can call tools or read resources across an IPC/stdio transport.

What is a Resource?

- A Resource is a named, addressable URI (for example `resource://info`).
- Resources are read-only endpoints implemented by the server and return structured or unstructured content. They are different from Tools which are callable operations.

What this Level teaches

- This level demonstrates the minimal MCP handshake:
  - Start a FastMCP server over stdio exposing a single resource: `resource://info`.
  - Launch the server as a subprocess from an asyncio client using `stdio_client`.
  - Initialize the client session, read the resource, and print the returned value.

How to run

1. Activate the project conda env (the examples assume an env named `mcp`):

```bash
conda activate mcp
```

2. Run the client from the repository root or the `level0` directory:

```bash
python level0/mcp_client.py
# or, when inside level0/
python mcp_client.py
```

Expected output:

```
Client connected.
This is a static resource from my MCP server.
```
