"""Game model for tic-tac-toe game."""

from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field

from models.move import Move
from models.player import Player


class GameStatus(str, Enum):
    """Game status enumeration."""

    WIN = "Win"
    DRAW = "Draw"
    ONGOING = "Ongoing"


class Game(BaseModel):
    """Game model."""

    uuid: UUID = Field(..., description="Unique identifier for the game")
    status: GameStatus = Field(..., description="Current status of the game")
    moves: list[Move] = Field(default_factory=list, description="List of moves made in the game")
    players: list[Player] = Field(..., description="List of players in the game")
    winner: UUID | None = Field(None, description="UUID of the winning player, or None if no winner")

