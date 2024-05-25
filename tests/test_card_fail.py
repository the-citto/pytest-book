"""Test Card fail."""

from mycards.api import Card

#


def test_equality_fail() -> None:
    c1 = Card("a", "b")
    c2 = Card("c", "d")
    assert c1 == c2

