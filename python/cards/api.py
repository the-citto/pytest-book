"""Cards api."""

import typing

from . import db

#



DbMethods = typing.Literal[
    "add_card",
    "config",
    "delete_card",
    "end_card",
    "get_cards",
    "get_count",
    "start_card",
    "update_card",
]

@typing.overload
def call_db(*, db_method: DbMethods, path: str = "cards.sqlite") -> db.GetCount | str: ...

@typing.overload
def call_db(*, db_method: DbMethods, card_id: db.Id, path: str = "cards.sqlite") -> None: ...

@typing.overload
def call_db(
    *,
    db_method: DbMethods,
    summary: db.Summary,
    owner: db.Owner = None,
    path: str = "cards.sqlite",
) -> None: ...

@typing.overload
def call_db(
    *,
    db_method: DbMethods,
    path: str = "cards.sqlite",
    owner: db.Owner = None,
    states: db.States = (),
) -> db.GetCards: ...

@typing.overload
def call_db(
    *,
    db_method: DbMethods,
    card_id: db.Id,
    owner: db.Owner = None,
    summary: db.Summary,
    path: str = "cards.sqlite",
) -> db.GetCount: ...

def call_db( # noqa: PLR0913
    *,
    db_method: DbMethods,
    summary: db.Summary | None = None,
    card_id: db.Id | None = None,
    path: str = "cards.sqlite",
    owner: db.Owner = None,
    states: db.States | None = None,
) -> db.GetCount | db.GetCards | str | None:
    """Call db."""
    with db.Db(path=path) as cards_db:
        if db_method == "config":
            return str(cards_db.engine.url)
        _method = getattr(cards_db, db_method)
        match db_method:
            case "add_card":
                _method(summary=summary, owner=owner)
            case "delete_card":
                _method(card_id=card_id)
            case "end_card":
                _method(card_id=card_id)
            case "get_cards":
                return _method(owner=owner, states=states)
            case "get_count":
                return _method()
            case "start_card":
                _method(card_id=card_id)
            case "update_card":
                _method(card_id=card_id, owner=owner, summary=summary)
            case _:
                raise TypeError(db_method)
        return None








