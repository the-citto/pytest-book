"""Cards api."""

import functools
import pathlib
import typing

import sqlalchemy

from . import db

#



def db_context(path: pathlib.Path = pathlib.Path("cards.sqlite")) -> typing.Callable:
    """Create context for db."""

    def decorator[R, **P](func: typing.Callable[P, R]) -> typing.Callable[P, R]:

        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            """Wrap."""
            with db.Db(path=path) as cards_db:
                return func(*args, cards_db=cards_db, **kwargs)

        return wrapper
    return decorator


@db_context()
def get_count(**kwargs: db.Db) -> typing.Sequence[sqlalchemy.Row[tuple[db.State, int]]]:
    """Retunr cards count."""
    cards_db = kwargs["cards_db"]
    return cards_db.get_count()


@db_context()
def add_card(*, summary: str, owner: str | None = None, **kwargs: db.Db) -> None:
    """Add card."""
    cards_db = kwargs["cards_db"]
    cards_db.add_card(summary=summary, owner=owner)

