import type { CompanyProfile, Quote, QuoteSnapshot, SymbolSearchResult } from '@/types'
import client from './client'

export const stocksApi = {
  async search(q: string): Promise<SymbolSearchResult[]> {
    const { data } = await client.get<SymbolSearchResult[]>('/stocks/search', { params: { q } })
    return data
  },

  async getQuote(symbol: string): Promise<Quote> {
    const { data } = await client.get<Quote>(`/stocks/${symbol}/quote`)
    return data
  },

  async getProfile(symbol: string): Promise<CompanyProfile> {
    const { data } = await client.get<CompanyProfile>(`/stocks/${symbol}/profile`)
    return data
  },

  async getHistory(symbol: string, limit = 500): Promise<QuoteSnapshot[]> {
    const { data } = await client.get<QuoteSnapshot[]>(`/stocks/${symbol}/history`, {
      params: { limit },
    })
    return data
  },
}
