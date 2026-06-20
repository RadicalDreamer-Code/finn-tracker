import type { WatchlistEntryWithQuote } from '@/types'
import client from './client'

export const watchlistApi = {
  async list(): Promise<WatchlistEntryWithQuote[]> {
    const { data } = await client.get<WatchlistEntryWithQuote[]>('/watchlist')
    return data
  },

  async add(symbol: string): Promise<WatchlistEntryWithQuote> {
    const { data } = await client.post<WatchlistEntryWithQuote>('/watchlist', { symbol })
    return data
  },

  async remove(symbol: string): Promise<void> {
    await client.delete(`/watchlist/${symbol}`)
  },
}
