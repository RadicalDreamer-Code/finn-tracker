<template>
  <aside class="sidebar">
    <div class="sidebar-header">
      <div class="tab-switcher">
        <button
          class="tab-btn"
          :class="{ active: activeTab === 'watchlist' }"
          @click="activeTab = 'watchlist'"
        >
          Watchlist
        </button>
        <button
          class="tab-btn"
          :class="{ active: activeTab === 'history' }"
          @click="activeTab = 'history'"
        >
          History
        </button>
      </div>
      <span v-if="eurRate !== null" class="currency-pill eur">EUR</span>
      <span v-else-if="rateLoading" class="currency-pill loading">USD</span>
      <span v-else class="currency-pill warn">USD</span>
    </div>

    <WatchlistPanel v-if="activeTab === 'watchlist'" />
    <HistoryPanel v-else />
  </aside>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useExchangeRate } from '@/composables/useExchangeRate'
import WatchlistPanel from './WatchlistPanel.vue'
import HistoryPanel from './HistoryPanel.vue'

const activeTab = ref<'watchlist' | 'history'>('watchlist')
const { rate: eurRate, loading: rateLoading } = useExchangeRate()
</script>

<style scoped>
.sidebar {
  width: 260px;
  min-width: 260px;
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--p-surface-0);
  border-right: 1px solid var(--p-surface-200);
  overflow: hidden;
}

.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem 0.75rem 0;
  gap: 0.5rem;
}

.tab-switcher {
  display: flex;
  gap: 0;
  background: var(--p-surface-100);
  border-radius: 8px;
  padding: 2px;
  flex: 1;
}

.tab-btn {
  flex: 1;
  padding: 0.3rem 0.5rem;
  border: none;
  background: transparent;
  border-radius: 6px;
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--p-text-muted-color);
  cursor: pointer;
  transition: background 0.15s, color 0.15s;
  letter-spacing: 0.01em;
}

.tab-btn:hover {
  color: var(--p-text-color);
}

.tab-btn.active {
  background: var(--p-surface-0);
  color: var(--p-text-color);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.currency-pill {
  display: inline-block;
  font-size: 0.62rem;
  font-weight: 600;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  padding: 2px 7px;
  border-radius: 999px;
  flex-shrink: 0;
}

.currency-pill.eur {
  background: var(--p-green-100);
  color: var(--p-green-700);
}

.currency-pill.loading {
  background: var(--p-surface-200);
  color: var(--p-text-muted-color);
}

.currency-pill.warn {
  background: var(--p-orange-100);
  color: var(--p-orange-700);
}
</style>
