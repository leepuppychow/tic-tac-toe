"""Random selection AI implementation."""

import random
from uuid import UUID

from models.game import Game

from game_ai.game_ai import GameAI
from game_engine import StandardGameEngine


class RandomSelection(GameAI):
    """AI that selects a random unoccupied square."""

    # Valid board positions: A1-A3, B1-B3, C1-C3
    VALID_POSITIONS = [
        "A1", "A2", "A3",
        "B1", "B2", "B3",
        "C1", "C2", "C3",
    ]

    def __init__(self, engine: StandardGameEngine | None = None) -> None:
        """Initialize the random selection AI.

        Args:
            engine: Optional game engine instance. If not provided, a new one will be created.
        """
        self._engine = engine or StandardGameEngine()

    def get_next_move(self, game: Game, player_uuid: UUID) -> str:
        """Get a random valid move.

        Args:
            game: The current game state.
            player_uuid: The UUID of the player making the move.

        Returns:
            A valid board position string.

        Raises:
            ValueError: If no valid moves are available.
        """
        # Get all valid moves
        valid_moves = [
            position
            for position in self.VALID_POSITIONS
            if self._engine.is_valid_move(game, position)
        ]

        if not valid_moves:
            raise ValueError("No valid moves available")

        # Return a random valid move
        return random.choice(valid_moves)

