<template>
  <aside class="sidebar">
    <div class="sidebar-header">
      <span class="sidebar-title">Watchlist</span>
      <Button
        icon="pi pi-plus"
        text
        rounded
        size="small"
        aria-label="Add symbol"
        @click="showDialog = true"
      />
    </div>

    <div class="search-bar">
      <IconField>
        <InputIcon class="pi pi-search" />
        <InputText
          v-model="filterQuery"
          placeholder="Filter…"
          class="w-full"
          size="small"
        />
      </IconField>
    </div>

    <div class="sidebar-list" v-if="!store.loading">
      <WatchlistItem
        v-for="item in filteredEntries"
        :key="item.entry.symbol"
        :item="item"
        :is-active="item.entry.symbol === store.selectedSymbol"
        @select="store.selectSymbol"
        @remove="confirmRemove"
      />
      <div class="empty-state" v-if="filteredEntries.length === 0">
        <i class="pi pi-chart-line" />
        <span v-if="store.entries.length === 0">Add your first symbol</span>
        <span v-else>No match for "{{ filterQuery }}"</span>
      </div>
    </div>

    <div class="sidebar-list loading-state" v-else>
      <Skeleton v-for="n in 4" :key="n" height="3rem" border-radius="8px" />
    </div>

    <AddSymbolDialog v-model="showDialog" @add="handleAdd" />
  </aside>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import Button from 'primevue/button'
import IconField from 'primevue/iconfield'
import InputIcon from 'primevue/inputicon'
import InputText from 'primevue/inputtext'
import Skeleton from 'primevue/skeleton'
import { useToast } from 'primevue/usetoast'
import { useWatchlistStore } from '@/stores/watchlist'
import AddSymbolDialog from './AddSymbolDialog.vue'
import WatchlistItem from './WatchlistItem.vue'

const store = useWatchlistStore()
const toast = useToast()
const showDialog = ref(false)
const filterQuery = ref('')

const filteredEntries = computed(() =>
  store.entries.filter((e) =>
    e.entry.symbol.toLowerCase().includes(filterQuery.value.toLowerCase()),
  ),
)

onMounted(() => store.fetchWatchlist())

async function handleAdd(symbol: string) {
  try {
    await store.addSymbol(symbol)
    toast.add({ severity: 'success', summary: `${symbol} added`, life: 2500 })
  } catch {
    toast.add({ severity: 'error', summary: 'Already in watchlist', life: 2500 })
  }
}

async function confirmRemove(symbol: string) {
  try {
    await store.removeSymbol(symbol)
    toast.add({ severity: 'info', summary: `${symbol} removed`, life: 2000 })
  } catch {
    toast.add({ severity: 'error', summary: 'Could not remove', life: 2000 })
  }
}
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
  padding: 1rem 0.75rem 0.5rem;
}

.sidebar-title {
  font-size: 0.875rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: var(--p-text-muted-color);
}

.search-bar {
  padding: 0 0.75rem 0.5rem;
}

.sidebar-list {
  flex: 1;
  overflow-y: auto;
  padding: 0.25rem 0.5rem 1rem;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.loading-state {
  gap: 0.5rem;
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
}

.empty-state .pi {
  font-size: 1.5rem;
  opacity: 0.4;
}
</style>
