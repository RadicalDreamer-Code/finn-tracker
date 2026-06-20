from datetime import datetime, timezone

import finnhub

from app.domain.models import CompanyProfile, Quote, SymbolSearchResult
from app.domain.ports import MarketDataPort


class FinnhubMarketDataProvider(MarketDataPort):
    def __init__(self, api_key: str) -> None:
        self._client = finnhub.Client(api_key=api_key)

    async def get_quote(self, symbol: str) -> Quote:
        data = await _run_sync(self._client.quote, symbol)
        return Quote(
            symbol=symbol.upper(),
            current_price=data["c"],
            change=data["d"],
            change_percent=data["dp"],
            high=data["h"],
            low=data["l"],
            open=data["o"],
            prev_close=data["pc"],
            timestamp=datetime.fromtimestamp(data["t"], tz=timezone.utc),
        )

    async def search_symbols(self, query: str) -> list[SymbolSearchResult]:
        data = await _run_sync(self._client.symbol_lookup, query)
        return [
            SymbolSearchResult(
                symbol=item["symbol"],
                description=item["description"],
                type=item["type"],
            )
            for item in (data.get("result") or [])
        ]

    async def get_company_profile(self, symbol: str) -> CompanyProfile:
        data = await _run_sync(self._client.company_profile2, symbol=symbol)
        return CompanyProfile(
            symbol=symbol.upper(),
            name=data.get("name", ""),
            logo=data.get("logo", ""),
            country=data.get("country", ""),
            currency=data.get("currency", ""),
            exchange=data.get("exchange", ""),
            sector=data.get("finnhubIndustry"),
            market_cap=data.get("marketCapitalization"),
            ipo_date=data.get("ipo"),
            weburl=data.get("weburl"),
        )


async def _run_sync(fn, *args, **kwargs):
    import asyncio

    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, lambda: fn(*args, **kwargs))
