# MCP Bridge & Math MCP Server

Bridge local Model Context Protocol (MCP) servers to an OpenAI-compatible LLM tool-calling interface. Includes a sample Math MCP server, a reusable bridge client that performs dynamic tool discovery, scenario tests, and a demo script.

## 📦 Components

### 1. Math MCP Server (`src/mcp_bridge/servers/math_server.py`)

Model Context Protocol server exposing math tools (`add`, `multiply`) using FastMCP.

### 2. LLM Client (`src/mcp_bridge/llm/openai_client.py`)

Lightweight OpenAI-compatible wrapper utilities for a local LLM (chat completions + helpers).

### 3. Bridge Client (`src/mcp_bridge/bridge/client.py`)

Discovers MCP tools at runtime and converts them to OpenAI `tools` format; orchestrates multi-round tool calling.

### 4. Demo (`examples/bridge_demo.py`)

Minimal example showing end-to-end tool calling with discovered MCP tools.

### 5. Scenario Tests (`tests/test_llm_mcp_bridge_scenarios.py`)

Extensible test runner exercising multi-round tool calls.

### 6. Math Server Tests (`tests/test_math_mcp_server.py`)

20 focused tests (functional + error handling) for server validation.

## 🚀 Features

### Math MCP Server

- **Addition Tool**: Sum any list of numbers
- **Multiplication Tool**: Multiply any list of numbers
- **Comprehensive Error Handling**: Validates inputs for type safety and edge cases
- **FastMCP Framework**: Built on the efficient FastMCP server framework
- **Stdio Transport**: Uses standard input/output for client-server communication

### LLM Client

- **Chat Completion**: Full-featured LLM API interactions with complete control
- **Simple Chat**: Quick interface for single prompts with optional system messages
- **Conversational Chat**: Multi-turn dialogue with conversation history management
- **OpenAI-Compatible**: Works with any OpenAI-compatible local LLM server
- **Flexible Configuration**: Customizable model, temperature, max tokens, and streaming

### MCP↔LLM Bridge Client

- **Dynamic Tool Discovery**: Queries MCP servers for tools at runtime (no hardcoded specs)
- **OpenAI Tools Mapping**: Converts MCP JSON Schemas to OpenAI-compatible `tools` entries
- **Tool Execution**: Calls MCP tools and injects results back into the conversation
- **Multi-round Orchestration**: Supports several rounds until a final answer is produced
- **Configurable Behavior**: Verbose logging, system prompt, max rounds (via `BridgeConfig`)

## 📋 Requirements

- Python 3.9+
- Local OpenAI-compatible LLM endpoint (default: `http://localhost:1234`)
- Dependencies: `mcp`, `fastmcp`, `httpx`, `requests`, `pydantic` (managed via `pyproject.toml`)

## 🔧 Installation

### Option 1: Editable Install with pyproject.toml (Recommended)

For active development and running tests:

```bash
git clone [https://github.com/y-nihat/mcp.git](https://github.com/y-nihat/mcp.git)
cd mcp
pip install -e .[dev]
````

This installs the package in editable mode with all runtime and development dependencies (including pytest).

For runtime-only (no test tools):

```bash
pip install -e .
```

### Option 2: Install from requirements.txt

If you prefer pinned versions without installing the package:

```bash
pip install -r requirements.txt
```

## 🏃 Usage

### Using the Math MCP Server

Run directly (stdio transport):

```bash
python src/mcp_bridge/servers/math_server.py
```

Programmatic usage:

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

### Using the LLM Client

The LLM client provides utility functions to interact with a local LLM server.

#### Prerequisites

Ensure you have a local LLM server running at `http://localhost:1234` with OpenAI-compatible API (e.g., LM Studio, LocalAI, Ollama with OpenAI compatibility, etc.).

#### Basic Usage

```python
from mcp_bridge.llm.openai_client import (
    simple_chat,
    chat_completion,
    conversational_chat,
)

# Simple single-prompt chat
response = simple_chat(
    prompt="What is Python?",
    system_message="You are a helpful programming tutor."
)
print(response)

# Full control with chat_completion
response = chat_completion(
    messages=[
        {"role": "system", "content": "Always answer in rhymes."},
        {"role": "user", "content": "What day is it today?"}
    ],
    temperature=0.7,
)
print(response)
```

### Using the MCP↔LLM Bridge (Demo)

Run the example:

```bash
python examples/bridge_demo.py
```

You'll see tool discovery, tool calls, execution, and final reasoning.

### Running Test Scenarios

Run a structured set of scenarios that use the bridge client:

```bash
# Basic math scenario
python tests/test_llm_mcp_bridge_scenarios.py --basic

# All math scenarios
python tests/test_llm_mcp_bridge_scenarios.py --math

# Run all suites (future servers can extend)
python tests/test_llm_mcp_bridge_scenarios.py --all
```

### Available Tools

#### Math MCP Server Tools

##### `add(numbers: List[float]) -> float`

Sums all numbers in the provided list.

**Parameters:**

- `numbers`: List of numeric values (int or float)

**Returns:**

- Sum of all numbers as float

**Example:**

```python
result = await session.call_tool("add", {"numbers": [1, 2, 3, 4, 5]})
# Returns: 15.0
```

##### `multiply(numbers: List[float]) -> float`

Multiplies all numbers in the provided list.

**Parameters:**

- `numbers`: List of numeric values (int or float)

**Returns:**

- Product of all numbers as float

**Example:**

```python
result = await session.call_tool("multiply", {"numbers": [2, 3, 4]})
# Returns: 24.0
```

## 🛡️ Error Handling

### Math MCP Server Validation

The Math MCP server includes comprehensive validation for all inputs:

#### Validation Checks

- ✅ **Type Validation**: Ensures input is a list
- ✅ **Non-Empty List**: Rejects empty lists
- ✅ **Numeric Values**: Validates all elements are int or float
- ✅ **NaN Detection**: Catches Not-a-Number values
- ✅ **Infinity Detection**: Catches infinite values (±inf)

#### Math Server Error Types

**ValueError** - Raised for:

- Empty lists
- NaN values
- Infinite values

**TypeError** - Raised for:

- Non-list inputs
- Non-numeric elements in the list

#### Math Server Error Examples

```python
# Empty list
await session.call_tool("add", {"numbers": []})
# Returns error: "Cannot add an empty list of numbers"

# Non-numeric value
await session.call_tool("add", {"numbers": [1, "two", 3]})
# Returns error: "Element at index 1 must be a number, got str: two"

# NaN value
await session.call_tool("add", {"numbers": [1, float('nan'), 3]})
# Returns error: "Element at index 1 is NaN (Not a Number)"

# Infinite value
await session.call_tool("multiply", {"numbers": [5, float('inf')]})
# Returns error: "Element at index 1 is infinite"
```

## 🧪 Testing

### Math MCP Server Tests

The project includes comprehensive test coverage with 20 tests:

- **12 Functional Tests**: Verify correct mathematical operations
- **8 Error Handling Tests**: Validate error detection and reporting

### Running Tests

```bash
python tests/test_math_mcp_server.py
```

### Test Coverage

**Functional Tests:**

- Basic addition and multiplication
- Decimal number operations
- Negative number handling
- Single number operations
- Zero operations
- Large number calculations
- Sequential operations (chaining)

**Error Handling Tests:**

- Empty list validation
- Non-numeric element detection
- NaN value detection
- Infinity detection (positive and negative)
- Mixed invalid values
- Type error reporting with index information

## 📁 Project Structure

```text
mcp/
├── pyproject.toml                        # Package metadata and dependencies
├── requirements.txt                      # Pinned dependencies (alternative)
├── examples/
│   └── bridge_demo.py                    # Demo entrypoint
├── src/
│   └── mcp_bridge/
│       ├── servers/
│       │   └── math_server.py            # FastMCP math server
│       ├── llm/
│       │   └── openai_client.py          # LLM client utils
│       └── bridge/
│           └── client.py                 # MCP↔LLM bridge orchestrator
├── tests/
│   ├── test_llm_mcp_bridge_scenarios.py  # Scenario runner
│   └── test_math_mcp_server.py           # Math server tests
├── README.md
├── CHANGELOG.md
└── .gitignore
```

## 🔄 Architecture

### Math MCP Server Architecture

The Math MCP server uses a client-server architecture with stdio transport:

```text
┌─────────────┐                    ┌──────────────────┐
│   Client    │                    │  Math MCP Server │
│             │                    │                  │
│  - Session  │ ──── stdio ──────► │  - add()         │
│  - call_tool│ ◄─── stdio ─────── │  - multiply()    │
│             │                    │                  │
└─────────────┘                    └──────────────────┘
```

1. Client spawns server as subprocess
2. Communication via standard input/output
3. Client sends tool call requests
4. Server validates inputs and executes operations
5. Server returns results or errors
6. Client processes responses

### LLM Client Architecture

The LLM client provides utility functions for HTTP-based communication with local LLM servers:

```text
┌─────────────────────┐                    ┌──────────────────────┐
│   Python Script     │                    │   Local LLM Server   │
│                     │                    │  (localhost:1234)    │
│  - simple_chat()    │ ──── HTTP POST ──► │                      │
│  - chat_completion()│ ◄─── JSON ──────── │  - Chat Completions  │
│  - conversational() │                    │  - OpenAI-compatible │
│                     │                    │                      │
└─────────────────────┘                    └──────────────────────┘
```

1. Import functions from `mcp_bridge.llm.openai_client`
2. Call functions with messages and parameters
3. Module sends HTTP POST to LLM API endpoint
4. LLM server processes request and generates response
5. Module validates and extracts response content
6. Returns assistant's message to caller

## 🤝 Contributing

Contributions are welcome\! Please feel free to submit a Pull Request.

### Development Guidelines

1. Use feature branches
2. Add/extend tests for new MCP tools
3. Keep dynamic tool discovery (avoid hard-coded tool schemas)
4. Run test suite before PR (`python tests/test_llm_mcp_bridge_scenarios.py --all`)
5. Install with dev extras: `pip install -e .[dev]`

## 📝 License

This project is open source and available under the MIT License.

## 👤 Author

- **Nihat**
- Email: [nihat@yinovasyon.com](mailto:nihat@yinovasyon.com)
- GitHub: [@y-nihat](https://github.com/y-nihat)

## 🙏 Acknowledgments

- Built with [FastMCP](https://github.com/jlowin/fastmcp) framework
- Uses [Model Context Protocol](https://modelcontextprotocol.io/) specification
- LLM integration via OpenAI-compatible API endpoints
- HTTP communication powered by [Requests](https://requests.readthedocs.io/) library

## 📚 Additional Resources

- [MCP Documentation](https://modelcontextprotocol.io/introduction)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [Python asyncio Documentation](https://docs.python.org/3/library/asyncio.html)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [Requests Documentation](https://requests.readthedocs.io/)

-----

**Version:** 1.2.0  
**Last Updated:** November 8, 2025
