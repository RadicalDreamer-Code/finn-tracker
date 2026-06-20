import asyncio

from app.domain.models import WatchlistEntry, WatchlistEntryWithQuote
from app.domain.ports import MarketDataPort, WatchlistRepository


class WatchlistService:
    def __init__(
        self,
        repository: WatchlistRepository,
        market_data: MarketDataPort,
    ) -> None:
        self._repo = repository
        self._market_data = market_data

    async def add_symbol(self, symbol: str) -> WatchlistEntry:
        upper = symbol.upper()
        if await self._repo.exists(upper):
            raise ValueError(f"{upper} is already in the watchlist")
        return await self._repo.add(upper)

    async def remove_symbol(self, symbol: str) -> None:
        upper = symbol.upper()
        if not await self._repo.exists(upper):
            raise KeyError(f"{upper} is not in the watchlist")
        await self._repo.remove(upper)

    async def list_with_quotes(self) -> list[WatchlistEntryWithQuote]:
        entries = await self._repo.list_all()
        quotes = await asyncio.gather(
            *[self._fetch_quote_safe(e.symbol) for e in entries]
        )
        return [
            WatchlistEntryWithQuote(entry=entry, quote=quote)
            for entry, quote in zip(entries, quotes)
        ]

    async def _fetch_quote_safe(self, symbol: str):
        try:
            return await self._market_data.get_quote(symbol)
        except Exception:
            return None
