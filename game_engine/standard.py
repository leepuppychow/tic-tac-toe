"""Standard game engine implementation."""

from uuid import UUID

from models.game import Game, GameStatus
from models.player import Piece

from game_engine.game_engine import GameEngine


class StandardGameEngine(GameEngine):
    """Standard implementation of the game engine."""

    # Valid board positions: A1-A3, B1-B3, C1-C3
    VALID_POSITIONS = {
        "A1": (0, 0), "A2": (0, 1), "A3": (0, 2),
        "B1": (1, 0), "B2": (1, 1), "B3": (1, 2),
        "C1": (2, 0), "C2": (2, 1), "C3": (2, 2),
    }

    def _parse_position(self, position: str) -> tuple[int, int] | None:
        """Parse a position string (e.g., 'A1') into row, column indices.

        Args:
            position: The position string.

        Returns:
            Tuple of (row, column) indices, or None if invalid.
        """
        return self.VALID_POSITIONS.get(position.upper())

    def _get_player_piece_map(self, game: Game) -> dict[UUID, str]:
        """Create a mapping from player UUID to piece symbol.

        Args:
            game: The game to get player mappings from.

        Returns:
            Dictionary mapping player UUID to "X" or "O".
        """
        return {player.uuid: player.piece.value for player in game.players}

    def get_board_state(self, game: Game) -> list[list[str | None]]:
        """Get representation of the current 3x3 tic-tac-toe board.

        Args:
            game: The game to get the board state for.

        Returns:
            A 3x3 matrix representing the board.
        """
        # Initialize empty board
        board: list[list[str | None]] = [[None, None, None] for _ in range(3)]

        # Create player UUID to piece mapping
        player_piece_map = self._get_player_piece_map(game)

        # Apply moves to board (sorted by order to ensure correct sequence)
        sorted_moves = sorted(game.moves, key=lambda m: m.order)
        for move in sorted_moves:
            coords = self._parse_position(move.position)
            if coords:
                row, col = coords
                piece = player_piece_map.get(move.player)
                if piece:
                    board[row][col] = piece

        return board

    def is_valid_move(self, game: Game, position: str) -> bool:
        """Check if a move is valid.

        Args:
            game: The game to check the move for.
            position: The board position (e.g., "A1", "B2", "C3").

        Returns:
            True if the move is valid, False otherwise.
        """
        # Check if position is valid format
        coords = self._parse_position(position)
        if coords is None:
            return False

        # Check if position is already occupied
        board = self.get_board_state(game)
        row, col = coords
        return board[row][col] is None

    def check_game_status(self, game: Game) -> GameStatus:
        """Check the current game status.

        Args:
            game: The game to check the status for.

        Returns:
            The current game status (WIN, DRAW, or ONGOING).
        """
        board = self.get_board_state(game)
        player_piece_map = self._get_player_piece_map(game)

        # Check for wins
        # Check rows
        for row in board:
            if row[0] is not None and row[0] == row[1] == row[2]:
                # Find the winning player UUID
                winning_piece = row[0]
                for player_uuid, piece in player_piece_map.items():
                    if piece == winning_piece:
                        return GameStatus.WIN

        # Check columns
        for col in range(3):
            if board[0][col] is not None and board[0][col] == board[1][col] == board[2][col]:
                winning_piece = board[0][col]
                for player_uuid, piece in player_piece_map.items():
                    if piece == winning_piece:
                        return GameStatus.WIN

        # Check diagonals
        # Top-left to bottom-right
        if board[0][0] is not None and board[0][0] == board[1][1] == board[2][2]:
            winning_piece = board[0][0]
            for player_uuid, piece in player_piece_map.items():
                if piece == winning_piece:
                    return GameStatus.WIN

        # Top-right to bottom-left
        if board[0][2] is not None and board[0][2] == board[1][1] == board[2][0]:
            winning_piece = board[0][2]
            for player_uuid, piece in player_piece_map.items():
                if piece == winning_piece:
                    return GameStatus.WIN

        # Check for draw (board full, no winner)
        is_board_full = all(board[row][col] is not None for row in range(3) for col in range(3))
        if is_board_full:
            return GameStatus.DRAW

        # Otherwise, game is ongoing
        return GameStatus.ONGOING

    def format_game_output(self, game: Game) -> str:
        """Format game state for user-friendly CLI output.

        Args:
            game: The game to format.

        Returns:
            A formatted string representation of the game state.
        """
        board = self.get_board_state(game)
        lines = []

        # Header
        lines.append("Tic-Tac-Toe Game")
        lines.append("=" * 20)
        lines.append("")

        # Board representation
        lines.append("    1   2   3")
        lines.append("  ┌───┬───┬───┐")
        for row_idx, row in enumerate(board):
            row_label = chr(ord("A") + row_idx)  # A, B, C
            cells = [cell if cell else " " for cell in row]
            lines.append(f"{row_label} │ {cells[0]} │ {cells[1]} │ {cells[2]} │")
            if row_idx < 2:
                lines.append("  ├───┼───┼───┤")
        lines.append("  └───┴───┴───┘")
        lines.append("")

        # Game status
        status = self.check_game_status(game)
        lines.append(f"Status: {status.value}")

        # Show winner if game is won
        if status == GameStatus.WIN and game.winner:
            player_piece_map = self._get_player_piece_map(game)
            winning_piece = player_piece_map.get(game.winner, "?")
            lines.append(f"Winner: {winning_piece}")

        # Move count
        lines.append(f"Moves made: {len(game.moves)}")

        return "\n".join(lines)

