LOANS = {
    "L1": "Rückgabe bis 25.10.",
    "L2": "Rückgabe bis 28.10.",
}


def get_loan_status(loan_id):
    status = LOANS.get(loan_id)

    if status is None:
        return "Ausleihnummer nicht gefunden."

    return status
