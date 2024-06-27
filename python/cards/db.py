"""Database."""

import pathlib
import typing

import sqlalchemy
from sqlalchemy import orm

#


COLUMNS = ["id", "state", "owner", "summary"]



DbPath = str | pathlib.Path

State = typing.Literal["todo", "wip", "done"]
Summary = str
Owner = str | None
Id = int



class SqlBase(orm.MappedAsDataclass, orm.DeclarativeBase):
    """SQLAlchemy base class."""


class Cards(SqlBase):
    """Cards table."""

    __tablename__ = "cards"

    id: orm.Mapped[Id] = orm.mapped_column(primary_key=True, autoincrement=True)
    summary: orm.Mapped[Summary] = orm.mapped_column(sqlalchemy.String(50))
    owner: orm.Mapped[Owner] = orm.mapped_column(sqlalchemy.String(20), default=None)
    state: orm.Mapped[State] = orm.mapped_column(sqlalchemy.String(20), default="todo")


class CardsDb(orm.Session):
    """Database session."""

    def __init__(self, path: DbPath) -> None:
        """Init."""
        self.engine = sqlalchemy.create_engine(f"sqlite:///{path}")
        SqlBase.metadata.create_all(bind=self.engine)
        super().__init__(bind=self.engine)




