
import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from agent_tools import TOOLS
from books import search_book
from loans import get_loan_status


load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

MODEL = "openai/gpt-oss-120b"

SYSTEM_PROMPT = """
Du bist ein hilfreicher Assistent für eine kleine Bibliothek in Hamburg.

Regeln:
- Bei Fragen zu Büchern musst du immer zuerst das Tool search_book verwenden.
- Verwende für Buchinformationen ausschließlich die Ergebnisse des Tools.
- Wenn das Tool "Buch nicht gefunden." zurückgibt, sage dem Nutzer,
  dass das Buch nicht im Bibliothekskatalog gefunden wurde.
- Verwende niemals dein eigenes Wissen, um fehlende Buchinformationen
  zu ergänzen.
- Bei Fragen zum Rückgabetermin musst du get_loan_status verwenden.
- Wenn die Ausleihnummer fehlt, frage nach ihr.
- Erfinde keine Informationen.
- Nenne keine Preise oder Telefonnummern.
"""


def execute_tool(name, arguments):
    if name == "search_book":
        return search_book(arguments["title"])

    if name == "get_loan_status":
        return get_loan_status(arguments["loan_id"])

    return "Unbekanntes Tool."



def run_agent(user_input, history):
    history_length = len(history)

    try:
        history.append({
            "role": "user",
            "content": user_input,
        })

        while True:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    *history,
                ],
                tools=TOOLS,
                tool_choice="auto",
            )

            message = response.choices[0].message

            if not message.tool_calls:
                answer = message.content or ""
                history.append({
                    "role": "assistant",
                    "content": answer,
                })
                return answer

            history.append(message.model_dump(exclude_none=True))

            for tool_call in message.tool_calls:
                name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)

                result = execute_tool(name, arguments)

                history.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result),
                })

    except Exception:
        del history[history_length:]
        raise


def main():
    history = []

    print("Bibliotheks-Agent gestartet. Mit 'exit' beenden.")

    while True:
        user_input = input("\nDu: ").strip()

        if user_input.lower() == "exit":
            print("Auf Wiedersehen!")
            break

        if not user_input:
            continue

        try:
            answer = run_agent(user_input, history)
            print(f"Agent: {answer}")
        except Exception as error:
            print(f"Fehler: {error}")


if __name__ == "__main__":
    main()
