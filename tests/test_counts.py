"""Test counts."""

import pathlib
import tempfile
import typing

import pytest

from cards import api

#


InMemoryPath = dict[typing.Literal["path"], typing.Literal[":memory:"]]

@pytest.fixture()
def in_memory_path() -> InMemoryPath:
    return {"path": ":memory:"}



def test_count_empty(in_memory_path: InMemoryPath) -> None:
    """Test count for empty db."""
    cards_counts = api.get_count(**in_memory_path)
    assert cards_counts == []



TempDbPath = dict[typing.Literal["path"], pathlib.Path]

@pytest.fixture()
def temp_db_path() -> typing.Generator[TempDbPath, None, None]:
    with tempfile.TemporaryDirectory() as temp_dir:
        yield {"path": pathlib.Path(temp_dir) / "temp_cards.sqlite"}



def test_count_one(temp_db_path: TempDbPath) -> None:
    """Test count for empty db."""
    api.add_card(summary="", owner=None, **temp_db_path)
    cards_count = api.get_count(**temp_db_path)
    assert cards_count == [("todo", 1)]


def test_count_two_same(temp_db_path: TempDbPath) -> None:
    """Test count for empty db."""
    api.add_card(summary="", owner=None, **temp_db_path)
    api.add_card(summary="", owner=None, **temp_db_path)
    cards_count = api.get_count(**temp_db_path)
    assert cards_count == [("todo", 2)]


def test_count_two_diff(temp_db_path: TempDbPath) -> None:
    """Test count for empty db."""
    api.add_card(summary="", owner=None, **temp_db_path)
    api.start_card(card_id=1, **temp_db_path)
    api.add_card(summary="", owner=None, **temp_db_path)
    cards_count = api.get_count(**temp_db_path)
    assert cards_count == [
        ("todo", 1),
        ("wip", 1),
    ]




