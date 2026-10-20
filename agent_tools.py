TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_book",
            "description": "Search for a book by its exact title.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "The exact title of the book.",
                    }
                },
                "required": ["title"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_loan_status",
            "description": "Look up the return deadline for a loan.",
            "parameters": {
                "type": "object",
                "properties": {
                    "loan_id": {
                        "type": "string",
                        "description": "The loan ID, for example L1.",
                    }
                },
                "required": ["loan_id"],
                "additionalProperties": False,
            },
        },
    },
]
