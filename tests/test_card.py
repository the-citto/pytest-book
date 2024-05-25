"""Test card."""

from mycards.api import Card

#


def test_field_access() -> None:
    c = Card("some", "name", "todo", 123)
    assert c.summary == "some"
    assert c.owner == "name"
    assert c.state == "todo"
    assert c.id == 123


def test_defaults() -> None:
    c = Card()
    assert c.summary is None
    assert c.owner is None
    assert c.state == "todo"
    assert c.id is None


def test_equality() -> None:
    c1 = Card("some", "alex", "todo", 123)
    c2 = Card("some", "alex", "todo", 123)
    assert c1 == c2


def test_equality_diff_ids() -> None:
    c1 = Card("some", "alex", "todo", 123)
    c2 = Card("some", "alex", "todo", 124)
    assert c1 == c2


def test_inequality() -> None:
    c1 = Card("some", "alex", "todo", 123)
    c2 = Card("some different", "alex", "todo", 124)
    assert c1 != c2


def test_from_dict() -> None:
    c1 = Card("some", "alex", "todo", 123)
    c2_dict = {
        "summary": "some",
        "owner": "alex",
        "state": "todo",
        "id": 123,
    }
    c2 = Card().from_dict(c2_dict)
    assert c1 == c2


def test_to_dict() -> None:
    c1 = Card("some", "alex", "todo", 123)
    c1_dict = c1.to_dict()
    c1_expected = {
        "summary": "some",
        "owner": "alex",
        "state": "todo",
        "id": 123,
    }
    assert c1_dict == c1_expected





