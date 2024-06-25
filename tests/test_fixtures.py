"""Test fixtures."""

import typing

import pytest

#


@pytest.fixture()
def some_data() -> int:
    """Return integer."""
    return 42


def test_some_data(some_data: typing.Callable) -> None:
    """Test some_data fixture."""
    assert some_data == 42

