"""In-memory To-Do List MCP Server

Phase 1: Implements only the Create capability via a tool.
Subsequent phases will add read/list/update/delete resource handlers.
"""

from __future__ import annotations

from typing import Dict, Any
from mcp.server.fastmcp import FastMCP
import os
from mcp_bridge.storage.store import get_store

# FastMCP server instance
mcp = FastMCP("todo-server")

store = get_store()


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
    """
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
    """
    if not isinstance(item_id, int):
        raise ValueError("item_id must be an integer")
    if title is None and completed is None:
        raise ValueError("provide at least one field to update: title or completed")

    return store.update(item_id, title=title, completed=completed)


@mcp.tool()
def delete_todo(item_id: int) -> dict[str, Any]:
    """Delete a to-do item and return the removed item."""
    if not isinstance(item_id, int):
        raise ValueError("item_id must be an integer")
    return store.delete(item_id)


if __name__ == "__main__":
    import logging

    logging.getLogger("mcp").setLevel(logging.WARNING)
    mcp.run(transport="stdio")
