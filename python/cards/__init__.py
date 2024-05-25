"""Cards init."""

import importlib.metadata

from .__main__ import main

#

__version__ = importlib.metadata.version(__name__)

__all__ = ["main"]



