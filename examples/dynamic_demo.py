"""Dynamic Tool Awareness Demo

This demo showcases the new dynamic tool awareness capability where:
1. Tools can be enabled/disabled at runtime
2. The LLM automatically detects tool changes without restart
3. The bridge client refreshes its tool cache dynamically

This solves the original problem where adding/modifying/disabling tools
required a full restart of both client and server.

Usage:
    python dynamic_demo.py
"""

from __future__ import annotations

import asyncio
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import os

from mcp_bridge.bridge.client import MCPLLMBridge, BridgeConfig


async def run_dynamic_demo() -> int:
    """
    Demonstrate dynamic tool awareness by:
    1. Starting with all tools enabled
    2. Performing calculations
    3. Dynamically disabling a tool
    4. Showing the LLM adapts without restart
    5. Re-enabling the tool
    6. Performing calculations again
    """

    print("\n" + "=" * 70)
    print("DYNAMIC TOOL AWARENESS DEMO")
    print("=" * 70)
    print("\nThis demo shows how tools can be enabled/disabled at runtime")
    print("without needing to restart the client or server.\n")

    # Start MCP math server
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "mcp_bridge.servers.math_server"],
        env=os.environ.copy(),
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("✓ Connected to Math MCP Server\n")

            # Create bridge with dynamic tools enabled (default)
            config = BridgeConfig(
                verbose=True,
                enable_dynamic_tools=True,  # This is the key feature!
                max_rounds=5,
            )
            bridge = MCPLLMBridge(session, config=config)

            # Scenario 1: Normal operation with all tools enabled
            print("\n" + "=" * 70)
            print("SCENARIO 1: All tools enabled")
            print("=" * 70)

            result1 = await bridge.run_conversation(
                user_prompt="Calculate (10 + 20) * 3 using available tools.",
            )

            print("\n" + "-" * 70)
            print("RESULT:")
            print(result1["final_response"])
            print("-" * 70)
            print(
                f"Stats: {result1['tool_calls_made']} tool calls, {result1['rounds']} rounds\n"
            )

            # Scenario 2: Disable multiply tool dynamically
            print("\n" + "=" * 70)
            print("SCENARIO 2: Disabling 'multiply' tool dynamically")
            print("=" * 70)
            print("\nNow we'll disable the 'multiply' tool WITHOUT restarting...")
            print("The bridge will automatically detect this change.\n")

            # Disable multiply using the management tool
            disable_result = await session.call_tool(
                "set_tool_enabled", {"tool_name": "multiply", "enabled": False}
            )
            print(f"✓ {disable_result.content[0].text}\n")

            # Try to use multiply - should fail or adapt
            result2 = await bridge.run_conversation(
                user_prompt="Try to multiply 5 * 6. What happens?",
            )

            print("\n" + "-" * 70)
            print("RESULT:")
            print(result2["final_response"])
            print("-" * 70)
            print(
                f"Stats: {result2['tool_calls_made']} tool calls, {result2['rounds']} rounds\n"
            )

            # Scenario 3: Re-enable multiply tool
            print("\n" + "=" * 70)
            print("SCENARIO 3: Re-enabling 'multiply' tool dynamically")
            print("=" * 70)
            print("\nNow we'll re-enable the 'multiply' tool WITHOUT restarting...")
            print("Again, the bridge will detect this change automatically.\n")

            # Re-enable multiply
            enable_result = await session.call_tool(
                "set_tool_enabled", {"tool_name": "multiply", "enabled": True}
            )
            print(f"✓ {enable_result.content[0].text}\n")

            # Use multiply again - should work
            result3 = await bridge.run_conversation(
                user_prompt="Now calculate 7 * 8 using tools.",
            )

            print("\n" + "-" * 70)
            print("RESULT:")
            print(result3["final_response"])
            print("-" * 70)
            print(
                f"Stats: {result3['tool_calls_made']} tool calls, {result3['rounds']} rounds\n"
            )

            # Final status check
            print("\n" + "=" * 70)
            print("FINAL TOOL STATUS")
            print("=" * 70)
            status_result = await session.call_tool("get_tool_status", {})
            print(f"\n{status_result.content[0].text}\n")

    print("=" * 70)
    print("DEMO COMPLETE!")
    print("=" * 70)
    print("\nKey Takeaway:")
    print("• Tools were enabled/disabled WITHOUT restarting client or server")
    print("• The bridge automatically detected changes and refreshed its cache")
    print("• This enables true dynamic tool management in MCP servers")
    print("=" * 70 + "\n")

    return 0


async def run_simple_demo() -> int:
    """Simple demo showing basic dynamic tool awareness without LLM."""

    print("\n" + "=" * 70)
    print("SIMPLE DYNAMIC TOOL DEMO (No LLM required)")
    print("=" * 70)
    print("\nThis shows tool enable/disable without needing an LLM server.\n")

    server_params = StdioServerParameters(
        command="python",
        args=["-m", "mcp_bridge.servers.math_server"],
        env=os.environ.copy(),
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("✓ Connected to Math MCP Server\n")

            # Check initial tools
            print("-" * 70)
            print("Initial tool list:")
            tools = await session.list_tools()
            for t in tools.tools:
                print(f"  • {t.name}")
            print("-" * 70 + "\n")

            # Test add (should work)
            print("Testing 'add' tool: 10 + 20")
            result = await session.call_tool("add", {"numbers": [10, 20]})
            print(f"Result: {result.content[0].text}\n")

            # Disable multiply
            print("-" * 70)
            print("Disabling 'multiply' tool...")
            disable = await session.call_tool(
                "set_tool_enabled", {"tool_name": "multiply", "enabled": False}
            )
            print(f"✓ {disable.content[0].text}\n")

            # Try multiply (should fail)
            print("Testing 'multiply' tool: 5 * 6")
            result = await session.call_tool("multiply", {"numbers": [5, 6]})
            if result.isError:
                print(f"✓ Expected error: {result.content[0].text}\n")
            else:
                print(f"✗ Unexpected success: {result.content[0].text}\n")

            # Re-enable multiply
            print("-" * 70)
            print("Re-enabling 'multiply' tool...")
            enable = await session.call_tool(
                "set_tool_enabled", {"tool_name": "multiply", "enabled": True}
            )
            print(f"✓ {enable.content[0].text}\n")

            # Try multiply again (should work)
            print("Testing 'multiply' tool again: 7 * 8")
            result = await session.call_tool("multiply", {"numbers": [7, 8]})
            print(f"Result: {result.content[0].text}\n")

    print("=" * 70)
    print("SIMPLE DEMO COMPLETE!")
    print("=" * 70 + "\n")
    return 0


def main(argv: list[str]) -> int:
    if "--simple" in argv:
        return asyncio.run(run_simple_demo())
    else:
        print("\n⚠️  NOTE: This demo requires an LLM server at http://localhost:1234")
        print("    Use --simple flag to run without LLM\n")
        try:
            return asyncio.run(run_dynamic_demo())
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("\nTip: Use '--simple' flag to run demo without LLM:")
            print("     python dynamic_demo.py --simple\n")
            return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
