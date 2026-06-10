import os
from dataclasses import dataclass


def _parse_bool(value: str | None, default: bool) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _parse_watchlist(value: str | None) -> list[str]:
    if not value:
        return ["AAPL", "MSFT", "TSLA"]
    return [ticker.strip().upper() for ticker in value.split(",") if ticker.strip()]


@dataclass(frozen=True)
class Settings:
    watchlist: list[str]
    check_interval_seconds: int
    enable_scheduler: bool
    telegram_bot_token: str | None
    telegram_chat_id: str | None
    options_provider: str

    @classmethod
    def from_env(cls) -> "Settings":
        interval_raw = os.getenv("CHECK_INTERVAL_SECONDS", "3600")
        try:
            interval = int(interval_raw)
        except ValueError as exc:
            raise ValueError(
                f"CHECK_INTERVAL_SECONDS must be an integer, got: {interval_raw!r}"
            ) from exc
        if interval <= 0:
            raise ValueError("CHECK_INTERVAL_SECONDS must be greater than 0.")

        return cls(
            watchlist=_parse_watchlist(os.getenv("WATCHLIST")),
            check_interval_seconds=interval,
            enable_scheduler=_parse_bool(os.getenv("ENABLE_SCHEDULER"), True),
            telegram_bot_token=os.getenv("TELEGRAM_BOT_TOKEN"),
            telegram_chat_id=os.getenv("TELEGRAM_CHAT_ID"),
            options_provider=os.getenv("OPTIONS_PROVIDER", "mock").lower(),
        )
