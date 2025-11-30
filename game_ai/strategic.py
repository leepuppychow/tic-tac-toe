"""Strategic AI implementation."""

from copy import deepcopy
from uuid import UUID

from models.game import Game
from models.move import Move

from game_ai.game_ai import GameAI
from game_engine import StandardGameEngine


class StrategicAI(GameAI):
    """AI that follows a strategic priority: block, center, corners, sides."""

    # Valid board positions: A1-A3, B1-B3, C1-C3
    VALID_POSITIONS = [
        "A1", "A2", "A3",
        "B1", "B2", "B3",
        "C1", "C2", "C3",
    ]

    # Priority order: center, corners, sides
    CENTER = "B2"
    CORNERS = ["A1", "A3", "C1", "C3"]
    SIDES = ["A2", "B1", "B3", "C2"]

    def __init__(self, engine: StandardGameEngine | None = None) -> None:
        """Initialize the strategic AI.

        Args:
            engine: Optional game engine instance. If not provided, a new one will be created.
        """
        self._engine = engine or StandardGameEngine()

    def _get_opponent_uuid(self, game: Game, player_uuid: UUID) -> UUID | None:
        """Get the opponent's UUID.

        Args:
            game: The current game state.
            player_uuid: The current player's UUID.

        Returns:
            The opponent's UUID, or None if not found.
        """
        for player in game.players:
            if player.uuid != player_uuid:
                return player.uuid
        return None

    def _would_win(self, game: Game, player_uuid: UUID, position: str) -> bool:
        """Check if a move would result in a win for the player.

        Args:
            game: The current game state.
            player_uuid: The player's UUID.
            position: The position to check.

        Returns:
            True if the move would result in a win, False otherwise.
        """
        # Create a copy of the game with the hypothetical move
        game_copy = deepcopy(game)
        next_order = len(game_copy.moves) + 1
        hypothetical_move = Move(
            position=position,
            player=player_uuid,
            order=next_order
        )
        game_copy.moves.append(hypothetical_move)

        # Check if this would result in a win
        status = self._engine.check_game_status(game_copy)
        return status.value == "Win"

    def get_next_move(self, game: Game, player_uuid: UUID) -> str:
        """Get the next move following strategic priorities.

        Priority order:
        0. Win if possible
        1. Block opponent from winning
        2. Take center (B2)
        3. Take corners
        4. Take sides

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

        # Get opponent UUID
        opponent_uuid = self._get_opponent_uuid(game, player_uuid)

        # Priority 0: Win if possible
        for position in valid_moves:
            if self._would_win(game, player_uuid, position):
                return position

        # Priority 1: Block opponent from winning
        if opponent_uuid:
            for position in valid_moves:
                if self._would_win(game, opponent_uuid, position):
                    return position

        # Priority 2: Take center if available
        if self.CENTER in valid_moves:
            return self.CENTER

        # Priority 3: Take corners (in order)
        for corner in self.CORNERS:
            if corner in valid_moves:
                return corner

        # Priority 4: Take sides (in order)
        for side in self.SIDES:
            if side in valid_moves:
                return side

        # Fallback (should not reach here if valid_moves is not empty)
        return valid_moves[0]

