"""Game storage service package."""

from storage.game_storage import GameStorage
from storage.in_memory import InMemoryGameStorage

__all__ = ["GameStorage", "InMemoryGameStorage"]

