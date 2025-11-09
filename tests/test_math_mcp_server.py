"""
Test file for Math MCP Server
Tests the add and multiply tools with various assertions
"""

import asyncio
import logging
import os
from pathlib import Path
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Suppress FastMCP server info logs during tests
logging.getLogger("mcp").setLevel(logging.WARNING)

# Editable install makes package importable; no manual path manipulation required.


async def _run_math_suite():
    """Test math server with comprehensive assertions"""
    print("\n" + "=" * 70)
    print("TESTING MATH MCP SERVER WITH ASSERTIONS")
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

            # Test 1: Basic Addition
            print("\n" + "-" * 70)
            print("TEST 1: Basic Addition")
            print("-" * 70)
            numbers = [10, 20, 30]
            result = await session.call_tool("add", {"numbers": numbers})
            actual = result.content[0].text
            expected = "60.0"
            assert actual == expected, f"Expected {expected}, got {actual}"
            print(f"✓ add({numbers}) = {actual}")
            print(f"  Assertion passed: {actual} == {expected}")

            # Test 2: Addition with Decimals
            print("\n" + "-" * 70)
            print("TEST 2: Addition with Decimals")
            print("-" * 70)
            numbers = [3.14, 2.86, 1.0]
            result = await session.call_tool("add", {"numbers": numbers})
            actual = float(result.content[0].text)
            expected = 7.0
            assert actual == expected, f"Expected {expected}, got {actual}"
            print(f"✓ add({numbers}) = {actual}")
            print(f"  Assertion passed: {actual} == {expected}")

            # Test 3: Addition with Negative Numbers
            print("\n" + "-" * 70)
            print("TEST 3: Addition with Negative Numbers")
            print("-" * 70)
            numbers = [-10, 5, -3]
            result = await session.call_tool("add", {"numbers": numbers})
            actual = float(result.content[0].text)
            expected = -8.0
            assert actual == expected, f"Expected {expected}, got {actual}"
            print(f"✓ add({numbers}) = {actual}")
            print(f"  Assertion passed: {actual} == {expected}")

            # Test 4: Addition with Single Number
            print("\n" + "-" * 70)
            print("TEST 4: Addition with Single Number")
            print("-" * 70)
            numbers = [42]
            result = await session.call_tool("add", {"numbers": numbers})
            actual = float(result.content[0].text)
            expected = 42.0
            assert actual == expected, f"Expected {expected}, got {actual}"
            print(f"✓ add({numbers}) = {actual}")
            print(f"  Assertion passed: {actual} == {expected}")

            # Test 5: Addition with Zeros
            print("\n" + "-" * 70)
            print("TEST 5: Addition with Zeros")
            print("-" * 70)
            numbers = [0, 0, 0]
            result = await session.call_tool("add", {"numbers": numbers})
            actual = float(result.content[0].text)
            expected = 0.0
            assert actual == expected, f"Expected {expected}, got {actual}"
            print(f"✓ add({numbers}) = {actual}")
            print(f"  Assertion passed: {actual} == {expected}")

            # Test 6: Basic Multiplication
            print("\n" + "-" * 70)
            print("TEST 6: Basic Multiplication")
            print("-" * 70)
            numbers = [7, 8]
            result = await session.call_tool("multiply", {"numbers": numbers})
            actual = float(result.content[0].text)
            expected = 56.0
            assert actual == expected, f"Expected {expected}, got {actual}"
            print(f"✓ multiply({numbers}) = {actual}")
            print(f"  Assertion passed: {actual} == {expected}")

            # Test 7: Multiplication with Multiple Numbers
            print("\n" + "-" * 70)
            print("TEST 7: Multiplication with Multiple Numbers")
            print("-" * 70)
            numbers = [2, 3, 4, 5]
            result = await session.call_tool("multiply", {"numbers": numbers})
            actual = float(result.content[0].text)
            expected = 120.0
            assert actual == expected, f"Expected {expected}, got {actual}"
            print(f"✓ multiply({numbers}) = {actual}")
            print(f"  Assertion passed: {actual} == {expected}")

            # Test 8: Multiplication with Decimals
            print("\n" + "-" * 70)
            print("TEST 8: Multiplication with Decimals")
            print("-" * 70)
            numbers = [2.5, 4.0]
            result = await session.call_tool("multiply", {"numbers": numbers})
            actual = float(result.content[0].text)
            expected = 10.0
            assert actual == expected, f"Expected {expected}, got {actual}"
            print(f"✓ multiply({numbers}) = {actual}")
            print(f"  Assertion passed: {actual} == {expected}")

            # Test 9: Multiplication with Negative Numbers
            print("\n" + "-" * 70)
            print("TEST 9: Multiplication with Negative Numbers")
            print("-" * 70)
            numbers = [-3, -4]
            result = await session.call_tool("multiply", {"numbers": numbers})
            actual = float(result.content[0].text)
            expected = 12.0
            assert actual == expected, f"Expected {expected}, got {actual}"
            print(f"✓ multiply({numbers}) = {actual}")
            print(f"  Assertion passed: {actual} == {expected}")

            # Test 10: Multiplication with Zero
            print("\n" + "-" * 70)
            print("TEST 10: Multiplication with Zero")
            print("-" * 70)
            numbers = [100, 0]
            result = await session.call_tool("multiply", {"numbers": numbers})
            actual = float(result.content[0].text)
            expected = 0.0
            assert actual == expected, f"Expected {expected}, got {actual}"
            print(f"✓ multiply({numbers}) = {actual}")
            print(f"  Assertion passed: {actual} == {expected}")

            # Test 11: Large Numbers Addition
            print("\n" + "-" * 70)
            print("TEST 11: Large Numbers Addition")
            print("-" * 70)
            numbers = [999999, 1]
            result = await session.call_tool("add", {"numbers": numbers})
            actual = float(result.content[0].text)
            expected = 1000000.0
            assert actual == expected, f"Expected {expected}, got {actual}"
            print(f"✓ add({numbers}) = {actual}")
            print(f"  Assertion passed: {actual} == {expected}")

            # Test 12: Sequential Operations (Chained)
            print("\n" + "-" * 70)
            print("TEST 12: Sequential Operations - (5 + 10) * 3")
            print("-" * 70)
            step1_result = await session.call_tool("add", {"numbers": [5, 10]})
            step1_value = float(step1_result.content[0].text)
            assert (
                step1_value == 15.0
            ), f"Step 1 failed: Expected 15.0, got {step1_value}"
            print(f"  Step 1: add([5, 10]) = {step1_value} ✓")
            step2_result = await session.call_tool(
                "multiply", {"numbers": [step1_value, 3]}
            )
            step2_value = float(step2_result.content[0].text)
            assert (
                step2_value == 45.0
            ), f"Step 2 failed: Expected 45.0, got {step2_value}"
            print(f"  Step 2: multiply([{step1_value}, 3]) = {step2_value} ✓")
            print(f"✓ Sequential operation passed: (5 + 10) * 3 = {step2_value}")

            # Test 13: Error Handling - Empty List (Addition)
            print("\n" + "-" * 70)
            print("TEST 13: Error Handling - Empty List (Addition)")
            print("-" * 70)
            result = await session.call_tool("add", {"numbers": []})
            assert result.isError, "Expected error for empty list (addition)"

            # Test 14: Error Handling - Empty List (Multiplication)
            print("\n" + "-" * 70)
            print("TEST 14: Error Handling - Empty List (Multiplication)")
            print("-" * 70)
            result = await session.call_tool("multiply", {"numbers": []})
            assert result.isError, "Expected error for empty list (multiplication)"

            # Test 15: Error Handling - Non-numeric Element (Addition)
            print("\n" + "-" * 70)
            print("TEST 15: Error Handling - Non-numeric Element (Addition)")
            print("-" * 70)
            result = await session.call_tool("add", {"numbers": [1, "two", 3]})
            assert result.isError, "Expected error for non-numeric element"

            # Test 16: Error Handling - Non-numeric Element (Multiplication)
            print("\n" + "-" * 70)
            print("TEST 16: Error Handling - Non-numeric Element (Multiplication)")
            print("-" * 70)
            result = await session.call_tool("multiply", {"numbers": [5, None, 10]})
            assert result.isError, "Expected error for None value"

            # Test 17: Error Handling - NaN Value (Addition)
            print("\n" + "-" * 70)
            print("TEST 17: Error Handling - NaN Value (Addition)")
            print("-" * 70)
            result = await session.call_tool("add", {"numbers": [1, float("nan"), 3]})
            assert result.isError, "Expected error for NaN value"

            # Test 18: Error Handling - Infinite Value (Multiplication)
            print("\n" + "-" * 70)
            print("TEST 18: Error Handling - Infinite Value (Multiplication)")
            print("-" * 70)
            result = await session.call_tool("multiply", {"numbers": [5, float("inf")]})
            assert result.isError, "Expected error for infinite value"

            # Test 19: Error Handling - Negative Infinity (Addition)
            print("\n" + "-" * 70)
            print("TEST 19: Error Handling - Negative Infinity (Addition)")
            print("-" * 70)
            result = await session.call_tool("add", {"numbers": [10, float("-inf"), 5]})
            assert result.isError, "Expected error for negative infinity"

            # Test 20: Error Handling - Mixed Invalid Values
            print("\n" + "-" * 70)
            print("TEST 20: Error Handling - Mixed Invalid Values")
            print("-" * 70)
            result = await session.call_tool("add", {"numbers": [1, 2, "invalid", 4]})
            assert result.isError, "Expected error for string in list"

    print("\n" + "=" * 70)
    print("ALL TESTS PASSED SUCCESSFULLY! ✓")
    print("Total Tests: 20 (12 functional + 8 error handling)")
    print("=" * 70 + "\n")


def test_math_server():
    """Synchronous-style pytest test using asyncio.run for consistency."""
    asyncio.run(_run_math_suite())


def main():
    asyncio.run(_run_math_suite())


if __name__ == "__main__":
    main()
