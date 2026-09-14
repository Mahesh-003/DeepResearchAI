# # import os
# # import json

# # from flask import Flask, render_template, request, jsonify
# # from dotenv import load_dotenv
# # from groq import Groq

# # from knowledge_base import save_research
# # from mcp_integration import mcp_research_search


# # # ==========================================
# # # FLASK APPLICATION
# # # ==========================================

# # app = Flask(__name__)


# # # ==========================================
# # # LOAD API KEY
# # # ==========================================

# # load_dotenv(
# #     r"C:\Users\MAHESH\OneDrive\Dokumen\DeepResearchAI\.env"
# # )

# # api_key = os.getenv("GROQ_API_KEY")

# # if not api_key:
# #     print("❌ GROQ_API_KEY not found in .env")


# # # ==========================================
# # # GROQ CLIENT
# # # ==========================================

# # client = Groq(
# #     api_key=api_key
# # ) if api_key else None

# # MODEL = "openai/gpt-oss-20b"


# # # ==========================================
# # # HOME PAGE
# # # ==========================================

# # @app.route("/")
# # def home():

# #     return render_template(
# #         "index.html"
# #     )


# # # ==========================================
# # # PLANNER AGENT
# # # ==========================================

# # def create_research_plan(question):

# #     prompt = f"""
# # You are an expert research planning agent.

# # The user wants to research this topic:

# # "{question}"

# # Break this topic into exactly 5 important research areas.

# # For each area provide:

# # 1. A short title
# # 2. A clear research question

# # IMPORTANT:

# # Return ONLY valid JSON.

# # Do not use Markdown.
# # Do not write ```json.
# # Do not add explanations.

# # Use this structure:

# # {{
# #     "main_topic": "{question}",
# #     "research_areas": [
# #         {{
# #             "title": "Area title",
# #             "question": "Research question"
# #         }}
# #     ]
# # }}
# # """

# #     response = client.chat.completions.create(
# #         model=MODEL,
# #         messages=[
# #             {
# #                 "role": "system",
# #                 "content": (
# #                     "You are a professional research "
# #                     "planning agent. Always return "
# #                     "valid JSON only."
# #                 )
# #             },
# #             {
# #                 "role": "user",
# #                 "content": prompt
# #             }
# #         ],
# #         temperature=0
# #     )

# #     result = response.choices[0].message.content.strip()

# #     # Remove Markdown code fences
# #     if result.startswith("```"):

# #         result = result.replace(
# #             "```json",
# #             ""
# #         )

# #         result = result.replace(
# #             "```",
# #             ""
# #         )

# #         result = result.strip()

# #     return json.loads(result)


# # # ==========================================
# # # RESEARCH AGENT
# # # ==========================================

# # def research_question(question):

# #     print(
# #         f"🔎 Researching: {question}"
# #     )

# #     # --------------------------------------
# #     # MCP RESEARCH
# #     # --------------------------------------

# #     try:

# #         mcp_result = mcp_research_search(
# #             question
# #         )

# #         if mcp_result:

# #             print(
# #                 "   ✅ MCP research tool used"
# #             )

# #             return mcp_result

# #     except Exception as e:

# #         print(
# #             f"   ⚠️ MCP error: {e}"
# #         )


# #     # --------------------------------------
# #     # FALLBACK
# #     # --------------------------------------

# #     prompt = f"""
# # Research this question:

# # {question}

# # Provide:

# # - 3 to 5 important findings
# # - Important evidence or statistics
# # - Important sources
# # - URLs when available

# # Keep the answer concise.
# # """

# #     try:

# #         response = client.chat.completions.create(
# #             model=MODEL,
# #             messages=[
# #                 {
# #                     "role": "system",
# #                     "content": (
# #                         "You are an evidence-based "
# #                         "research assistant."
# #                     )
# #                 },
# #                 {
# #                     "role": "user",
# #                     "content": prompt
# #                 }
# #             ],
# #             temperature=0.2
# #         )

# #         content = (
# #             response
# #             .choices[0]
# #             .message
# #             .content
# #         )

# #         if content:

# #             return content

# #         return (
# #             "No research information returned."
# #         )

# #     except Exception as e:

# #         error = str(e)

# #         if "rate_limit_exceeded" in error:

# #             return (
# #                 "⚠️ RATE_LIMIT_REACHED: "
# #                 "Groq token limit has been reached."
# #             )

# #         return (
# #             f"❌ RESEARCH_ERROR: {error}"
# #         )


# # # ==========================================
# # # RESEARCH API
# # # ==========================================

# # @app.route(
# #     "/research",
# #     methods=["POST"]
# # )
# # def research():

# #     try:

# #         # ----------------------------------
# #         # GET REQUEST DATA
# #         # ----------------------------------

# #         data = request.get_json()

# #         if not data:

# #             return jsonify({
# #                 "error":
# #                 "No request data received."
# #             }), 400


# #         question = data.get(
# #             "question",
# #             ""
# #         ).strip()


# #         if not question:

# #             return jsonify({
# #                 "error":
# #                 "Research question is empty."
# #             }), 400


# #         print()
# #         print("=" * 60)
# #         print(
# #             "🔬 NEW RESEARCH REQUEST"
# #         )
# #         print("=" * 60)

# #         print(
# #             f"Topic: {question}"
# #         )


# #         # ----------------------------------
# #         # CREATE PLAN
# #         # ----------------------------------

# #         print(
# #             "\n🧠 Creating research plan..."
# #         )

# #         plan = create_research_plan(
# #             question
# #         )


# #         research_areas = (
# #             plan.get(
# #                 "research_areas",
# #                 []
# #             )
# #         )


# #         print(
# #             f"📋 Created "
# #             f"{len(research_areas)} "
# #             f"research areas."
# #         )


# #         # ----------------------------------
# #         # RESEARCH AREAS
# #         # ----------------------------------

# #         research_results = []


# #         for i, area in enumerate(
# #             research_areas,
# #             start=1
# #         ):

# #             title = area.get(
# #                 "title",
# #                 f"Research Area {i}"
# #             )

# #             research_question_text = (
# #                 area.get(
# #                     "question",
# #                     ""
# #                 )
# #             )


# #             print(
# #                 f"\n🔎 Researching "
# #                 f"{i}/{len(research_areas)}: "
# #                 f"{title}"
# #             )


# #             result = research_question(
# #                 research_question_text
# #             )


# #             # Stop if rate limit occurs

# #             if result.startswith(
# #                 "⚠️ RATE_LIMIT_REACHED"
# #             ):

# #                 print(
# #                     "⚠️ Groq rate limit reached."
# #                 )

# #                 break


# #             research_results.append({

# #                 "title": title,

# #                 "question":
# #                     research_question_text,

# #                 "result": result

# #             })


# #         # ----------------------------------
# #         # SAVE RESULTS
# #         # ----------------------------------

# #         if research_results:

# #             print(
# #                 "\n💾 Saving research..."
# #             )

# #             save_research(
# #                 research_results
# #             )


# #         # ----------------------------------
# #         # RETURN JSON
# #         # ----------------------------------

# #         print(
# #             "\n✅ Research completed."
# #         )


# #         return jsonify({

# #             "success": True,

# #             "question": question,

# #             "plan": plan,

# #             "results":
# #                 research_results

# #         })


# #     except Exception as e:

# #         print(
# #             "\n❌ RESEARCH ERROR:"
# #         )

# #         print(e)


# #         return jsonify({

# #             "success": False,

# #             "error": str(e)

# #         }), 500


# # # ==========================================
# # # RUN FLASK
# # # ==========================================

# # if __name__ == "__main__":

# #     print()
# #     print("=" * 60)
# #     print("🔬 DEEPRESEARCH AI")
# #     print("=" * 60)

# #     print(
# #         "🌐 Starting web server..."
# #     )

# #     print(
# #         "📍 http://127.0.0.1:5000"
# #     )

# #     print("=" * 60)

# #     app.run(
# #         host="127.0.0.1",
# #         port=5000,
# #         debug=True
# #     )

# import os
# import json

# from flask import Flask, render_template, request, jsonify
# from dotenv import load_dotenv
# from groq import Groq

# from knowledge_base import save_research
# from mcp_integration import mcp_research_search


# # ============================================================
# # FLASK APPLICATION
# # ============================================================

# app = Flask(__name__)


# # ============================================================
# # LOAD API KEY
# # ============================================================

# load_dotenv(
#     r"C:\Users\MAHESH\OneDrive\Dokumen\DeepResearchAI\.env"
# )

# api_key = os.getenv("GROQ_API_KEY")

# if not api_key:
#     print("❌ GROQ_API_KEY not found in .env")


# # ============================================================
# # GROQ CLIENT
# # ============================================================

# client = Groq(api_key=api_key) if api_key else None

# MODEL = "openai/gpt-oss-20b"


# # ============================================================
# # HOME PAGE
# # ============================================================

# @app.route("/")
# def home():
#     return render_template("index.html")


# # ============================================================
# # SIMPLE ANSWER
# # ============================================================

# def simple_answer(question):

#     print("💬 Simple question detected.")
#     print("⚡ Giving direct answer...")

#     prompt = f"""
# You are DeepResearch AI.

# Answer this question directly:

# "{question}"

# IMPORTANT RULES:

# - Keep the answer SHORT.
# - For a simple definition, use 2-3 sentences.
# - For a basic explanation, use 3-5 sentences.
# - Use simple language.
# - Give ONE real-life example when useful.
# - Do NOT perform web research.
# - Do NOT create a research report.
# - Do NOT provide unnecessary statistics.
# - Do NOT provide unnecessary sources.
# - Do NOT repeat the question.
# - Answer ONLY what the user asked.

# The user wants a quick and useful answer.
# """

#     try:

#         response = client.chat.completions.create(
#             model=MODEL,
#             messages=[
#                 {
#                     "role": "system",
#                     "content": (
#                         "You are a concise AI assistant. "
#                         "Give short, useful answers."
#                     )
#                 },
#                 {
#                     "role": "user",
#                     "content": prompt
#                 }
#             ],
#             temperature=0.2,
#             max_tokens=250
#         )

#         content = response.choices[0].message.content

#         if content:
#             return content.strip()

#         return "Sorry, I could not generate an answer."

#     except Exception as e:

#         error = str(e)

#         if "rate_limit_exceeded" in error.lower():
#             return (
#                 "⚠️ API rate limit reached. "
#                 "Please try again later."
#             )

#         return f"❌ AI ERROR: {error}"


# # ============================================================
# # CHECK IF USER WANTS DEEP RESEARCH
# # ============================================================

# def is_deep_research(question):

#     question = question.lower().strip()

#     research_keywords = [

#         "deep research",
#         "detailed research",
#         "research report",
#         "do research",
#         "research on",
#         "research about",

#         "latest information",
#         "latest research",
#         "current information",
#         "recent information",

#         "detailed analysis",
#         "comprehensive analysis",
#         "in-depth analysis",

#         "statistics",
#         "statistical analysis",

#         "compare",
#         "comparison",

#         "advantages and disadvantages",

#         "sources",
#         "evidence",

#         "literature review",

#         "market research",
#         "case study"
#     ]

#     for keyword in research_keywords:

#         if keyword in question:
#             return True

#     return False


# # ============================================================
# # PLANNER AGENT
# # ============================================================

# def create_research_plan(question):

#     prompt = f"""
# You are an expert research planning agent.

# The user wants deep research on:

# "{question}"

# Break the topic into exactly 5 important research areas.

# For each area provide:

# 1. A short title
# 2. A clear research question

# IMPORTANT:

# Return ONLY valid JSON.

# Do not use Markdown.
# Do not use ```json.
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

#     try:

#         response = client.chat.completions.create(
#             model=MODEL,

#             messages=[
#                 {
#                     "role": "system",
#                     "content": (
#                         "You are a professional research "
#                         "planning agent. Always return "
#                         "valid JSON only."
#                     )
#                 },
#                 {
#                     "role": "user",
#                     "content": prompt
#                 }
#             ],

#             temperature=0,
#             max_tokens=700
#         )

#         result = response.choices[0].message.content.strip()

#         # Remove Markdown fences if model adds them

#         if result.startswith("```"):

#             result = result.replace("```json", "")
#             result = result.replace("```", "")
#             result = result.strip()

#         return json.loads(result)

#     except Exception as e:

#         print(f"❌ Planner error: {e}")

#         return {
#             "main_topic": question,
#             "research_areas": [
#                 {
#                     "title": "Main Research",
#                     "question": question
#                 }
#             ]
#         }


# # ============================================================
# # RESEARCH AGENT
# # ============================================================

# def research_question(question):

#     print(f"🔎 Researching: {question}")

#     # --------------------------------------------------------
#     # MCP RESEARCH
#     # --------------------------------------------------------

#     try:

#         mcp_result = mcp_research_search(question)

#         if mcp_result:

#             print("   ✅ MCP research tool used")

#             return mcp_result

#     except Exception as e:

#         print(f"   ⚠️ MCP error: {e}")


#     # --------------------------------------------------------
#     # FALLBACK LLM RESEARCH
#     # --------------------------------------------------------

#     prompt = f"""
# Research this question:

# {question}

# Provide:

# - Important findings
# - Relevant evidence
# - Statistics only when reliable
# - Important sources
# - URLs when available

# Keep the answer focused and concise.
# Do not add unnecessary information.
# """

#     try:

#         response = client.chat.completions.create(
#             model=MODEL,

#             messages=[
#                 {
#                     "role": "system",
#                     "content": (
#                         "You are an evidence-based "
#                         "research assistant."
#                     )
#                 },
#                 {
#                     "role": "user",
#                     "content": prompt
#                 }
#             ],

#             temperature=0.2,
#             max_tokens=700
#         )

#         content = response.choices[0].message.content

#         if content:
#             return content.strip()

#         return "No research information returned."

#     except Exception as e:

#         error = str(e)

#         if "rate_limit_exceeded" in error.lower():

#             return (
#                 "⚠️ RATE_LIMIT_REACHED: "
#                 "Groq token limit has been reached."
#             )

#         return f"❌ RESEARCH_ERROR: {error}"


# # ============================================================
# # RESEARCH API
# # ============================================================

# @app.route("/research", methods=["POST"])
# def research():

#     try:

#         # ----------------------------------------------------
#         # GET REQUEST
#         # ----------------------------------------------------

#         data = request.get_json()

#         if not data:

#             return jsonify({
#                 "success": False,
#                 "error": "No request data received."
#             }), 400


#         question = data.get(
#             "question",
#             ""
#         ).strip()


#         if not question:

#             return jsonify({
#                 "success": False,
#                 "error": "Question is empty."
#             }), 400


#         print()
#         print("=" * 60)
#         print("🔬 NEW REQUEST")
#         print("=" * 60)
#         print(f"Question: {question}")


#         # ====================================================
#         # SIMPLE QUESTION
#         # ====================================================

#         if not is_deep_research(question):

#             print()
#             print("⚡ MODE: QUICK ANSWER")

#             answer = simple_answer(question)

#             print()
#             print("✅ Quick answer completed.")
#             print("=" * 60)

#             return jsonify({

#                 "success": True,

#                 "mode": "quick",

#                 "question": question,

#                 "answer": answer,

#                 "plan": None,

#                 "results": []

#             })


#         # ====================================================
#         # DEEP RESEARCH
#         # ====================================================

#         print()
#         print("🔬 MODE: DEEP RESEARCH")


#         # ----------------------------------------------------
#         # CREATE PLAN
#         # ----------------------------------------------------

#         print()
#         print("🧠 Creating research plan...")

#         plan = create_research_plan(question)

#         research_areas = plan.get(
#             "research_areas",
#             []
#         )

#         print(
#             f"📋 Created {len(research_areas)} research areas."
#         )


#         # ----------------------------------------------------
#         # RESEARCH EACH AREA
#         # ----------------------------------------------------

#         research_results = []


#         for i, area in enumerate(
#             research_areas,
#             start=1
#         ):

#             title = area.get(
#                 "title",
#                 f"Research Area {i}"
#             )

#             research_question_text = area.get(
#                 "question",
#                 ""
#             )


#             print()
#             print(
#                 f"🔎 Researching "
#                 f"{i}/{len(research_areas)}: "
#                 f"{title}"
#             )


#             result = research_question(
#                 research_question_text
#             )


#             # Stop if rate limit occurs

#             if result.startswith(
#                 "⚠️ RATE_LIMIT_REACHED"
#             ):

#                 print(
#                     "⚠️ Groq rate limit reached."
#                 )

#                 break


#             research_results.append({

#                 "title": title,

#                 "question":
#                     research_question_text,

#                 "result": result

#             })


#         # ----------------------------------------------------
#         # SAVE RESULTS
#         # ----------------------------------------------------

#         if research_results:

#             print()
#             print("💾 Saving research...")

#             try:

#                 save_research(
#                     research_results
#                 )

#                 print("✅ Research saved.")

#             except Exception as e:

#                 print(
#                     f"⚠️ Could not save research: {e}"
#                 )


#         # ----------------------------------------------------
#         # RETURN RESPONSE
#         # ----------------------------------------------------

#         print()
#         print("✅ Deep research completed.")
#         print("=" * 60)


#         return jsonify({

#             "success": True,

#             "mode": "research",

#             "question": question,

#             "answer": None,

#             "plan": plan,

#             "results":
#                 research_results

#         })


#     except Exception as e:

#         print()
#         print("❌ APPLICATION ERROR")
#         print(e)


#         return jsonify({

#             "success": False,

#             "error": str(e)

#         }), 500


# # ============================================================
# # RUN FLASK
# # ============================================================

# if __name__ == "__main__":

#     print()

#     print("=" * 60)
#     print("🔬 DEEPRESEARCH AI")
#     print("=" * 60)

#     print(
#         "🌐 Starting web server..."
#     )

#     print(
#         "📍 http://127.0.0.1:5000"
#     )

#     print("=" * 60)


#     app.run(
#         host="127.0.0.1",
#         port=5000,
#         debug=True
#     )

import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from groq import Groq

# MCP is optional
try:
    from mcp_integration import mcp_research_search
    MCP_AVAILABLE = True
except Exception as e:
    print("⚠️ MCP not available:", e)
    MCP_AVAILABLE = False


# =========================================================
# FLASK APPLICATION
# =========================================================

app = Flask(__name__)


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

# .env should be inside the project folder
# DeepResearchAI/
#     .env
#     app.py

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("❌ GROQ_API_KEY not found in .env")
    client = None
else:
    client = Groq(api_key=api_key)


# =========================================================
# MODEL
# =========================================================

MODEL = "openai/gpt-oss-20b"


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def home():
    return render_template("index.html")


# =========================================================
# CHECK IF USER WANTS DEEP RESEARCH
# =========================================================

def is_deep_research(question):

    keywords = [
        "deep research",
        "research report",
        "detailed research",
        "latest research",
        "research on",
        "compare",
        "comparison",
        "statistics",
        "sources",
        "evidence",
        "latest",
        "recent developments",
        "market analysis",
        "literature review"
    ]

    question_lower = question.lower()

    return any(
        keyword in question_lower
        for keyword in keywords
    )


# =========================================================
# SHORT AI ANSWER
# =========================================================

def generate_short_answer(question):

    if not client:
        return "❌ GROQ_API_KEY is not configured."

    prompt = f"""
You are a concise AI assistant.

User question:
{question}

Answer the question directly.

Rules:
- Keep the answer SHORT.
- Simple definition: 2-3 sentences.
- Basic explanation: maximum 5 sentences.
- Give ONE real-life example when useful.
- Do not repeat the question.
- Do not create a long report.
- Do not add unnecessary headings.
- Use simple language.
- Answer only what the user asked.
"""

    try:

        response = client.chat.completions.create(
            model=MODEL,

            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a concise and helpful AI assistant. "
                        "Never provide unnecessary information."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.2,
            max_tokens=250
        )

        answer = response.choices[0].message.content

        if answer:
            return answer.strip()

        return "No answer was generated."

    except Exception as e:

        print("❌ Groq Error:", e)

        if "rate_limit" in str(e).lower():
            return "⚠️ API rate limit reached. Please try again later."

        return f"❌ Error: {str(e)}"


# =========================================================
# MCP RESEARCH
# =========================================================

def perform_mcp_research(question):

    if not MCP_AVAILABLE:
        return None

    try:

        print("🔎 Trying MCP research...")

        result = mcp_research_search(question)

        if result is None:
            print("⚠️ MCP returned None")
            return None

        result = str(result).strip()

        invalid_results = [
            "",
            "none",
            "no results found.",
            "no research results were returned.",
            "no research information returned."
        ]

        if result.lower() in invalid_results:
            print("⚠️ MCP returned no useful information")
            return None

        print("✅ MCP returned research")
        return result

    except Exception as e:

        print("⚠️ MCP Error:", e)
        return None


# =========================================================
# DEEP RESEARCH FALLBACK
# =========================================================

def generate_research_answer(question):

    if not client:
        return "❌ GROQ_API_KEY is not configured."

    prompt = f"""
You are a research assistant.

Research question:
{question}

Provide a concise research-oriented answer.

Rules:
- Give 3 important findings.
- Give important facts or evidence when known.
- Mention important sources only when you actually know them.
- Do not invent statistics.
- Do not invent URLs.
- Keep the response under 400 words.
- Use simple language.
- Focus only on the research question.
"""

    try:

        response = client.chat.completions.create(
            model=MODEL,

            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an evidence-based research assistant. "
                        "Be concise and do not invent sources."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.2,
            max_tokens=500
        )

        answer = response.choices[0].message.content

        if answer:
            return answer.strip()

        return "No research answer was generated."

    except Exception as e:

        print("❌ Research fallback error:", e)

        if "rate_limit" in str(e).lower():
            return "⚠️ API rate limit reached."

        return f"❌ Error: {str(e)}"


# =========================================================
# MAIN RESEARCH FUNCTION
# =========================================================

def research_question(question):

    print()
    print("=" * 60)
    print("🔎 PROCESSING QUESTION")
    print("=" * 60)
    print("Question:", question)

    # -----------------------------------------------------
    # SIMPLE QUESTION
    # -----------------------------------------------------

    if not is_deep_research(question):

        print("⚡ Mode: QUICK ANSWER")

        answer = generate_short_answer(question)

        return {
            "mode": "quick",
            "answer": answer
        }


    # -----------------------------------------------------
    # DEEP RESEARCH
    # -----------------------------------------------------

    print("🔬 Mode: DEEP RESEARCH")

    # First try MCP
    mcp_result = perform_mcp_research(question)

    if mcp_result:

        return {
            "mode": "research",
            "answer": mcp_result,
            "source": "MCP Research Tool"
        }

    # If MCP fails, use Groq fallback
    print("➡️ Using Groq research fallback")

    answer = generate_research_answer(question)

    return {
        "mode": "research",
        "answer": answer,
        "source": "Groq LLM"
    }


# =========================================================
# RESEARCH API
# =========================================================

@app.route("/research", methods=["POST"])
def research():

    try:

        # -------------------------------------------------
        # GET JSON DATA
        # -------------------------------------------------

        data = request.get_json()

        if not data:

            return jsonify({
                "success": False,
                "error": "No request data received."
            }), 400


        question = data.get(
            "question",
            ""
        ).strip()


        # -------------------------------------------------
        # EMPTY QUESTION
        # -------------------------------------------------

        if not question:

            return jsonify({
                "success": False,
                "error": "Please enter a research question."
            }), 400


        # -------------------------------------------------
        # PROCESS
        # -------------------------------------------------

        result = research_question(question)


        print()
        print("✅ RESPONSE GENERATED")
        print("=" * 60)


        # -------------------------------------------------
        # RETURN RESPONSE
        # -------------------------------------------------

        return jsonify({

            "success": True,

            "question": question,

            "mode": result.get(
                "mode",
                "quick"
            ),

            "answer": result.get(
                "answer",
                "No answer generated."
            ),

            "source": result.get(
                "source",
                "Groq LLM"
            ),

            # Compatibility with your existing frontend
            "results": [
                {
                    "title": (
                        "AI Answer"
                        if result.get("mode") == "quick"
                        else "Research Findings"
                    ),

                    "question": question,

                    "result": result.get(
                        "answer",
                        "No answer generated."
                    )
                }
            ],

            "plan": {
                "main_topic": question,
                "research_areas": []
            }

        })


    except Exception as e:

        print()
        print("❌ RESEARCH ERROR")
        print(e)

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500


# =========================================================
# HEALTH CHECK
# =========================================================

@app.route("/health")
def health():

    return jsonify({

        "status": "running",

        "groq": (
            "connected"
            if client
            else "not configured"
        ),

        "mcp": (
            "connected"
            if MCP_AVAILABLE
            else "not available"
        ),

        "model": MODEL

    })


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    print()
    print("=" * 60)
    print("🔬 DEEPRESEARCH AI")
    print("=" * 60)

    print(
        "🤖 Model:",
        MODEL
    )

    print(
        "🔑 Groq:",
        "Connected" if client else "Not configured"
    )

    print(
        "🔌 MCP:",
        "Available" if MCP_AVAILABLE else "Not available"
    )

    print()
    print(
        "🌐 http://127.0.0.1:5000"
    )

    print("=" * 60)

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )