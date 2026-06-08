from app.providers.base import OptionsDataProvider


class MockOptionsDataProvider(OptionsDataProvider):
    async def get_atm_straddle(self, symbol: str) -> tuple[float, float]:
        seed = sum(ord(ch) for ch in symbol) % 100
        call = round(1.0 + (seed / 100), 2)
        put = round(0.9 + (seed / 120), 2)
        return call, put
