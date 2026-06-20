export interface Quote {
  symbol: string
  current_price: number
  change: number
  change_percent: number
  high: number
  low: number
  open: number
  prev_close: number
  timestamp: string
}

export interface CompanyProfile {
  symbol: string
  name: string
  logo: string
  country: string
  currency: string
  exchange: string
  sector: string | null
  industry: string | null
  market_cap: number | null
  ipo_date: string | null
  weburl: string | null
}

export interface SymbolSearchResult {
  symbol: string
  description: string
  type: string
}

export interface WatchlistEntry {
  symbol: string
  added_at: string
}

export interface WatchlistEntryWithQuote {
  entry: WatchlistEntry
  quote: Quote | null
}
