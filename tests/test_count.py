"""Fixture Scope."""

from cards import (
    api,
    db,
)
from tests.conftest import (
    DUMMY_DATA_ENTRIES,
    TempDbPath,
)

#




def test_count_one_mod(temp_db_path_mod: TempDbPath) -> None:
    """Test count for empty db."""
    api.add_card(summary="", owner=None, **temp_db_path_mod)
    cards_count = api.get_count(**temp_db_path_mod)
    assert cards_count == [("todo", 1)]


def test_count_two_same_mod(temp_db_path_mod: TempDbPath) -> None:
    """Test count for empty db."""
    api.add_card(summary="", owner=None, **temp_db_path_mod)
    cards_count = api.get_count(**temp_db_path_mod)
    assert cards_count == [("todo", 2)]


def test_count_two_diff_mod(temp_db_path_mod: TempDbPath) -> None:
    """Test count for empty db."""
    api.start_card(card_id=1, **temp_db_path_mod)
    cards_count = api.get_count(**temp_db_path_mod)
    assert cards_count == [
        ("todo", 1),
        ("wip", 1),
    ]


def test_reset_count_mod(empty_db_path: TempDbPath) -> None:
    """Test count on re-set DB."""
    api.add_card(summary="", owner=None, **empty_db_path)
    cards_count = api.get_count(**empty_db_path)
    assert cards_count == [("todo", 1)]


def test_count_1(temp_db_path: TempDbPath, dummy_data: list[db.Cards]) -> None:
    """Test count with dummy data from fixture."""
    default_state = "todo"
    expected_count = len(dummy_data)
    for c in dummy_data:
        api.add_card(summary=c.summary, owner=c.owner, **temp_db_path)
    cards_count = api.get_count(**temp_db_path)
    assert cards_count == [(default_state, expected_count)]


def test_count_2(populate_db: TempDbPath) -> None:
    """Test count on DB populated from fixture with default states."""
    default_state = "todo"
    cards_count = api.get_count(**populate_db)
    assert cards_count == [(default_state, DUMMY_DATA_ENTRIES)]


# def test_count_3(populate_db: TempDbPath) -> None:
#     """Test count with DB populated from fixture."""
#     default_state = "todo"









