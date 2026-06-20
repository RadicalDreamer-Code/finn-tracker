<template>
  <div class="dashboard">
    <div v-if="selectedSymbol" class="stock-detail">
      <div class="detail-header" v-if="profile">
        <img v-if="profile.logo" :src="profile.logo" :alt="profile.name" class="company-logo" />
        <div class="detail-title">
          <h1 class="company-name">{{ profile.name }}</h1>
          <span class="detail-meta">{{ selectedSymbol }} · {{ profile.exchange }} · {{ profile.currency }}</span>
        </div>
      </div>

      <div class="quote-cards" v-if="quote">
        <div class="quote-price">
          <span class="price-label">Price</span>
          <span class="price-value">{{ formatCurrency(quote.current_price) }}</span>
          <Tag
            :value="`${quote.change >= 0 ? '+' : ''}${quote.change.toFixed(2)} (${quote.change_percent.toFixed(2)}%)`"
            :severity="quote.change_percent >= 0 ? 'success' : 'danger'"
            class="price-change"
          />
        </div>
        <div class="metric-grid">
          <div class="metric">
            <span class="metric-label">Open</span>
            <span class="metric-value">{{ formatCurrency(quote.open) }}</span>
          </div>
          <div class="metric">
            <span class="metric-label">Prev Close</span>
            <span class="metric-value">{{ formatCurrency(quote.prev_close) }}</span>
          </div>
          <div class="metric">
            <span class="metric-label">Day High</span>
            <span class="metric-value">{{ formatCurrency(quote.high) }}</span>
          </div>
          <div class="metric">
            <span class="metric-label">Day Low</span>
            <span class="metric-value">{{ formatCurrency(quote.low) }}</span>
          </div>
        </div>
      </div>

      <div class="profile-section" v-if="profile">
        <div class="profile-row" v-if="profile.sector">
          <span class="profile-key">Sector</span>
          <span class="profile-val">{{ profile.sector }}</span>
        </div>
        <div class="profile-row" v-if="profile.market_cap">
          <span class="profile-key">Market Cap</span>
          <span class="profile-val">{{ formatMarketCap(profile.market_cap) }}</span>
        </div>
        <div class="profile-row" v-if="profile.country">
          <span class="profile-key">Country</span>
          <span class="profile-val">{{ profile.country }}</span>
        </div>
        <div class="profile-row" v-if="profile.ipo_date">
          <span class="profile-key">IPO Date</span>
          <span class="profile-val">{{ profile.ipo_date }}</span>
        </div>
        <div class="profile-row" v-if="profile.weburl">
          <span class="profile-key">Website</span>
          <a :href="profile.weburl" target="_blank" rel="noopener" class="profile-link">
            {{ profile.weburl }}
          </a>
        </div>
      </div>

      <div class="loading-overlay" v-if="loading">
        <ProgressSpinner />
      </div>
    </div>

    <div class="empty-detail" v-else>
      <i class="pi pi-chart-line" />
      <p>Select a symbol from the watchlist to see details</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import ProgressSpinner from 'primevue/progressspinner'
import Tag from 'primevue/tag'
import { stocksApi } from '@/api/stocks'
import type { CompanyProfile, Quote } from '@/types'
import { useWatchlistStore } from '@/stores/watchlist'
import { storeToRefs } from 'pinia'

const store = useWatchlistStore()
const { selectedSymbol } = storeToRefs(store)

const quote = ref<Quote | null>(null)
const profile = ref<CompanyProfile | null>(null)
const loading = ref(false)

watch(
  selectedSymbol,
  async (symbol) => {
    if (!symbol) return
    loading.value = true
    quote.value = null
    profile.value = null
    try {
      ;[quote.value, profile.value] = await Promise.all([
        stocksApi.getQuote(symbol),
        stocksApi.getProfile(symbol),
      ])
    } finally {
      loading.value = false
    }
  },
  { immediate: true },
)

function formatCurrency(value: number): string {
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(value)
}

function formatMarketCap(value: number): string {
  if (value >= 1_000) return `$${(value / 1_000).toFixed(2)}B`
  return `$${value.toFixed(2)}M`
}
</script>

<style scoped>
.dashboard {
  flex: 1;
  overflow-y: auto;
  padding: 2rem;
  position: relative;
}

.stock-detail {
  max-width: 720px;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  position: relative;
}

.detail-header {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.company-logo {
  width: 48px;
  height: 48px;
  object-fit: contain;
  border-radius: 8px;
  border: 1px solid var(--p-surface-200);
  padding: 4px;
  background: white;
}

.company-name {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 700;
}

.detail-meta {
  font-size: 0.8rem;
  color: var(--p-text-muted-color);
}

.quote-cards {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  background: var(--p-surface-50);
  border: 1px solid var(--p-surface-200);
  border-radius: 12px;
  padding: 1.25rem 1.5rem;
}

.quote-price {
  display: flex;
  align-items: baseline;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.price-label {
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--p-text-muted-color);
}

.price-value {
  font-size: 2rem;
  font-weight: 700;
  color: var(--p-text-color);
}

.metric-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0.75rem;
}

.metric {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.metric-label {
  font-size: 0.7rem;
  text-transform: uppercase;
  color: var(--p-text-muted-color);
  letter-spacing: 0.04em;
}

.metric-value {
  font-size: 0.95rem;
  font-weight: 500;
}

.profile-section {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  border: 1px solid var(--p-surface-200);
  border-radius: 12px;
  padding: 1rem 1.25rem;
}

.profile-row {
  display: flex;
  gap: 1rem;
  font-size: 0.875rem;
}

.profile-key {
  width: 120px;
  flex-shrink: 0;
  color: var(--p-text-muted-color);
}

.profile-val {
  font-weight: 500;
}

.profile-link {
  color: var(--p-primary-color);
  text-decoration: none;
}

.profile-link:hover {
  text-decoration: underline;
}

.loading-overlay {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(var(--p-surface-0-rgb), 0.6);
}

.empty-detail {
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  color: var(--p-text-muted-color);
}

.empty-detail .pi {
  font-size: 3rem;
  opacity: 0.3;
}

.empty-detail p {
  margin: 0;
  font-size: 0.95rem;
}
</style>
