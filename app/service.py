from app.calculations import expected_move_from_atm_straddle
from app.models import ExpectedMoveRecord
from app.providers.base import OptionsDataProvider
from app.storage import InMemoryExpectedMoveStore


class ExpectedMoveService:
    def __init__(
        self,
        provider: OptionsDataProvider,
        store: InMemoryExpectedMoveStore,
        notifier: object | None = None,
    ) -> None:
        self.provider = provider
        self.store = store
        self.notifier = notifier

    async def run_watchlist_once(self, watchlist: list[str]) -> list[ExpectedMoveRecord]:
        records: list[ExpectedMoveRecord] = []
        for symbol in watchlist:
            call, put = await self.provider.get_atm_straddle(symbol)
            records.append(
                ExpectedMoveRecord(
                    symbol=symbol,
                    call_premium=call,
                    put_premium=put,
                    expected_move=expected_move_from_atm_straddle(call, put),
                )
            )
        self.store.upsert_records(records)

        if self.notifier is not None and records:
            lines = [
                "Expected move update (ATM straddle):",
                *[
                    f"{record.symbol}: ±{record.expected_move} "
                    f"(call={record.call_premium}, put={record.put_premium})"
                    for record in records
                ],
            ]
            await self.notifier.send_message("\n".join(lines))

        return records
