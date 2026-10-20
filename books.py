BOOKS = {
    "Der Vorleser": {
        "author": "Bernhard Schlink",
        "available": True,
    },
    "Faust": {
        "author": "Johann Wolfgang von Goethe",
        "available": False,
    },
    "Tschick": {
        "author": "Wolfgang Herrndorf",
        "available": True,
    },
}


def search_book(title):
    book = BOOKS.get(title)

    if book is None:
        return "Buch nicht gefunden."

    availability = "verfügbar" if book["available"] else "nicht verfügbar"
    return f'{book["author"]}, {availability}'
