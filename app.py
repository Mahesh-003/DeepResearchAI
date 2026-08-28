# import os
# import json

# from dotenv import load_dotenv
# from groq import Groq

# from knowledge_base import save_research
# from mcp_integration import mcp_research_search


# # ==========================================
# # LOAD API KEY
# # ==========================================

# load_dotenv(
#     r"C:\Users\MAHESH\OneDrive\Dokumen\DeepResearchAI\.env"
# )

# api_key = os.getenv("GROQ_API_KEY")

# if not api_key:
#     print("❌ API key not found")
#     exit()


# # ==========================================
# # GROQ CLIENT
# # ==========================================

# client = Groq(api_key=api_key)

# MODEL = "openai/gpt-oss-20b"


# # ==========================================
# # PLANNER AGENT
# # ==========================================

# def create_research_plan(question):

#     prompt = f"""
# You are an expert research planning agent.

# The user wants to research this topic:

# "{question}"

# Break this topic into exactly 5 important research areas.

# For each area provide:

# 1. A short title
# 2. A clear research question

# IMPORTANT:

# Return ONLY valid JSON.

# Do not use Markdown.
# Do not write ```json.
# Do not add explanations.

# Use this structure:

# {{
#     "main_topic": "{question}",
#     "research_areas": [
#         {{
#             "title": "Area title",
#             "question": "Research question"
#         }}
#     ]
# }}
# """

#     response = client.chat.completions.create(
#         model=MODEL,
#         messages=[
#             {
#                 "role": "system",
#                 "content": (
#                     "You are a professional research planning agent. "
#                     "Always return valid JSON only."
#                 )
#             },
#             {
#                 "role": "user",
#                 "content": prompt
#             }
#         ],
#         temperature=0
#     )

#     result = response.choices[0].message.content.strip()

#     # Remove Markdown code fences if the model adds them
#     if result.startswith("```"):
#         result = result.replace("```json", "")
#         result = result.replace("```", "")
#         result = result.strip()

#     return json.loads(result)


# # ==========================================
# # RESEARCH AGENT
# # ==========================================

# def research_question(question):

#     print("   🔎 Checking MCP research knowledge...")

#     try:

#         # ==================================
#         # MCP RESEARCH SEARCH
#         # ==================================

#         mcp_result = mcp_research_search(question)

#         if mcp_result and not mcp_result.startswith(
#             "Research search error:"
#         ):

#             print("   ✅ MCP research tool used")

#             return mcp_result

#         print(
#             "   ⚠️ MCP did not return useful results."
#         )

#     except Exception as e:

#         print(
#             f"   ⚠️ MCP research unavailable: {e}"
#         )


#     # ==================================
#     # GROQ RESEARCH FALLBACK
#     # ==================================

#     print("   🌐 Using Groq research agent...")

#     prompt = f"""
# Research this question:

# {question}

# Find reliable and relevant information.

# Return:

# - 3 to 5 important findings
# - Important evidence or statistics
# - Important sources
# - URLs when available

# Keep the answer concise.
# """

#     try:

#         response = client.chat.completions.create(
#             model=MODEL,
#             messages=[
#                 {
#                     "role": "system",
#                     "content": (
#                         "You are an autonomous research agent. "
#                         "Provide concise, evidence-based information."
#                     )
#                 },
#                 {
#                     "role": "user",
#                     "content": prompt
#                 }
#             ],
#             temperature=0.2
#         )

#         message = response.choices[0].message

#         if message.content:
#             return message.content

#         return (
#             "⚠️ Research completed but "
#             "no research text was returned."
#         )

#     except Exception as e:

#         error = str(e)

#         if "rate_limit_exceeded" in error:

#             return (
#                 "⚠️ RATE_LIMIT_REACHED: "
#                 "Groq token limit has been reached."
#             )

#         return f"❌ RESEARCH_ERROR: {error}"


# # ==========================================
# # MAIN PROGRAM
# # ==========================================

# print()

# print("🔎 DEEPRESEARCH AI")
# print("=" * 60)

# question = input(
#     "\nEnter your research topic: "
# )

# if not question.strip():

#     print(
#         "❌ Please enter a research topic."
#     )

#     exit()


# # ==========================================
# # CREATE RESEARCH PLAN
# # ==========================================

# print(
#     "\n🧠 Creating research plan...\n"
# )

# try:

#     plan = create_research_plan(question)

# except Exception as e:

#     print(
#         "❌ Planner Agent Error:"
#     )

#     print(e)

#     exit()


# # ==========================================
# # DISPLAY PLAN
# # ==========================================

# print("=" * 60)
# print("📋 RESEARCH PLAN")
# print("=" * 60)

# research_areas = plan.get(
#     "research_areas",
#     []
# )

# for i, area in enumerate(
#     research_areas,
#     start=1
# ):

#     print(
#         f"\n{i}. {area['title']}"
#     )

#     print(
#         f"   Question: {area['question']}"
#     )


# # ==========================================
# # START RESEARCH
# # ==========================================

# print("\n")
# print("=" * 60)
# print("🌐 STARTING RESEARCH")
# print("=" * 60)

# research_results = []


# for i, area in enumerate(
#     research_areas,
#     start=1
# ):

#     title = area["title"]

#     research_question_text = (
#         area["question"]
#     )

#     print(
#         f"\n🔎 Researching "
#         f"{i}/{len(research_areas)}: "
#         f"{title}"
#     )

#     result = research_question(
#         research_question_text
#     )


#     # ==================================
#     # RATE LIMIT CHECK
#     # ==================================

#     if result.startswith(
#         "⚠️ RATE_LIMIT_REACHED"
#     ):

#         print(
#             "   ⚠️ Groq token limit reached."
#         )

#         print(
#             "   Stopping further research calls."
#         )

#         break


#     # ==================================
#     # SAVE RESULT
#     # ==================================

#     research_results.append(
#         {
#             "title": title,
#             "question": research_question_text,
#             "result": result
#         }
#     )

#     print(
#         "   ✅ Completed"
#     )


# # ==========================================
# # SAVE TO KNOWLEDGE BASE
# # ==========================================

# if research_results:

#     print("\n")
#     print("=" * 60)
#     print("💾 SAVING RESEARCH")
#     print("=" * 60)

#     save_research(
#         research_results
#     )

# else:

#     print(
#         "\n⚠️ No research results were collected."
#     )


# # ==========================================
# # DISPLAY RESULTS
# # ==========================================

# print("\n")
# print("=" * 60)
# print("📚 RESEARCH RESULTS")
# print("=" * 60)


# for i, result in enumerate(
#     research_results,
#     start=1
# ):

#     print(
#         f"\n### {i}. "
#         f"{result['title']}"
#     )

#     print(
#         "-" * 60
#     )

#     print(
#         "Research Question:"
#     )

#     print(
#         result["question"]
#     )

#     print(
#         "\nResearch Findings:"
#     )

#     print(
#         result["result"]
#     )


# # ==========================================
# # FINISHED
# # ==========================================

# print("\n")
# print("=" * 60)
# print("✅ MCP-INTEGRATED DEEPRESEARCH COMPLETE")
# print("=" * 60)

import os
import json

from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from groq import Groq

from knowledge_base import save_research
from mcp_integration import mcp_research_search


# ==========================================
# FLASK APPLICATION
# ==========================================

app = Flask(__name__)


# ==========================================
# LOAD API KEY
# ==========================================

load_dotenv(
    r"C:\Users\MAHESH\OneDrive\Dokumen\DeepResearchAI\.env"
)

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("❌ GROQ_API_KEY not found in .env")


# ==========================================
# GROQ CLIENT
# ==========================================

client = Groq(
    api_key=api_key
) if api_key else None

MODEL = "openai/gpt-oss-20b"


# ==========================================
# HOME PAGE
# ==========================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# ==========================================
# PLANNER AGENT
# ==========================================

def create_research_plan(question):

    prompt = f"""
You are an expert research planning agent.

The user wants to research this topic:

"{question}"

Break this topic into exactly 5 important research areas.

For each area provide:

1. A short title
2. A clear research question

IMPORTANT:

Return ONLY valid JSON.

Do not use Markdown.
Do not write ```json.
Do not add explanations.

Use this structure:

{{
    "main_topic": "{question}",
    "research_areas": [
        {{
            "title": "Area title",
            "question": "Research question"
        }}
    ]
}}
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a professional research "
                    "planning agent. Always return "
                    "valid JSON only."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    result = response.choices[0].message.content.strip()

    # Remove Markdown code fences
    if result.startswith("```"):

        result = result.replace(
            "```json",
            ""
        )

        result = result.replace(
            "```",
            ""
        )

        result = result.strip()

    return json.loads(result)


# ==========================================
# RESEARCH AGENT
# ==========================================

def research_question(question):

    print(
        f"🔎 Researching: {question}"
    )

    # --------------------------------------
    # MCP RESEARCH
    # --------------------------------------

    try:

        mcp_result = mcp_research_search(
            question
        )

        if mcp_result:

            print(
                "   ✅ MCP research tool used"
            )

            return mcp_result

    except Exception as e:

        print(
            f"   ⚠️ MCP error: {e}"
        )


    # --------------------------------------
    # FALLBACK
    # --------------------------------------

    prompt = f"""
Research this question:

{question}

Provide:

- 3 to 5 important findings
- Important evidence or statistics
- Important sources
- URLs when available

Keep the answer concise.
"""

    try:

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an evidence-based "
                        "research assistant."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2
        )

        content = (
            response
            .choices[0]
            .message
            .content
        )

        if content:

            return content

        return (
            "No research information returned."
        )

    except Exception as e:

        error = str(e)

        if "rate_limit_exceeded" in error:

            return (
                "⚠️ RATE_LIMIT_REACHED: "
                "Groq token limit has been reached."
            )

        return (
            f"❌ RESEARCH_ERROR: {error}"
        )


# ==========================================
# RESEARCH API
# ==========================================

@app.route(
    "/research",
    methods=["POST"]
)
def research():

    try:

        # ----------------------------------
        # GET REQUEST DATA
        # ----------------------------------

        data = request.get_json()

        if not data:

            return jsonify({
                "error":
                "No request data received."
            }), 400


        question = data.get(
            "question",
            ""
        ).strip()


        if not question:

            return jsonify({
                "error":
                "Research question is empty."
            }), 400


        print()
        print("=" * 60)
        print(
            "🔬 NEW RESEARCH REQUEST"
        )
        print("=" * 60)

        print(
            f"Topic: {question}"
        )


        # ----------------------------------
        # CREATE PLAN
        # ----------------------------------

        print(
            "\n🧠 Creating research plan..."
        )

        plan = create_research_plan(
            question
        )


        research_areas = (
            plan.get(
                "research_areas",
                []
            )
        )


        print(
            f"📋 Created "
            f"{len(research_areas)} "
            f"research areas."
        )


        # ----------------------------------
        # RESEARCH AREAS
        # ----------------------------------

        research_results = []


        for i, area in enumerate(
            research_areas,
            start=1
        ):

            title = area.get(
                "title",
                f"Research Area {i}"
            )

            research_question_text = (
                area.get(
                    "question",
                    ""
                )
            )


            print(
                f"\n🔎 Researching "
                f"{i}/{len(research_areas)}: "
                f"{title}"
            )


            result = research_question(
                research_question_text
            )


            # Stop if rate limit occurs

            if result.startswith(
                "⚠️ RATE_LIMIT_REACHED"
            ):

                print(
                    "⚠️ Groq rate limit reached."
                )

                break


            research_results.append({

                "title": title,

                "question":
                    research_question_text,

                "result": result

            })


        # ----------------------------------
        # SAVE RESULTS
        # ----------------------------------

        if research_results:

            print(
                "\n💾 Saving research..."
            )

            save_research(
                research_results
            )


        # ----------------------------------
        # RETURN JSON
        # ----------------------------------

        print(
            "\n✅ Research completed."
        )


        return jsonify({

            "success": True,

            "question": question,

            "plan": plan,

            "results":
                research_results

        })


    except Exception as e:

        print(
            "\n❌ RESEARCH ERROR:"
        )

        print(e)


        return jsonify({

            "success": False,

            "error": str(e)

        }), 500


# ==========================================
# RUN FLASK
# ==========================================

if __name__ == "__main__":

    print()
    print("=" * 60)
    print("🔬 DEEPRESEARCH AI")
    print("=" * 60)

    print(
        "🌐 Starting web server..."
    )

    print(
        "📍 http://127.0.0.1:5000"
    )

    print("=" * 60)

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )