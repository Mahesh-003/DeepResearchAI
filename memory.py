import json
import os


MEMORY_FILE = "conversation_memory.json"


def load_memory():

    if not os.path.exists(MEMORY_FILE):
        return []

    with open(
        MEMORY_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def save_memory(memory):

    with open(
        MEMORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            memory,
            file,
            indent=4,
            ensure_ascii=False
        )


def add_memory(user_message, assistant_message):

    memory = load_memory()

    memory.append(
        {
            "user": user_message,
            "assistant": assistant_message
        }
    )

    save_memory(memory)


def get_recent_memory(limit=5):

    memory = load_memory()

    return memory[-limit:]


if __name__ == "__main__":

    print("🧠 Memory System")
    print("=" * 50)

    add_memory(
        "What is Generative AI?",
        "Generative AI is AI that can create new content."
    )

    memory = get_recent_memory()

    print(f"Stored memories: {len(memory)}")

    for item in memory:

        print("\nUser:")
        print(item["user"])

        print("\nAssistant:")
        print(item["assistant"])