import { defineStore } from 'pinia'
import { ref } from 'vue'
import { watchlistApi } from '@/api/watchlist'
import type { WatchlistEntryWithQuote } from '@/types'

export const useWatchlistStore = defineStore('watchlist', () => {
  const entries = ref<WatchlistEntryWithQuote[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)
  const selectedSymbol = ref<string | null>(null)

  async function fetchWatchlist() {
    loading.value = true
    error.value = null
    try {
      entries.value = await watchlistApi.list()
    } catch (e) {
      error.value = 'Failed to load watchlist'
    } finally {
      loading.value = false
    }
  }

  async function addSymbol(symbol: string) {
    const item = await watchlistApi.add(symbol)
    entries.value.unshift(item)
    selectedSymbol.value = item.entry.symbol
  }

  async function removeSymbol(symbol: string) {
    await watchlistApi.remove(symbol)
    entries.value = entries.value.filter((e) => e.entry.symbol !== symbol)
    if (selectedSymbol.value === symbol) {
      selectedSymbol.value = entries.value[0]?.entry.symbol ?? null
    }
  }

  function selectSymbol(symbol: string) {
    selectedSymbol.value = symbol
  }

  return { entries, loading, error, selectedSymbol, fetchWatchlist, addSymbol, removeSymbol, selectSymbol }
})
