"""Tests with classes."""

import typing

import pytest

from cards import api

#


class TestCard:
    """Test Card."""

    def test_field_access(self) -> None:
        """Test field access."""
        c = api.Cards(id=1, owner="me", summary="test summary", state="wip")
        assert c.id == 1
        assert c.owner == "me"
        assert c.summary == "test summary"
        assert c.state == "wip"


    def test_default(self) -> None:
        """Test default."""
        c = api.Cards(id=1, summary="test summary")
        assert c.id == 1
        assert c.owner is None
        assert c.summary == "test summary"
        assert c.state == "todo"



class TestApi:
    """Test Db."""

    def test_add_card_summary(self) -> None:
        """Test add one card with summary."""
        db = api.Db(path=":memory:")
        summary = "summary 1"
        db.add_card(summary=summary)
        assert db.get_cards() == [(1, "todo", None, summary)]

    def test_add_card_summary_owner(self) -> None:
        """Test add one card with summary and owner."""
        db = api.Db(path=":memory:")
        summary = "summary 1"
        owner = "owner 1"
        db.add_card(summary=summary, owner=owner)
        assert db.get_cards() == [(1, "todo", owner, summary)]

    def test_add_cards_summaries(self) -> None:
        """Test add cards with summaries."""
        db = api.Db(path=":memory:")
        summary1 = "summary 1"
        summary2 = "summary 2"
        db.add_card(summary=summary1)
        db.add_card(summary=summary2)
        assert db.get_cards() == [
            (1, "todo", None, summary1),
            (2, "todo", None, summary2),
        ]

    def test_add_cards_summaries_owners(self) -> None:
        """Test add cards with summaries and owners."""
        db = api.Db(path=":memory:")
        summary1 = "summary 1"
        summary2 = "summary 2"
        owner1 = "owner1"
        db.add_card(summary=summary1, owner=owner1)
        db.add_card(summary=summary2)
        assert db.get_cards() == [
            (1, "todo", owner1, summary1),
            (2, "todo", None, summary2),
        ]

    def test_add_card_fail(self) -> None:
        """Test correct failure adding card with no summary."""
        db = api.Db(path=":memory:")
        with pytest.raises(TypeError):
            db.add_card() # pyright: ignore [reportCallIssue]




