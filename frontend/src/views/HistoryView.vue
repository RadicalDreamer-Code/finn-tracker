<template>
  <div class="history-view">
    <div class="view-header">
      <h1 class="view-title">History</h1>
      <Select
        v-model="selected"
        :options="symbols"
        placeholder="Select a symbol"
        class="symbol-select"
        size="small"
        :disabled="symbols.length === 0"
        filter
      />
    </div>

    <div class="empty-state" v-if="!selected">
      <i class="pi pi-clock" />
      <span v-if="symbols.length === 0">Add symbols to your watchlist first</span>
      <span v-else>Select a symbol to view its history</span>
    </div>

    <template v-else>
      <div class="history-meta" v-if="!loading">
        <span class="history-count">{{ snapshots.length }} entries</span>
      </div>

      <div class="snapshot-list" v-if="!loading">
        <div class="empty-state" v-if="snapshots.length === 0">
          <i class="pi pi-database" />
          <span>No history yet for {{ selected }}</span>
        </div>
        <div v-for="snap in snapshots" :key="snap.fetched_at" class="snapshot-row">
          <div class="snap-time">{{ formatTime(snap.fetched_at) }}</div>
          <div class="snap-right">
            <span class="snap-price">{{ formatCurrency(snap.current_price, snap.eur_rate) }}</span>
            <span
              class="snap-change"
              :class="snap.change_percent >= 0 ? 'positive' : 'negative'"
            >
              {{ snap.change_percent >= 0 ? '+' : '' }}{{ snap.change_percent.toFixed(2) }}%
            </span>
          </div>
        </div>
      </div>

      <div class="snapshot-list loading-state" v-else>
        <Skeleton v-for="n in 8" :key="n" height="2.5rem" border-radius="6px" />
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import Select from 'primevue/select'
import Skeleton from 'primevue/skeleton'
import { useWatchlistStore } from '@/stores/watchlist'
import { stocksApi } from '@/api/stocks'
import type { QuoteSnapshot } from '@/types'
import { useExchangeRate } from '@/composables/useExchangeRate'

const store = useWatchlistStore()
const { rate: eurRate } = useExchangeRate()

const symbols = computed(() => store.entries.map((e) => e.entry.symbol))
const selected = ref<string | null>(store.selectedSymbol)
const snapshots = ref<QuoteSnapshot[]>([])
const loading = ref(false)

onMounted(async () => {
  if (store.entries.length === 0) await store.fetchWatchlist()
  if (!selected.value) selected.value = symbols.value[0] ?? null
})

watch(
  selected,
  async (symbol) => {
    if (!symbol) return
    store.selectSymbol(symbol)
    loading.value = true
    snapshots.value = []
    try {
      snapshots.value = await stocksApi.getHistory(symbol)
    } finally {
      loading.value = false
    }
  },
  { immediate: true },
)

function formatCurrency(usd: number, snapshotRate: number): string {
  const rate = eurRate.value ?? snapshotRate
  if (rate !== null) {
    return new Intl.NumberFormat('de-DE', {
      style: 'currency',
      currency: 'EUR',
      minimumFractionDigits: 2,
    }).format(usd * rate)
  }
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 2,
  }).format(usd)
}

function formatTime(iso: string): string {
  return new Intl.DateTimeFormat('de-DE', {
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  }).format(new Date(iso))
}
</script>

<style scoped>
.history-view {
  flex: 1;
  overflow-y: auto;
  padding: 2rem;
  display: flex;
  flex-direction: column;
}

.view-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.view-title {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 700;
}

.symbol-select {
  width: 220px;
}

.history-meta {
  margin-bottom: 0.75rem;
}

.history-count {
  font-size: 0.8rem;
  color: var(--p-text-muted-color);
}

.snapshot-list {
  max-width: 720px;
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.loading-state {
  gap: 0.5rem;
}

.snapshot-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.6rem 0.8rem;
  border-radius: 6px;
  border: 1px solid var(--p-surface-200);
  background: var(--p-surface-0);
  font-size: 0.85rem;
}

.snap-time {
  color: var(--p-text-muted-color);
  font-size: 0.8rem;
  font-variant-numeric: tabular-nums;
}

.snap-right {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 1px;
}

.snap-price {
  font-weight: 500;
  font-variant-numeric: tabular-nums;
}

.snap-change {
  font-size: 0.75rem;
  font-variant-numeric: tabular-nums;
}

.snap-change.positive {
  color: var(--p-green-600);
}

.snap-change.negative {
  color: var(--p-red-500);
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  padding: 3rem 1rem;
  color: var(--p-text-muted-color);
  font-size: 0.9rem;
  text-align: center;
}

.empty-state .pi {
  font-size: 2rem;
  opacity: 0.4;
}
</style>
