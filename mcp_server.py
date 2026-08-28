# from mcp.server.mcpserver import MCPServer


# # ==========================================
# # CREATE MCP SERVER
# # ==========================================

# server = MCPServer(
#     name="DeepResearchAI"
# )


# # ==========================================
# # CALCULATOR TOOL
# # ==========================================

# @server.tool(
#     name="calculate",
#     description="Calculate a mathematical expression."
# )
# def calculate(expression: str) -> str:

#     try:
#         # Safe basic calculator
#         allowed = "0123456789+-*/(). "

#         if not all(
#             character in allowed
#             for character in expression
#         ):
#             return "Invalid mathematical expression."

#         result = eval(
#             expression,
#             {"__builtins__": {}},
#             {}
#         )

#         return str(result)

#     except Exception as e:

#         return f"Calculator error: {e}"


# # ==========================================
# # RESEARCH SEARCH TOOL
# # ==========================================

# @server.tool(
#     name="research_search",
#     description="Search the DeepResearchAI research knowledge base."
# )
# def research_search(query: str) -> str:

#     from tools import search_knowledge

#     return search_knowledge(query)


# # ==========================================
# # SERVER INFORMATION
# # ==========================================

# @server.resource(
#     "research://info"
# )
# def research_info() -> str:

#     return """
# DeepResearchAI MCP Server

# Available tools:

# 1. calculate
#    Performs mathematical calculations.

# 2. research_search
#    Searches the DeepResearchAI knowledge base.

# Resource:

# research://info
# """


# # ==========================================
# # START SERVER
# # ==========================================

# if __name__ == "__main__":

#     print("🚀 DeepResearchAI MCP Server")
#     print("=" * 50)
#     print("Tools:")
#     print("1. calculate")
#     print("2. research_search")
#     print()
#     print("Starting server...")

#     server.run()

# 22import asyncio
# import sys

# from mcp.server.mcpserver import MCPServer


# server = MCPServer(
#     name="DeepResearchAI"
# )


# @server.tool(
#     name="calculate",
#     description="Calculate a mathematical expression."
# )
# def calculate(expression: str) -> str:
#     try:
#         result = eval(
#             expression,
#             {"__builtins__": {}},
#             {}
#         )
#         return str(result)

#     except Exception as e:
#         return f"Error: {e}"


# if __name__ == "__main__":

#     print(
#         "MCP server started",
#         file=sys.stderr,
#         flush=True
#     )

#     asyncio.run(
#         server.run_stdio_async()
#     )
import asyncio
import sys

from mcp.server.mcpserver import MCPServer
from tools import calculator, search_knowledge

server = MCPServer(
    name="DeepResearchAI"
)


@server.tool(
    name="calculate",
    description="Calculate a mathematical expression."
)
def calculate(expression: str) -> str:
    try:
        return str(calculator(expression))
    except Exception as e:
        return f"Calculator error: {e}"


@server.tool(
    name="research_search",
    description="Search the DeepResearchAI research knowledge base."
)
def research_search(query: str) -> str:
    try:
        return search_knowledge(query)
    except Exception as e:
        return f"Research search error: {e}"


if __name__ == "__main__":

    print(
        "DeepResearchAI MCP Server started",
        file=sys.stderr,
        flush=True
    )

    asyncio.run(
        server.run_stdio_async()
    )