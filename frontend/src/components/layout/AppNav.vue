<template>
  <aside class="nav">
    <div class="nav-brand">
      <i class="pi pi-chart-line" />
      <span>Finn Tracker</span>
    </div>

    <nav class="nav-links">
      <RouterLink :to="{ name: 'watchlist' }" class="nav-link" active-class="active">
        <i class="pi pi-list" />
        <span>Watchlist</span>
      </RouterLink>
      <RouterLink :to="{ name: 'history' }" class="nav-link" active-class="active">
        <i class="pi pi-clock" />
        <span>History</span>
      </RouterLink>
    </nav>

    <div class="nav-footer">
      <span v-if="eurRate !== null" class="currency-pill eur">EUR</span>
      <span v-else-if="rateLoading" class="currency-pill loading">USD</span>
      <span v-else class="currency-pill warn">USD</span>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { useExchangeRate } from '@/composables/useExchangeRate'

const { rate: eurRate, loading: rateLoading } = useExchangeRate()
</script>

<style scoped>
.nav {
  width: 220px;
  min-width: 220px;
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--p-surface-0);
  border-right: 1px solid var(--p-surface-200);
  overflow: hidden;
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem 1rem 0.75rem;
  font-weight: 700;
  font-size: 1rem;
  color: var(--p-text-color);
}

.nav-brand .pi {
  color: var(--p-primary-color);
}

.nav-links {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  padding: 0.5rem;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  padding: 0.55rem 0.75rem;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--p-text-muted-color);
  text-decoration: none;
  transition: background 0.15s, color 0.15s;
}

.nav-link:hover {
  background: var(--p-surface-100);
  color: var(--p-text-color);
}

.nav-link.active {
  background: var(--p-primary-50);
  color: var(--p-primary-color);
}

.nav-link .pi {
  font-size: 0.95rem;
}

.nav-footer {
  padding: 0.75rem 1rem 1rem;
}

.currency-pill {
  display: inline-block;
  font-size: 0.62rem;
  font-weight: 600;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  padding: 2px 7px;
  border-radius: 999px;
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
