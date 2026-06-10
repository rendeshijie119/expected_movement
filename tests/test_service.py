import asyncio

from app.service import ExpectedMoveService
from app.storage import InMemoryExpectedMoveStore


class DummyProvider:
    async def get_atm_straddle(self, symbol: str) -> tuple[float, float]:
        if symbol == "AAPL":
            return 2.0, 1.5
        return 1.0, 1.0


class DummyNotifier:
    def __init__(self) -> None:
        self.messages: list[str] = []

    async def send_message(self, message: str) -> bool:
        self.messages.append(message)
        return True


def test_service_runs_watchlist_and_persists_latest_records() -> None:
    store = InMemoryExpectedMoveStore()
    notifier = DummyNotifier()
    service = ExpectedMoveService(provider=DummyProvider(), store=store, notifier=notifier)

    records = asyncio.run(service.run_watchlist_once(["AAPL", "MSFT"]))

    assert len(records) == 2
    assert records[0].expected_move == 3.5
    assert records[1].expected_move == 2.0
    assert set(store.latest().keys()) == {"AAPL", "MSFT"}
    assert notifier.messages
