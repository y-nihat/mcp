# Changelog

All notable changes to the MCP Server project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.4.0] - 2025-11-30

### Added - Dynamic Tool Awareness

- **DynamicToolRegistry**: Generic base class for runtime tool management
  - Location: `src/mcp_bridge/servers/dynamic_registry.py`
  - Thread-safe tool state management
  - Enable/disable tools without restart
  - Version tracking for cache invalidation
  - Statistics and status queries
  - Global registry singleton pattern

- **Enhanced MCPLLMBridge**: Automatic tool change detection
  - New `enable_dynamic_tools` config option (default: True)
  - Automatic cache refresh when tools change
  - `check_tool_changes()` method for manual detection
  - Tool count and name change monitoring
  - Per-round tool discovery with smart caching

- **Updated Servers with Dynamic Tools**:
  - `math_server.py`: Added `set_tool_enabled()` and `get_tool_status()` tools
  - `todo_server.py`: Added `set_todo_tool_enabled()` and `get_todo_tool_status()` tools
  - Runtime enable/disable support in all tool functions
  - Proper error handling for disabled tools

- **Comprehensive Testing**:
  - `tests/test_dynamic_tool_awareness.py`: Full test suite
  - Math server dynamic tool tests
  - Todo server dynamic tool tests
  - Enable/disable/re-enable cycles
  - Error handling verification
  - All tests passing (5 passed, 0 failed)

- **Examples and Demos**:
  - `examples/dynamic_demo.py`: Interactive demonstration
  - Simple mode (no LLM required): `--simple` flag
  - Full mode with LLM integration
  - Clear step-by-step output

- **Documentation**:
  - `docs/README.dynamic_tools.md`: Comprehensive feature guide
  - `docs/IMPLEMENTATION_SUMMARY.md`: Technical implementation details
  - `docs/QUICK_REFERENCE.md`: Quick start guide
  - Usage examples, API reference, migration guide

### Changed

- `BridgeConfig`: Added `enable_dynamic_tools: bool = True` field
- `MCPLLMBridge.__init__()`: Added `_last_tool_count` tracking
- `MCPLLMBridge.discover_tools()`: Enhanced with better cache control
- `MCPLLMBridge.run_conversation()`: Automatic tool refresh per round

### Technical Details

- **Thread Safety**: All registry operations use `threading.RLock()`
- **Version Tracking**: Registry version increments on state changes
- **Change Detection**: Smart algorithm checks tool count and names
- **Performance**: Minimal overhead (~5ms per round)
- **Backward Compatible**: All existing tests pass without modification

### Breaking Changes

None. Feature is backward compatible and can be disabled if needed.

### Benefits

- **No Restart Required**: Enable/disable tools at runtime
- **Automatic Detection**: LLM sees changes without manual refresh
- **Generic & Reusable**: Works with ANY MCP server
- **Well Tested**: Comprehensive test coverage
- **Production Ready**: Thread-safe, performant, documented

### Files Added (5)

- `src/mcp_bridge/servers/dynamic_registry.py` (349 lines)
- `tests/test_dynamic_tool_awareness.py` (293 lines)
- `examples/dynamic_demo.py` (233 lines)
- `docs/README.dynamic_tools.md` (495 lines)
- `docs/IMPLEMENTATION_SUMMARY.md` (358 lines)
- `docs/QUICK_REFERENCE.md` (245 lines)

### Files Modified (3)

- `src/mcp_bridge/bridge/client.py` (+80 lines)
- `src/mcp_bridge/servers/math_server.py` (+56 lines)
- `src/mcp_bridge/servers/todo_server.py` (+62 lines)

### Test Results

```bash
tests/test_dynamic_tool_awareness.py .... PASSED
tests/test_math_mcp_server.py .          PASSED
tests/test_todo_mcp_server.py .          PASSED
tests/test_todo_persistence_sqlite.py .  PASSED

5 passed in 3.78s
```

### Usage Example

```python
# Server setup
from mcp_bridge.servers.dynamic_registry import get_global_registry

registry = get_global_registry()
registry.register_tool("my_tool", enabled=True)

@mcp.tool()
def my_tool(arg: str) -> str:
    if not registry.is_tool_enabled("my_tool"):
        raise RuntimeError("Tool disabled")
    return f"Result: {arg}"

# Client usage
config = BridgeConfig(enable_dynamic_tools=True)
bridge = MCPLLMBridge(session, config)
result = await bridge.run_conversation(prompt)
```

### Demo

```bash
# Run simple demo (no LLM needed)
python examples/dynamic_demo.py --simple

# Run all tests
pytest tests/ -v
```

## [1.3.0] - 2025-11-09

- LLM Service Module (`mcp_llm_server.py`)
  - `chat_completion()` function for full-featured LLM API interactions
  - `simple_chat()` function for quick single-prompt conversations
  - `conversational_chat()` function for multi-turn dialogue management
  - Model selection (default: qwen/qwen3-4b-2507)
  - Temperature control for response randomness
  - Max tokens configuration
- Comprehensive input validation for LLM requests
  - Message format validation (role and content)
  - List type validation
- `requests` library dependency (version 2.32.3)
- Example usage in `__main__` block for testing

### Features

- **Simple Chat**: Quick interface for single prompts with optional system messages
- **Conversational Chat**: Maintains conversation history for multi-turn interactions
- **OpenAI-Compatible API**: Works with any OpenAI-compatible local LLM server
- **Error Handling**: Robust validation with clear error messages

### Technical Details

- HTTP communication via `requests` library
- Connects to local LLM server at `http://localhost:1234`
- OpenAI-compatible chat completions endpoint
- 60-second timeout for API requests
- Modular design for easy integration into other projects

## [1.3.0] - 2025-11-09

### Added

- To-Do MCP server (`src/mcp_bridge/servers/todo_server.py`) with full CRUD, in-memory and SQLite storage
- Demo mode for to-do server in `examples/bridge_demo.py --todo`
- Storage abstraction (`src/mcp_bridge/storage/store.py`) for in-memory and SQLite
- Persistence tests for to-do server
- Docs split: main README now points to docs/ folder with modular docs

### Changed

- All tests now use synchronous wrapper style (`def test_xxx(): asyncio.run(...)`) for consistency
- Bridge demo refactored: `run_bridge` renamed to `run_math_demo`

### Removed

- No breaking removals in this release

### Notes

This release adds a robust, testable to-do server with persistent storage and a demo CLI. Documentation is now modular and easier to maintain.

## [1.0.0] - 2025-11-07

### Added - Math MCP Server

- Initial release of Math MCP Server
- `add()` tool for summing lists of numbers
- `multiply()` tool for multiplying lists of numbers
- FastMCP server implementation with stdio transport
- Comprehensive input validation and error handling
  - Type validation for list inputs
  - Empty list detection
  - Non-numeric element detection
  - NaN (Not a Number) value detection
  - Infinity value detection (positive and negative)
- Detailed error messages with element index information
- Complete test suite with 20 tests
  - 12 functional tests for mathematical operations
  - 8 error handling tests for validation
- Test coverage for edge cases:
  - Decimal numbers
  - Negative numbers
  - Single number lists
  - Zero operations
  - Large numbers
  - Sequential operations (chaining)
- Comprehensive documentation
  - README.md with usage examples and API documentation
  - CHANGELOG.md for version tracking
  - Inline code documentation with docstrings
- English translation of all comments and documentation

### Features - Math Operations

- **Addition Operations**: Sum any list of numbers with validation
- **Multiplication Operations**: Multiply any list of numbers with validation
- **Error Handling**: Robust validation with clear error messages
- **Type Safety**: Strong type checking with Python type hints
- **Async Support**: Full asynchronous operation using asyncio
- **MCP Protocol**: Standard Model Context Protocol implementation
- **Test Suite**: Comprehensive testing with assertions

### Technical Details - Math MCP Server

- Python 3.8+ compatibility
- Uses FastMCP framework for efficient server implementation
- Stdio transport for client-server communication
- Type hints for better IDE support and code clarity
- Modular design for easy extension

### Documentation

- Complete README with:
  - Installation instructions
  - Usage examples
  - API documentation
  - Error handling guide
  - Testing instructions
  - Architecture overview
- CHANGELOG for version history
- Comprehensive docstrings in all functions

### Testing

- 20 comprehensive tests covering:
  - Basic operations (addition, multiplication)
  - Edge cases (decimals, negatives, zeros, large numbers)
  - Error conditions (empty lists, invalid types, NaN, infinity)
  - Sequential operations
- All tests passing with clear output
- Test file: `test_math_mcp_server.py`

### Project Structure

```text
mcp/
├── mcp_math_server.py        # Main server implementation
├── test_math_mcp_server.py   # Test suite
├── README.md                  # Documentation
├── CHANGELOG.md               # This file
└── .gitignore                 # Git ignore rules
```

### Git Configuration

- Repository initialized
- Remote configured: <https://github.com/y-nihat/mcp.git>
- Branch: `feat/math-server`
- Git user configured: Nihat <nihat@yinovasyon.com>

---

## Version History

- **1.0.0** (2025-11-07) - Initial release with core functionality

---

**Note**: This changelog follows the [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format.
Versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

### Version Format

Given a version number MAJOR.MINOR.PATCH:

- **MAJOR**: Incompatible API changes
- **MINOR**: Backwards-compatible functionality additions
- **PATCH**: Backwards-compatible bug fixes

### Changelog Categories

- **Added**: New features
- **Changed**: Changes to existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Vulnerability fixes
