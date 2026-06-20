from functools import lru_cache

from app.adapters.market_data.finnhub_provider import FinnhubMarketDataProvider
from app.adapters.persistence.sqlite_quote_history_repo import (
    SqliteQuoteHistoryRepository,
)
from app.adapters.persistence.sqlite_watchlist_repo import (
    SqliteWatchlistRepository,
)
from app.core.config import settings
from app.services.market_data_service import MarketDataService
from app.services.watchlist_service import WatchlistService


@lru_cache
def get_market_data_provider() -> FinnhubMarketDataProvider:
    return FinnhubMarketDataProvider(api_key=settings.finnhub_api_key)


@lru_cache
def get_watchlist_repository() -> SqliteWatchlistRepository:
    return SqliteWatchlistRepository(db_path=settings.database_url)


@lru_cache
def get_quote_history_repository() -> SqliteQuoteHistoryRepository:
    return SqliteQuoteHistoryRepository(db_path=settings.database_url)


@lru_cache
def get_market_data_service() -> MarketDataService:
    return MarketDataService(
        market_data=get_market_data_provider(),
        history_repo=get_quote_history_repository(),
    )


def get_watchlist_service() -> WatchlistService:
    return WatchlistService(
        repository=get_watchlist_repository(),
        market_data=get_market_data_service(),
    )
