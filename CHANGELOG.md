# Changelog

All notable changes to the MCP Server project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-11-07

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

## [1.2.0] - 2025-11-08

### Added

- MCP↔LLM Bridge Client (`mcp_llm_bridge_client.py`)
  - Dynamic discovery of MCP server tools via `list_tools()`
  - Automatic conversion of MCP tool schemas to OpenAI `tools` specification
  - Multi-round orchestration with configurable max rounds and verbosity
  - Structured tool execution with result injection into conversation history
  - Caching of discovered tools to avoid repeated listing
- Bridge Demo (`llm_mcp_tool_bridge_demo.py`) now a thin wrapper around the reusable bridge
- Scenario Test Runner (`test_llm_mcp_bridge_scenarios.py`)
  - Extensible test case abstraction (`TestCase`)
  - Multiple math scenarios (basic arithmetic, chained operations, decimals, large numbers)
  - CLI options: `--basic`, `--math`, `--all`, `--stop-on-failure`
- Documentation updates in `README.md` for bridge architecture, usage, and test scenarios

### Changed (Bridge)

- Removed prototype playground & debug scripts (tool-call playground and debug demo) in favor of production-ready bridge client and scenario tests
- `llm_mcp_tool_bridge_demo.py` refactored to use `MCPLLMBridge` instead of inline logic

### Removed (Bridge)

- `llm_tool_playground.py` (replaced by structured bridge + scenarios)
- `llm_tool_debug_demo.py` (superseded by scenario runner and bridge)
- `test_llm_tool_playground.py`
- `test_llm_tool_debug_demo.py`

### Notes

This release embraces MCP's philosophy of dynamic capability discovery and eliminates hardcoded OpenAI tool schemas. Future MCP servers can be integrated without modifying bridge code—only new test cases are needed.

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
