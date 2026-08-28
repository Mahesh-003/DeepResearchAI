import json
import os


KNOWLEDGE_FILE = "research_knowledge.json"


def save_research(research_results):

    data = {
        "research_results": research_results
    }

    with open(KNOWLEDGE_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    print(f"✅ Research saved to {KNOWLEDGE_FILE}")


def load_research():

    if not os.path.exists(KNOWLEDGE_FILE):
        return []

    with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data.get("research_results", [])


if __name__ == "__main__":

    print("📚 Knowledge Base")

    results = load_research()

    if results:
        print(f"Loaded {len(results)} research results.")

        for i, result in enumerate(results, start=1):
            print(f"{i}. {result.get('title', 'Unknown')}")

    else:
        print("⚠️ Knowledge base is empty.")