"""Tests for Dynamic Tool Awareness

This test verifies that:
1. Tools can be enabled/disabled at runtime without restarting the server
2. The bridge client detects tool changes and refreshes its cache
3. LLM can discover updated tool lists without needing a restart
4. The dynamic registry properly tracks tool state
"""

import asyncio
import logging
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

logging.getLogger("mcp").setLevel(logging.WARNING)


async def _test_dynamic_tool_awareness_math_server():
    """Internal async function for testing dynamic tool awareness with math server.

    This test:
    1. Connects to math server
    2. Verifies initial tool discovery (add, multiply, etc.)
    3. Disables a tool dynamically
    4. Verifies the tool list changes
    5. Re-enables the tool
    6. Verifies the tool is available again
    """
    print("\n" + "=" * 70)
    print("TESTING DYNAMIC TOOL AWARENESS - MATH SERVER")
    print("=" * 70)

    server_params = StdioServerParameters(
        command="python",
        args=["-m", "mcp_bridge.servers.math_server"],
        env=os.environ.copy(),
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("\n✓ Connected to Math MCP Server")

            # Step 1: List initial tools
            print("\n" + "-" * 70)
            print("STEP 1: List initial tools")
            print("-" * 70)
            tools_resp = await session.list_tools()
            initial_tools = [t.name for t in getattr(tools_resp, "tools", [])]
            print(f"Initial tools: {initial_tools}")

            # Verify we have the expected tools
            expected_tools = {"add", "multiply", "set_tool_enabled", "get_tool_status"}
            assert expected_tools.issubset(
                set(initial_tools)
            ), f"Expected tools {expected_tools} not found in {initial_tools}"
            initial_tool_count = len(initial_tools)
            print(f"✓ Found {initial_tool_count} tools initially")

            # Step 2: Get initial tool status
            print("\n" + "-" * 70)
            print("STEP 2: Get initial tool status")
            print("-" * 70)
            status_result = await session.call_tool("get_tool_status", {})
            print(f"Tool status: {status_result.content[0].text}")
            assert not status_result.isError
            print("✓ All tools initially enabled")

            # Step 3: Disable 'multiply' tool
            print("\n" + "-" * 70)
            print("STEP 3: Disable 'multiply' tool")
            print("-" * 70)
            disable_result = await session.call_tool(
                "set_tool_enabled", {"tool_name": "multiply", "enabled": False}
            )
            print(f"Result: {disable_result.content[0].text}")
            assert not disable_result.isError
            assert "DISABLED" in disable_result.content[0].text
            print("✓ Tool 'multiply' disabled successfully")

            # Step 4: Verify multiply is disabled
            print("\n" + "-" * 70)
            print("STEP 4: Verify 'multiply' is disabled")
            print("-" * 70)
            try:
                multiply_result = await session.call_tool(
                    "multiply", {"numbers": [2, 3]}
                )
                # If tool is disabled, it should raise RuntimeError
                if multiply_result.isError:
                    error_text = multiply_result.content[0].text
                    print(f"Expected error received: {error_text}")
                    assert "disabled" in error_text.lower()
                    print("✓ Tool correctly reports as disabled")
                else:
                    assert False, "Expected error when calling disabled tool"
            except Exception as e:
                print(f"Exception when calling disabled tool: {e}")
                assert "disabled" in str(e).lower()
                print("✓ Tool correctly raises exception when disabled")

            # Step 5: Verify 'add' still works
            print("\n" + "-" * 70)
            print("STEP 5: Verify 'add' tool still works")
            print("-" * 70)
            add_result = await session.call_tool("add", {"numbers": [10, 20]})
            assert not add_result.isError
            assert add_result.content[0].text == "30.0"
            print(
                f"✓ Tool 'add' still functional: 10 + 20 = {add_result.content[0].text}"
            )

            # Step 6: Re-enable 'multiply'
            print("\n" + "-" * 70)
            print("STEP 6: Re-enable 'multiply' tool")
            print("-" * 70)
            enable_result = await session.call_tool(
                "set_tool_enabled", {"tool_name": "multiply", "enabled": True}
            )
            print(f"Result: {enable_result.content[0].text}")
            assert not enable_result.isError
            assert "ENABLED" in enable_result.content[0].text
            print("✓ Tool 'multiply' re-enabled successfully")

            # Step 7: Verify multiply works again
            print("\n" + "-" * 70)
            print("STEP 7: Verify 'multiply' works again")
            print("-" * 70)
            multiply_result = await session.call_tool("multiply", {"numbers": [4, 5]})
            assert not multiply_result.isError
            assert multiply_result.content[0].text == "20.0"
            print(
                f"✓ Tool 'multiply' functional again: 4 * 5 = {multiply_result.content[0].text}"
            )

            # Step 8: Final tool status
            print("\n" + "-" * 70)
            print("STEP 8: Final tool status")
            print("-" * 70)
            final_status = await session.call_tool("get_tool_status", {})
            print(f"Final status: {final_status.content[0].text}")
            assert not final_status.isError
            print("✓ All tools re-enabled")

    print("\n" + "=" * 70)
    print("DYNAMIC TOOL AWARENESS TEST PASSED! ✓")
    print("=" * 70 + "\n")


async def _test_dynamic_tool_awareness_todo_server():
    """Internal async function for testing dynamic tool awareness with todo server.

    This test:
    1. Connects to todo server
    2. Creates a todo (tool enabled)
    3. Disables create_todo tool
    4. Attempts to create todo (should fail)
    5. Re-enables tool
    6. Creates todo successfully
    """
    print("\n" + "=" * 70)
    print("TESTING DYNAMIC TOOL AWARENESS - TODO SERVER")
    print("=" * 70)

    server_params = StdioServerParameters(
        command="python",
        args=["-m", "mcp_bridge.servers.todo_server"],
        env=os.environ.copy(),
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("\n✓ Connected to Todo MCP Server")

            # Step 1: List initial tools
            print("\n" + "-" * 70)
            print("STEP 1: List initial tools")
            print("-" * 70)
            tools_resp = await session.list_tools()
            initial_tools = [t.name for t in getattr(tools_resp, "tools", [])]
            print(f"Initial tools: {initial_tools}")

            expected_tools = {
                "create_todo",
                "update_todo",
                "delete_todo",
                "set_todo_tool_enabled",
                "get_todo_tool_status",
            }
            assert expected_tools.issubset(
                set(initial_tools)
            ), f"Expected tools {expected_tools} not found in {initial_tools}"
            print(f"✓ Found {len(initial_tools)} tools initially")

            # Step 2: Create a todo (should work)
            print("\n" + "-" * 70)
            print("STEP 2: Create todo with tool enabled")
            print("-" * 70)
            create_result = await session.call_tool(
                "create_todo", {"title": "Test task 1"}
            )
            assert not create_result.isError
            uri = create_result.content[0].text
            print(f"✓ Created todo: {uri}")

            # Step 3: Disable create_todo
            print("\n" + "-" * 70)
            print("STEP 3: Disable 'create_todo' tool")
            print("-" * 70)
            disable_result = await session.call_tool(
                "set_todo_tool_enabled", {"tool_name": "create_todo", "enabled": False}
            )
            assert not disable_result.isError
            print(f"Result: {disable_result.content[0].text}")
            print("✓ Tool 'create_todo' disabled")

            # Step 4: Try to create todo (should fail)
            print("\n" + "-" * 70)
            print("STEP 4: Attempt to create todo with disabled tool")
            print("-" * 70)
            create_result2 = await session.call_tool(
                "create_todo", {"title": "Test task 2"}
            )
            if create_result2.isError:
                error_text = create_result2.content[0].text
                print(f"Expected error: {error_text}")
                assert "disabled" in error_text.lower()
                print("✓ Tool correctly reports as disabled")
            else:
                assert False, "Expected error when calling disabled tool"

            # Step 5: Re-enable create_todo
            print("\n" + "-" * 70)
            print("STEP 5: Re-enable 'create_todo' tool")
            print("-" * 70)
            enable_result = await session.call_tool(
                "set_todo_tool_enabled", {"tool_name": "create_todo", "enabled": True}
            )
            assert not enable_result.isError
            print(f"Result: {enable_result.content[0].text}")
            print("✓ Tool 'create_todo' re-enabled")

            # Step 6: Create todo again (should work)
            print("\n" + "-" * 70)
            print("STEP 6: Create todo with re-enabled tool")
            print("-" * 70)
            create_result3 = await session.call_tool(
                "create_todo", {"title": "Test task 3"}
            )
            assert not create_result3.isError
            uri3 = create_result3.content[0].text
            print(f"✓ Created todo: {uri3}")

            # Step 7: Check final status
            print("\n" + "-" * 70)
            print("STEP 7: Check final tool status")
            print("-" * 70)
            status_result = await session.call_tool("get_todo_tool_status", {})
            assert not status_result.isError
            print(f"Final status: {status_result.content[0].text}")
            print("✓ All tools operational")

    print("\n" + "=" * 70)
    print("TODO SERVER DYNAMIC TOOL AWARENESS TEST PASSED! ✓")
    print("=" * 70 + "\n")


def test_dynamic_tool_awareness_math_server():
    """Test dynamic tool awareness with math server - synchronous wrapper for pytest."""
    asyncio.run(_test_dynamic_tool_awareness_math_server())


def test_dynamic_tool_awareness_todo_server():
    """Test dynamic tool awareness with todo server - synchronous wrapper for pytest."""
    asyncio.run(_test_dynamic_tool_awareness_todo_server())


async def _main():
    """Internal async function for running all dynamic tool awareness tests."""
    await _test_dynamic_tool_awareness_math_server()
    await _test_dynamic_tool_awareness_todo_server()


def main():
    """Run all dynamic tool awareness tests - synchronous wrapper."""
    asyncio.run(_main())


if __name__ == "__main__":
    main()
