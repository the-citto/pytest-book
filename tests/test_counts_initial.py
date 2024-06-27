"""Test counts - initial."""

import pathlib
import tempfile

from cards import api

#


def test_empty_with_dir() -> None:
    """Tests empty database creation in temporary dir."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        db_path = pathlib.Path(tmp_dir) / "cards_tmp.sqlite"
        count_cards = api.get_count(path=db_path)
        assert count_cards == []


def test_empty_in_memory() -> None:
    """Tests empty database creation in-memory."""
    db_path = ":memory:"
    count_cards = api.get_count(path=db_path)
    assert count_cards == []





