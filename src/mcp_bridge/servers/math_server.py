import math
from typing import List
from mcp.server.fastmcp import FastMCP
from mcp_bridge.servers.dynamic_registry import get_global_registry

# Create FastMCP server instance
mcp = FastMCP("math-server")

# Get dynamic tool registry for runtime enable/disable
registry = get_global_registry()

# Register tools in the registry (all enabled by default)
registry.register_tool("add", enabled=True)
registry.register_tool("multiply", enabled=True)


@mcp.tool()
def add(numbers: List[float]) -> float:
    """
    Sums the given list of numbers.
    'numbers' argument is a list of floats.

    Raises:
        ValueError: If numbers list is empty or contains invalid values
        TypeError: If input is not a list or contains non-numeric values
        RuntimeError: If tool is disabled
    """
    # Check if tool is enabled via dynamic registry
    if not registry.is_tool_enabled("add"):
        raise RuntimeError("Tool 'add' is currently disabled")

    # Validate input is a list
    if not isinstance(numbers, list):
        raise TypeError(f"Input must be a list, got {type(numbers).__name__}")

    # Validate list is not empty
    if len(numbers) == 0:
        raise ValueError("Cannot add an empty list of numbers")

    # Validate all elements are numeric
    for i, num in enumerate(numbers):
        if not isinstance(num, (int, float)):
            raise TypeError(
                f"Element at index {i} must be a number, got {type(num).__name__}: {num}"
            )
        if math.isnan(num):
            raise ValueError(f"Element at index {i} is NaN (Not a Number)")
        if math.isinf(num):
            raise ValueError(f"Element at index {i} is infinite")

    print(f"Server: Addition request received: {numbers}")
    return sum(numbers)


@mcp.tool()
def multiply(numbers: List[float]) -> float:
    """
    Multiplies the given list of numbers.
    'numbers' argument is a list of floats.

    Raises:
        ValueError: If numbers list is empty or contains invalid values
        TypeError: If input is not a list or contains non-numeric values
        RuntimeError: If tool is disabled
    """
    # Check if tool is enabled via dynamic registry
    if not registry.is_tool_enabled("multiply"):
        raise RuntimeError("Tool 'multiply' is currently disabled")

    # Validate input is a list
    if not isinstance(numbers, list):
        raise TypeError(f"Input must be a list, got {type(numbers).__name__}")

    # Validate list is not empty
    if len(numbers) == 0:
        raise ValueError("Cannot multiply an empty list of numbers")

    # Validate all elements are numeric
    for i, num in enumerate(numbers):
        if not isinstance(num, (int, float)):
            raise TypeError(
                f"Element at index {i} must be a number, got {type(num).__name__}: {num}"
            )
        if math.isnan(num):
            raise ValueError(f"Element at index {i} is NaN (Not a Number)")
        if math.isinf(num):
            raise ValueError(f"Element at index {i} is infinite")

    print(f"Server: Multiplication request received: {numbers}")
    # Use math.prod for multiplication operation
    return math.prod(numbers)


@mcp.tool()
def set_tool_enabled(tool_name: str, enabled: bool) -> str:
    """
    Enable or disable a math tool dynamically without restart.

    Args:
        tool_name: Name of the tool to modify ('add' or 'multiply')
        enabled: True to enable, False to disable

    Returns:
        Status message

    Raises:
        ValueError: If tool_name is invalid
    """
    valid_tools = {"add", "multiply"}
    if tool_name not in valid_tools:
        raise ValueError(
            f"Invalid tool name: {tool_name}. Must be one of {valid_tools}"
        )

    if enabled:
        registry.enable_tool(tool_name)
        return f"Tool '{tool_name}' is now ENABLED"
    else:
        registry.disable_tool(tool_name)
        return f"Tool '{tool_name}' is now DISABLED"


@mcp.tool()
def get_tool_status() -> dict:
    """
    Get the current status of all registered math tools.

    Returns:
        Dictionary with tool status information
    """
    stats = registry.get_stats()
    enabled_tools = list(registry.get_enabled_tools())
    all_tools = registry.get_all_tools()

    tool_details = {}
    for name, metadata in all_tools.items():
        tool_details[name] = {
            "enabled": metadata.enabled,
            "last_modified": metadata.last_modified,
        }

    return {
        "stats": stats,
        "enabled_tools": enabled_tools,
        "tool_details": tool_details,
    }


if __name__ == "__main__":
    import logging

    # Suppress verbose INFO logs from FastMCP server
    logging.getLogger("mcp").setLevel(logging.WARNING)
    # Start the server with stdio transport
    mcp.run(transport="stdio")
