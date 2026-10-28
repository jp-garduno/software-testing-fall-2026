"""Advanced feature 4: borrowing history, member report and statistics."""

import pytest

from src.exceptions import MemberNotFoundError
from tests.conftest import CLEAN_CODE, REFACTORING


def test_new_member_has_empty_history(library):
    assert library.get_member_history("S1") == []


def test_history_records_every_borrow_in_order(library):
    library.borrow_book("S1", CLEAN_CODE)
    library.borrow_book("S1", REFACTORING)
    assert [loan.isbn for loan in library.get_member_history("S1")] == [CLEAN_CODE, REFACTORING]


def test_history_keeps_returned_loans_with_return_date(library, clock):
    library.borrow_book("S1", CLEAN_CODE)
    clock.advance(3)
    library.return_book("S1", CLEAN_CODE)
    assert library.get_member_history("S1")[0].returned_on == clock.today


def test_history_only_includes_the_requested_member(library):
    library.borrow_book("S1", CLEAN_CODE)
    library.borrow_book("S2", REFACTORING)
    assert [loan.member_id for loan in library.get_member_history("S2")] == ["S2"]


def test_history_raises_for_unknown_member(library):
    with pytest.raises(MemberNotFoundError):
        library.get_member_history("NOPE")
