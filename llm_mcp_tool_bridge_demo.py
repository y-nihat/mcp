"""MCP↔LLM Tool-Call Bridge Demo

Purpose:
    Demonstrate introducing MCP tools to a local OpenAI-compatible LLM via
    the standard tools=[] parameter. The LLM emits tool_calls, which we route
    to an MCP server (stdio) and feed results back to the LLM.

    This is now a simple wrapper around the mcp_llm_bridge_client module.
    For new test cases, see test_llm_mcp_bridge_scenarios.py

Requirements:
    - Local LLM server at http://localhost:1234 (OpenAI-compatible)
    - This repo's math MCP server (mcp_math_server.py)
    - dependencies from requirements.txt installed

Usage:
    python llm_mcp_tool_bridge_demo.py            # live roundtrip (needs LLM)
    python llm_mcp_tool_bridge_demo.py --stub     # stubbed tool_calls (deprecated)

Note:
    The --stub mode is deprecated. Use test_llm_mcp_bridge_scenarios.py for testing.
"""

from __future__ import annotations

import asyncio
import json
import sys
from typing import List

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from mcp_llm_bridge_client import MCPLLMBridge, BridgeConfig


async def run_bridge(use_stub: bool = False) -> int:
    """Run the bridge demo (backward compatible with original interface)."""

    if use_stub:
        print("Warning: --stub mode is deprecated. Using live mode instead.")
        print("For test scenarios, use: python test_llm_mcp_bridge_scenarios.py")
        print()

    # Start MCP math server over stdio
    server_params = StdioServerParameters(
        command="python", args=["mcp_math_server.py"], env=None
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("✓ Connected to Math MCP Server")

            # Create bridge with default config
            bridge = MCPLLMBridge(session, config=BridgeConfig())

            # Run conversation
            result = await bridge.run_conversation(
                user_prompt="Compute (3 + 5) * 4 using available tools and explain briefly.",
            )

            print("\n" + "=" * 70)
            print("FINAL RESPONSE:")
            print(result["final_response"])
            print("=" * 70)
            print(
                f"Stats: {result['tool_calls_made']} tool calls, {result['rounds']} rounds"
            )

    return 0


def main(argv: List[str]) -> int:
    use_stub = "--stub" in argv
    return asyncio.run(run_bridge(use_stub=use_stub))


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
