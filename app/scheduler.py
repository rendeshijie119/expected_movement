import asyncio
import contextlib

from app.service import ExpectedMoveService


class Scheduler:
    def __init__(
        self,
        service: ExpectedMoveService,
        watchlist: list[str],
        interval_seconds: int,
    ) -> None:
        self.service = service
        self.watchlist = watchlist
        self.interval_seconds = interval_seconds
        self._task: asyncio.Task[None] | None = None
        self._stop_event = asyncio.Event()

    @property
    def running(self) -> bool:
        return self._task is not None and not self._task.done()

    def start(self) -> None:
        if self.running:
            return
        self._stop_event.clear()
        self._task = asyncio.create_task(self._run_loop())

    async def stop(self) -> None:
        if not self.running:
            return
        self._stop_event.set()
        if self._task:
            self._task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._task
        self._task = None

    async def _run_loop(self) -> None:
        while not self._stop_event.is_set():
            await self.service.run_watchlist_once(self.watchlist)
            await asyncio.sleep(self.interval_seconds)
