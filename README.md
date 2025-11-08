# MCP Bridge & Math MCP Server# MCP Bridge & Math MCP Server



Bridge local Model Context Protocol (MCP) servers to an OpenAI-compatible LLM tool-calling interface. Includes a sample Math MCP server, a reusable bridge client that performs dynamic tool discovery, scenario tests, and a demo script.Bridge local Model Context Protocol (MCP) servers to an OpenAI-compatible LLM tool-calling interface. Includes a sample Math MCP server, a reusable bridge client that performs dynamic tool discovery, scenario tests, and a demo script.



## 📦 Components### 1. Math MCP Server (`src/mcp_bridge/servers/math_server.py`)



### 1. Math MCP Server (`src/mcp_bridge/servers/math_server.py`)Model Context Protocol server exposing math tools (`add`, `multiply`) using FastMCP.



Model Context Protocol server exposing math tools (`add`, `multiply`) using FastMCP.### 2. LLM Client (`src/mcp_bridge/llm/openai_client.py`)



### 2. LLM Client (`src/mcp_bridge/llm/openai_client.py`)Lightweight OpenAI-compatible wrapper utilities for a local LLM (chat completions + helpers).



Lightweight OpenAI-compatible wrapper utilities for a local LLM (chat completions + helpers).### 3. Bridge Client (`src/mcp_bridge/bridge/client.py`)



### 3. Bridge Client (`src/mcp_bridge/bridge/client.py`)Discovers MCP tools at runtime and converts them to OpenAI `tools` format; orchestrates multi-round tool calling.



Discovers MCP tools at runtime and converts them to OpenAI `tools` format; orchestrates multi-round tool calling.### 4. Demo (`examples/bridge_demo.py`)



### 4. Demo (`examples/bridge_demo.py`)Minimal example showing end-to-end tool calling with discovered MCP tools.



Minimal example showing end-to-end tool calling with discovered MCP tools.### 5. Scenario Tests (`tests/test_llm_mcp_bridge_scenarios.py`)



### 5. Scenario Tests (`tests/test_llm_mcp_bridge_scenarios.py`)Extensible test runner exercising multi-round tool calls.



Extensible test runner exercising multi-round tool calls.### 6. Math Server Tests (`tests/test_math_mcp_server.py`)



### 6. Math Server Tests (`tests/test_math_mcp_server.py`)20 focused tests (functional + error handling) for server validation.



20 focused tests (functional + error handling) for server validation.### Editable Install (recommended)



## 🚀 Features```bash



### Math MCP ServerOr install dependencies directly:



- **Addition Tool**: Sum any list of numbers```bash

- **Multiplication Tool**: Multiply any list of numbers

- **Comprehensive Error Handling**: Validates inputs for type safety and edge casesRun directly (stdio transport):

- **FastMCP Framework**: Built on the efficient FastMCP server framework

- **Stdio Transport**: Uses standard input/output for client-server communication```bash



### LLM ClientProgrammatic usage:



- **Chat Completion**: Full-featured LLM API interactions with complete control```python

- **Simple Chat**: Quick interface for single prompts with optional system messages

- **Conversational Chat**: Multi-turn dialogue with conversation history management```python

- **OpenAI-Compatible**: Works with any OpenAI-compatible local LLM serverfrom mcp import ClientSession, StdioServerParameters

- **Flexible Configuration**: Customizable model, temperature, max tokens, and streamingfrom mcp.client.stdio import stdio_client



### MCP↔LLM Bridge ClientRun the example:



- **Dynamic Tool Discovery**: Queries MCP servers for tools at runtime (no hardcoded specs)```bash

- **OpenAI Tools Mapping**: Converts MCP JSON Schemas to OpenAI-compatible `tools` entries

- **Tool Execution**: Calls MCP tools and injects results back into the conversation```bash

- **Multi-round Orchestration**: Supports several rounds until a final answer is produced# Basic math scenario

- **Configurable Behavior**: Verbose logging, system prompt, max rounds (via `BridgeConfig`)python tests/test_llm_mcp_bridge_scenarios.py --basic



## 📋 Requirements# All math scenarios

python tests/test_llm_mcp_bridge_scenarios.py --math

- Python 3.9+

- Local OpenAI-compatible LLM endpoint (default: `http://localhost:1234`)# Run all suites (future servers can extend)

- Dependencies: `mcp`, `fastmcp`, `httpx`, `requests`, `pydantic` (managed via `pyproject.toml`)python tests/test_llm_mcp_bridge_scenarios.py --all



## 🔧 Installation```bash

python tests/test_math_mcp_server.py

### Option 1: Editable Install with pyproject.toml (Recommended)```

# MCP Server Project

For active development and running tests:

A collection of Model Context Protocol (MCP) server implementations and utilities for mathematical operations and LLM interactions.

```bash

git clone https://github.com/y-nihat/mcp.git## 📦 Modules

cd mcp

pip install -e .[dev]### 1. Math MCP Server (`mcp_math_server.py`)

```

A Model Context Protocol server that provides mathematical operations through a standardized interface.

This installs the package in editable mode with all runtime and development dependencies (including pytest).

### 2. LLM Service Module (`mcp_llm_server.py`)

For runtime-only (no test tools):

A utility module for interacting with local LLM servers via OpenAI-compatible APIs.

```bash

pip install -e .### 3. MCP↔LLM Bridge Client (`mcp_llm_bridge_client.py`)

```

A reusable client that dynamically discovers MCP tools, converts them into OpenAI tools schema, orchestrates tool calls with your OpenAI-compatible local LLM, and executes them via MCP.

### Option 2: Install from requirements.txt

### 4. Test Scenarios (`test_llm_mcp_bridge_scenarios.py`)

If you prefer pinned versions without installing the package:

Extensible scenario runner that connects to your MCP servers and validates end-to-end LLM tool calling using the bridge client.

```bash

pip install -r requirements.txt### 5. Bridge Demo (`llm_mcp_tool_bridge_demo.py`)

```

A thin, backwards-compatible demo that uses the bridge client to run a simple example.

## 🏃 Usage

## 🚀 Features

### Using the Math MCP Server

### Math MCP Server

Run directly (stdio transport):

- **Addition Tool**: Sum any list of numbers

```bash- **Multiplication Tool**: Multiply any list of numbers

python src/mcp_bridge/servers/math_server.py- **Comprehensive Error Handling**: Validates inputs for type safety and edge cases

```- **FastMCP Framework**: Built on the efficient FastMCP server framework

- **Stdio Transport**: Uses standard input/output for client-server communication

Programmatic usage:

### LLM Service Module

```python

from mcp import ClientSession, StdioServerParameters- **Chat Completion**: Full-featured LLM API interactions with complete control

from mcp.client.stdio import stdio_client- **Simple Chat**: Quick interface for single prompts with optional system messages

- **Conversational Chat**: Multi-turn dialogue with conversation history management

server_params = StdioServerParameters(- **OpenAI-Compatible**: Works with any OpenAI-compatible local LLM server

    command="python",- **Flexible Configuration**: Customizable model, temperature, max tokens, and streaming

    args=["src/mcp_bridge/servers/math_server.py"],

    env=None,### MCP↔LLM Bridge Client

)

- **Dynamic Tool Discovery**: Queries MCP servers for tools at runtime (no hardcoded specs)

async with stdio_client(server_params) as (read, write):- **OpenAI Tools Mapping**: Converts MCP JSON Schemas to OpenAI-compatible `tools` entries

    async with ClientSession(read, write) as session:- **Tool Execution**: Calls MCP tools and injects results back into the conversation

        await session.initialize()- **Multi-round Orchestration**: Supports several rounds until a final answer is produced

        result = await session.call_tool("add", {"numbers": [10, 20, 30]})- **Configurable Behavior**: Verbose logging, system prompt, max rounds (via `BridgeConfig`)

        print(result.content[0].text)  # 60.0

```## 📋 Requirements



### Using the LLM Client- Python 3.8+

- Required packages:

The LLM client provides utility functions to interact with a local LLM server.  - `mcp` - Model Context Protocol library

  - `fastmcp` - Fast MCP server implementation

#### Prerequisites  - `requests` - HTTP library for LLM API communication



Ensure you have a local LLM server running at `http://localhost:1234` with OpenAI-compatible API (e.g., LM Studio, LocalAI, Ollama with OpenAI compatibility, etc.).## 🔧 Installation



#### Basic Usage1. Clone the repository:



```python```bash

from mcp_bridge.llm.openai_client import (git clone https://github.com/y-nihat/mcp.git

    simple_chat,cd mcp

    chat_completion,```

    conversational_chat,

)1. Install dependencies:



# Simple single-prompt chat```bash

response = simple_chat(pip install -r requirements.txt

    prompt="What is Python?",```

    system_message="You are a helpful programming tutor."

)## 🏃 Usage

print(response)

### Using the Math MCP Server

# Full control with chat_completion

response = chat_completion(The server runs as a subprocess and communicates via stdio:

    messages=[

        {"role": "system", "content": "Always answer in rhymes."},```python

        {"role": "user", "content": "What day is it today?"}from mcp import ClientSession, StdioServerParameters

    ],from mcp.client.stdio import stdio_client

    temperature=0.7,

)server_params = StdioServerParameters(

print(response)    command="python",

```    args=["mcp_math_server.py"],

    env=None

### Using the MCP↔LLM Bridge (Demo))



Run the example:async with stdio_client(server_params) as (read, write):

    async with ClientSession(read, write) as session:

```bash        await session.initialize()

python examples/bridge_demo.py        

```        # Call the add tool

        result = await session.call_tool("add", {"numbers": [10, 20, 30]})

You'll see tool discovery, tool calls, execution, and final reasoning.        print(result.content[0].text)  # Output: 60.0

        

### Running Test Scenarios        # Call the multiply tool

        result = await session.call_tool("multiply", {"numbers": [7, 8]})

Run a structured set of scenarios that use the bridge client:        print(result.content[0].text)  # Output: 24.0

```

```bash

# Basic math scenario# MCP Bridge & Math MCP Server

python tests/test_llm_mcp_bridge_scenarios.py --basicBridge local Model Context Protocol (MCP) servers to an OpenAI-compatible LLM tool-calling interface. Includes a sample Math MCP server, a reusable bridge client that performs dynamic tool discovery, scenario tests, and a demo script.

The LLM service provides utility functions to interact with a local LLM server.

# All math scenarios

python tests/test_llm_mcp_bridge_scenarios.py --mathModel Context Protocol server exposing math tools (`add`, `multiply`) using FastMCP.

#### Prerequisites

# Run all suites (future servers can extend)Lightweight OpenAI-compatible wrapper utilities for a local LLM (chat completions + helpers).

python tests/test_llm_mcp_bridge_scenarios.py --all

```Discovers MCP tools at runtime and converts them to OpenAI `tools` format; orchestrates multi-round tool calling.

Ensure you have a local LLM server running at `http://localhost:1234` with OpenAI-compatible API (e.g., LM Studio, LocalAI, Ollama with OpenAI compatibility, etc.).

### Available ToolsMinimal example showing end-to-end tool calling with discovered MCP tools.



#### Math MCP Server ToolsExtensible test runner exercising multi-round tool calls.

#### Basic Usage

##### `add(numbers: List[float]) -> float`20 focused tests (functional + error handling) for server validation.



Sums all numbers in the provided list.Python 3.9+

Local OpenAI-compatible LLM endpoint (default: `http://localhost:1234`)

**Parameters:**Dependencies: `requests`, `fastmcp` (see `pyproject.toml` or `requirements.txt`)

    prompt="What is Python?",

- `numbers`: List of numeric values (int or float)### Editable Install (recommended)

```bash

**Returns:**git clone https://github.com/y-nihat/mcp.git

cd mcp

- Sum of all numbers as floatpip install -e .

```

**Example:**Or install dependencies directly:

```bash

```pythonpip install -r requirements.txt

result = await session.call_tool("add", {"numbers": [1, 2, 3, 4, 5]})```

# Returns: 15.0    ],

```Run directly (stdio transport):

```bash

##### `multiply(numbers: List[float]) -> float`python src/mcp_bridge/servers/math_server.py

```

Multiplies all numbers in the provided list.Programmatic usage:

```python

**Parameters:**from mcp import ClientSession, StdioServerParameters

from mcp.client.stdio import stdio_client

- `numbers`: List of numeric values (int or float)

server_params = StdioServerParameters(

**Returns:**    command="python",

    args=["src/mcp_bridge/servers/math_server.py"],

- Product of all numbers as float    env=None,

)

**Example:**

async with stdio_client(server_params) as (read, write):

```python    async with ClientSession(read, write) as session:

result = await session.call_tool("multiply", {"numbers": [2, 3, 4]})        await session.initialize()

# Returns: 24.0        result = await session.call_tool("add", {"numbers": [10, 20, 30]})

```        print(result.content[0].text)  # 60.0

```

## 🛡️ Error Handling    temperature=0.7,

```python

### Math MCP Server Validationfrom mcp_bridge.llm.openai_client import (

    simple_chat,

The Math MCP server includes comprehensive validation for all inputs:    chat_completion,

    conversational_chat,

#### Validation Checks)

```

- ✅ **Type Validation**: Ensures input is a list)

- ✅ **Non-Empty List**: Rejects empty listsRun the example:

- ✅ **Numeric Values**: Validates all elements are int or float```bash

- ✅ **NaN Detection**: Catches Not-a-Number valuespython examples/bridge_demo.py

- ✅ **Infinity Detection**: Catches infinite values (±inf)```

You’ll see tool discovery, tool calls, execution, and final reasoning.

#### Math Server Error Types    conversation_history=history,

The project includes comprehensive test coverage with 20 tests:

**ValueError** - Raised for:)

python tests/test_math_mcp_server.py

- Empty listshistory = result["updated_history"]

- NaN values

- Infinite values# Continue the conversation

result = conversational_chat(

**TypeError** - Raised for:    conversation_history=history,

    new_message="Tell me a joke"

- Non-list inputs)

- Non-numeric elements in the listprint(result["response"])

```

#### Math Server Error Examples

#### Testing the LLM Module

```python

# Empty listRun the module directly to test with the example:

await session.call_tool("add", {"numbers": []})

# Returns error: "Cannot add an empty list of numbers"```bash

python mcp_llm_server.py

# Non-numeric value```

await session.call_tool("add", {"numbers": [1, "two", 3]})

# Returns error: "Element at index 1 must be a number, got str: two"### Using the MCP↔LLM Bridge (Demo)



# NaN valueRuns a simple example that asks the LLM to use MCP tools it discovers dynamically.

await session.call_tool("add", {"numbers": [1, float('nan'), 3]})

# Returns error: "Element at index 1 is NaN (Not a Number)"```bash

python llm_mcp_tool_bridge_demo.py

# Infinite value```

await session.call_tool("multiply", {"numbers": [5, float('inf')]})Import functions from `mcp_bridge.llm.openai_client`

# Returns error: "Element at index 1 is infinite"You should see the bridge discover tools from the server, the model emit tool calls, the MCP server execute them, and the model produce a final answer.

```1. Use feature branches

1. Add/extend tests for new MCP tools

## 🧪 Testing1. Keep dynamic tool discovery (avoid hard-coded tool schemas)

1. Run test suite before PR (`python tests/test_llm_mcp_bridge_scenarios.py --all`)

### Math MCP Server Tests# Basic math scenario

python test_llm_mcp_bridge_scenarios.py --basic

The project includes comprehensive test coverage with 20 tests:

# All math scenarios

- **12 Functional Tests**: Verify correct mathematical operationspython test_llm_mcp_bridge_scenarios.py --math

- **8 Error Handling Tests**: Validate error detection and reporting

# Run all suites (extend as you add more servers)

### Running Testspython test_llm_mcp_bridge_scenarios.py --all

```

```bash

python tests/test_math_mcp_server.py### Available Tools

```

#### Math MCP Server Tools

### Test Coverage

##### `add(numbers: List[float]) -> float`

**Functional Tests:**

Sums all numbers in the provided list.

- Basic addition and multiplication

- Decimal number operations**Parameters:**

- Negative number handling

- Single number operations- `numbers`: List of numeric values (int or float)

- Zero operations

- Large number calculations**Returns:**

- Sequential operations (chaining)

- Sum of all numbers as float

**Error Handling Tests:**

**Example:**

- Empty list validation

- Non-numeric element detection```python

- NaN value detectionresult = await session.call_tool("add", {"numbers": [1, 2, 3, 4, 5]})

- Infinity detection (positive and negative)# Returns: 15.0

- Mixed invalid values```

- Type error reporting with index information

##### `multiply(numbers: List[float]) -> float`

## 📁 Project Structure

Multiplies all numbers in the provided list.

```text

mcp/**Parameters:**

├── pyproject.toml                        # Package metadata and dependencies

├── requirements.txt                      # Pinned dependencies (alternative)- `numbers`: List of numeric values (int or float)

├── examples/

│   └── bridge_demo.py                    # Demo entrypoint**Returns:**

├── src/

│   └── mcp_bridge/- Product of all numbers as float

│       ├── servers/

│       │   └── math_server.py            # FastMCP math server**Example:**

│       ├── llm/

│       │   └── openai_client.py          # LLM client utils```python

│       └── bridge/result = await session.call_tool("multiply", {"numbers": [2, 3, 4]})

│           └── client.py                 # MCP↔LLM bridge orchestrator# Returns: 24.0

├── tests/```

│   ├── test_llm_mcp_bridge_scenarios.py  # Scenario runner

│   └── test_math_mcp_server.py           # Math server tests#### LLM Service Module Functions

├── README.md

├── CHANGELOG.md##### `chat_completion(messages, model=None, temperature=0.7, max_tokens=-1, stream=False) -> str`

└── .gitignore

```Send a chat completion request to the local LLM server with full control over all parameters.



## 🔄 Architecture**Parameters:**



### Math MCP Server Architecture- `messages`: List of message dictionaries with 'role' and 'content' keys

- `model`: The model to use (default: "qwen/qwen3-4b-2507")

The Math MCP server uses a client-server architecture with stdio transport:- `temperature`: Controls randomness, 0.0 to 1.0 (default: 0.7)

- `max_tokens`: Maximum tokens to generate, -1 for unlimited (default: -1)

```text- `stream`: Whether to stream the response (default: False)

┌─────────────┐                    ┌──────────────────┐

│   Client    │                    │  Math MCP Server │**Returns:**

│             │                    │                  │

│  - Session  │ ──── stdio ───────►│  - add()         │- The assistant's response as a string

│  - call_tool│ ◄─── stdio ───────│  - multiply()    │

│             │                    │                  │**Example:**

└─────────────┘                    └──────────────────┘

``````python

response = chat_completion(

1. Client spawns server as subprocess    messages=[

2. Communication via standard input/output        {"role": "system", "content": "You are a helpful assistant."},

3. Client sends tool call requests        {"role": "user", "content": "Explain Python in one sentence."}

4. Server validates inputs and executes operations    ],

5. Server returns results or errors    temperature=0.5

6. Client processes responses)

```

### LLM Client Architecture

##### `simple_chat(prompt, system_message=None) -> str`

The LLM client provides utility functions for HTTP-based communication with local LLM servers:

Simple chat interface for quick single-prompt interactions.

```text

┌─────────────────────┐                    ┌──────────────────────┐**Parameters:**

│   Python Script     │                    │   Local LLM Server   │

│                     │                    │  (localhost:1234)    │- `prompt`: The user's message/question

│  - simple_chat()    │ ──── HTTP POST ───►│                      │- `system_message`: Optional system message to set context or behavior

│  - chat_completion()│ ◄─── JSON ─────────│  - Chat Completions  │

│  - conversational() │                    │  - OpenAI-compatible │**Returns:**

│                     │                    │                      │

└─────────────────────┘                    └──────────────────────┘- The assistant's response as a string

```

**Example:**

1. Import functions from `mcp_bridge.llm.openai_client`

2. Call functions with messages and parameters```python

3. Module sends HTTP POST to LLM API endpointresponse = simple_chat(

4. LLM server processes request and generates response    prompt="What is machine learning?",

5. Module validates and extracts response content    system_message="You are an expert data scientist."

6. Returns assistant's message to caller)

```

## 🤝 Contributing

##### `conversational_chat(conversation_history, new_message) -> Dict`

Contributions are welcome! Please feel free to submit a Pull Request.

Continue a conversation with context from previous messages.

### Development Guidelines

**Parameters:**

1. Use feature branches

2. Add/extend tests for new MCP tools- `conversation_history`: List of previous message dictionaries

3. Keep dynamic tool discovery (avoid hard-coded tool schemas)- `new_message`: New user message to add to the conversation

4. Run test suite before PR (`python tests/test_llm_mcp_bridge_scenarios.py --all`)

5. Install with dev extras: `pip install -e .[dev]`**Returns:**



## 📝 License- Dictionary with 'response' (str) and 'updated_history' (list)



This project is open source and available under the MIT License.**Example:**



## 👤 Author```python

history = []

- **Nihat**result = conversational_chat(history, "Hello!")

- Email: <nihat@yinovasyon.com>print(result["response"])

- GitHub: [@y-nihat](https://github.com/y-nihat)history = result["updated_history"]



## 🙏 Acknowledgmentsresult = conversational_chat(history, "Tell me more")

print(result["response"])

- Built with [FastMCP](https://github.com/jlowin/fastmcp) framework```

- Uses [Model Context Protocol](https://modelcontextprotocol.io/) specification

- LLM integration via OpenAI-compatible API endpoints## 🛡️ Error Handling

- HTTP communication powered by [Requests](https://requests.readthedocs.io/) library

### Math MCP Server Validation

## 📚 Additional Resources

The Math MCP server includes comprehensive validation for all inputs:

- [MCP Documentation](https://modelcontextprotocol.io/introduction)

- [FastMCP Documentation](https://github.com/jlowin/fastmcp)#### Validation Checks

- [Python asyncio Documentation](https://docs.python.org/3/library/asyncio.html)

- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)- ✅ **Type Validation**: Ensures input is a list

- [Requests Documentation](https://requests.readthedocs.io/)- ✅ **Non-Empty List**: Rejects empty lists

- ✅ **Numeric Values**: Validates all elements are int or float

---- ✅ **NaN Detection**: Catches Not-a-Number values

- ✅ **Infinity Detection**: Catches infinite values (±inf)

**Version:** 1.2.0  

**Last Updated:** November 8, 2025#### Math Server Error Types


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

### LLM Service Module Validation

The LLM service includes validation for chat messages and API communication:

#### LLM Validation Checks

- ✅ **Message List Validation**: Ensures messages is a non-empty list
- ✅ **Message Format**: Validates each message has 'role' and 'content' keys
- ✅ **Role Validation**: Ensures role is one of: system, user, assistant
- ✅ **API Communication**: Handles HTTP errors and timeouts (60s timeout)
- ✅ **Response Format**: Validates LLM API response structure

#### LLM Service Error Types

**ValueError** - Raised for:

- Empty message lists
- Malformed message dictionaries
- Invalid role types
- Unexpected API response format

**requests.RequestException** - Raised for:

- Network communication errors
- HTTP errors (4xx, 5xx status codes)
- Request timeouts

#### LLM Service Error Examples

```python
# Empty messages list
chat_completion([])
# Raises: "messages must be a non-empty list"

# Invalid role
chat_completion([{"role": "invalid", "content": "Hello"}])
# Raises: "Invalid role 'invalid' at index 0"

# Missing content key
chat_completion([{"role": "user"}])
# Raises: "Message at index 0 must have 'role' and 'content' keys"

# LLM server not running
simple_chat("Hello")
# Raises: requests.RequestException with connection error details
```

## 🧪 Testing

### Math MCP Server Tests

The project includes comprehensive test coverage with 20 tests:

- **12 Functional Tests**: Verify correct mathematical operations
- **8 Error Handling Tests**: Validate error detection and reporting

### Running Tests

```bash
python test_math_mcp_server.py
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
├── mcp_math_server.py              # Math MCP server (add, multiply)
├── mcp_llm_server.py               # LLM service utility (OpenAI-compatible)
├── mcp_llm_bridge_client.py        # Reusable MCP↔LLM bridge (dynamic discovery)
├── llm_mcp_tool_bridge_demo.py     # Thin demo wrapper using the bridge
├── test_llm_mcp_bridge_scenarios.py# Scenario runner for end-to-end tests
├── test_math_mcp_server.py         # Math server tests (functional + errors)
├── requirements.txt                # Python dependencies
├── README.md                       # Documentation
├── CHANGELOG.md                    # Version history and changes
└── .gitignore                      # Git ignore rules
```

## 🔄 Architecture

### Math MCP Server Architecture

The Math MCP server uses a client-server architecture with stdio transport:

```text
┌─────────────┐                    ┌──────────────────┐
│   Client    │                    │  Math MCP Server │
│             │                    │                  │
│  - Session  │ ──── stdio ───────►│  - add()         │
│  - call_tool│ ◄─── stdio ───────│  - multiply()    │
│             │                    │                  │
└─────────────┘                    └──────────────────┘
```

1. Client spawns server as subprocess
2. Communication via standard input/output
3. Client sends tool call requests
4. Server validates inputs and executes operations
5. Server returns results or errors
6. Client processes responses

### LLM Service Module Architecture

The LLM service module provides utility functions for HTTP-based communication with local LLM servers:

```text
┌─────────────────────┐                    ┌──────────────────────┐
│   Python Script     │                    │   Local LLM Server   │
│                     │                    │  (localhost:1234)    │
│  - simple_chat()    │ ──── HTTP POST ───►│                      │
│  - chat_completion()│ ◄─── JSON ─────────│  - Chat Completions  │
│  - conversational() │                    │  - OpenAI-compatible │
│                     │                    │                      │
└─────────────────────┘                    └──────────────────────┘
```

1. Import functions from `mcp_llm_server`
2. Call functions with messages and parameters
3. Module sends HTTP POST to LLM API endpoint
4. LLM server processes request and generates response
5. Module validates and extracts response content
6. Returns assistant's message to caller

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Guidelines

1. Follow PEP 8 style guidelines
1. Add tests for new features
1. Update documentation for API changes
1. Ensure all tests pass before submitting PR

## 📝 License

This project is open source and available under the MIT License.

## 👤 Author

- **Nihat**
- Email: <nihat@yinovasyon.com>
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

---

**Version:** 1.1.0  
**Last Updated:** November 8, 2025
