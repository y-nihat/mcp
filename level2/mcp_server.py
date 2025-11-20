from mcp.server.fastmcp import FastMCP

# Create FastMCP server instance
mcp = FastMCP("level2-server")


@mcp.resource(
    "resource://health",
    name="health",
    title="Health",
    description="Server health status",
)
def health() -> str:
    """Return a short health status string for Level 2."""
    # Keep this lightweight: a simple OK / healthy indicator. This can be
    # extended to return JSON or more details (uptime, version) if needed.
    return "ok"


@mcp.tool()
def greet(name: str) -> str:
    """Return a greeting message for the provided name."""
    if not isinstance(name, str):
        raise ValueError("name must be a string")
    return f"Hello, {name}! Welcome to MCP."


@mcp.tool()
def math(a: float, b: float, operation: str) -> dict:
    """Perform a simple math operation on two numbers.

    operation must be either 'add' or 'multiply'. Returns a dict: {"result": value}
    """
    if operation == "add":
        return {"result": a + b}
    if operation == "multiply":
        return {"result": a * b}
    raise ValueError(f"invalid operation: {operation}. expected 'add' or 'multiply'")


if __name__ == "__main__":
    import logging

    logging.getLogger("mcp").setLevel(logging.WARNING)
    mcp.run(transport="stdio")
