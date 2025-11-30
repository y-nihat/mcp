"""Dynamic Tool Registry for MCP Servers

Provides a generic base class and helper that ANY MCP server can use to enable
dynamic tool awareness. The registry tracks tool state (enabled/disabled) and
version changes, allowing the LLM to discover tool updates without restarting.

Key Features:
- Tool enable/disable at runtime
- Automatic version tracking (changes trigger re-discovery)
- Thread-safe operations
- Compatible with FastMCP servers
- No server restart required

Usage:
    registry = DynamicToolRegistry()

    # Register tools
    registry.register_tool("add", enabled=True)
    registry.register_tool("multiply", enabled=True)

    # Disable a tool dynamically
    registry.disable_tool("multiply")

    # Check tool status
    if registry.is_tool_enabled("add"):
        # Execute tool logic
        pass

    # Get current version for cache invalidation
    version = registry.get_version()
"""

from __future__ import annotations

import threading
from dataclasses import dataclass, field
from typing import Dict, Set, Optional
from datetime import datetime, timezone


@dataclass
class ToolMetadata:
    """Metadata for a registered tool."""

    name: str
    enabled: bool
    registered_at: str
    last_modified: str
    metadata: Dict[str, any] = field(default_factory=dict)


class DynamicToolRegistry:
    """Registry for managing dynamic tool state in MCP servers.

    This registry allows MCP servers to:
    - Enable/disable tools at runtime
    - Track tool state changes
    - Provide version tracking for cache invalidation
    - Support thread-safe operations

    The registry maintains a version counter that increments whenever tool
    state changes, allowing clients to detect when to refresh their tool cache.
    """

    def __init__(self) -> None:
        """Initialize the dynamic tool registry."""
        self._tools: Dict[str, ToolMetadata] = {}
        self._version: int = 0
        self._lock = threading.RLock()

    def _now(self) -> str:
        """Get current UTC timestamp."""
        return datetime.now(timezone.utc).isoformat()

    def _increment_version(self) -> None:
        """Increment version counter (call under lock)."""
        self._version += 1

    def register_tool(
        self, name: str, enabled: bool = True, metadata: Optional[Dict[str, any]] = None
    ) -> None:
        """Register a new tool or update existing tool registration.

        Args:
            name: Tool name (must be unique)
            enabled: Whether tool is initially enabled
            metadata: Optional metadata dict for tool

        Raises:
            ValueError: If name is empty
        """
        if not name or not isinstance(name, str):
            raise ValueError("Tool name must be a non-empty string")

        with self._lock:
            now = self._now()
            if name in self._tools:
                # Update existing tool
                tool = self._tools[name]
                tool.last_modified = now
                if enabled != tool.enabled:
                    tool.enabled = enabled
                    self._increment_version()
                if metadata:
                    tool.metadata.update(metadata)
            else:
                # Register new tool
                self._tools[name] = ToolMetadata(
                    name=name,
                    enabled=enabled,
                    registered_at=now,
                    last_modified=now,
                    metadata=metadata or {},
                )
                self._increment_version()

    def enable_tool(self, name: str) -> bool:
        """Enable a registered tool.

        Args:
            name: Tool name

        Returns:
            True if state changed, False if already enabled or not found

        Raises:
            ValueError: If tool not registered
        """
        with self._lock:
            if name not in self._tools:
                raise ValueError(f"Tool '{name}' not registered")

            tool = self._tools[name]
            if not tool.enabled:
                tool.enabled = True
                tool.last_modified = self._now()
                self._increment_version()
                return True
            return False

    def disable_tool(self, name: str) -> bool:
        """Disable a registered tool.

        Args:
            name: Tool name

        Returns:
            True if state changed, False if already disabled or not found

        Raises:
            ValueError: If tool not registered
        """
        with self._lock:
            if name not in self._tools:
                raise ValueError(f"Tool '{name}' not registered")

            tool = self._tools[name]
            if tool.enabled:
                tool.enabled = False
                tool.last_modified = self._now()
                self._increment_version()
                return True
            return False

    def is_tool_enabled(self, name: str) -> bool:
        """Check if a tool is enabled.

        Args:
            name: Tool name

        Returns:
            True if tool is registered and enabled, False otherwise
        """
        with self._lock:
            tool = self._tools.get(name)
            return tool.enabled if tool else False

    def get_enabled_tools(self) -> Set[str]:
        """Get set of all enabled tool names.

        Returns:
            Set of enabled tool names
        """
        with self._lock:
            return {name for name, tool in self._tools.items() if tool.enabled}

    def get_all_tools(self) -> Dict[str, ToolMetadata]:
        """Get all registered tools with their metadata.

        Returns:
            Dictionary mapping tool names to their metadata
        """
        with self._lock:
            return dict(self._tools)

    def get_version(self) -> int:
        """Get current registry version.

        The version increments whenever tool state changes (enable/disable/register).
        Clients can use this for cache invalidation.

        Returns:
            Current version number
        """
        with self._lock:
            return self._version

    def get_tool_metadata(self, name: str) -> Optional[ToolMetadata]:
        """Get metadata for a specific tool.

        Args:
            name: Tool name

        Returns:
            ToolMetadata if found, None otherwise
        """
        with self._lock:
            return self._tools.get(name)

    def unregister_tool(self, name: str) -> bool:
        """Unregister a tool completely.

        Args:
            name: Tool name

        Returns:
            True if tool was removed, False if not found
        """
        with self._lock:
            if name in self._tools:
                del self._tools[name]
                self._increment_version()
                return True
            return False

    def clear(self) -> None:
        """Clear all registered tools and reset version."""
        with self._lock:
            self._tools.clear()
            self._version = 0

    def get_stats(self) -> Dict[str, any]:
        """Get registry statistics.

        Returns:
            Dictionary with registry stats (total, enabled, disabled, version)
        """
        with self._lock:
            enabled_count = sum(1 for t in self._tools.values() if t.enabled)
            return {
                "total_tools": len(self._tools),
                "enabled_tools": enabled_count,
                "disabled_tools": len(self._tools) - enabled_count,
                "version": self._version,
            }


# Global registry instance for FastMCP servers
_global_registry: Optional[DynamicToolRegistry] = None


def get_global_registry() -> DynamicToolRegistry:
    """Get or create the global tool registry instance.

    Returns:
        Global DynamicToolRegistry instance
    """
    global _global_registry
    if _global_registry is None:
        _global_registry = DynamicToolRegistry()
    return _global_registry


def reset_global_registry() -> None:
    """Reset the global registry (useful for testing)."""
    global _global_registry
    if _global_registry is not None:
        _global_registry.clear()
    _global_registry = None


__all__ = [
    "DynamicToolRegistry",
    "ToolMetadata",
    "get_global_registry",
    "reset_global_registry",
]
