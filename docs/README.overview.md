# MCP Bridge & Math MCP Server — Overview

This project bridges Model Context Protocol (MCP) servers to OpenAI-compatible LLM tool-calling interfaces. It includes:

- Math MCP server (add, multiply)
- To-Do MCP server (full CRUD, in-memory/SQLite)
- Reusable bridge client for dynamic tool discovery
- Scenario tests and demo scripts

## Main Features

- Dynamic tool discovery and execution
- Multi-round orchestration for LLM tool calls
- Comprehensive error handling and validation
- SQLite-backed persistence for to-do server

## Quick Start

- Install with `pip install -e .[dev]`
- Run math server: `python src/mcp_bridge/servers/math_server.py`
- Run to-do server: `python src/mcp_bridge/servers/todo_server.py`
- Try the demo: `python examples/bridge_demo.py --todo`

See other docs for details on usage, architecture, and testing.
