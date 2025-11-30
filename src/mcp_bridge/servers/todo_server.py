"""In-memory To-Do List MCP Server

Phase 1: Implements only the Create capability via a tool.
Subsequent phases will add read/list/update/delete resource handlers.
"""

from __future__ import annotations

from typing import Dict, Any
from mcp.server.fastmcp import FastMCP
import os
from mcp_bridge.storage.store import get_store
from mcp_bridge.servers.dynamic_registry import get_global_registry

# FastMCP server instance
mcp = FastMCP("todo-server")

store = get_store()

# Get dynamic tool registry
registry = get_global_registry()

# Register all todo tools
registry.register_tool("create_todo", enabled=True)
registry.register_tool("update_todo", enabled=True)
registry.register_tool("delete_todo", enabled=True)


@mcp.resource(
    "resource://todos",
    name="todos",
    title="All To-Dos",
    description="List all to-do items",
)
def list_todos() -> dict[str, Any]:
    """Resource handler returning all todos.

    Returns:
        A dictionary mapping id -> todo dict.
    """
    return store.list_all()


@mcp.resource(
    "resource://todos/{item_id}",
    name="todo-item",
    title="Get To-Do Item",
    description="Return a specific to-do by id",
)
def get_todo(item_id: str) -> dict[str, Any]:
    """Return a single to-do item by id.

    Raises ValueError if the id is invalid or does not exist.
    """
    try:
        tid = int(item_id)
    except Exception:
        raise ValueError(f"invalid item_id: {item_id}")

    item = store.get(tid)
    if item is None:
        raise ValueError(f"todo {tid} not found")
    return item


@mcp.tool()
def create_todo(title: str) -> str:
    """Create a new to-do item and return its resource URI.

    Args:
        title: Human readable title of the task. Must be non-empty.

    Returns:
        Resource URI of the created to-do, e.g. resource://todos/1

    Raises:
        ValueError: If title is empty or only whitespace.
        RuntimeError: If tool is disabled.
    """
    if not registry.is_tool_enabled("create_todo"):
        raise RuntimeError("Tool 'create_todo' is currently disabled")

    if not isinstance(title, str):
        raise ValueError("title must be a string")
    todo_id = store.create(title)
    uri = f"resource://todos/{todo_id}"
    return uri


@mcp.tool()
def update_todo(
    item_id: int, title: str | None = None, completed: bool | None = None
) -> dict[str, Any]:
    """Update fields of a to-do item and return the updated item.

    Args:
        item_id: ID of the to-do.
        title: Optional new title.
        completed: Optional new completed flag.

    Raises:
        RuntimeError: If tool is disabled.
    """
    if not registry.is_tool_enabled("update_todo"):
        raise RuntimeError("Tool 'update_todo' is currently disabled")

    if not isinstance(item_id, int):
        raise ValueError("item_id must be an integer")
    if title is None and completed is None:
        raise ValueError("provide at least one field to update: title or completed")

    return store.update(item_id, title=title, completed=completed)


@mcp.tool()
def delete_todo(item_id: int) -> dict[str, Any]:
    """Delete a to-do item and return the removed item.

    Raises:
        RuntimeError: If tool is disabled.
    """
    if not registry.is_tool_enabled("delete_todo"):
        raise RuntimeError("Tool 'delete_todo' is currently disabled")

    if not isinstance(item_id, int):
        raise ValueError("item_id must be an integer")
    return store.delete(item_id)


@mcp.tool()
def set_todo_tool_enabled(tool_name: str, enabled: bool) -> str:
    """
    Enable or disable a todo tool dynamically without restart.

    Args:
        tool_name: Name of the tool ('create_todo', 'update_todo', or 'delete_todo')
        enabled: True to enable, False to disable

    Returns:
        Status message

    Raises:
        ValueError: If tool_name is invalid
    """
    valid_tools = {"create_todo", "update_todo", "delete_todo"}
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
def get_todo_tool_status() -> dict:
    """
    Get the current status of all registered todo tools.

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

    logging.getLogger("mcp").setLevel(logging.WARNING)
    mcp.run(transport="stdio")
