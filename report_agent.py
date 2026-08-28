import os
from dotenv import load_dotenv
from groq import Groq

from retriever import retrieve_relevant_research
from analysis_agent import analyze_research


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
# FINAL REPORT AGENT
# ==========================================

def create_report(question):

    # --------------------------------------
    # GET RESEARCH
    # --------------------------------------

    documents = retrieve_relevant_research(question)

    if not documents:
        return "❌ No relevant research found."


    # --------------------------------------
    # GET ANALYSIS
    # --------------------------------------

    analysis = analyze_research(question)

    if analysis.startswith("❌"):
        return analysis


    # --------------------------------------
    # BUILD RESEARCH CONTEXT
    # --------------------------------------

    research_context = ""

    for i, document in enumerate(
        documents,
        start=1
    ):

        research_context += f"""

SOURCE {i}

Title:
{document.get("title", "")}

Question:
{document.get("question", "")}

Findings:
{document.get("result", "")}

----------------------------------------
"""


    # --------------------------------------
    # REPORT PROMPT
    # --------------------------------------

    prompt = f"""
You are a professional research report writer.

Create a clear and well-structured research report
using the research and analysis provided below.

RESEARCH QUESTION:
{question}

RESEARCH:
{research_context}

ANALYSIS:
{analysis}

Create the report using this structure:

# Research Report

## 1. Executive Summary

Give a short summary of the research.

## 2. Introduction

Explain the topic and why it is important.

## 3. Key Findings

Present the most important research findings.

## 4. Detailed Analysis

Explain the major patterns, trends,
evidence and differences.

## 5. Benefits and Opportunities

Explain the major benefits and opportunities.

## 6. Challenges and Limitations

Explain important limitations,
risks and challenges.

## 7. Practical Implications

Explain how the findings can be applied
in real-world situations.

## 8. Conclusion

Give a concise overall conclusion.

## 9. Sources

List the sources mentioned in the research.

IMPORTANT:
- Use only the provided research and analysis.
- Do not invent sources or statistics.
- Do not introduce unsupported facts.
- Keep the writing professional.
- Use clear headings and bullet points where useful.
"""


    # --------------------------------------
    # GENERATE REPORT
    # --------------------------------------

    try:

        response = client.chat.completions.create(
            model=MODEL,

            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a professional research "
                        "report writer. Create accurate, "
                        "well-structured reports."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.2
        )

        return response.choices[0].message.content


    except Exception as e:

        return f"❌ REPORT ERROR:\n{e}"


# ==========================================
# TEST REPORT AGENT
# ==========================================

if __name__ == "__main__":

    print()
    print("📝 DEEPRESEARCH AI - REPORT AGENT")
    print("=" * 60)

    question = input(
        "\nEnter research topic: "
    )

    if not question.strip():

        print("❌ Please enter a research topic.")
        exit()


    print()
    print("🔍 Collecting research...")
    print()

    report = create_report(question)


    print("=" * 60)
    print("📄 FINAL RESEARCH REPORT")
    print("=" * 60)

    print(report)

    print()
    print("=" * 60)
    print("✅ REPORT GENERATION COMPLETE")
    print("=" * 60)