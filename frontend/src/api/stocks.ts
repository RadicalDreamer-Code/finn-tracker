import type { CompanyProfile, Quote, SymbolSearchResult } from '@/types'
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
}
