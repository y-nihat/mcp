"""Test Scenarios for MCP↔LLM Bridge

This file contains test scenarios that exercise the MCP↔LLM bridge with
different MCP servers and prompts. Add new test cases here as you develop
new MCP tools.

Each test case should:
1. Define an MCP server to connect to
2. Provide a user prompt
3. Optionally configure bridge behavior
4. Run and validate the result
"""

from __future__ import annotations

import asyncio
import sys
from typing import Any, Dict, List, Optional

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from mcp_llm_bridge_client import MCPLLMBridge, BridgeConfig


# =============================================================================
# Test Case Definitions
# =============================================================================


class TestCase:
    """Base class for test scenarios."""

    def __init__(
        self,
        name: str,
        server_command: str,
        server_args: List[str],
        user_prompt: str,
        system_prompt: Optional[str] = None,
        config: Optional[BridgeConfig] = None,
        use_tools: bool = True,
    ):
        self.name = name
        self.server_command = server_command
        self.server_args = server_args
        self.user_prompt = user_prompt
        self.system_prompt = system_prompt
        self.config = config or BridgeConfig()
        self.use_tools = use_tools

    async def run(self) -> Dict[str, Any]:
        """Run the test case and return results."""
        print("\n" + "=" * 70)
        print(f"TEST: {self.name}")
        print("=" * 70)
        print(f"User prompt: {self.user_prompt}")
        print("-" * 70)

        server_params = StdioServerParameters(
            command=self.server_command,
            args=self.server_args,
            env=None,
        )

        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                print(f"✓ Connected to MCP server")

                bridge = MCPLLMBridge(session, config=self.config)
                result = await bridge.run_conversation(
                    user_prompt=self.user_prompt,
                    system_prompt=self.system_prompt,
                    use_tools=self.use_tools,
                )

                print("\n" + "-" * 70)
                print("FINAL RESPONSE:")
                print(result["final_response"])
                print("-" * 70)
                print(
                    f"Stats: {result['tool_calls_made']} tool calls, {result['rounds']} rounds"
                )
                print("=" * 70 + "\n")

                return result


# =============================================================================
# Math Server Test Cases
# =============================================================================


def math_basic_arithmetic() -> TestCase:
    """Basic arithmetic with add and multiply tools."""
    return TestCase(
        name="Math: Basic Arithmetic",
        server_command="python",
        server_args=["mcp_math_server.py"],
        user_prompt="Compute (3 + 5) * 4 using available tools and explain briefly.",
    )


def math_complex_calculation() -> TestCase:
    """More complex calculation requiring multiple tool calls."""
    return TestCase(
        name="Math: Complex Calculation",
        server_command="python",
        server_args=["mcp_math_server.py"],
        user_prompt="Calculate ((10 + 20) * 3) + (5 * 7) using tools. Show your work.",
    )


def math_sequential_operations() -> TestCase:
    """Test sequential operations with explanation."""
    return TestCase(
        name="Math: Sequential Operations",
        server_command="python",
        server_args=["mcp_math_server.py"],
        user_prompt="First add 15, 25, and 10. Then multiply the result by 2. Explain each step.",
    )


def math_large_numbers() -> TestCase:
    """Test with large numbers."""
    return TestCase(
        name="Math: Large Numbers",
        server_command="python",
        server_args=["mcp_math_server.py"],
        user_prompt="Add these numbers: 999999, 1, 500000, 250000. What's the total?",
    )


def math_decimals() -> TestCase:
    """Test with decimal numbers."""
    return TestCase(
        name="Math: Decimal Operations",
        server_command="python",
        server_args=["mcp_math_server.py"],
        user_prompt="Calculate 3.14 * 2.5 + 1.86. Use tools and show the result.",
    )


# =============================================================================
# Test Suites
# =============================================================================


def get_math_test_suite() -> List[TestCase]:
    """Get all math server test cases."""
    return [
        math_basic_arithmetic(),
        math_complex_calculation(),
        math_sequential_operations(),
        math_large_numbers(),
        math_decimals(),
    ]


def get_all_test_cases() -> List[TestCase]:
    """Get all available test cases."""
    return get_math_test_suite()
    # Add more suites here as you develop new MCP servers:
    # return get_math_test_suite() + get_weather_test_suite() + ...


# =============================================================================
# Test Runner
# =============================================================================


async def run_test_case(test_case: TestCase) -> bool:
    """Run a single test case and return success status."""
    try:
        await test_case.run()
        return True
    except Exception as e:
        print(f"\n❌ TEST FAILED: {test_case.name}")
        print(f"Error: {e}\n")
        return False


async def run_test_suite(
    test_cases: List[TestCase], stop_on_failure: bool = False
) -> Dict[str, Any]:
    """Run a suite of test cases.

    Args:
        test_cases: List of test cases to run
        stop_on_failure: If True, stop on first failure

    Returns:
        Dictionary with test results
    """
    results = {"passed": 0, "failed": 0, "total": len(test_cases)}

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*70}")
        print(f"Running test {i}/{len(test_cases)}")
        print(f"{'='*70}")

        success = await run_test_case(test_case)
        if success:
            results["passed"] += 1
        else:
            results["failed"] += 1
            if stop_on_failure:
                break

    return results


def print_summary(results: Dict[str, Any]) -> None:
    """Print test summary."""
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Total:  {results['total']}")
    print(f"Passed: {results['passed']} ✓")
    print(f"Failed: {results['failed']} ✗")
    if results["failed"] == 0:
        print("\n🎉 All tests passed!")
    print("=" * 70 + "\n")


# =============================================================================
# Main Entry Point
# =============================================================================


async def main(argv: List[str]) -> int:
    """Main entry point for test scenarios."""

    # Parse command line arguments
    if "--help" in argv or "-h" in argv:
        print("Usage: python test_llm_mcp_bridge_scenarios.py [options]")
        print("\nOptions:")
        print("  --all              Run all test cases")
        print("  --math             Run math server test cases")
        print("  --basic            Run basic arithmetic test only")
        print("  --stop-on-failure  Stop on first failure")
        print("  --help, -h         Show this help message")
        return 0

    stop_on_failure = "--stop-on-failure" in argv

    # Select test cases based on arguments
    if "--all" in argv:
        test_cases = get_all_test_cases()
    elif "--math" in argv:
        test_cases = get_math_test_suite()
    elif "--basic" in argv:
        test_cases = [math_basic_arithmetic()]
    else:
        # Default: run basic test
        print("Running default test (use --help for more options)")
        test_cases = [math_basic_arithmetic()]

    # Run tests
    results = await run_test_suite(test_cases, stop_on_failure=stop_on_failure)

    # Print summary
    print_summary(results)

    return 0 if results["failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main(sys.argv)))
