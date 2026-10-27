import pytest
from src.member import Member

def test_member_can_be_created():
    m = Member("m1", "Ana")
    assert (m.member_id, m.name) == ("m1", "Ana")
