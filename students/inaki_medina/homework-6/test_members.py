import library_system

Member = library_system.Member

# Test 1: Member exists
def test_member_can_be_created():
    member = Member("Juan", 0, 3)
    assert member.name == "Juan"