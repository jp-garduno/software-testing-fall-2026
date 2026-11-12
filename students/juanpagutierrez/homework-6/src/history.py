"""Borrowing history reports and lending statistics."""

from collections import Counter


def _describe(loan, book):
    if loan.is_open:
        status = f"on loan, due {loan.due_date.isoformat()}"
    else:
        status = f"returned {loan.returned_on.isoformat()}"
    return f"{loan.borrowed_on.isoformat()} {book.title} - {status}"


def history_report(member, loans, find_book):
    """Return the report lines for ``member`` given their ``loans``."""
    lines = [f"History for {member.name} ({member.member_id})"]
    lines += [_describe(loan, find_book(loan.isbn)) for loan in loans]
    lines.append(f"Total loans: {len(loans)}")
    return lines


def most_borrowed_isbn(loans):
    """Return the ISBN with the most loans (ties go to the one borrowed first), or None."""
    ranking = Counter(loan.isbn for loan in loans).most_common(1)
    return ranking[0][0] if ranking else None
