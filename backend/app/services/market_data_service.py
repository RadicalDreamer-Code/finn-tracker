from datetime import datetime, timedelta, timezone

from app.adapters.market_data.frankfurter_provider import fetch_eur_rate
from app.domain.models import (
    CompanyProfile,
    Quote,
    QuoteSnapshot,
    SymbolSearchResult,
)
from app.domain.ports import MarketDataPort, QuoteHistoryRepository

_QUOTE_TTL = timedelta(seconds=60)


class MarketDataService(MarketDataPort):
    def __init__(
        self,
        market_data: MarketDataPort,
        history_repo: QuoteHistoryRepository,
    ) -> None:
        self._market_data = market_data
        self._history_repo = history_repo

    async def get_quote(self, symbol: str) -> Quote:
        upper = symbol.upper()
        latest = await self._history_repo.get_latest(upper)
        if (
            latest is not None
            and datetime.now(timezone.utc) - latest.fetched_at < _QUOTE_TTL
        ):
            return latest

        quote = await self._market_data.get_quote(upper)
        eur_rate = await fetch_eur_rate()
        snapshot = QuoteSnapshot(
            **quote.model_dump(),
            eur_rate=eur_rate,
            fetched_at=datetime.now(timezone.utc),
        )
        await self._history_repo.save(snapshot)
        return quote

    async def search_symbols(self, query: str) -> list[SymbolSearchResult]:
        return await self._market_data.search_symbols(query)

    async def get_company_profile(self, symbol: str) -> CompanyProfile:
        return await self._market_data.get_company_profile(symbol.upper())
