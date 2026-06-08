from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from app.providers.base import OptionsDataProvider
from app.providers.mock import MockOptionsDataProvider
from app.scheduler import Scheduler
from app.service import ExpectedMoveService
from app.settings import Settings
from app.storage import InMemoryExpectedMoveStore
from app.notifiers.telegram import TelegramNotifier


def build_provider(settings: Settings) -> OptionsDataProvider:
    if settings.options_provider == "mock":
        return MockOptionsDataProvider()
    raise ValueError(f"Unsupported provider: {settings.options_provider}")


settings = Settings.from_env()
store = InMemoryExpectedMoveStore()
provider = build_provider(settings)
notifier = TelegramNotifier(settings.telegram_bot_token, settings.telegram_chat_id)
service = ExpectedMoveService(provider=provider, store=store, notifier=notifier)
scheduler = Scheduler(
    service=service,
    watchlist=settings.watchlist,
    interval_seconds=settings.check_interval_seconds,
)


@asynccontextmanager
async def lifespan(_: FastAPI):
    if settings.enable_scheduler:
        scheduler.start()
    try:
        yield
    finally:
        await scheduler.stop()


app = FastAPI(title="Expected Movement Service", lifespan=lifespan)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/status")
async def status() -> dict[str, object]:
    return {
        "watchlist": settings.watchlist,
        "provider": settings.options_provider,
        "scheduler_running": scheduler.running,
        "last_run_at": store.last_run_at(),
        "telegram_enabled": notifier.enabled,
    }


@app.get("/moves/latest")
async def latest_moves() -> dict[str, object]:
    return {
        "last_run_at": store.last_run_at(),
        "items": list(store.latest().values()),
    }


@app.post("/moves/run")
async def run_once() -> dict[str, object]:
    try:
        records = await service.run_watchlist_once(settings.watchlist)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"items": records, "count": len(records)}
