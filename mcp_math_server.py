import math
from typing import List
from mcp.server.fastmcp import FastMCP

# Create FastMCP server instance
mcp = FastMCP("math-server")


@mcp.tool()
def add(numbers: List[float]) -> float:
    """
    Sums the given list of numbers.
    'numbers' argument is a list of floats.

    Raises:
        ValueError: If numbers list is empty or contains invalid values
        TypeError: If input is not a list or contains non-numeric values
    """
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
    """
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


if __name__ == "__main__":
    # Start the server with stdio transport
    mcp.run(transport="stdio")
