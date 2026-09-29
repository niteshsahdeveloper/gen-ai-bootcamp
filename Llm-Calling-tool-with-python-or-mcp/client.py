import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():

    # ------------------------------------------------
    # Start the MCP server
    # ------------------------------------------------

    server_params = StdioServerParameters(
        command="python",
        args=["server.py"]
    )

    # ------------------------------------------------
    # Connect Python client to MCP server
    # ------------------------------------------------

    async with stdio_client(server_params) as (read, write):

        async with ClientSession(read, write) as session:

            # Initialize MCP connection
            await session.initialize()

            print("\nConnected to MCP server!")

            # ------------------------------------------------
            # Get available tools
            # ------------------------------------------------

            tools = await session.list_tools()

            print("\nAvailable MCP tools:")

            for tool in tools.tools:
                print(
                    f"- {tool.name}: "
                    f"{tool.description}"
                )

            # ------------------------------------------------
            # Call MCP tool
            # ------------------------------------------------

            print("\nCalling get_account_balance...")

            result = await session.call_tool(
                "get_account_balance",
                {
                    "account_number": "12345"
                }
            )

            print("\nTool result:")

            for content in result.content:
                print(content)


if __name__ == "__main__":
    asyncio.run(main())