import os
from dotenv import load_dotenv
from groq import Groq

from memory import (
    get_recent_memory,
    add_memory
)


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
# MEMORY AGENT
# ==========================================

def chat_with_memory(user_question):

    # Load recent conversations
    memories = get_recent_memory(limit=5)

    memory_context = ""

    if memories:

        for item in memories:

            memory_context += f"""
User:
{item["user"]}

Assistant:
{item["assistant"]}

-------------------------
"""

    else:

        memory_context = "No previous conversation."


    # ======================================
    # PROMPT
    # ======================================

    prompt = f"""
You are an intelligent AI assistant with conversation memory.

Previous conversation:

{memory_context}

Current user question:

{user_question}

Use the previous conversation when it is relevant.

If the current question is unrelated,
answer it normally.

Do not mention the internal memory system
unless the user asks about it.
"""


    # ======================================
    # LLM CALL
    # ======================================

    try:

        response = client.chat.completions.create(
            model=MODEL,

            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful AI assistant "
                        "with conversational memory."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.3
        )

        answer = response.choices[0].message.content


        # ==================================
        # SAVE MEMORY
        # ==================================

        add_memory(
            user_question,
            answer
        )


        return answer


    except Exception as e:

        return f"❌ ERROR:\n{e}"


# ==========================================
# TEST MEMORY AGENT
# ==========================================

if __name__ == "__main__":

    print()
    print("🧠 DEEPRESEARCH AI - MEMORY AGENT")
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


        answer = chat_with_memory(
            question
        )

        print(
            "\nAI:",
            answer
        )