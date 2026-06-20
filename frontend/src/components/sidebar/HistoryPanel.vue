<template>
  <div class="history-panel">
    <div class="empty-state" v-if="!selectedSymbol">
      <i class="pi pi-clock" />
      <span>Select a symbol to view history</span>
    </div>

    <template v-else>
      <div class="history-header">
        <span class="history-symbol">{{ selectedSymbol }}</span>
        <span class="history-count" v-if="!loading">{{ snapshots.length }} entries</span>
      </div>

      <div class="snapshot-list" v-if="!loading">
        <div class="empty-state" v-if="snapshots.length === 0">
          <i class="pi pi-database" />
          <span>No history yet</span>
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
        <Skeleton v-for="n in 6" :key="n" height="2.5rem" border-radius="6px" />
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import Skeleton from 'primevue/skeleton'
import { storeToRefs } from 'pinia'
import { useWatchlistStore } from '@/stores/watchlist'
import { stocksApi } from '@/api/stocks'
import type { QuoteSnapshot } from '@/types'
import { useExchangeRate } from '@/composables/useExchangeRate'

const store = useWatchlistStore()
const { selectedSymbol } = storeToRefs(store)
const { rate: eurRate } = useExchangeRate()

const snapshots = ref<QuoteSnapshot[]>([])
const loading = ref(false)

watch(
  selectedSymbol,
  async (symbol) => {
    if (!symbol) return
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
.history-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.history-header {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  padding: 0 0.75rem 0.5rem;
}

.history-symbol {
  font-weight: 700;
  font-size: 0.875rem;
}

.history-count {
  font-size: 0.75rem;
  color: var(--p-text-muted-color);
}

.snapshot-list {
  flex: 1;
  overflow-y: auto;
  padding: 0 0.75rem 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.loading-state {
  gap: 0.5rem;
}

.snapshot-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.5rem 0.6rem;
  border-radius: 6px;
  border: 1px solid var(--p-surface-200);
  background: var(--p-surface-0);
  font-size: 0.8rem;
}

.snap-time {
  color: var(--p-text-muted-color);
  font-size: 0.75rem;
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
  font-size: 0.72rem;
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
  padding: 2rem 1rem;
  color: var(--p-text-muted-color);
  font-size: 0.85rem;
  text-align: center;
  flex: 1;
  justify-content: center;
}

.empty-state .pi {
  font-size: 1.5rem;
  opacity: 0.4;
}
</style>
