from datetime import datetime
from pydantic import BaseModel


class Quote(BaseModel):
    symbol: str
    current_price: float
    change: float
    change_percent: float
    high: float
    low: float
    open: float
    prev_close: float
    timestamp: datetime


class CompanyProfile(BaseModel):
    symbol: str
    name: str
    logo: str
    country: str
    currency: str
    exchange: str
    sector: str | None = None
    industry: str | None = None
    market_cap: float | None = None
    ipo_date: str | None = None
    weburl: str | None = None


class SymbolSearchResult(BaseModel):
    symbol: str
    description: str
    type: str


class WatchlistEntry(BaseModel):
    symbol: str
    added_at: datetime


class WatchlistEntryWithQuote(BaseModel):
    entry: WatchlistEntry
    quote: Quote | None = None
