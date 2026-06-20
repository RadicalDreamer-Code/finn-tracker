from abc import ABC, abstractmethod

from app.domain.models import CompanyProfile, Quote, SymbolSearchResult, WatchlistEntry


class MarketDataPort(ABC):
    @abstractmethod
    async def get_quote(self, symbol: str) -> Quote: ...

    @abstractmethod
    async def search_symbols(self, query: str) -> list[SymbolSearchResult]: ...

    @abstractmethod
    async def get_company_profile(self, symbol: str) -> CompanyProfile: ...


class WatchlistRepository(ABC):
    @abstractmethod
    async def add(self, symbol: str) -> WatchlistEntry: ...

    @abstractmethod
    async def remove(self, symbol: str) -> None: ...

    @abstractmethod
    async def list_all(self) -> list[WatchlistEntry]: ...

    @abstractmethod
    async def exists(self, symbol: str) -> bool: ...
