"""MCP↔LLM Bridge Client

A reusable client that discovers MCP tools, converts them to OpenAI tool specs,
orchestrates LLM tool calls, and executes them against MCP servers.

This module is designed to work with any MCP server without modification.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from mcp import ClientSession

from mcp_llm_server import chat_completion


@dataclass
class ToolCall:
    """Represents a single tool call from the LLM."""

    id: Optional[str]
    name: str
    args: Dict[str, Any]


@dataclass
class BridgeConfig:
    """Configuration for the MCP↔LLM bridge."""

    system_prompt: str = (
        "You can call tools when needed. Use them to compute results before replying.\n"
        "Tools are provided by an MCP server and may vary."
    )
    max_rounds: int = 5  # Max tool call rounds to prevent infinite loops
    verbose: bool = True


class MCPLLMBridge:
    """Bridge between MCP servers and OpenAI-compatible LLMs.

    This class handles:
    - Dynamic tool discovery from MCP servers
    - Conversion of MCP tool schemas to OpenAI format
    - Tool call extraction from LLM responses
    - Tool execution via MCP
    - Multi-round orchestration
    """

    def __init__(self, session: ClientSession, config: Optional[BridgeConfig] = None):
        """Initialize the bridge with an active MCP session.

        Args:
            session: Active MCP ClientSession
            config: Optional configuration (uses defaults if not provided)
        """
        self.session = session
        self.config = config or BridgeConfig()
        self._tools_cache: Optional[List[Dict[str, Any]]] = None

    async def discover_tools(self, force_refresh: bool = False) -> List[Dict[str, Any]]:
        """Query MCP server for available tools and convert to OpenAI format.

        Args:
            force_refresh: If True, bypass cache and re-query the server

        Returns:
            List of OpenAI-compatible tool specifications
        """
        if self._tools_cache is not None and not force_refresh:
            return self._tools_cache

        tools_spec: List[Dict[str, Any]] = []

        # Ask the MCP server for its tool list
        resp = await self.session.list_tools()
        mcp_tools = getattr(resp, "tools", []) or []

        if self.config.verbose:
            print(f"Discovered {len(mcp_tools)} MCP tools:")
            for t in mcp_tools:
                print(f"  - {getattr(t, 'name', 'Unknown')}")

        for t in mcp_tools:
            name = getattr(t, "name", None)
            description = getattr(t, "description", None)
            # MCP servers expose JSON Schema under `inputSchema`
            schema = getattr(t, "inputSchema", None) or {
                "type": "object",
                "properties": {},
            }

            # Normalize schema if type is missing
            if isinstance(schema, dict) and "type" not in schema:
                schema = {"type": "object", **schema}

            if not name:
                continue

            tools_spec.append(
                {
                    "type": "function",
                    "function": {
                        "name": name,
                        "description": description or "",
                        "parameters": schema,
                    },
                }
            )

        self._tools_cache = tools_spec
        return tools_spec

    def extract_tool_calls(self, full_response: Dict[str, Any]) -> List[ToolCall]:
        """Extract OpenAI-style tool_calls from LLM response.

        Args:
            full_response: Raw response from chat_completion with return_raw=True

        Returns:
            List of ToolCall objects
        """
        calls: List[ToolCall] = []
        try:
            msg = full_response.get("choices", [{}])[0].get("message", {})
            tcs = msg.get("tool_calls") or []
            for tc in tcs:
                fn = tc.get("function", {})
                name = fn.get("name")
                raw_args = fn.get("arguments")
                args: Dict[str, Any] = {}
                if isinstance(raw_args, str):
                    try:
                        args = json.loads(raw_args)
                    except json.JSONDecodeError:
                        args = {}
                if name:
                    calls.append(ToolCall(id=tc.get("id"), name=name, args=args))
        except Exception:
            pass
        return calls

    async def execute_tool(self, name: str, args: Dict[str, Any]) -> Tuple[bool, str]:
        """Execute a tool via MCP.

        Args:
            name: Tool name
            args: Tool arguments

        Returns:
            Tuple of (success: bool, result: str)
        """
        try:
            result = await self.session.call_tool(name, args)
            if getattr(result, "isError", False):
                # Surface MCP error text
                if getattr(result, "content", None):
                    text = getattr(result.content[0], "text", "MCP error")
                else:
                    text = "MCP error"
                return False, text
            # Successful content
            if getattr(result, "content", None):
                text = getattr(result.content[0], "text", "")
                return True, text
            return True, ""
        except Exception as e:  # noqa: BLE001
            return False, f"Exception while calling MCP tool '{name}': {e}"

    async def run_conversation(
        self,
        user_prompt: str,
        system_prompt: Optional[str] = None,
        use_tools: bool = True,
    ) -> Dict[str, Any]:
        """Run a complete conversation with tool calling support.

        Args:
            user_prompt: The user's message
            system_prompt: Optional system prompt (uses config default if not provided)
            use_tools: Whether to enable tool calling

        Returns:
            Dictionary with:
                - final_response: str (assistant's final answer)
                - messages: List[Dict] (full conversation history)
                - tool_calls_made: int (number of tool calls executed)
                - rounds: int (number of LLM calls made)
        """
        messages: List[Dict[str, str]] = []

        # Add system prompt
        sys_prompt = system_prompt or self.config.system_prompt
        messages.append({"role": "system", "content": sys_prompt})

        # Add user prompt
        messages.append({"role": "user", "content": user_prompt})

        tool_calls_made = 0
        rounds = 0

        for round_num in range(self.config.max_rounds):
            rounds += 1

            if use_tools and round_num == 0:
                # First round: request with tools
                tools = await self.discover_tools()
                if self.config.verbose:
                    print(f"\n[Round {round_num + 1}] Requesting LLM with tools...")
                full_response = chat_completion(messages, tools=tools, return_raw=True)
            else:
                # Subsequent rounds or no-tools mode
                if self.config.verbose:
                    print(f"\n[Round {round_num + 1}] Requesting LLM...")
                full_response = chat_completion(messages, return_raw=True)

            # Extract tool calls
            tool_calls = self.extract_tool_calls(full_response)

            if not tool_calls:
                # No tool calls - get final response
                assistant_message = full_response.get("choices", [{}])[0].get(
                    "message", {}
                )
                content = assistant_message.get("content") or ""
                if content:
                    messages.append({"role": "assistant", "content": content})
                return {
                    "final_response": content,
                    "messages": messages,
                    "tool_calls_made": tool_calls_made,
                    "rounds": rounds,
                }

            # Execute tool calls
            for tc in tool_calls:
                tool_calls_made += 1
                ok, output = await self.execute_tool(tc.name, tc.args)
                prefix = "TOOL RESULT" if ok else "TOOL ERROR"
                if self.config.verbose:
                    print(f"{prefix} ({tc.name}): {output}")
                # Append tool result to conversation
                messages.append(
                    {
                        "role": "assistant",
                        "content": f"{prefix} ({tc.name}): {output}",
                    }
                )

        # Max rounds reached
        if self.config.verbose:
            print(f"\nWarning: Max rounds ({self.config.max_rounds}) reached")

        return {
            "final_response": "Max conversation rounds reached without completion",
            "messages": messages,
            "tool_calls_made": tool_calls_made,
            "rounds": rounds,
        }
