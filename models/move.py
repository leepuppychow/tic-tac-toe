"""Move model for tic-tac-toe game."""

from uuid import UUID

from pydantic import BaseModel, Field


class Move(BaseModel):
    """Move model."""

    position: str = Field(..., description="Board position (e.g., A1, A2, B2, C3)")
    player: UUID = Field(..., description="UUID of the player who made the move")
    order: int = Field(..., ge=1, le=9, description="Move order number (1-9)")

