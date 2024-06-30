"""Cards api."""

import typing

import sqlalchemy
from sqlalchemy.sql.dml import (
    Delete,
    Insert,
    Update,
)
from sqlalchemy.sql.selectable import Select

from . import db

#


DB_NAME = "cards.sqlite"
DB_COLUMNS = ["id", "state", "owner", "summary"]


Dml = Delete | Insert | Update
Dql = Select

States = tuple[db.State, ...]

GetCount = typing.Sequence[sqlalchemy.Row[tuple[db.State, int]]]
GetCards = typing.Sequence[sqlalchemy.Row[tuple[db.Id, db.State, db.Owner, db.Summary]]]
DqlResult = typing.Sequence[sqlalchemy.Row]
Url = str


class CardsError(Exception):
    """General Cards exception."""

class MissingSummaryError(CardsError):
    """Missing summary."""

class InvalidCardIdError(CardsError):
    """Card invalid id error."""



def _dml_execute(*, path: db.DbPath, stmt: Dml) -> None:
    with db.CardsDb(path=path) as cards_db:
        curs = cards_db.execute(stmt)
        if curs.rowcount != 1:
            raise InvalidCardIdError
        cards_db.commit()


def _dql_execute(*, path: db.DbPath, stmt: Dql) -> DqlResult:
    with db.CardsDb(path=path) as cards_db:
        return cards_db.execute(stmt).fetchall()



def add_card(
    *,
    summary: db.Summary,
    owner: db.Owner = None,
    path: db.DbPath = DB_NAME,
) -> None:
    """Add card to DB."""
    stmt = sqlalchemy.insert(db.Cards).values(owner=owner, summary=summary)
    _dml_execute(path=path, stmt=stmt)


def get_cards(
    *,
    owner: db.Owner,
    states: States,
    path: db.DbPath = DB_NAME,
) -> GetCards:
    """Get cards."""
    # stmt = sqlalchemy.select(db.Cards.id, db.Cards.state, db.Cards.owner, db.Cards.summary)
    stmt = sqlalchemy.select(*[getattr(db.Cards, c) for c in DB_COLUMNS])
    if owner is not None:
        stmt = stmt.where(db.Cards.owner == owner)
    if states:
        stmt.where(db.Cards.state.in_(states))
    return _dql_execute(path=path, stmt=stmt)


def delete_card(*, card_id: db.Id, path: db.DbPath = DB_NAME) -> None:
    """Delete card."""
    stmt = sqlalchemy.delete(db.Cards).where(db.Cards.id == card_id)
    _dml_execute(path=path, stmt=stmt)


def update_card(
    *, card_id: db.Id,
    owner: db.Owner,
    summary: db.Summary | None,
    path: db.DbPath = DB_NAME,
) -> None:
    """Update card."""
    stmt = sqlalchemy.update(db.Cards).where(db.Cards.id == card_id)
    if owner is not None:
        stmt = stmt.values(owner=owner)
    if summary:
        stmt = stmt.values(summary=summary)
    _dml_execute(path=path, stmt=stmt)


def start_card(*, card_id: db.Id, path: db.DbPath = DB_NAME) -> None:
    """Start card."""
    stmt = sqlalchemy.update(db.Cards).where(db.Cards.id == card_id).values(state="wip")
    _dml_execute(path=path, stmt=stmt)


def end_card(*, card_id: db.Id, path: db.DbPath = DB_NAME) -> None:
    """Start card."""
    stmt = sqlalchemy.update(db.Cards).where(db.Cards.id == card_id).values(state="done")
    _dml_execute(path=path, stmt=stmt)


def get_count(path: db.DbPath = DB_NAME) -> GetCount:
    """Get count of cards."""
    case_order = {s: n for n, s in enumerate(typing.get_args(db.State))}
    stmt = sqlalchemy.select(db.Cards.state, sqlalchemy.func.count(db.Cards.state))
    stmt = stmt.group_by(db.Cards.state)
    stmt = stmt.order_by(sqlalchemy.case(case_order, value=db.Cards.state))
    return _dql_execute(path=path, stmt=stmt)


def get_url(path: db.DbPath = DB_NAME) -> Url:
    """Get DB URL."""
    with db.CardsDb(path=path) as cards_db:
        return str(cards_db.engine.url)





