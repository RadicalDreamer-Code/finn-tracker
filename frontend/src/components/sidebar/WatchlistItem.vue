<template>
  <div
    class="watchlist-item"
    :class="{ active: isActive }"
    @click="emit('select', item.entry.symbol)"
  >
    <div class="item-left">
      <span class="symbol">{{ item.entry.symbol }}</span>
      <span class="price" v-if="item.quote">
        {{ formatCurrency(item.quote.current_price) }}
      </span>
      <span class="price no-data" v-else>—</span>
    </div>
    <div class="item-right">
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
</template>

<script setup lang="ts">
import Button from 'primevue/button'
import Tag from 'primevue/tag'
import type { WatchlistEntryWithQuote } from '@/types'

defineProps<{
  item: WatchlistEntryWithQuote
  isActive: boolean
}>()

const emit = defineEmits<{
  select: [symbol: string]
  remove: [symbol: string]
}>()

function formatCurrency(value: number): string {
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', minimumFractionDigits: 2 }).format(value)
}

function formatChange(value: number): string {
  return `${value >= 0 ? '+' : ''}${value.toFixed(2)}%`
}
</script>

<style scoped>
.watchlist-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.6rem 0.75rem;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.15s;
  gap: 0.5rem;
}

.watchlist-item:hover {
  background: var(--p-surface-100);
}

.watchlist-item.active {
  background: var(--p-primary-50);
}

.item-left {
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

.item-right {
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

.watchlist-item:hover .remove-btn {
  opacity: 1;
}
</style>
