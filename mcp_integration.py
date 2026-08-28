import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


PYTHON_PATH = (
    r"C:\Users\MAHESH\anaconda4\envs\deepresearch\python.exe"
)

SERVER_PATH = (
    r"C:\Users\MAHESH\OneDrive\Dokumen\DeepResearchAI\mcp_server.py"
)


async def call_mcp_tool(tool_name, arguments):

    server_params = StdioServerParameters(
        command=PYTHON_PATH,
        args=[SERVER_PATH]
    )

    async with stdio_client(
        server_params
    ) as (read, write):

        async with ClientSession(
            read,
            write
        ) as session:

            await session.initialize()

            result = await session.call_tool(
                tool_name,
                arguments
            )

            output = []

            for item in result.content:

                if hasattr(item, "text"):
                    output.append(item.text)

            return "\n".join(output)


def mcp_calculate(expression):

    return asyncio.run(
        call_mcp_tool(
            "calculate",
            {
                "expression": expression
            }
        )
    )


def mcp_research_search(query):

    return asyncio.run(
        call_mcp_tool(
            "research_search",
            {
                "query": query
            }
        )
    )


if __name__ == "__main__":

    print("Testing MCP integration...")

    result = mcp_calculate("100 / 4")

    print("\nCalculator:")
    print(result)

    result = mcp_research_search(
        "Generative AI developer productivity"
    )

    print("\nResearch:")
    print(result)

    print("\n✅ MCP integration working!")