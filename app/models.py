from datetime import datetime, timezone

from pydantic import BaseModel, Field


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class ExpectedMoveRecord(BaseModel):
    symbol: str
    call_premium: float
    put_premium: float
    expected_move: float
    computed_at: datetime = Field(default_factory=utc_now)
