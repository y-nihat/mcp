# Math MCP Server

A Model Context Protocol (MCP) server implementation that provides mathematical operations through a standardized interface. This server exposes `add` and `multiply` tools for performing arithmetic operations on lists of numbers.

## 🚀 Features

- **Addition Tool**: Sum any list of numbers
- **Multiplication Tool**: Multiply any list of numbers
- **Comprehensive Error Handling**: Validates inputs for type safety and edge cases
- **FastMCP Framework**: Built on the efficient FastMCP server framework
- **Stdio Transport**: Uses standard input/output for client-server communication

## 📋 Requirements

- Python 3.8+
- Required packages:
  - `mcp` - Model Context Protocol library
  - `fastmcp` - Fast MCP server implementation

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

### Running the Server

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
        print(result.content[0].text)  # Output: 56.0
```

### Available Tools

#### `add(numbers: List[float]) -> float`

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

#### `multiply(numbers: List[float]) -> float`

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

The server includes comprehensive validation for all inputs:

### Validation Checks

- ✅ **Type Validation**: Ensures input is a list
- ✅ **Non-Empty List**: Rejects empty lists
- ✅ **Numeric Values**: Validates all elements are int or float
- ✅ **NaN Detection**: Catches Not-a-Number values
- ✅ **Infinity Detection**: Catches infinite values (±inf)

### Error Types

**ValueError** - Raised for:

- Empty lists
- NaN values
- Infinite values

**TypeError** - Raised for:

- Non-list inputs
- Non-numeric elements in the list

### Error Examples

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
├── mcp_math_server.py        # Main MCP server implementation
├── test_math_mcp_server.py   # Comprehensive test suite
├── README.md                  # This file
├── CHANGELOG.md               # Version history and changes
└── .gitignore                 # Git ignore rules
```

## 🔄 Architecture

The server uses a client-server architecture with stdio transport:

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

## 📚 Additional Resources

- [MCP Documentation](https://modelcontextprotocol.io/introduction)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [Python asyncio Documentation](https://docs.python.org/3/library/asyncio.html)

---

**Version:** 1.0.0  
**Last Updated:** November 7, 2025
