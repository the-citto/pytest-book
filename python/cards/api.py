"""Cards api."""

# import pathlib
# import sqlite3
import typing

import sqlalchemy
from sqlalchemy import orm
from sqlalchemy.sql import (
    dml,
    selectable,
)

#



State = typing.Literal["todo", "wip", "done"]



COLUMNS = ["id", "state", "owner", "summary"]



class CardsError(Exception):
    """General Cards exception."""

class MissingSummaryError(CardsError):
    """Missing summary."""

class MissingParametersError(CardsError):
    """Missing parameter."""

class InvalidCardIdError(CardsError):
    """Card invalid id error."""



class SqlBase(orm.MappedAsDataclass, orm.DeclarativeBase):
    """SQLAlchemy base class."""


class Cards(SqlBase):
    """Cards table."""

    __tablename__ = "cards"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    owner: orm.Mapped[str | None] = orm.mapped_column(sqlalchemy.String(20))
    summary: orm.Mapped[str] = orm.mapped_column(sqlalchemy.String(50))
    state: orm.Mapped[State] = orm.mapped_column(sqlalchemy.String(20), default="todo")


engine = sqlalchemy.create_engine("sqlite:///cards.sqlite")
SqlBase.metadata.create_all(engine)



def _execute_dml(stmt: dml.Insert | dml.Update | dml.Delete) -> None:
    with sqlalchemy.Connection(engine) as conn:
        curs = conn.execute(stmt)
        if curs.rowcount != 1:
            raise InvalidCardIdError
        conn.commit()


def _execute_dql(stmt: selectable.Select) -> typing.Sequence[sqlalchemy.Row]:
    with sqlalchemy.Connection(engine) as conn:
        curs = conn.execute(stmt)
        return curs.fetchall()


def add_card(*, summary: str, owner: str | None = None) -> None:
    """Add card to DB."""
    stmt = sqlalchemy.insert(Cards).values(owner=owner, summary=summary)
    _execute_dml(stmt=stmt)


def get_cards(
    *,
    owner: str | None = None,
    states: tuple[State, ...] = (),
) -> typing.Sequence[sqlalchemy.Row[tuple[int, State, str | None, str]]]:
    """Get cards."""
    stmt = sqlalchemy.select(Cards.id, Cards.state, Cards.owner, Cards.summary)
    if owner is not None:
        stmt = stmt.where(Cards.owner == owner)
    if states:
        stmt.where(Cards.state.in_(states))
    return _execute_dql(stmt=stmt)


def delete_card(*, card_id: int) -> None:
    """Delete card."""
    stmt = sqlalchemy.delete(Cards).where(Cards.id == card_id)
    _execute_dml(stmt=stmt)


def update_card(*, card_id: int, owner: str | None, summary: str) -> None:
    """Update card."""
    stmt = sqlalchemy.update(Cards).where(Cards.id == card_id)
    if owner is not None:
        stmt = stmt.values(owner=owner)
    if summary:
        stmt = stmt.values(summary=summary)
    _execute_dml(stmt=stmt)
    # if owner is None and not summary:
    #     raise MissingParametersError


def start_card(*, card_id: int) -> None:
    """Start card."""
    stmt = sqlalchemy.update(Cards).where(Cards.id == card_id).values(state="wip")
    _execute_dml(stmt=stmt)


def end_card(*, card_id: int) -> None:
    """Start card."""
    stmt = sqlalchemy.update(Cards).where(Cards.id == card_id).values(state="done")
    _execute_dml(stmt=stmt)


def get_count() -> typing.Sequence[sqlalchemy.Row[tuple[State, int]]]:
    """Get count of cards."""
    case_order = {s: n for n, s in enumerate(typing.get_args(State))}
    stmt = sqlalchemy.select(Cards.state, sqlalchemy.func.count(Cards.state))
    stmt = stmt.group_by(Cards.state)
    stmt = stmt.order_by(sqlalchemy.case(case_order, value=Cards.state))
    return _execute_dql(stmt)













# keeping in case future me sould ever need this crazy

# class _Engine(sqlalchemy.Engine):
#     """Engine with create_all."""
#
#     @classmethod
#     def init(cls: type[typing.Self], url: str) -> sqlalchemy.Engine:
#         """Init."""
#         engine = sqlalchemy.create_engine(url)
#         SqlBase.metadata.create_all(engine)
#         return engine
#
#
#
# class DbConn(sqlalchemy.Connection):
#     """Database connection."""
#
#     def __init__(self) -> None:
#         """Init."""
#         engine = _Engine.init("sqlite:///cards.sqlite")
#         super().__init__(engine)
#
#     def __enter__(self) -> typing.Self:
#         """Customize enter."""
#         return self
#
#     def add_card(self, *, summary: str, owner: str | None = None) -> None:
#         """Add card to DB."""
#         stmt = sqlalchemy.insert(Cards).values(owner=owner, summary=summary)
#         curs = self.execute(stmt)
#         if curs.rowcount != 1:
#             raise CardsError
#         self.commit()
#
#     def get_cards(
#         self,
#         *,
#         owner: str | None = None,
#         states: tuple[State, ...] = (),
#     ) -> typing.Sequence[sqlalchemy.Row[tuple[int, State, str | None, str]]]:
#         """Get cards."""
#         stmt = sqlalchemy.select(Cards.id, Cards.state, Cards.owner, Cards.summary)
#         if owner is not None:
#             stmt = stmt.where(Cards.owner == owner)
#         if states:
#             stmt.where(Cards.state.in_(states))
#         curs = self.execute(stmt)
#         return curs.fetchall()
#
#     def delete_card(self, card_id: int) -> None:
#         """Delete card."""
#         stmt = sqlalchemy.delete(Cards).where(Cards.id == card_id)
#         curs = self.execute(stmt)
#         if curs.rowcount != 1:
#             raise InvalidCardIdError
#         self.commit()
#
#     def update_card(self, *, card_id: int, owner: str | None, summary: str) -> None:
#         """Update card."""
#         if owner is None and not summary:
#             raise MissingParametersError
#         stmt = sqlalchemy.update(Cards).where(Cards.id == card_id)
#         if owner is not None:
#             stmt = stmt.values(owner=owner)
#         if summary:
#             stmt = stmt.values(summary=summary)
#         curs = self.execute(stmt)
#         if curs.rowcount != 1:
#             raise InvalidCardIdError
#         self.commit()











