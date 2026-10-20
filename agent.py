
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

MODEL = "llama-3.3-70b-versatile"

SYSTEM_PROMPT = """
Du bist ein hilfreicher Assistent für eine kleine Bibliothek in Hamburg.

Du kannst Bücher suchen und den Rückgabetermin einer Ausleihe prüfen.
Erfinde keine Informationen.
Wenn die Ausleihnummer fehlt, frage nach ihr.
Nenne keine Preise oder Telefonnummern.
"""

def execute_tool(name, arguments):
    if name == "search_book":
        return search_book(arguments["title"])

    if name == "get_loan_status":
        return get_loan_status(arguments["loan_id"])

    return "Unbekanntes Tool."
