from datetime import datetime, timezone
from typing import Iterable

from app.models import ExpectedMoveRecord


class InMemoryExpectedMoveStore:
    def __init__(self) -> None:
        self._latest_by_symbol: dict[str, ExpectedMoveRecord] = {}
        self._history: list[ExpectedMoveRecord] = []
        self._last_run_at: datetime | None = None

    def upsert_records(self, records: Iterable[ExpectedMoveRecord]) -> None:
        record_list = list(records)
        for record in record_list:
            self._latest_by_symbol[record.symbol] = record
        self._history.extend(record_list)
        self._last_run_at = datetime.now(timezone.utc)

    def latest(self) -> dict[str, ExpectedMoveRecord]:
        return dict(self._latest_by_symbol)

    def history(self) -> list[ExpectedMoveRecord]:
        return list(self._history)

    def last_run_at(self) -> datetime | None:
        return self._last_run_at
