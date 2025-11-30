"""Game storage interface."""

from abc import ABC, abstractmethod
from uuid import UUID

from models.game import Game


class GameStorage(ABC):
    """Abstract interface for game storage implementations."""

    @abstractmethod
    def write_game(self, game: Game) -> None:
        """Write a game to storage.

        Args:
            game: The game to store.
        """
        pass

    @abstractmethod
    def read_game(self, game_uuid: UUID) -> Game | None:
        """Read a game from storage.

        Args:
            game_uuid: The UUID of the game to retrieve.

        Returns:
            The game if found, None otherwise.
        """
        pass

