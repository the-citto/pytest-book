"""Test counts - initial."""

import pathlib
import tempfile

from cards import api

#


def test_empty() -> None:
    """Tests empty database creation."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        db_path = pathlib.Path(tmp_dir) / "cards_tmp.sqlite"
        with api.Db(path=db_path) as db:
            count_tbl = db.get_count()
        assert count_tbl == []


