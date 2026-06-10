from typing import Protocol, runtime_checkable


@runtime_checkable
class OptionsDataProvider(Protocol):
    async def get_atm_straddle(self, symbol: str) -> tuple[float, float]:
        """Return ATM call and put premiums for the symbol."""
