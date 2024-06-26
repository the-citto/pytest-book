"""Command Line Interface."""

import typing

import click
import rich.box
import rich.table
import sqlalchemy.exc

from . import (
    __version__,
    api,
    db,
)

#




def _get_card_param(ctx: click.Context, option: str) -> click.Parameter:
    params = ctx.command.get_params(ctx)
    param = [p for p in params if p.name == option]
    if not param:
        err_msg = f"system: '{option}' option not found"
        raise click.ClickException(err_msg)
    return param[0]


def _invalid_card_id(ctx: click.Context, card_id: int, err: api.InvalidCardIdError) -> None:
    param = _get_card_param(ctx, option="card_id")
    raise click.BadParameter(message=str(card_id),param=param) from err



@click.group(invoke_without_command=True, context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(__version__, "-V", "--version")
@click.pass_context
def cli(ctx: click.Context) -> None:
    """Cards app CLI."""
    if ctx.invoked_subcommand is None:
        ctx.invoke(list_cards)


@cli.command()
@click.argument("summary", type=str)
@click.option("-o", "--owner", type=str)
def add (summary: str, owner: str | None) -> None:
    """Add a card to DB."""
    api.add_card(summary=summary, owner=owner)


@cli.command()
@click.argument("card_id", metavar="ID", type=int)
@click.pass_context
def delete(ctx: click.Context, card_id: int) -> None:
    """Delete card by id."""
    try:
        api.delete_card(card_id=card_id)
    except api.InvalidCardIdError as err:
        _invalid_card_id(ctx=ctx, card_id=card_id, err=err)


@cli.command(name="list")
@click.option("-o", "--owner", type=str)
@click.option(
    "-s",
    "--state",
    "states",
    type=click.Choice(typing.get_args(db.State)),
    multiple=True,
)
def list_cards(owner: str | None, states: tuple[db.State, ...]) -> None:
    """List cards."""
    cards = api.get_cards(owner=owner, states=states)
    table = rich.table.Table(box=rich.box.SIMPLE)
    for hd in db.COLUMNS:
        table.add_column(hd)
    for card in cards:
        id_, state, owner, summary = card
        table.add_row(str(id_), state, owner if owner else "", summary)
    rich.print(table)


@cli.command()
@click.argument("card_id", metavar="ID", type=int)
@click.option("-o", "--owner", type=str)
@click.option("-s", "--summary", type=str)
@click.pass_context
def update(ctx: click.Context, card_id: int, owner: str | None, summary: str) -> None:
    """Update card."""
    try:
        api.update_card(card_id=card_id, owner=owner, summary=summary)
    except api.InvalidCardIdError as err:
        _invalid_card_id(ctx=ctx, card_id=card_id, err=err)
    except sqlalchemy.exc.OperationalError as err:
        owner_opts = [f"'{o}'" for o in _get_card_param(ctx, option="owner").opts]
        err_msg = f"Missing summary or option {' '.join(owner_opts)}."
        raise click.UsageError(err_msg) from err


@cli.command()
@click.argument("card_id", metavar="ID", type=int)
@click.pass_context
def start(ctx: click.Context, card_id: int) -> None:
    """Set a card state to 'wip'."""
    try:
        api.start_card(card_id=card_id)
    except api.InvalidCardIdError as err:
        _invalid_card_id(ctx=ctx, card_id=card_id, err=err)


@cli.command()
@click.argument("card_id", metavar="ID", type=int)
@click.pass_context
def end(ctx: click.Context, card_id: int) -> None:
    """Set a card state to 'done'."""
    try:
        api.end_card(card_id=card_id)
    except api.InvalidCardIdError as err:
        _invalid_card_id(ctx=ctx, card_id=card_id, err=err)


@cli.command()
def url() -> None:
    """Show the path to the Cards DB."""
    db_url = api.get_url()
    table = rich.table.Table(box=rich.box.SIMPLE)
    table.add_column("Database URL")
    table.add_row(db_url)
    rich.print(table)


@cli.command()
def count() -> None:
    """Show the number of cards in the DB."""
    cards_count = api.get_count()
    table = rich.table.Table(box=rich.box.SIMPLE)
    table.add_column("state")
    table.add_column("count")
    for state, count in cards_count:
        table.add_row(state, str(count))
    rich.print(table)





