"""Cards api."""

import dataclasses
import typing

#


@dataclasses.dataclass
class Card:
    """Card dataclass."""

    summary: str | None = None
    owner: str | None = None
    state: str = "todo"
    id: int | None = dataclasses.field(default=None, compare=False)

    @classmethod
    def from_dict(cls: type[typing.Self], d: dict) -> typing.Self:
        """Class method from dictionary."""
        return cls(**d)

    def to_dict(self) -> dict:
        """Dataclass to dict."""
        return dataclasses.asdict(self)



