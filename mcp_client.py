# import asyncio
# import sys

# from mcp.server.mcpserver import MCPServer
# from tools import calculator, search_knowledge


# server = MCPServer(
#     name="DeepResearchAI"
# )


# @server.tool(
#     name="calculate",
#     description="Calculate a mathematical expression."
# )
# def calculate(expression: str) -> str:
#     try:
#         return str(calculator(expression))
#     except Exception as e:
#         return f"Calculator error: {e}"


# @server.tool(
#     name="research_search",
#     description="Search the DeepResearchAI research knowledge base."
# )
# def research_search(query: str) -> str:
#     try:
#         return search_knowledge(query)
#     except Exception as e:
#         return f"Research search error: {e}"


# @server.resource("research://info")
# def research_info() -> str:
#     return """
# DeepResearchAI MCP Server

# Available tools:
# 1. calculate
# 2. research_search
# """


# if __name__ == "__main__":

#     print(
#         "DeepResearchAI MCP Server started",
#         file=sys.stderr,
#         flush=True
#     )

#     asyncio.run(
#         server.run_stdio_async()
#     )
import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


# ==========================================
# MCP SERVER CONFIGURATION
# ==========================================

server_params = StdioServerParameters(
    command=r"C:\Users\MAHESH\anaconda4\envs\deepresearch\python.exe",
    args=[
        r"C:\Users\MAHESH\OneDrive\Dokumen\DeepResearchAI\mcp_server.py"
    ]
)


# ==========================================
# MAIN MCP CLIENT
# ==========================================

async def main():

    print("🔌 Connecting to MCP server...")

    async with stdio_client(
        server_params
    ) as (read, write):

        print("📡 STDIO connection established")

        async with ClientSession(
            read,
            write
        ) as session:

            # ==================================
            # INITIALIZE MCP
            # ==================================

            print("🤝 Initializing MCP...")

            await session.initialize()

            print("✅ MCP connection successful!")


            # ==================================
            # LIST AVAILABLE TOOLS
            # ==================================

            tools = await session.list_tools()

            print("\n🛠️ Available MCP tools:")
            print("=" * 50)

            for tool in tools.tools:

                print(
                    f"- {tool.name}: "
                    f"{tool.description}"
                )


            # ==================================
            # TEST CALCULATOR
            # ==================================

            print("\n🧮 Testing calculator...")

            calculator_result = await session.call_tool(
                "calculate",
                {
                    "expression": "25 * 4 + 10"
                }
            )

            print("\nCalculator result:")

            for item in calculator_result.content:

                if hasattr(item, "text"):
                    print(item.text)


            # ==================================
            # TEST RESEARCH SEARCH
            # ==================================

            print("\n🔍 Testing research search...")

            research_result = await session.call_tool(
                "research_search",
                {
                    "query":
                    "Generative AI developer productivity"
                }
            )

            print("\nResearch result:")
            print("=" * 50)

            for item in research_result.content:

                if hasattr(item, "text"):
                    print(item.text)


            # ==================================
            # COMPLETE
            # ==================================

            print("\n" + "=" * 50)
            print("✅ MCP TEST COMPLETE")
            print("=" * 50)


# ==========================================
# RUN CLIENT
# ==========================================

if __name__ == "__main__":

    asyncio.run(main())