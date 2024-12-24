import json
from difflib import get_close_matches
from random import choice


def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, "r") as f:
        data: dict = json.load(f)

    return data


def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)


def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None


def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]


def chatbot():
    knowledge_base: dict = load_knowledge_base("knowledge_base.json")
    while True:
        user_input: str = input("You: ")

        if user_input.lower() == "quit":
            break

        best_match: str | None = find_best_match(
            user_input, [q["question"] for q in knowledge_base["questions"]]
        )

        if best_match:
            answer: str = get_answer_for_question(best_match, knowledge_base)  # type: ignore
            print(f"Bot: {answer}")

        else:
            not_understand_replies = choice(
                [
                    "I dont understand. Can you tell me the answer?",
                    "I dont know the answer. Can you teach me?",
                    "Im not that smart yet. Can you tell me the answer?",
                ]
            )
            print(f"Bot: {not_understand_replies}")
            new_answer: str = input("Type the answer or 'skip' to skip ")

            if new_answer.lower() != "skip":
                knowledge_base["questions"].append(
                    {"question": user_input, "answer": new_answer}
                )
                save_knowledge_base("knowledge_base.json", knowledge_base)
                i_learned_replies = choice(
                    [
                        "Thank you! I learned something new.",
                        "Thanks to you, I am smarter now.",
                        "Thanks! I learned something new.",
                    ]
                )
                print(f"Bot: {i_learned_replies}")


if __name__ == "__main__":
    chatbot()
