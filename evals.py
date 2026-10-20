
from agent import run_agent
import unicodedata

def run_tests():
    tests = [
        {
            "name": "Buchsuche",
            "input": "Wer ist der Autor von Der Vorleser?",
            "expected": "Bernhard Schlink",
            "tool": "search_book",
        },
        {
            "name": "Ausleihstatus",
            "input": "Wie ist der Rückgabetermin für Ausleihe L1?",
            "expected": "25",
            "tool": "get_loan_status",
        },
        {
            "name": "Unbekanntes Buch",
            "input": "Wer ist der Autor von Harry Potter?",
            "expected": "Bibliothekskatalog",
            "forbidden": "J. K. Rowling",
            "tool": "search_book",
        },
        {
            "name": "Fehlende Ausleihnummer",
            "input": "Wann muss ich das Buch zurückgeben?",
            "expected": "Ausleih",
            "no_tool": True,
        },
        {
            "name": "Zwei Fragen mit Verlauf",
            "input": "Und wie ist es für L2?",
            "expected": "28",
            "tool": "get_loan_status",
            "previous": "Wie ist der Rückgabetermin für Ausleihe L1?",
        },
    ]

    passed = 0

    for test in tests:
        print(f"\nTest: {test['name']}")

        try:
            history = []

            if "previous" in test:
                run_agent(test["previous"], history)

            answer = run_agent(test["input"], history)
            answer_lower = " ".join(
                unicodedata.normalize("NFKC", answer).casefold().split()
            )

            tool_names = []
            for message in history:
                if message.get("role") == "assistant":
                    for call in message.get("tool_calls") or []:
                        tool_names.append(call["function"]["name"])

            success = test["expected"].lower() in answer_lower

            if "forbidden" in test:
                success = success and (
                    test["forbidden"].lower() not in answer_lower
                )

            if "tool" in test:
                success = success and test["tool"] in tool_names

            if test.get("no_tool"):
                success = success and len(tool_names) == 0

            if success:
                print("PASS")
                passed += 1
            else:
                print("FAIL")
                print(f"Antwort: {answer}")
                print(f"Verwendete Tools: {tool_names}")

        except Exception as error:
            print(f"ERROR: {error}")

    print(f"\nErgebnis: {passed}/{len(tests)} Tests bestanden.")


if __name__ == "__main__":
    run_tests()
