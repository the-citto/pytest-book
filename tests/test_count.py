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



def test_count_defaults(populated_db: TempDbPath) -> None:
    """Test count on DB populated from fixture with default states."""
    default_state = "todo"
    cards_count = api.get_count(**populated_db)
    assert cards_count == [(default_state, DUMMY_DATA_ENTRIES)]


def test_count_start_one(populated_db: TempDbPath) -> None:
    """Test count with DB populated from fixture."""
    default_state: db.State = "todo"
    started_state: db.State = "wip"
    started_card_id = 2
    api.start_card(card_id=started_card_id, **populated_db)
    cards_count = api.get_count(**populated_db)
    assert cards_count == [
        (default_state, DUMMY_DATA_ENTRIES - 1),
        (started_state, 1),
    ]










