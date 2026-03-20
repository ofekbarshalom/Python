from dotenv import load_dotenv
load_dotenv()

import csv
import os
from openai import OpenAI

client = OpenAI()
MODEL = "gpt-4o"
CSV_FILE = "conversation.csv"


def load_messages():
    messages = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                messages.append({"role": row["role"], "content": row["content"]})
    return messages


def save_messages(messages):
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["role", "content"])
        writer.writeheader()
        writer.writerows(messages)


def main():
    print("=== Gaslight GPT ===")
    print("Chat with GPT. Edit conversation.csv to change any answers before your next message.")
    print("Commands: /quit to exit, /reset to start over\n")

    messages = load_messages()

    if messages:
        print("Loaded existing conversation:")
        for msg in messages:
            prefix = "You" if msg["role"] == "user" else "GPT"
            print(f"  {prefix}: {msg['content']}")
        print()

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        if user_input.lower() == "/quit":
            break
        if user_input.lower() == "/reset":
            messages = []
            save_messages(messages)
            print("Conversation reset.\n")
            continue

        # Reload from CSV in case user edited it
        messages = load_messages()

        messages.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
        )
        reply = response.choices[0].message.content

        messages.append({"role": "assistant", "content": reply})
        save_messages(messages)

        print(f"\nGPT: {reply}\n")


if __name__ == "__main__":
    main()
