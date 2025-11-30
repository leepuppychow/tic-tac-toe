"""Unit tests for StandardGameEngine."""

import pytest
from uuid import uuid4

from game_engine import StandardGameEngine
from models import Game, GameStatus, Move, Player, PlayerType, Piece


@pytest.fixture
def engine():
    """Create a StandardGameEngine instance."""
    return StandardGameEngine()


@pytest.fixture
def player1():
    """Create player 1 (X)."""
    return Player(uuid=uuid4(), type=PlayerType.HUMAN, piece=Piece.X)


@pytest.fixture
def player2():
    """Create player 2 (O)."""
    return Player(uuid=uuid4(), type=PlayerType.COMPUTER, piece=Piece.O)


@pytest.fixture
def empty_game(player1, player2):
    """Create an empty game."""
    return Game(
        uuid=uuid4(),
        status=GameStatus.ONGOING,
        moves=[],
        players=[player1, player2],
        winner=None,
    )


class TestGetBoardState:
    """Tests for get_board_state method."""

    def test_empty_board(self, engine, empty_game):
        """Test that empty board returns all None values."""
        board = engine.get_board_state(empty_game)
        assert len(board) == 3
        assert all(len(row) == 3 for row in board)
        assert all(cell is None for row in board for cell in row)

    def test_board_with_single_move(self, engine, empty_game, player1):
        """Test board with a single move."""
        move = Move(position="B2", player=player1.uuid, order=1)
        empty_game.moves.append(move)

        board = engine.get_board_state(empty_game)
        assert board[1][1] == "X"
        assert board[0][0] is None
        assert board[2][2] is None

    def test_board_with_multiple_moves(self, engine, empty_game, player1, player2):
        """Test board with multiple moves."""
        moves = [
            Move(position="A1", player=player1.uuid, order=1),
            Move(position="B2", player=player2.uuid, order=2),
            Move(position="C3", player=player1.uuid, order=3),
        ]
        empty_game.moves.extend(moves)

        board = engine.get_board_state(empty_game)
        assert board[0][0] == "X"  # A1
        assert board[1][1] == "O"  # B2
        assert board[2][2] == "X"  # C3

    def test_board_preserves_move_order(self, engine, empty_game, player1, player2):
        """Test that moves are applied in order."""
        # Add moves out of order
        moves = [
            Move(position="C3", player=player1.uuid, order=3),
            Move(position="A1", player=player1.uuid, order=1),
            Move(position="B2", player=player2.uuid, order=2),
        ]
        empty_game.moves.extend(moves)

        board = engine.get_board_state(empty_game)
        # Should be applied in order: A1, B2, C3
        assert board[0][0] == "X"  # A1
        assert board[1][1] == "O"  # B2
        assert board[2][2] == "X"  # C3


class TestIsValidMove:
    """Tests for is_valid_move method."""

    def test_valid_empty_position(self, engine, empty_game):
        """Test that valid empty positions return True."""
        assert engine.is_valid_move(empty_game, "A1") is True
        assert engine.is_valid_move(empty_game, "B2") is True
        assert engine.is_valid_move(empty_game, "C3") is True

    def test_invalid_position_format(self, engine, empty_game):
        """Test that invalid position formats return False."""
        assert engine.is_valid_move(empty_game, "Z9") is False
        assert engine.is_valid_move(empty_game, "D1") is False
        assert engine.is_valid_move(empty_game, "A4") is False
        assert engine.is_valid_move(empty_game, "invalid") is False

    def test_occupied_position(self, engine, empty_game, player1):
        """Test that occupied positions return False."""
        move = Move(position="B2", player=player1.uuid, order=1)
        empty_game.moves.append(move)

        assert engine.is_valid_move(empty_game, "B2") is False
        assert engine.is_valid_move(empty_game, "A1") is True  # Still valid

    def test_case_insensitive_position(self, engine, empty_game):
        """Test that position parsing is case-insensitive."""
        assert engine.is_valid_move(empty_game, "a1") is True
        assert engine.is_valid_move(empty_game, "B2") is True
        assert engine.is_valid_move(empty_game, "C3") is True


class TestCheckGameStatus:
    """Tests for check_game_status method."""

    def test_ongoing_empty_board(self, engine, empty_game):
        """Test that empty board returns ONGOING."""
        status = engine.check_game_status(empty_game)
        assert status == GameStatus.ONGOING

    def test_ongoing_partial_board(self, engine, empty_game, player1, player2):
        """Test that partial board returns ONGOING."""
        moves = [
            Move(position="A1", player=player1.uuid, order=1),
            Move(position="B2", player=player2.uuid, order=2),
        ]
        empty_game.moves.extend(moves)

        status = engine.check_game_status(empty_game)
        assert status == GameStatus.ONGOING

    def test_win_horizontal_row_a(self, engine, empty_game, player1):
        """Test horizontal win in row A."""
        moves = [
            Move(position="A1", player=player1.uuid, order=1),
            Move(position="A2", player=player1.uuid, order=2),
            Move(position="A3", player=player1.uuid, order=3),
        ]
        empty_game.moves.extend(moves)

        status = engine.check_game_status(empty_game)
        assert status == GameStatus.WIN

    def test_win_horizontal_row_b(self, engine, empty_game, player2):
        """Test horizontal win in row B."""
        moves = [
            Move(position="B1", player=player2.uuid, order=1),
            Move(position="B2", player=player2.uuid, order=2),
            Move(position="B3", player=player2.uuid, order=3),
        ]
        empty_game.moves.extend(moves)

        status = engine.check_game_status(empty_game)
        assert status == GameStatus.WIN

    def test_win_vertical_column_1(self, engine, empty_game, player1):
        """Test vertical win in column 1."""
        moves = [
            Move(position="A1", player=player1.uuid, order=1),
            Move(position="B1", player=player1.uuid, order=2),
            Move(position="C1", player=player1.uuid, order=3),
        ]
        empty_game.moves.extend(moves)

        status = engine.check_game_status(empty_game)
        assert status == GameStatus.WIN

    def test_win_vertical_column_2(self, engine, empty_game, player2):
        """Test vertical win in column 2."""
        moves = [
            Move(position="A2", player=player2.uuid, order=1),
            Move(position="B2", player=player2.uuid, order=2),
            Move(position="C2", player=player2.uuid, order=3),
        ]
        empty_game.moves.extend(moves)

        status = engine.check_game_status(empty_game)
        assert status == GameStatus.WIN

    def test_win_diagonal_top_left_to_bottom_right(self, engine, empty_game, player1):
        """Test diagonal win from A1-B2-C3."""
        moves = [
            Move(position="A1", player=player1.uuid, order=1),
            Move(position="B2", player=player1.uuid, order=2),
            Move(position="C3", player=player1.uuid, order=3),
        ]
        empty_game.moves.extend(moves)

        status = engine.check_game_status(empty_game)
        assert status == GameStatus.WIN

    def test_win_diagonal_top_right_to_bottom_left(self, engine, empty_game, player2):
        """Test diagonal win from A3-B2-C1."""
        moves = [
            Move(position="A3", player=player2.uuid, order=1),
            Move(position="B2", player=player2.uuid, order=2),
            Move(position="C1", player=player2.uuid, order=3),
        ]
        empty_game.moves.extend(moves)

        status = engine.check_game_status(empty_game)
        assert status == GameStatus.WIN

    def test_draw_full_board_no_winner(self, engine, empty_game, player1, player2):
        """Test draw when board is full with no winner."""
        # X O X
        # O O X
        # X X O
        moves = [
            Move(position="A1", player=player1.uuid, order=1),  # X
            Move(position="A2", player=player2.uuid, order=2),  # O
            Move(position="A3", player=player1.uuid, order=3),  # X
            Move(position="B1", player=player2.uuid, order=4),  # O
            Move(position="B2", player=player2.uuid, order=5),  # O
            Move(position="B3", player=player1.uuid, order=6),  # X
            Move(position="C1", player=player1.uuid, order=7),  # X
            Move(position="C2", player=player1.uuid, order=8),  # X
            Move(position="C3", player=player2.uuid, order=9),  # O
        ]
        empty_game.moves.extend(moves)

        status = engine.check_game_status(empty_game)
        assert status == GameStatus.DRAW

    def test_win_takes_precedence_over_draw(self, engine, empty_game, player1, player2):
        """Test that win is detected even if board is full."""
        # X X X (win)
        # O O X
        # X O O
        moves = [
            Move(position="A1", player=player1.uuid, order=1),  # X
            Move(position="A2", player=player1.uuid, order=2),  # X
            Move(position="A3", player=player1.uuid, order=3),  # X (WIN)
            Move(position="B1", player=player2.uuid, order=4),  # O
            Move(position="B2", player=player2.uuid, order=5),  # O
            Move(position="B3", player=player1.uuid, order=6),  # X
            Move(position="C1", player=player1.uuid, order=7),  # X
            Move(position="C2", player=player2.uuid, order=8),  # O
            Move(position="C3", player=player2.uuid, order=9),  # O
        ]
        empty_game.moves.extend(moves)

        status = engine.check_game_status(empty_game)
        assert status == GameStatus.WIN


class TestFormatGameOutput:
    """Tests for format_game_output method."""

    def test_format_empty_board(self, engine, empty_game):
        """Test formatting of empty board."""
        output = engine.format_game_output(empty_game)
        assert "Tic-Tac-Toe Game" in output
        assert "Status: Ongoing" in output
        assert "Moves made: 0" in output
        assert "│   │   │   │" in output  # Empty cells

    def test_format_board_with_moves(self, engine, empty_game, player1, player2):
        """Test formatting of board with moves."""
        moves = [
            Move(position="A1", player=player1.uuid, order=1),
            Move(position="B2", player=player2.uuid, order=2),
        ]
        empty_game.moves.extend(moves)

        output = engine.format_game_output(empty_game)
        assert "X" in output
        assert "O" in output
        assert "Moves made: 2" in output

    def test_format_winning_board(self, engine, empty_game, player1):
        """Test formatting of winning board."""
        moves = [
            Move(position="A1", player=player1.uuid, order=1),
            Move(position="A2", player=player1.uuid, order=2),
            Move(position="A3", player=player1.uuid, order=3),
        ]
        empty_game.moves.extend(moves)
        empty_game.status = GameStatus.WIN
        empty_game.winner = player1.uuid

        output = engine.format_game_output(empty_game)
        assert "Status: Win" in output
        assert "Winner: X" in output

    def test_format_draw_board(self, engine, empty_game, player1, player2):
        """Test formatting of draw board."""
        # Create a draw scenario
        moves = [
            Move(position="A1", player=player1.uuid, order=1),
            Move(position="A2", player=player2.uuid, order=2),
            Move(position="A3", player=player1.uuid, order=3),
            Move(position="B1", player=player2.uuid, order=4),
            Move(position="B2", player=player2.uuid, order=5),
            Move(position="B3", player=player1.uuid, order=6),
            Move(position="C1", player=player1.uuid, order=7),
            Move(position="C2", player=player1.uuid, order=8),
            Move(position="C3", player=player2.uuid, order=9),
        ]
        empty_game.moves.extend(moves)
        empty_game.status = GameStatus.DRAW

        output = engine.format_game_output(empty_game)
        assert "Status: Draw" in output
        assert "Moves made: 9" in output

