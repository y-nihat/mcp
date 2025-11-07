# MCP Server Project

A collection of Model Context Protocol (MCP) server implementations and utilities for mathematical operations and LLM interactions.

## 📦 Modules

### 1. Math MCP Server (`mcp_math_server.py`)

A Model Context Protocol server that provides mathematical operations through a standardized interface.

### 2. LLM Service Module (`mcp_llm_server.py`)

A utility module for interacting with local LLM servers via OpenAI-compatible APIs.

## 🚀 Features

### Math MCP Server

- **Addition Tool**: Sum any list of numbers
- **Multiplication Tool**: Multiply any list of numbers
- **Comprehensive Error Handling**: Validates inputs for type safety and edge cases
- **FastMCP Framework**: Built on the efficient FastMCP server framework
- **Stdio Transport**: Uses standard input/output for client-server communication

### LLM Service Module

- **Chat Completion**: Full-featured LLM API interactions with complete control
- **Simple Chat**: Quick interface for single prompts with optional system messages
- **Conversational Chat**: Multi-turn dialogue with conversation history management
- **OpenAI-Compatible**: Works with any OpenAI-compatible local LLM server
- **Flexible Configuration**: Customizable model, temperature, max tokens, and streaming

## 📋 Requirements

- Python 3.8+
- Required packages:
  - `mcp` - Model Context Protocol library
  - `fastmcp` - Fast MCP server implementation
  - `requests` - HTTP library for LLM API communication

## 🔧 Installation

1. Clone the repository:

```bash
git clone https://github.com/y-nihat/mcp.git
cd mcp
```

1. Install dependencies:

```bash
pip install -r requirements.txt
```

## 🏃 Usage

### Using the Math MCP Server

The server runs as a subprocess and communicates via stdio:

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

server_params = StdioServerParameters(
    command="python",
    args=["mcp_math_server.py"],
    env=None
)

async with stdio_client(server_params) as (read, write):
    async with ClientSession(read, write) as session:
        await session.initialize()
        
        # Call the add tool
        result = await session.call_tool("add", {"numbers": [10, 20, 30]})
        print(result.content[0].text)  # Output: 60.0
        
        # Call the multiply tool
        result = await session.call_tool("multiply", {"numbers": [7, 8]})
        print(result.content[0].text)  # Output: 24.0
```

### Using the LLM Service Module

The LLM service provides utility functions to interact with a local LLM server.

#### Prerequisites

Ensure you have a local LLM server running at `http://localhost:1234` with OpenAI-compatible API (e.g., LM Studio, LocalAI, Ollama with OpenAI compatibility, etc.).

#### Basic Usage

```python
from mcp_llm_server import simple_chat, chat_completion, conversational_chat

# Simple single-prompt chat
response = simple_chat(
    prompt="What is Python?",
    system_message="You are a helpful programming tutor."
)
print(response)

# Full control with chat_completion
response = chat_completion(
    messages=[
        {"role": "system", "content": "Always answer in rhymes. Today is Thursday"},
        {"role": "user", "content": "What day is it today?"}
    ],
    model="qwen/qwen3-4b-2507",
    temperature=0.7,
    max_tokens=-1
)
print(response)

# Multi-turn conversation
history = []
result = conversational_chat(
    conversation_history=history,
    new_message="Hello! How are you?"
)
print(result["response"])
history = result["updated_history"]

# Continue the conversation
result = conversational_chat(
    conversation_history=history,
    new_message="Tell me a joke"
)
print(result["response"])
```

#### Testing the LLM Module

Run the module directly to test with the example:

```bash
python mcp_llm_server.py
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

#### LLM Service Module Functions

##### `chat_completion(messages, model=None, temperature=0.7, max_tokens=-1, stream=False) -> str`

Send a chat completion request to the local LLM server with full control over all parameters.

**Parameters:**

- `messages`: List of message dictionaries with 'role' and 'content' keys
- `model`: The model to use (default: "qwen/qwen3-4b-2507")
- `temperature`: Controls randomness, 0.0 to 1.0 (default: 0.7)
- `max_tokens`: Maximum tokens to generate, -1 for unlimited (default: -1)
- `stream`: Whether to stream the response (default: False)

**Returns:**

- The assistant's response as a string

**Example:**

```python
response = chat_completion(
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain Python in one sentence."}
    ],
    temperature=0.5
)
```

##### `simple_chat(prompt, system_message=None) -> str`

Simple chat interface for quick single-prompt interactions.

**Parameters:**

- `prompt`: The user's message/question
- `system_message`: Optional system message to set context or behavior

**Returns:**

- The assistant's response as a string

**Example:**

```python
response = simple_chat(
    prompt="What is machine learning?",
    system_message="You are an expert data scientist."
)
```

##### `conversational_chat(conversation_history, new_message) -> Dict`

Continue a conversation with context from previous messages.

**Parameters:**

- `conversation_history`: List of previous message dictionaries
- `new_message`: New user message to add to the conversation

**Returns:**

- Dictionary with 'response' (str) and 'updated_history' (list)

**Example:**

```python
history = []
result = conversational_chat(history, "Hello!")
print(result["response"])
history = result["updated_history"]

result = conversational_chat(history, "Tell me more")
print(result["response"])
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
├── mcp_math_server.py        # Math MCP server implementation
├── mcp_llm_server.py          # LLM service utility module
├── test_math_mcp_server.py   # Test suite for math server
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── CHANGELOG.md               # Version history and changes
└── .gitignore                 # Git ignore rules
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
**Last Updated:** November 7, 2025
