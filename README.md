# expected_movement

MVP FastAPI service for tracking a stock watchlist, estimating expected move from ATM straddle premiums, and sending Telegram alerts.

## Features

- FastAPI app scaffold with health/status endpoints
- Provider interface for options data
- Mock options provider (swap with real provider later)
- ATM straddle expected-move calculation:
  - `expected_move ≈ atm_call_premium + atm_put_premium`
- In-memory persistence layer for latest/history records
- Background scheduler scaffold for hourly/daily execution
- Telegram notification channel

## Project structure

```text
expected_movement/
  app/
    calculations.py
    main.py
    scheduler.py
    service.py
    settings.py
    storage.py
    models.py
    providers/
      base.py
      mock.py
    notifiers/
      telegram.py
  tests/
    test_calculations.py
    test_service.py
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuration

Set environment variables before running:

- `WATCHLIST` (default: `AAPL,MSFT,TSLA`)
- `CHECK_INTERVAL_SECONDS` (default: `3600`, use `86400` for daily)
- `ENABLE_SCHEDULER` (default: `true`)
- `TELEGRAM_BOT_TOKEN` (required for real Telegram sends)
- `TELEGRAM_CHAT_ID` (required for real Telegram sends)
- `OPTIONS_PROVIDER` (default: `mock`)

Example:

```bash
export WATCHLIST="AAPL,MSFT,NVDA"
export CHECK_INTERVAL_SECONDS="3600"
export ENABLE_SCHEDULER="true"
export TELEGRAM_BOT_TOKEN="your_bot_token"
export TELEGRAM_CHAT_ID="your_chat_id"
```

## Run locally

```bash
uvicorn app.main:app --reload
```

## Endpoints

- `GET /health` - health check
- `GET /status` - watchlist, scheduler status, and latest run time
- `GET /moves/latest` - latest expected move by symbol
- `POST /moves/run` - manually trigger a watchlist run

## Notes on real options data integration

The app uses `OptionsDataProvider` interface (`app/providers/base.py`).

To plug in a real options chain source:
1. Implement a new provider class with `get_atm_straddle(symbol)` returning call/put premiums.
2. Add provider selection logic in `app/main.py` (`build_provider`).
3. Configure provider credentials via environment variables in `app/settings.py`.

## Tests

```bash
python -m pytest -q
```
