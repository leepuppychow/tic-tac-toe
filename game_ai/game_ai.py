"""Game AI interface."""

from abc import ABC, abstractmethod
from uuid import UUID

from models.game import Game


class GameAI(ABC):
    """Abstract interface for game AI implementations."""

    @abstractmethod
    def get_next_move(self, game: Game, player_uuid: UUID) -> str:
        """Get the next move for a player.

        Args:
            game: The current game state.
            player_uuid: The UUID of the player making the move.

        Returns:
            A board position string (e.g., "A1", "B2", "C3").
        """
        pass

