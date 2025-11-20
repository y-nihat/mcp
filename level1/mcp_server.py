from mcp.server.fastmcp import FastMCP

# Create FastMCP server instance
mcp = FastMCP("level1-server")


@mcp.resource(
    "resource://health",
    name="health",
    title="Health",
    description="Server health status",
)
def health() -> str:
    """Return a short health status string for Level 1."""
    return "ok"


@mcp.tool()
def greet(name: str) -> str:
    """Return a greeting message for the provided name."""
    if not isinstance(name, str):
        raise ValueError("name must be a string")
    return f"Hello, {name}! Welcome to MCP."


if __name__ == "__main__":
    import logging

    # Suppress verbose INFO logs from FastMCP server in examples/tests
    logging.getLogger("mcp").setLevel(logging.WARNING)
    # Run the server over stdio transport
    mcp.run(transport="stdio")
