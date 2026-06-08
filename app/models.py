from datetime import datetime, timezone

from pydantic import BaseModel, Field


class ExpectedMoveRecord(BaseModel):
    symbol: str
    call_premium: float
    put_premium: float
    expected_move: float
    computed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
