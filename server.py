"""Tic-tac-toe MCP server."""

from uuid import UUID, uuid4

from fastmcp import FastMCP

from game_ai import StrategicAI
from game_engine import StandardGameEngine
from models import Game, GameStatus, Move, Player, PlayerType, Piece
from storage import InMemoryGameStorage

mcp = FastMCP("Tic-Tac-Toe MCP Server")


# TODO: create a config service / mappings to use here
# Initialize services
storage = InMemoryGameStorage()
engine = StandardGameEngine()
ai = StrategicAI(engine)


@mcp.tool
def create_game(
    player1_type: str = "human",
    player2_type: str = "computer",
    player1_piece: str = "X",
    player2_piece: str = "O",
) -> dict:
    """Create a new tic-tac-toe game.

    Args:
        player1_type: Type of player 1 ("human" or "computer"). Defaults to "human".
        player2_type: Type of player 2 ("human" or "computer"). Defaults to "computer".
        player1_piece: Piece for player 1 ("X" or "O"). Defaults to "X".
        player2_piece: Piece for player 2 ("X" or "O"). Defaults to "O".

    Returns:
        Dictionary containing game_uuid, player1_uuid, and player2_uuid.
    """
    # Create players
    player1 = Player(
        uuid=uuid4(),
        type=PlayerType(player1_type.lower()),
        piece=Piece(player1_piece.upper()),
    )
    player2 = Player(
        uuid=uuid4(),
        type=PlayerType(player2_type.lower()),
        piece=Piece(player2_piece.upper()),
    )

    # Create game
    game = Game(
        uuid=uuid4(),
        status=GameStatus.ONGOING,
        moves=[],
        players=[player1, player2],
        winner=None,
    )

    # Store game
    storage.write_game(game)

    return {
        "game_uuid": str(game.uuid),
        "player1_uuid": str(player1.uuid),
        "player2_uuid": str(player2.uuid),
        "message": "Game created successfully",
    }


@mcp.tool
def display_board(game_uuid: str) -> str:
    """Display the current board state for a game.

    Args:
        game_uuid: The UUID of the game to display.

    Returns:
        Formatted string representation of the board.
    """
    game = storage.read_game(UUID(game_uuid))
    if not game:
        return f"Game {game_uuid} not found"

    return engine.format_game_output(game)


@mcp.tool
def get_next_move(game_uuid: str, player_uuid: str, ai_type: str = "strategic") -> dict:
    """Get the next move for a player using AI.

    Args:
        game_uuid: The UUID of the game.
        player_uuid: The UUID of the player making the move.
        ai_type: Type of AI to use ("strategic" or "random"). Defaults to "strategic".

    Returns:
        Dictionary containing the suggested position.
    """
    game = storage.read_game(UUID(game_uuid))
    if not game:
        return {"error": f"Game {game_uuid} not found"}

    # Select AI based on type
    # TODO: feels like the AI implementation should be chosen at the start of the MCP server
    # or maybe in the create_game tool (refactor later)
    if ai_type.lower() == "random":
        from game_ai import RandomSelection

        selected_ai = RandomSelection(engine)
    else:
        selected_ai = ai

    try:
        position = selected_ai.get_next_move(game, UUID(player_uuid))
        return {
            "game_uuid": game_uuid,
            "player_uuid": player_uuid,
            "position": position,
            "message": f"Suggested move: {position}",
        }
    except ValueError as e:
        return {"error": str(e)}


@mcp.tool
def add_move(game_uuid: str, player_uuid: str, position: str) -> dict:
    """Add a move to the game.

    Args:
        game_uuid: The UUID of the game.
        player_uuid: The UUID of the player making the move.
        position: The board position (e.g., "A1", "B2", "C3").

    Returns:
        Dictionary containing the result of the move.
    """
    game = storage.read_game(UUID(game_uuid))
    if not game:
        return {"error": f"Game {game_uuid} not found"}

    # Validate move
    if not engine.is_valid_move(game, position):
        return {"error": f"Invalid move: {position} is not a valid or available position"}

    # Create move
    next_order = len(game.moves) + 1
    move = Move(
        position=position.upper(),
        player=UUID(player_uuid),
        order=next_order,
    )

    # Add move to game
    game.moves.append(move)

    # Update game status
    game.status = engine.check_game_status(game)

    # Update winner if game is won
    if game.status == GameStatus.WIN:
        # Find the winning player
        board = engine.get_board_state(game)
        player_piece_map = {p.uuid: p.piece.value for p in game.players}
        # Check who won by looking at the board
        # (The engine already determined there's a winner)
        # We'll set the winner based on the last move
        game.winner = UUID(player_uuid)

    # Save game
    storage.write_game(game)

    return {
        "game_uuid": game_uuid,
        "move": {
            "position": position.upper(),
            "player_uuid": player_uuid,
            "order": next_order,
        },
        "status": game.status.value,
        "winner": str(game.winner) if game.winner else None,
        "message": f"Move added: {position.upper()}",
    }


@mcp.tool
def get_game_state(game_uuid: str) -> dict:
    """Get the full game state.

    Args:
        game_uuid: The UUID of the game.

    Returns:
        Dictionary containing the complete game state.
    """
    game = storage.read_game(UUID(game_uuid))
    if not game:
        return {"error": f"Game {game_uuid} not found"}

    # TODO: cant we just return the Pydantic model and let the client handle the formatting?
    return {
        "game_uuid": str(game.uuid),
        "status": game.status.value,
        "winner": str(game.winner) if game.winner else None,
        "players": [
            {
                "uuid": str(p.uuid),
                "type": p.type.value,
                "piece": p.piece.value,
            }
            for p in game.players
        ],
        "moves": [
            {
                "position": m.position,
                "player_uuid": str(m.player),
                "order": m.order,
            }
            for m in sorted(game.moves, key=lambda m: m.order)
        ],
    }


@mcp.tool
def check_game_status(game_uuid: str) -> dict:
    """Check the current game status (win, draw, or ongoing).

    Args:
        game_uuid: The UUID of the game.

    Returns:
        Dictionary containing the game status and winner if applicable.
    """
    game = storage.read_game(UUID(game_uuid))
    if not game:
        return {"error": f"Game {game_uuid} not found"}

    status = engine.check_game_status(game)

    # Update game status if it changed
    if game.status != status:
        game.status = status
        if status == GameStatus.WIN and not game.winner:
            # Determine winner from board state
            # The last move that resulted in a win is the winner
            if game.moves:
                last_move = sorted(game.moves, key=lambda m: m.order)[-1]
                game.winner = last_move.player
        storage.write_game(game)

    return {
        "game_uuid": game_uuid,
        "status": status.value,
        "winner": str(game.winner) if game.winner else None,
        "is_game_over": status != GameStatus.ONGOING,
    }


@mcp.tool
def list_moves(game_uuid: str) -> dict:
    """List all moves in the game history.

    Args:
        game_uuid: The UUID of the game.

    Returns:
        Dictionary containing the list of moves in chronological order.
    """
    game = storage.read_game(UUID(game_uuid))
    if not game:
        return {"error": f"Game {game_uuid} not found"}

    sorted_moves = sorted(game.moves, key=lambda m: m.order)

    return {
        "game_uuid": game_uuid,
        "moves": [
            {
                "order": m.order,
                "position": m.position,
                "player_uuid": str(m.player),
            }
            for m in sorted_moves
        ],
    }


if __name__ == "__main__":
    mcp.run()
