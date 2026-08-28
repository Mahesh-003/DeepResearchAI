import os
import json
from dotenv import load_dotenv
from groq import Groq

from tools import calculator, search_knowledge


# ==========================================
# LOAD API KEY
# ==========================================

load_dotenv(
    r"C:\Users\MAHESH\OneDrive\Dokumen\DeepResearchAI\.env"
)

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("❌ GROQ_API_KEY not found")


# ==========================================
# GROQ CLIENT
# ==========================================

client = Groq(api_key=api_key)

MODEL = "openai/gpt-oss-20b"


# ==========================================
# TOOL DEFINITIONS
# ==========================================

tools = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Calculate mathematical expressions.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression to calculate."
                    }
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_knowledge",
            "description": "Search the research knowledge base for relevant information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Research query to search."
                    }
                },
                "required": ["query"]
            }
        }
    }
]


# ==========================================
# TOOL EXECUTION
# ==========================================

def execute_tool(name, arguments):

    if name == "calculator":

        return str(
            calculator(
                arguments["expression"]
            )
        )

    elif name == "search_knowledge":

        return search_knowledge(
            arguments["query"]
        )

    return "Unknown tool."


# ==========================================
# TOOL-CALLING AGENT
# ==========================================

def run_agent(user_question):

    messages = [
        {
            "role": "system",
            "content": """
You are an intelligent research assistant.

You have access to two tools:

1. calculator
   Use it for mathematical calculations.

2. search_knowledge
   Use it when the user asks about information
   that may exist in the research knowledge base.

Decide yourself whether a tool is necessary.

If no tool is necessary, answer directly.
"""
        },
        {
            "role": "user",
            "content": user_question
        }
    ]

    # --------------------------------------
    # FIRST LLM CALL
    # --------------------------------------

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto",
        temperature=0.2
    )

    assistant_message = response.choices[0].message

    # --------------------------------------
    # NO TOOL REQUIRED
    # --------------------------------------

    if not assistant_message.tool_calls:

        return assistant_message.content

    # --------------------------------------
    # ADD ASSISTANT TOOL REQUEST
    # --------------------------------------

    messages.append(
        assistant_message
    )

    # --------------------------------------
    # EXECUTE TOOLS
    # --------------------------------------

    for tool_call in assistant_message.tool_calls:

        tool_name = tool_call.function.name

        arguments = json.loads(
            tool_call.function.arguments
        )

        print(
            f"\n🛠️ Agent selected tool: "
            f"{tool_name}"
        )

        print(
            f"Arguments: {arguments}"
        )

        result = execute_tool(
            tool_name,
            arguments
        )

        # Add tool result to conversation
        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            }
        )

    # --------------------------------------
    # SECOND LLM CALL
    # --------------------------------------

    final_response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.2
    )

    return final_response.choices[0].message.content


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    print()
    print("🤖 DEEPRESEARCH AI - TOOL AGENT")
    print("=" * 60)

    print(
        "\nType 'exit' to stop."
    )

    while True:

        question = input(
            "\nYou: "
        )

        if question.lower() == "exit":
            break

        try:

            answer = run_agent(
                question
            )

            print(
                "\n🤖 AI:",
                answer
            )

        except Exception as e:

            print(
                "\n❌ ERROR:"
            )

            print(e)