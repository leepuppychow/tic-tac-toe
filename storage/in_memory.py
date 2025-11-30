"""In-memory game storage implementation."""

from uuid import UUID

from models.game import Game

from storage.game_storage import GameStorage


class InMemoryGameStorage(GameStorage):
    """In-memory implementation of game storage."""

    def __init__(self) -> None:
        """Initialize the in-memory storage."""
        self._games: dict[UUID, Game] = {}

    def write_game(self, game: Game) -> None:
        """Write a game to in-memory storage.

        Args:
            game: The game to store.
        """
        self._games[game.uuid] = game

    def read_game(self, game_uuid: UUID) -> Game | None:
        """Read a game from in-memory storage.

        Args:
            game_uuid: The UUID of the game to retrieve.

        Returns:
            The game if found, None otherwise.
        """
        return self._games.get(game_uuid)

