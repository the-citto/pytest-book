"""Conftest."""

import pathlib
import tempfile
import typing

import pytest
import sqlalchemy

from cards import (
    api,
    db,
)

#


DUMMY_DATA_ENTRIES = 6


TempDbPath = dict[typing.Literal["path"], pathlib.Path]



@pytest.fixture(scope="module")
def temp_db_path_mod() -> typing.Generator[TempDbPath, None, None]:
    """Yield temporary SQLite DB in tempfile.TemporaryDirectory() - module scope."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield {"path": pathlib.Path(temp_dir) / "temp_cards.sqlite"}


@pytest.fixture()
def empty_db_path(temp_db_path_mod: TempDbPath) -> TempDbPath:
    """Delete DB content."""
    stmt = sqlalchemy.delete(db.Cards)
    with db.CardsDb(**temp_db_path_mod) as cards_db:
        cards_db.execute(stmt)
        cards_db.commit()
    return temp_db_path_mod


@pytest.fixture()
def temp_db_path() -> typing.Generator[TempDbPath, None, None]:
    """Yield temporary SQLite DB in tempfile.TemporaryDirectory() - module scope."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield {"path": pathlib.Path(temp_dir) / "temp_cards.sqlite"}


@pytest.fixture()
def dummy_data() -> list[db.Cards]:
    return [
        db.Cards(id=n+1, summary=f"summary {n+1}", owner=None, state="todo")
        for n in range(DUMMY_DATA_ENTRIES)
    ]


@pytest.fixture()
def populate_db(temp_db_path: TempDbPath, dummy_data: list[db.Cards]) -> TempDbPath:
    for c in dummy_data:
        api.add_card(summary=c.summary, owner=c.owner, **temp_db_path)
    return temp_db_path







