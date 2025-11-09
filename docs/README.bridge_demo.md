# Bridge Demo

Demonstrates MCP↔LLM tool-call bridging and to-do CRUD flows.

## Usage

- Math bridge demo (requires local LLM):

  ```bash
  python examples/bridge_demo.py
  ```

- To-do CRUD demo (no LLM required):

  ```bash
  python examples/bridge_demo.py --todo
  ```

  Optionally persist with SQLite:

  ```bash
  python examples/bridge_demo.py --todo --db=/tmp/todos.db
  ```

## What It Shows

- Tool discovery and execution
- End-to-end CRUD for to-do items
- Pretty-printed resource outputs

See code for details and CLI options.
