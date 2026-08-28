import os
from dotenv import load_dotenv
from groq import Groq

from retriever import retrieve_relevant_research


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
# ANALYSIS AGENT
# ==========================================

def analyze_research(question):

    # --------------------------------------
    # RETRIEVE RESEARCH
    # --------------------------------------

    documents = retrieve_relevant_research(question)

    if not documents:

        return "❌ No relevant research found."


    # --------------------------------------
    # BUILD RESEARCH CONTEXT
    # --------------------------------------

    context = ""

    for i, document in enumerate(
        documents,
        start=1
    ):

        context += f"""

RESEARCH SOURCE {i}

Title:
{document.get("title", "")}

Research Question:
{document.get("question", "")}

Findings:
{document.get("result", "")}

----------------------------------------
"""


    # --------------------------------------
    # ANALYSIS PROMPT
    # --------------------------------------

    prompt = f"""
You are an expert AI research analyst.

Analyze the research information below
to answer the user's question.

USER QUESTION:
{question}

RESEARCH INFORMATION:
{context}

Perform the following analysis:

1. Identify the most important findings.
2. Identify common patterns or trends.
3. Identify differences or contradictions.
4. Evaluate the strength of the evidence.
5. Identify important limitations.
6. Provide practical insights.
7. Give a clear overall conclusion.

IMPORTANT:
- Use only the provided research.
- Do not invent facts.
- Clearly distinguish evidence from interpretation.
- If evidence is insufficient, say so.

Structure your answer as:

## Key Findings

## Patterns and Trends

## Differences or Contradictions

## Evidence Assessment

## Limitations

## Practical Insights

## Overall Conclusion
"""


    # --------------------------------------
    # CALL LLM
    # --------------------------------------

    try:

        response = client.chat.completions.create(
            model=MODEL,

            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a professional research "
                        "analysis agent. Analyze evidence "
                        "carefully and do not invent facts."
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

        return f"❌ ANALYSIS ERROR:\n{e}"


# ==========================================
# TEST ANALYSIS AGENT
# ==========================================

if __name__ == "__main__":

    print()
    print("🧠 DEEPRESEARCH AI - ANALYSIS AGENT")
    print("=" * 60)

    question = input(
        "\nEnter a research question: "
    )

    if not question.strip():

        print("❌ Please enter a question.")
        exit()


    print()
    print("🔍 Retrieving research...")
    print()

    analysis = analyze_research(question)


    print("=" * 60)
    print("📊 RESEARCH ANALYSIS")
    print("=" * 60)

    print(analysis)

    print()
    print("=" * 60)
    print("✅ ANALYSIS COMPLETE")
    print("=" * 60)
    