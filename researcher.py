# import os
# from dotenv import load_dotenv
# from groq import Groq

# # ==========================================
# # LOAD API KEY
# # ==========================================

# load_dotenv(
#     r"C:\Users\MAHESH\OneDrive\Dokumen\DeepResearchAI\.env"
# )

# api_key = os.getenv("GROQ_API_KEY")

# if not api_key:
#     raise ValueError("❌ GROQ_API_KEY not found")

# # ==========================================
# # GROQ CLIENT
# # ==========================================

# client = Groq(api_key=api_key)

# MODEL = "openai/gpt-oss-20b"


# # ==========================================
# # RESEARCH AGENT
# # ==========================================

# def research_topic(question):

#     prompt = f"""
# Research the following question using web search:

# {question}

# Find reliable and relevant information.

# Return:
# - 3 to 5 important findings
# - Important evidence or statistics
# - Names of important sources
# - URLs when available

# Keep the final response concise and focused on the research question.
# """

#     try:

#         response = client.chat.completions.create(
#             model=MODEL,

#             messages=[
#                 {
#                     "role": "system",
#                     "content": (
#                         "You are an autonomous web research agent. "
#                         "Use reliable sources and provide evidence-based information."
#                     )
#                 },
#                 {
#                     "role": "user",
#                     "content": prompt
#                 }
#             ],

#             tools=[
#                 {
#                     "type": "browser_search"
#                 }
#             ],

#             tool_choice="required",

#             temperature=0.2
#         )

#         # ==================================
#         # DEBUG INFORMATION
#         # ==================================

#         print("\n")
#         print("=" * 60)
#         print("🔧 DEBUG RESPONSE")
#         print("=" * 60)

#         print(response)

#         print("=" * 60)
#         print()

#         # ==================================
#         # EXTRACT FINAL ANSWER
#         # ==================================

#         message = response.choices[0].message

#         if message.content:

#             return message.content

#         else:

#             return (
#                 "⚠️ The browser search was executed, "
#                 "but the model did not return a text response."
#             )

#     except Exception as e:

#         error = str(e)

#         if "rate_limit_exceeded" in error:

#             return (
#                 "⚠️ RATE_LIMIT_REACHED\n"
#                 "Groq token limit has been reached. "
#                 "Please wait until the limit resets."
#             )

#         return f"❌ RESEARCH_ERROR:\n{error}"


# # ==========================================
# # TEST RESEARCH AGENT
# # ==========================================

# if __name__ == "__main__":

#     print()
#     print("🔎 DEEPRESEARCH AI - RESEARCH AGENT")
#     print("=" * 60)

#     question = input(
#         "\nEnter a research question: "
#     )

#     if not question.strip():

#         print("❌ Please enter a research question.")

#         exit()


#     print()
#     print("🌐 Searching the web...")
#     print()


#     result = research_topic(question)


#     print()
#     print("=" * 60)
#     print("📚 RESEARCH RESULT")
#     print("=" * 60)

#     print(result)

#     print()
#     print("=" * 60)
#     print("✅ RESEARCH AGENT FINISHED")
#     print("=" * 60)

import os
from dotenv import load_dotenv
from groq import Groq

# ==========================================
# LOAD API KEY
# ==========================================

load_dotenv(
    r"C:\Users\MAHESH\OneDrive\Dokumen\DeepResearchAI\.env"
)

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found")


# ==========================================
# GROQ CLIENT
# ==========================================

client = Groq(api_key=api_key)

MODEL = "openai/gpt-oss-20b"


# ==========================================
# AI RESPONSE
# ==========================================

def research_topic(question):

    prompt = f"""
You are a helpful AI assistant.

User question:
{question}

Answer the question directly.

IMPORTANT:
- Keep the answer SHORT.
- For a simple definition, answer in 2-3 sentences.
- For a basic explanation, answer in 4-6 sentences.
- Give one simple real-life example when useful.
- Do not give unnecessary information.
- Do not create a long report.
- Do not repeat the question.
- Use simple language.
- Answer only what the user asked.

If the user explicitly asks for deep research, detailed research,
latest information, statistics, sources, or a research report,
then provide a more detailed answer.

Otherwise keep it concise.
"""

    try:

        response = client.chat.completions.create(
            model=MODEL,

            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a concise and helpful AI assistant. "
                        "Give short answers unless detailed research "
                        "is explicitly requested."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.2,

            # Limit response length
            max_tokens=300
        )

        message = response.choices[0].message

        if message.content:
            return message.content.strip()

        return "Sorry, I could not generate an answer."

    except Exception as e:

        if "rate_limit_exceeded" in str(e).lower():
            return "⚠️ API rate limit reached. Please try again later."

        return f"❌ Error: {str(e)}"


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    print("=" * 50)
    print("🔬 DEEPRESEARCH AI")
    print("=" * 50)

    question = input("\nYou: ")

    if not question.strip():
        print("Please enter a question.")
        exit()

    print("\n🤖 AI:")

    answer = research_topic(question)

    print(answer)