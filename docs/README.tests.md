# Testing & Test Style

## Test Coverage

- Math MCP server: 20 tests (functional + error handling)
- To-Do MCP server: full CRUD, error, and persistence tests
- Scenario runner: multi-round tool-call orchestration

## Test Style

All tests now use the synchronous wrapper pattern:

- Each test is a regular `def` function
- Async logic is placed in a helper coroutine
- The test calls `asyncio.run(coroutine())`
- No `@pytest.mark.asyncio` required

Example:

```python
def test_math_server():
    async def _run():
        # ... async test code ...
    asyncio.run(_run())
```

## Running Tests

```bash
pytest
```

Or run individual files:

```bash
pytest tests/test_math_mcp_server.py
pytest tests/test_todo_mcp_server.py
```
