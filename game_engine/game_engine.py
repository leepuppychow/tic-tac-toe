"""Game engine interface."""

from abc import ABC, abstractmethod

from models.game import Game, GameStatus


class GameEngine(ABC):
    """Abstract interface for game engine implementations."""

    @abstractmethod
    def get_board_state(self, game: Game) -> list[list[str | None]]:
        """Get representation of the current 3x3 tic-tac-toe board.

        Args:
            game: The game to get the board state for.

        Returns:
            A 3x3 matrix representing the board. Each cell contains:
            - "X" or "O" if occupied by a player
            - None if empty
            Rows are indexed 0-2 (top to bottom), columns are indexed 0-2 (left to right).
        """
        pass

    @abstractmethod
    def is_valid_move(self, game: Game, position: str) -> bool:
        """Check if a move is valid.

        Args:
            game: The game to check the move for.
            position: The board position (e.g., "A1", "B2", "C3").

        Returns:
            True if the move is valid (position is in bounds and not occupied), False otherwise.
        """
        pass

    @abstractmethod
    def check_game_status(self, game: Game) -> GameStatus:
        """Check the current game status.

        Args:
            game: The game to check the status for.

        Returns:
            The current game status (WIN, DRAW, or ONGOING).
        """
        pass

    @abstractmethod
    def format_game_output(self, game: Game) -> str:
        """Format game state for user-friendly CLI output.

        Args:
            game: The game to format.

        Returns:
            A formatted string representation of the game state.
        """
        pass

