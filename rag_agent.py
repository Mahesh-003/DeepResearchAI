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
# RAG GENERATION
# ==========================================

def generate_answer(question):

    # Retrieve relevant information
    documents = retrieve_relevant_research(question)

    if not documents:

        return (
            "I could not find relevant information "
            "in the research knowledge base."
        )

    # Build context
    context_parts = []

    for document in documents:

        context_parts.append(
            f"""
Title:
{document['title']}

Research Question:
{document['question']}

Research Findings:
{document['result']}
"""
        )

    context = "\n".join(context_parts)

    # ======================================
    # GENERATION PROMPT
    # ======================================

    prompt = f"""
You are an AI research analyst.

Answer the user's question using ONLY
the research information provided below.

User Question:
{question}

Research Context:
{context}

Instructions:
- Give a clear and useful answer.
- Use the research evidence.
- Do not invent facts.
- If the research does not contain enough information,
  clearly say so.
- Keep the answer concise.
"""

    # ======================================
    # CALL LLM
    # ======================================

    response = client.chat.completions.create(
        model=MODEL,

        messages=[
            {
                "role": "system",
                "content": (
                    "You are a research analysis agent. "
                    "Answer using the provided research context."
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


# ==========================================
# TEST RAG
# ==========================================

if __name__ == "__main__":

    print()
    print("🧠 RAG RESEARCH AGENT")
    print("=" * 60)

    question = input(
        "\nAsk a research question: "
    )

    print(
        "\n🔍 Retrieving relevant research..."
    )

    answer = generate_answer(question)

    print()
    print("=" * 60)
    print("📚 FINAL ANSWER")
    print("=" * 60)

    print(answer)

    print()
    print("=" * 60)
    print("✅ RAG COMPLETE")
    print("=" * 60)