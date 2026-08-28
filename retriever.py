import json
import os


KNOWLEDGE_FILE = "research_knowledge.json"


def load_knowledge():

    if not os.path.exists(KNOWLEDGE_FILE):
        print("❌ Knowledge base not found.")
        return []

    with open(
        KNOWLEDGE_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        data = json.load(file)

    return data.get("research_results", [])


def retrieve_relevant_research(query):

    documents = load_knowledge()

    if not documents:
        return []

    query_words = set(
        query.lower().split()
    )

    scored_documents = []

    for document in documents:

        text = (
            document.get("title", "") + " " +
            document.get("question", "") + " " +
            document.get("result", "")
        ).lower()

        score = 0

        for word in query_words:

            if len(word) > 2 and word in text:
                score += 1

        scored_documents.append(
            (
                score,
                document
            )
        )

    scored_documents.sort(
        key=lambda x: x[0],
        reverse=True
    )

    return [
        document
        for score, document
        in scored_documents
        if score > 0
    ]


# ==========================================
# TEST RETRIEVER
# ==========================================

if __name__ == "__main__":

    print()
    print("🔍 RAG RETRIEVER")
    print("=" * 60)

    query = input(
        "\nEnter your question: "
    )

    results = retrieve_relevant_research(query)

    if not results:

        print("\n⚠️ No relevant research found.")

    else:

        print(
            f"\n✅ Found {len(results)} relevant "
            f"research document(s).\n"
        )

        for i, result in enumerate(
            results,
            start=1
        ):

            print(
                f"### Result {i}: "
                f"{result['title']}"
            )

            print(
                "\nQuestion:"
            )

            print(
                result["question"]
            )

            print(
                "\nResearch:"
            )

            print(
                result["result"]
            )

            print("\n" + "-" * 60)