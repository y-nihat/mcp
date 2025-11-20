from mcp.server.fastmcp import FastMCP

# Create FastMCP server instance
mcp = FastMCP("level1-server")


@mcp.resource(
    "resource://info",
    name="info",
    title="Static info",
    description="A static informational resource",
)
def info() -> str:
    """Return a static informational string for Level 1."""
    return "This is a static resource from my MCP server."


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
