<template>
  <div
    class="stock-card"
    :class="{ active: isActive }"
    @click="emit('select', item.entry.symbol)"
  >
    <div class="card-main">
      <div class="card-left">
        <span class="symbol">{{ item.entry.symbol }}</span>
        <span class="price" v-if="item.quote">{{ formatCurrency(item.quote.current_price) }}</span>
        <span class="price no-data" v-else>—</span>
      </div>
      <div class="card-right">
        <Tag
          v-if="item.quote"
          :value="formatChange(item.quote.change_percent)"
          :severity="item.quote.change_percent >= 0 ? 'success' : 'danger'"
          class="change-tag"
        />
        <Button
          icon="pi pi-times"
          text
          rounded
          size="small"
          severity="secondary"
          class="remove-btn"
          @click.stop="emit('remove', item.entry.symbol)"
          aria-label="Remove"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import Button from 'primevue/button'
import Tag from 'primevue/tag'
import type { WatchlistEntryWithQuote } from '@/types'
import { useExchangeRate } from '@/composables/useExchangeRate'

withDefaults(
  defineProps<{
    item: WatchlistEntryWithQuote
    isActive?: boolean
  }>(),
  { isActive: false },
)

const emit = defineEmits<{
  select: [symbol: string]
  remove: [symbol: string]
}>()

const { rate: eurRate } = useExchangeRate()

function formatCurrency(value: number): string {
  if (eurRate.value !== null) {
    return new Intl.NumberFormat('de-DE', {
      style: 'currency',
      currency: 'EUR',
      minimumFractionDigits: 2,
    }).format(value * eurRate.value)
  }
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 2,
  }).format(value)
}

function formatChange(value: number): string {
  return `${value >= 0 ? '+' : ''}${value.toFixed(2)}%`
}
</script>

<style scoped>
.stock-card {
  display: flex;
  flex-direction: column;
  padding: 0.6rem 0.75rem;
  border-radius: 8px;
  border: 1px solid var(--p-surface-200);
  background: var(--p-surface-0);
  cursor: pointer;
  transition: border-color 0.15s, background 0.15s;
}

.stock-card:hover {
  background: var(--p-surface-50);
  border-color: var(--p-surface-300);
}

.stock-card.active {
  background: var(--p-primary-50);
  border-color: var(--p-primary-200);
}

.card-main {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
}

.card-left {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.symbol {
  font-weight: 600;
  font-size: 0.875rem;
  color: var(--p-text-color);
}

.price {
  font-size: 0.8rem;
  color: var(--p-text-muted-color);
}

.price.no-data {
  color: var(--p-text-muted-color);
}

.card-right {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  flex-shrink: 0;
}

.change-tag {
  font-size: 0.7rem;
  padding: 2px 6px;
}

.remove-btn {
  opacity: 0;
  transition: opacity 0.15s;
  width: 1.5rem;
  height: 1.5rem;
}

.stock-card:hover .remove-btn {
  opacity: 1;
}
</style>
