from mcp.server.fastmcp import FastMCP

# Create FastMCP server instance
mcp = FastMCP("level0-server")


@mcp.resource(
    "resource://health",
    name="health",
    title="Health",
    description="A static health resource",
)
def health() -> str:
    """Return a static health string for Level 0."""
    return "This is a static health resource from my MCP server."


if __name__ == "__main__":
    import logging

    # Suppress verbose INFO logs from FastMCP server in examples/tests
    logging.getLogger("mcp").setLevel(logging.WARNING)
    # Run the server over stdio transport
    mcp.run(transport="stdio")
