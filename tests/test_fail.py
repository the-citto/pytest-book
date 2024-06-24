"""Test two - fail."""


#

def test_failing() -> None:
    """First failing test."""
    assert (1, 2, 3) != (3, 2, 1)
