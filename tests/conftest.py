"""Conftest."""

import pathlib
import tempfile
import typing

import pytest

from cards import (
    api,
    db,
)

#


DUMMY_DATA_ENTRIES = 6


TempDbPath = dict[typing.Literal["path"], pathlib.Path]


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
def populated_db(temp_db_path: TempDbPath, dummy_data: list[db.Cards]) -> TempDbPath:
    for c in dummy_data:
        api.add_card(summary=c.summary, owner=c.owner, **temp_db_path)
    return temp_db_path




### completely lacking in the book with a mere reference "it'll be explained in chapter 15"
# def pytest_addoption(parser):
#     parser.addoption(
#         "--func-db",
#         action="store_true",
#         defalut=False,
#         help="new db for ech test",
#     )
#
# def db_scope(fixture_name, config):
#     if config.getoption("--finc-test"):
#         return "function"
#     return "session"
#
# @pytest.fixture(scope=db_scope)
# def cards_db():
#     with tempfile.TemporaryDirectory() as temp_dir:
#         yield {"path": pathlib.Path(temp_dir) / "temp_cards.sqlite"}





