# Finn Tracker — Project Overview

## Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI, Python 3.12+, uvicorn |
| Data provider | finnhub-python (swappable via adapter) |
| Persistence | SQLite via aiosqlite |
| Frontend | Vue 3 + TypeScript, Vite |
| Component library | PrimeVue 4 (Aura theme) |
| State management | Pinia |
| HTTP client | Axios |

## Running locally

```bash
# Backend (from repo root)
cd backend
cp .env.example .env          # fill in FINNHUB_API_KEY
.venv/bin/uvicorn app.main:app --port 3101 --reload

# Frontend (from repo root)
cd frontend
npm install
npm run dev                   # http://localhost:5173
```

Vite proxies `/api/*` → `http://localhost:3101` so no CORS issues in dev.

---

## Architecture

Ports & adapters (hexagonal). The domain layer has zero infrastructure dependencies.

```
backend/app/
├── domain/
│   ├── models.py        # Pure domain types — Quote, CompanyProfile, WatchlistEntry, …
│   └── ports.py         # Abstract interfaces — MarketDataPort, WatchlistRepository
├── adapters/
│   ├── market_data/
│   │   └── finnhub_provider.py   # Finnhub impl of MarketDataPort
│   └── persistence/
│       └── sqlite_watchlist_repo.py
├── services/
│   ├── watchlist_service.py      # Add/remove/list with live quotes
│   └── market_data_service.py    # Quote, search, profile
├── api/v1/
│   ├── watchlist.py     # REST endpoints for watchlist
│   └── stocks.py        # REST endpoints for market data
└── core/
    ├── config.py         # pydantic-settings (.env)
    └── dependencies.py   # DI wiring — lru_cache singletons
```

### Swapping the data provider

Implement `MarketDataPort` from `app/domain/ports.py` in a new file under `adapters/market_data/`, then change the two lines in `core/dependencies.py` that instantiate `FinnhubMarketDataProvider`.

---

## API reference

Base URL: `http://localhost:3101/api/v1`

| Method | Path | Description |
|---|---|---|
| GET | `/watchlist` | List all watched symbols with current quotes |
| POST | `/watchlist` | Add symbol — body: `{"symbol": "AAPL"}` |
| DELETE | `/watchlist/{symbol}` | Remove symbol |
| GET | `/stocks/search?q=` | Search symbols / companies |
| GET | `/stocks/{symbol}/quote` | Live quote for a symbol |
| GET | `/stocks/{symbol}/profile` | Company profile |

Interactive docs available at `http://localhost:3101/docs` when backend is running.

---

## Frontend structure

```
frontend/src/
├── api/
│   ├── client.ts          # Axios instance (baseURL /api/v1)
│   ├── watchlist.ts       # watchlistApi — list, add, remove
│   └── stocks.ts          # stocksApi — search, getQuote, getProfile
├── types/index.ts          # Shared TS types mirroring backend models
├── stores/watchlist.ts     # Pinia store — entries, selectedSymbol, loading
├── components/
│   ├── layout/AppLayout.vue       # Sidebar + main slot
│   └── sidebar/
│       ├── WatchlistSidebar.vue   # Full sidebar with filter + skeleton loading
│       ├── WatchlistItem.vue      # Single row — price, change tag, remove button
│       └── AddSymbolDialog.vue    # Debounced search dialog
└── views/DashboardView.vue        # Quote cards + company profile detail panel
```

---

## What is built (Core MVP)

- [x] Watchlist persisted in SQLite (add / remove)
- [x] Left sidebar with all watched symbols, live prices and day change %
- [x] Inline filter to quickly find a symbol in the sidebar
- [x] Add symbol dialog with debounced search (300 ms) against Finnhub
- [x] Remove symbol via hover button on each sidebar item
- [x] Detail panel — quote cards (price, change, open, prev close, high, low)
- [x] Detail panel — company profile (name, logo, sector, market cap, country, IPO date, website)
- [x] Toast notifications for add / remove feedback
- [x] Skeleton loading state while watchlist fetches
- [x] Quotes fetched in parallel on watchlist load (`asyncio.gather`)
- [x] Port adapter pattern — Finnhub is one concrete impl behind `MarketDataPort`

---

## Roadmap

### Phase 2 — Analyst & Sentiment

- [ ] Analyst price target + consensus (buy / hold / sell bar)
- [ ] Recommendation trend chart (last 4 quarters)
- [ ] Upgrade / downgrade history table
- [ ] News feed per symbol with sentiment score badge
- [ ] Social sentiment trend (Reddit / Twitter) sparkline

### Phase 3 — Events & Calendar

- [ ] Earnings calendar widget (upcoming + recent)
- [ ] Earnings surprise history (actual vs estimate bar chart)
- [ ] EPS / revenue estimate table (quarterly / annual toggle)
- [ ] IPO calendar page
- [ ] Economic calendar sidebar section

### Phase 4 — Technical Analysis

- [ ] Candlestick / OHLCV chart (daily / weekly / monthly resolution toggle)
- [ ] Overlay indicators — SMA, EMA (configurable periods)
- [ ] RSI panel below chart
- [ ] MACD panel below chart
- [ ] Support & resistance level markers on chart
- [ ] Aggregate buy/sell signal badge (Finnhub `aggregate_indicator`)
- [ ] Candlestick pattern recognition annotations

### Phase 5 — Fundamentals Deep-Dive

- [ ] Financials tabs — income statement, balance sheet, cash flow (annual / quarterly)
- [ ] Basic financials grid (P/E, P/B, EPS, beta, 52-week range, dividend yield)
- [ ] Revenue breakdown by segment (treemap or bar)
- [ ] Insider transaction activity feed
- [ ] Insider sentiment net score

### Phase 6 — Portfolio Tracker

- [ ] Portfolio positions (symbol, quantity, cost basis, purchase date)
- [ ] P/L calculation (unrealised gain/loss per position and total)
- [ ] Portfolio allocation pie chart by sector
- [ ] Performance vs S&P 500 (SPY) benchmark chart
- [ ] Dividend income tracker

### Phase 7 — Polish & Infrastructure

- [ ] Dark mode toggle (PrimeVue `darkModeSelector` already wired)
- [ ] Auto-refresh quotes in sidebar on a configurable interval
- [ ] WebSocket / SSE for real-time price push (Finnhub websocket feed)
- [ ] Pagination / virtual scroll for large watchlists
- [ ] Export watchlist to CSV
- [ ] Unit tests — pytest for services, Vitest for composables
- [ ] Docker Compose for one-command local setup

---

## Finnhub API methods available (not yet used)

These are all accessible via the existing `FinnhubMarketDataProvider` — just extend `MarketDataPort` and add the method.

| Category | Method | Returns |
|---|---|---|
| Technicals | `technical_indicator` | Any indicator (RSI, MACD, SMA, …) |
| Technicals | `pattern_recognition` | Candlestick patterns |
| Technicals | `support_resistance` | S/R levels |
| Technicals | `aggregate_indicator` | Overall buy/sell signal |
| Analyst | `price_target` | Analyst price targets |
| Analyst | `recommendation_trends` | Buy/hold/sell trend |
| Analyst | `upgrade_downgrade` | Rating changes |
| Sentiment | `news_sentiment` | Sentiment score per symbol |
| Sentiment | `stock_social_sentiment` | Reddit/Twitter sentiment |
| News | `company_news` | News articles |
| News | `press_releases` | Press releases |
| Earnings | `company_earnings` | Earnings surprises |
| Earnings | `company_eps_estimates` | EPS estimates |
| Earnings | `earnings_calendar` | Upcoming earnings dates |
| Fundamentals | `company_basic_financials` | P/E, beta, 52-week, etc. |
| Fundamentals | `financials` | Balance sheet / income / cash flow |
| Fundamentals | `stock_revenue_breakdown` | Revenue by segment |
| Fundamentals | `stock_insider_transactions` | Insider buys/sells |
| Fundamentals | `stock_insider_sentiment` | Net insider sentiment |
| Candles | `stock_candles` | OHLCV for any resolution |
| ETF | `etfs_profile`, `etfs_holdings` | ETF data |
| Calendar | `ipo_calendar` | Upcoming IPOs |
| Calendar | `calendar_economic` | Macro events |
