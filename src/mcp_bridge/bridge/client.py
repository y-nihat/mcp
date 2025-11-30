"""MCP↔LLM Bridge Client

Reusable client that discovers MCP tools, converts them to OpenAI tool specs,
orchestrates LLM tool calls, and executes them against MCP servers.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from mcp import ClientSession

from mcp_bridge.llm.openai_client import chat_completion


@dataclass
class ToolCall:
    id: Optional[str]
    name: str
    args: Dict[str, Any]


@dataclass
class BridgeConfig:
    system_prompt: str = (
        "You can call tools when needed. Use them to compute results before replying.\n"
        "Tools are provided by an MCP server and may vary."
    )
    max_rounds: int = 5
    verbose: bool = True
    enable_dynamic_tools: bool = True  # Auto-detect tool changes without restart


class MCPLLMBridge:
    def __init__(self, session: ClientSession, config: Optional[BridgeConfig] = None):
        self.session = session
        self.config = config or BridgeConfig()
        self._tools_cache: Optional[List[Dict[str, Any]]] = None
        self._last_tool_count: int = 0  # Track tool count for change detection

    async def discover_tools(self, force_refresh: bool = False) -> List[Dict[str, Any]]:
        """Discover available MCP tools.

        Args:
            force_refresh: Force cache refresh even if cache exists

        Returns:
            List of tool specifications in OpenAI format
        """
        if self._tools_cache is not None and not force_refresh:
            return self._tools_cache

        tools_spec: List[Dict[str, Any]] = []
        resp = await self.session.list_tools()
        mcp_tools = getattr(resp, "tools", []) or []

        if self.config.verbose and (force_refresh or self._tools_cache is None):
            print(f"Discovered {len(mcp_tools)} MCP tools:")
            for t in mcp_tools:
                print(f"  - {getattr(t, 'name', 'Unknown')}")

        for t in mcp_tools:
            name = getattr(t, "name", None)
            description = getattr(t, "description", None)
            schema = getattr(t, "inputSchema", None) or {
                "type": "object",
                "properties": {},
            }
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
        self._last_tool_count = len(tools_spec)
        return tools_spec

    async def check_tool_changes(self) -> bool:
        """Check if tools have changed on the server.

        Returns:
            True if tools have changed and cache should be refreshed
        """
        if not self.config.enable_dynamic_tools:
            return False

        try:
            resp = await self.session.list_tools()
            current_tools = getattr(resp, "tools", []) or []
            current_count = len(current_tools)

            # Check if tool count changed
            if current_count != self._last_tool_count:
                if self.config.verbose:
                    print(
                        f"Tool count changed: {self._last_tool_count} → {current_count}"
                    )
                return True

            # Check if tool names changed (could be same count but different tools)
            if self._tools_cache:
                cached_names = {tool["function"]["name"] for tool in self._tools_cache}
                current_names = {getattr(t, "name", None) for t in current_tools}
                if cached_names != current_names:
                    if self.config.verbose:
                        added = current_names - cached_names
                        removed = cached_names - current_names
                        if added:
                            print(f"Tools added: {added}")
                        if removed:
                            print(f"Tools removed: {removed}")
                    return True

            return False
        except Exception as e:  # noqa: BLE001
            if self.config.verbose:
                print(f"Warning: Tool change detection failed: {e}")
            return False

    def extract_tool_calls(self, full_response: Dict[str, Any]) -> List[ToolCall]:
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
        try:
            result = await self.session.call_tool(name, args)
            if getattr(result, "isError", False):
                if getattr(result, "content", None):
                    text = getattr(result.content[0], "text", "MCP error")
                else:
                    text = "MCP error"
                return False, text
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
        messages: List[Dict[str, str]] = []
        sys_prompt = system_prompt or self.config.system_prompt
        messages.append({"role": "system", "content": sys_prompt})
        messages.append({"role": "user", "content": user_prompt})

        tool_calls_made = 0
        rounds = 0

        for round_num in range(self.config.max_rounds):
            rounds += 1

            # Check for tool changes before each round (dynamic awareness)
            if use_tools and self.config.enable_dynamic_tools and round_num > 0:
                if await self.check_tool_changes():
                    if self.config.verbose:
                        print("\n[Tool changes detected - refreshing cache]")
                    await self.discover_tools(force_refresh=True)

            if use_tools and round_num == 0:
                tools = await self.discover_tools()
                if self.config.verbose:
                    print(f"\n[Round {round_num + 1}] Requesting LLM with tools...")
                full_response = chat_completion(messages, tools=tools, return_raw=True)
            elif use_tools and round_num > 0:
                # Use cached tools (may have been refreshed above)
                tools = await self.discover_tools()
                if self.config.verbose:
                    print(f"\n[Round {round_num + 1}] Requesting LLM with tools...")
                full_response = chat_completion(messages, tools=tools, return_raw=True)
            else:
                if self.config.verbose:
                    print(f"\n[Round {round_num + 1}] Requesting LLM...")
                full_response = chat_completion(messages, return_raw=True)

            tool_calls = self.extract_tool_calls(full_response)
            if not tool_calls:
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

            for tc in tool_calls:
                tool_calls_made += 1
                ok, output = await self.execute_tool(tc.name, tc.args)
                prefix = "TOOL RESULT" if ok else "TOOL ERROR"
                if self.config.verbose:
                    print(f"{prefix} ({tc.name}): {output}")
                messages.append(
                    {
                        "role": "assistant",
                        "content": f"{prefix} ({tc.name}): {output}",
                    }
                )

        if self.config.verbose:
            print(f"\nWarning: Max rounds ({self.config.max_rounds}) reached")

        return {
            "final_response": "Max conversation rounds reached without completion",
            "messages": messages,
            "tool_calls_made": tool_calls_made,
            "rounds": rounds,
        }


__all__ = ["MCPLLMBridge", "BridgeConfig", "ToolCall"]
