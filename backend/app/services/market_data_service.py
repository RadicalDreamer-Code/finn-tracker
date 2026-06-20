from app.domain.models import CompanyProfile, Quote, SymbolSearchResult
from app.domain.ports import MarketDataPort


class MarketDataService:
    def __init__(self, market_data: MarketDataPort) -> None:
        self._market_data = market_data

    async def get_quote(self, symbol: str) -> Quote:
        return await self._market_data.get_quote(symbol.upper())

    async def search_symbols(self, query: str) -> list[SymbolSearchResult]:
        return await self._market_data.search_symbols(query)

    async def get_company_profile(self, symbol: str) -> CompanyProfile:
        return await self._market_data.get_company_profile(symbol.upper())
