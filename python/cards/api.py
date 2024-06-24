"""Cards api."""

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

class InvalidCardIdError(CardsError):
    """Card invalid id error."""



class SqlBase(orm.MappedAsDataclass, orm.DeclarativeBase):
    """SQLAlchemy base class."""


class Cards(SqlBase):
    """Cards table."""

    __tablename__ = "cards"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, autoincrement=True)
    summary: orm.Mapped[str] = orm.mapped_column(sqlalchemy.String(50))
    owner: orm.Mapped[str | None] = orm.mapped_column(sqlalchemy.String(20), default=None)
    state: orm.Mapped[State] = orm.mapped_column(sqlalchemy.String(20), default="todo")





class Db(orm.Session):
    """Database session."""

    def __init__(self, path: str = "cards.sqlite") -> None:
        """Init."""
        self.engine = sqlalchemy.create_engine(f"sqlite:///{path}")
        SqlBase.metadata.create_all(bind=self.engine)

    def _execute_dml(self, *, stmt: dml.Insert | dml.Update | dml.Delete) -> None:
        with orm.Session(self.engine) as session:
            curs = session.execute(stmt)
            if curs.rowcount != 1:
                raise InvalidCardIdError
            session.commit()

    def _execute_dql(self, *, stmt: selectable.Select) -> typing.Sequence[sqlalchemy.Row]:
        with orm.Session(self.engine) as session:
            curs = session.execute(stmt)
            return curs.fetchall()

    def add_card(self, *, summary: str, owner: str | None = None) -> None:
        """Add card to DB."""
        stmt = sqlalchemy.insert(Cards).values(owner=owner, summary=summary)
        self._execute_dml(stmt=stmt)

    def get_cards(
        self,
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
        return self._execute_dql(stmt=stmt)

    def delete_card(self, *, card_id: int) -> None:
        """Delete card."""
        stmt = sqlalchemy.delete(Cards).where(Cards.id == card_id)
        self._execute_dml(stmt=stmt)

    def update_card(self, *, card_id: int, owner: str | None, summary: str) -> None:
        """Update card."""
        stmt = sqlalchemy.update(Cards).where(Cards.id == card_id)
        if owner is not None:
            stmt = stmt.values(owner=owner)
        if summary:
            stmt = stmt.values(summary=summary)
        self._execute_dml(stmt=stmt)


    def start_card(self, *, card_id: int) -> None:
        """Start card."""
        stmt = sqlalchemy.update(Cards).where(Cards.id == card_id).values(state="wip")
        self._execute_dml(stmt=stmt)


    def end_card(self, *, card_id: int) -> None:
        """Start card."""
        stmt = sqlalchemy.update(Cards).where(Cards.id == card_id).values(state="done")
        self._execute_dml(stmt=stmt)


    def get_count(self) -> typing.Sequence[sqlalchemy.Row[tuple[State, int]]]:
        """Get count of cards."""
        case_order = {s: n for n, s in enumerate(typing.get_args(State))}
        stmt = sqlalchemy.select(Cards.state, sqlalchemy.func.count(Cards.state))
        stmt = stmt.group_by(Cards.state)
        stmt = stmt.order_by(sqlalchemy.case(case_order, value=Cards.state))
        return self._execute_dql(stmt=stmt)









# engine = sqlalchemy.create_engine("sqlite:///cards.sqlite")
# SqlBase.metadata.create_all(bind=engine)



# def _execute_dml(*, stmt: dml.Insert | dml.Update | dml.Delete, engine: sqlalchemy.Engine = engine) -> None:
#     with orm.Session(engine) as session:
#         curs = session.execute(stmt)
#         if curs.rowcount != 1:
#             raise InvalidCardIdError
#         session.commit()


# def _execute_dql(*, stmt: selectable.Select, engine: sqlalchemy.Engine = engine) -> typing.Sequence[sqlalchemy.Row]:
#     with sqlalchemy.Connection(engine) as conn:
#         curs = conn.execute(stmt)
#         return curs.fetchall()


# def add_card(*, summary: str, owner: str | None = None, engine: sqlalchemy.Engine = engine) -> None:
#     """Add card to DB."""
#     stmt = sqlalchemy.insert(Cards).values(owner=owner, summary=summary)
#     _execute_dml(stmt=stmt, engine=engine)


# def get_cards(
#     *,
#     owner: str | None = None,
#     states: tuple[State, ...] = (),
#     engine: sqlalchemy.Engine = engine,
# ) -> typing.Sequence[sqlalchemy.Row[tuple[int, State, str | None, str]]]:
#     """Get cards."""
#     stmt = sqlalchemy.select(Cards.id, Cards.state, Cards.owner, Cards.summary)
#     if owner is not None:
#         stmt = stmt.where(Cards.owner == owner)
#     if states:
#         stmt.where(Cards.state.in_(states))
#     return _execute_dql(stmt=stmt, engine=engine)


# def delete_card(*, card_id: int) -> None:
#     """Delete card."""
#     stmt = sqlalchemy.delete(Cards).where(Cards.id == card_id)
#     _execute_dml(stmt=stmt)


# def update_card(*, card_id: int, owner: str | None, summary: str) -> None:
#     """Update card."""
#     stmt = sqlalchemy.update(Cards).where(Cards.id == card_id)
#     if owner is not None:
#         stmt = stmt.values(owner=owner)
#     if summary:
#         stmt = stmt.values(summary=summary)
#     _execute_dml(stmt=stmt)


# def start_card(*, card_id: int) -> None:
#     """Start card."""
#     stmt = sqlalchemy.update(Cards).where(Cards.id == card_id).values(state="wip")
#     _execute_dml(stmt=stmt)


# def end_card(*, card_id: int) -> None:
#     """Start card."""
#     stmt = sqlalchemy.update(Cards).where(Cards.id == card_id).values(state="done")
#     _execute_dml(stmt=stmt)


# def get_count() -> typing.Sequence[sqlalchemy.Row[tuple[State, int]]]:
#     """Get count of cards."""
#     case_order = {s: n for n, s in enumerate(typing.get_args(State))}
#     stmt = sqlalchemy.select(Cards.state, sqlalchemy.func.count(Cards.state))
#     stmt = stmt.group_by(Cards.state)
#     stmt = stmt.order_by(sqlalchemy.case(case_order, value=Cards.state))
#     return _execute_dql(stmt=stmt)




