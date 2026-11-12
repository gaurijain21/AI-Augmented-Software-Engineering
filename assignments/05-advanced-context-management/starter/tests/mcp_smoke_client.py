"""Small MCP client used to capture the Week 5 transcript."""

import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main() -> None:
    server_path = Path(__file__).parents[1] / "server.py"
    params = StdioServerParameters(command=sys.executable, args=[str(server_path)])
    print("starting:", server_path, flush=True)

    async with stdio_client(params) as (read_stream, write_stream):
        print("stdio connected", flush=True)
        async with ClientSession(read_stream, write_stream) as session:
            print("session created", flush=True)
            await session.initialize()
            print("session initialized", flush=True)
            listed = await session.list_tools()
            print("tools:", [tool.name for tool in listed.tools])

            search = await session.call_tool(
                "search_countries", {"query": "Germany", "limit": 1}
            )
            print("search:", search.content[0].text)

            details = await session.call_tool("get_country_details", {"name": "Germany"})
            print("details:", details.content[0].text)


if __name__ == "__main__":
    asyncio.run(main())
