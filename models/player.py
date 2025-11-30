"""Player model for tic-tac-toe game."""

from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class PlayerType(str, Enum):
    """Player type enumeration."""

    COMPUTER = "computer"
    HUMAN = "human"


class Piece(str, Enum):
    """Game piece enumeration."""

    X = "X"
    O = "O"


class Player(BaseModel):
    """Player model."""

    uuid: UUID = Field(..., description="Unique identifier for the player")
    type: PlayerType = Field(..., description="Type of player (computer or human)")
    piece: Piece = Field(..., description="Game piece assigned to the player (X or O)")

